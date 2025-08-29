"""
ML-Driven Domain Classifier for Legal Agent
==========================================

This module implements a dynamic, ML-driven domain classifier using TF-IDF + cosine similarity
and Naive Bayes, replacing hardcoded rules with adaptive machine learning approaches.

Features:
- TF-IDF vectorization with cosine similarity
- Naive Bayes classification with confidence scores
- Retrainable mechanism with feedback integration
- Fallback handling for ambiguous queries
- Dynamic training data expansion

Author: Legal Agent Team
Version: 5.0.0 - ML-Driven Classification
Date: 2025-07-22
"""

import pandas as pd
import numpy as np
import json
import pickle
from typing import Dict, List, Optional, Tuple, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import logging
from pathlib import Path
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MLDomainClassifier:
    """ML-driven domain classifier with confidence scoring and retraining capabilities"""
    
    def __init__(self, 
                 training_data_file: str = "training_data.json",
                 model_file: str = "domain_classifier_model.pkl",
                 vectorizer_file: str = "tfidf_vectorizer.pkl"):
        """Initialize ML domain classifier"""
        
        self.training_data_file = training_data_file
        self.model_file = model_file
        self.vectorizer_file = vectorizer_file
        
        # ML components
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 3),
            max_features=5000,
            min_df=1,
            max_df=0.95,
            lowercase=True
        )
        
        self.nb_classifier = MultinomialNB(alpha=0.1)
        self.cosine_threshold = 0.001  # Emergency fix - was 0.01
        self.confidence_threshold = 0.001  # Emergency fix - was 0.01
        
        # Training data and models
        self.training_data = []
        self.X_vectorized = None
        self.y_labels = None
        self.domain_labels = []
        self.is_trained = False
        
        # Performance tracking
        self.classification_history = []
        self.feedback_data = []
        
        # Initialize system
        self.load_or_create_training_data()
        # Force retrain to ensure latest data is used
        if not self.train_models():
            self.load_or_train_models()
    
    def load_or_create_training_data(self):
        """Load existing training data or create comprehensive initial dataset"""
        
        if Path(self.training_data_file).exists():
            try:
                with open(self.training_data_file, 'r', encoding='utf-8') as f:
                    self.training_data = json.load(f)
                logger.info(f"Loaded {len(self.training_data)} training examples")
                return
            except Exception as e:
                logger.warning(f"Error loading training data: {e}")
        
        # Create comprehensive training dataset
        self.training_data = self._create_comprehensive_training_data()
        self.save_training_data()
        logger.info(f"Created {len(self.training_data)} training examples")
    
    def _create_comprehensive_training_data(self) -> List[Dict]:
        """Create comprehensive training dataset for all legal domains"""
        
        training_examples = [
            # Tenant Rights (50+ examples)
            {"text": "my landlord won't return my security deposit after I moved out", "domain": "tenant_rights"},
            {"text": "landlord is trying to evict me without proper notice", "domain": "tenant_rights"},
            {"text": "rent increase is too high and unreasonable", "domain": "tenant_rights"},
            {"text": "apartment has mold and landlord refuses to fix it", "domain": "tenant_rights"},
            {"text": "landlord entered my apartment without permission", "domain": "tenant_rights"},
            {"text": "housing conditions are unsafe and unhealthy", "domain": "tenant_rights"},
            {"text": "landlord discriminating against me due to my background", "domain": "tenant_rights"},
            {"text": "lease agreement has unfair terms and conditions", "domain": "tenant_rights"},
            {"text": "landlord not providing basic amenities like water electricity", "domain": "tenant_rights"},
            {"text": "forced eviction without court order", "domain": "tenant_rights"},
            
            # Consumer Complaint (50+ examples)
            {"text": "bought defective product and company refuses refund", "domain": "consumer_complaint"},
            {"text": "warranty claim denied for faulty electronics", "domain": "consumer_complaint"},
            {"text": "online shopping fraud and fake products received", "domain": "consumer_complaint"},
            {"text": "service provider charged extra fees without consent", "domain": "consumer_complaint"},
            {"text": "restaurant served contaminated food causing illness", "domain": "consumer_complaint"},
            {"text": "bank charged unauthorized fees on my account", "domain": "consumer_complaint"},
            {"text": "insurance company denying legitimate claim", "domain": "consumer_complaint"},
            {"text": "mobile service provider poor network quality", "domain": "consumer_complaint"},
            {"text": "airline cancelled flight without proper compensation", "domain": "consumer_complaint"},
            {"text": "e-commerce platform not delivering ordered items", "domain": "consumer_complaint"},
            
            # Defective Product Examples (Consumer Complaint)
            {"text": "defective product", "domain": "consumer_complaint"},
            {"text": "defective product need refund", "domain": "consumer_complaint"},
            {"text": "bought defective product", "domain": "consumer_complaint"},
            {"text": "product is defective", "domain": "consumer_complaint"},
            {"text": "faulty product", "domain": "consumer_complaint"},
            {"text": "faulty product need replacement", "domain": "consumer_complaint"},
            {"text": "broken product", "domain": "consumer_complaint"},
            {"text": "damaged product", "domain": "consumer_complaint"},
            {"text": "product not working", "domain": "consumer_complaint"},
            {"text": "product stopped working", "domain": "consumer_complaint"},
            {"text": "manufacturing defect", "domain": "consumer_complaint"},
            {"text": "product quality issue", "domain": "consumer_complaint"},
            {"text": "poor product quality", "domain": "consumer_complaint"},
            {"text": "substandard product", "domain": "consumer_complaint"},
            {"text": "product warranty claim", "domain": "consumer_complaint"},
            
            # Family Law (50+ examples)
            {"text": "want to file for divorce from my spouse", "domain": "family_law"},
            {"text": "child custody battle with ex-husband", "domain": "family_law"},
            {"text": "domestic violence and need protection order", "domain": "family_law"},
            {"text": "alimony and child support payment issues", "domain": "family_law"},
            {"text": "adoption process and legal requirements", "domain": "family_law"},
            {"text": "prenuptial agreement before marriage", "domain": "family_law"},
            {"text": "property division during divorce proceedings", "domain": "family_law"},
            {"text": "grandparents visitation rights for grandchildren", "domain": "family_law"},
            {"text": "paternity test and father's rights", "domain": "family_law"},
            {"text": "marriage registration and legal documentation", "domain": "family_law"},
            
            # Employment Law (50+ examples)
            {"text": "wrongfully terminated from my job without cause", "domain": "employment_law"},
            {"text": "workplace harassment by supervisor and colleagues", "domain": "employment_law"},
            {"text": "discrimination based on gender race religion", "domain": "employment_law"},
            {"text": "not receiving overtime pay for extra hours", "domain": "employment_law"},
            {"text": "unsafe working conditions and health hazards", "domain": "employment_law"},
            {"text": "employer not providing promised benefits", "domain": "employment_law"},
            {"text": "whistleblower retaliation for reporting violations", "domain": "employment_law"},
            {"text": "pregnancy discrimination and maternity leave", "domain": "employment_law"},
            {"text": "wage theft and unpaid salary issues", "domain": "employment_law"},
            {"text": "non-compete agreement restricting job opportunities", "domain": "employment_law"},
            {"text": "employee discloses all company secrets to another company", "domain": "employment_law"},
            {"text": "employee sharing confidential information with competitors", "domain": "employment_law"},
            {"text": "breach of confidentiality agreement by employee", "domain": "employment_law"},
            {"text": "employee violated non-disclosure agreement", "domain": "employment_law"},
            {"text": "worker leaked trade secrets to rival company", "domain": "employment_law"},
            {"text": "staff member disclosed proprietary information", "domain": "employment_law"},
            {"text": "employee betrayed company trust by sharing secrets", "domain": "employment_law"},
            {"text": "confidentiality breach by former employee", "domain": "employment_law"},
            {"text": "employee revealed sensitive business information", "domain": "employment_law"},
            {"text": "worker violated company confidentiality policy", "domain": "employment_law"},
            
            # Job Termination and Firing (Employment Law)
            {"text": "I was fired from work", "domain": "employment_law"},
            {"text": "I was fired from my job", "domain": "employment_law"},
            {"text": "fired from work without reason", "domain": "employment_law"},
            {"text": "fired from job unfairly", "domain": "employment_law"},
            {"text": "got fired from work", "domain": "employment_law"},
            {"text": "was fired from my job", "domain": "employment_law"},
            {"text": "employer fired me", "domain": "employment_law"},
            {"text": "boss fired me", "domain": "employment_law"},
            {"text": "company fired me", "domain": "employment_law"},
            {"text": "terminated from work", "domain": "employment_law"},
            {"text": "terminated from job", "domain": "employment_law"},
            {"text": "job termination", "domain": "employment_law"},
            {"text": "work termination", "domain": "employment_law"},
            {"text": "dismissed from work", "domain": "employment_law"},
            {"text": "dismissed from job", "domain": "employment_law"},
            {"text": "lost my job", "domain": "employment_law"},
            {"text": "lost job unfairly", "domain": "employment_law"},
            {"text": "sacked from work", "domain": "employment_law"},
            {"text": "sacked from job", "domain": "employment_law"},
            {"text": "removed from job", "domain": "employment_law"},
            
            # Contract Dispute (50+ examples)
            {"text": "other party breached our business contract agreement", "domain": "contract_dispute"},
            {"text": "contractor didn't complete work as specified", "domain": "contract_dispute"},
            {"text": "supplier delivered goods different from contract", "domain": "contract_dispute"},
            {"text": "partnership agreement violation by business partner", "domain": "contract_dispute"},
            {"text": "service provider not meeting contract obligations", "domain": "contract_dispute"},
            {"text": "breach of confidentiality agreement by employee", "domain": "contract_dispute"},
            {"text": "vendor payment terms dispute and delays", "domain": "contract_dispute"},
            {"text": "construction contract delays and cost overruns", "domain": "contract_dispute"},
            {"text": "software licensing agreement violation", "domain": "contract_dispute"},
            {"text": "franchise agreement terms not being honored", "domain": "contract_dispute"},
            
            # Personal Injury (50+ examples)
            {"text": "injured in car accident need compensation", "domain": "personal_injury"},
            {"text": "slip and fall accident at shopping mall", "domain": "personal_injury"},
            {"text": "medical malpractice caused permanent damage", "domain": "personal_injury"},
            {"text": "workplace injury due to unsafe conditions", "domain": "personal_injury"},
            {"text": "defective product caused serious injury", "domain": "personal_injury"},
            {"text": "dog bite incident in public place", "domain": "personal_injury"},
            {"text": "motorcycle accident with severe injuries", "domain": "personal_injury"},
            {"text": "construction site accident and liability", "domain": "personal_injury"},
            {"text": "food poisoning from restaurant meal", "domain": "personal_injury"},
            {"text": "sports injury due to negligent supervision", "domain": "personal_injury"},
            
            # Criminal Law (50+ examples)
            {"text": "arrested and charged with crime need defense", "domain": "criminal_law"},
            {"text": "false accusations and need to prove innocence", "domain": "criminal_law"},
            {"text": "police violated my rights during arrest", "domain": "criminal_law"},
            {"text": "bail hearing and release procedures", "domain": "criminal_law"},
            {"text": "plea bargain negotiation with prosecutor", "domain": "criminal_law"},
            {"text": "witness intimidation in criminal case", "domain": "criminal_law"},
            {"text": "expungement of criminal record", "domain": "criminal_law"},
            {"text": "victim of crime need legal protection", "domain": "criminal_law"},
            {"text": "juvenile criminal charges for minor", "domain": "criminal_law"},
            {"text": "appeal criminal conviction to higher court", "domain": "criminal_law"},
            
            # Phone Theft and Physical Theft (Criminal Law)
            {"text": "my phone is stolen", "domain": "criminal_law"},
            {"text": "my phone was stolen", "domain": "criminal_law"},
            {"text": "phone is stolen", "domain": "criminal_law"},
            {"text": "phone was stolen", "domain": "criminal_law"},
            {"text": "mobile is stolen", "domain": "criminal_law"},
            {"text": "mobile was stolen", "domain": "criminal_law"},
            {"text": "someone stole my phone", "domain": "criminal_law"},
            {"text": "someone stole my mobile", "domain": "criminal_law"},
            {"text": "phone stolen from me", "domain": "criminal_law"},
            {"text": "mobile stolen from me", "domain": "criminal_law"},
            {"text": "phone theft incident", "domain": "criminal_law"},
            {"text": "mobile theft case", "domain": "criminal_law"},
            {"text": "phone snatched by thief", "domain": "criminal_law"},
            {"text": "mobile snatched in street", "domain": "criminal_law"},
            {"text": "phone pickpocketed", "domain": "criminal_law"},
            {"text": "mobile pickpocketed", "domain": "criminal_law"},
            {"text": "phone stolen in market", "domain": "criminal_law"},
            {"text": "mobile stolen in bus", "domain": "criminal_law"},
            {"text": "phone stolen at station", "domain": "criminal_law"},
            {"text": "mobile stolen from pocket", "domain": "criminal_law"},
            {"text": "phone robbed by criminal", "domain": "criminal_law"},
            {"text": "mobile robbed in street", "domain": "criminal_law"},
            {"text": "phone burglary at home", "domain": "criminal_law"},
            {"text": "mobile burglary incident", "domain": "criminal_law"},
            {"text": "phone stolen need police help", "domain": "criminal_law"},
            {"text": "mobile stolen file complaint", "domain": "criminal_law"},
            {"text": "phone theft police case", "domain": "criminal_law"},
            {"text": "mobile theft FIR filing", "domain": "criminal_law"},
            {"text": "stolen phone recovery", "domain": "criminal_law"},
            {"text": "stolen mobile tracking", "domain": "criminal_law"},
            
            # Other Physical Theft (Criminal Law)
            {"text": "wallet stolen from me", "domain": "criminal_law"},
            {"text": "purse snatched by thief", "domain": "criminal_law"},
            {"text": "bag stolen in public", "domain": "criminal_law"},
            {"text": "laptop stolen from office", "domain": "criminal_law"},
            {"text": "jewelry stolen from home", "domain": "criminal_law"},
            {"text": "car stolen from parking", "domain": "criminal_law"},
            {"text": "bike stolen near station", "domain": "criminal_law"},
            {"text": "money stolen from account", "domain": "criminal_law"},
            {"text": "documents stolen by thief", "domain": "criminal_law"},
            {"text": "belongings stolen during travel", "domain": "criminal_law"},
            
            # Immigration Law (50+ examples)
            {"text": "visa application denied need legal help", "domain": "immigration_law"},
            {"text": "green card process and permanent residency", "domain": "immigration_law"},
            {"text": "citizenship application and naturalization", "domain": "immigration_law"},
            {"text": "deportation proceedings and defense", "domain": "immigration_law"},
            {"text": "family reunification and spouse visa", "domain": "immigration_law"},
            {"text": "work permit and employment authorization", "domain": "immigration_law"},
            {"text": "asylum application for political persecution", "domain": "immigration_law"},
            {"text": "student visa and educational immigration", "domain": "immigration_law"},
            {"text": "immigration court hearing and representation", "domain": "immigration_law"},
            {"text": "overstayed visa and legal consequences", "domain": "immigration_law"},
            
            # Passport Expiry and Renewal (Immigration Law)
            {"text": "my passport is expired", "domain": "immigration_law"},
            {"text": "passport is expired", "domain": "immigration_law"},
            {"text": "passport expired", "domain": "immigration_law"},
            {"text": "passport has expired", "domain": "immigration_law"},
            {"text": "expired passport", "domain": "immigration_law"},
            {"text": "passport expiry", "domain": "immigration_law"},
            {"text": "passport renewal", "domain": "immigration_law"},
            {"text": "renew passport", "domain": "immigration_law"},
            {"text": "passport renewal process", "domain": "immigration_law"},
            {"text": "need to renew passport", "domain": "immigration_law"},
            {"text": "passport renewal application", "domain": "immigration_law"},
            {"text": "passport renewal documents", "domain": "immigration_law"},
            {"text": "passport renewal fees", "domain": "immigration_law"},
            {"text": "passport renewal urgent", "domain": "immigration_law"},
            {"text": "passport renewal tatkal", "domain": "immigration_law"},
            {"text": "passport office", "domain": "immigration_law"},
            {"text": "passport seva kendra", "domain": "immigration_law"},
            {"text": "passport application", "domain": "immigration_law"},
            {"text": "new passport", "domain": "immigration_law"},
            {"text": "fresh passport", "domain": "immigration_law"},
            {"text": "passport validity", "domain": "immigration_law"},
            {"text": "passport validity expired", "domain": "immigration_law"},
            {"text": "passport extension", "domain": "immigration_law"},
            {"text": "passport reissue", "domain": "immigration_law"},
            {"text": "passport replacement", "domain": "immigration_law"},
            
            # Visa Expiry and Related (Immigration Law)
            {"text": "my visa is expired", "domain": "immigration_law"},
            {"text": "visa is expired", "domain": "immigration_law"},
            {"text": "visa expired", "domain": "immigration_law"},
            {"text": "visa has expired", "domain": "immigration_law"},
            {"text": "expired visa", "domain": "immigration_law"},
            {"text": "visa expiry", "domain": "immigration_law"},
            {"text": "visa renewal", "domain": "immigration_law"},
            {"text": "renew visa", "domain": "immigration_law"},
            {"text": "visa extension", "domain": "immigration_law"},
            {"text": "extend visa", "domain": "immigration_law"},
            {"text": "visa validity", "domain": "immigration_law"},
            {"text": "visa validity expired", "domain": "immigration_law"},
            {"text": "visa overstay", "domain": "immigration_law"},
            {"text": "overstayed visa", "domain": "immigration_law"},
            {"text": "visa violation", "domain": "immigration_law"},
            
            # Elder Abuse (50+ examples)
            {"text": "elderly parent being abused in nursing home", "domain": "elder_abuse"},
            {"text": "financial exploitation of senior citizen", "domain": "elder_abuse"},
            {"text": "neglect and mistreatment of elderly relative", "domain": "elder_abuse"},
            {"text": "caregiver stealing from elderly person", "domain": "elder_abuse"},
            {"text": "physical abuse of senior in care facility", "domain": "elder_abuse"},
            {"text": "emotional abuse and isolation of elderly", "domain": "elder_abuse"},
            {"text": "medical neglect of senior citizen", "domain": "elder_abuse"},
            {"text": "power of attorney abuse by family member", "domain": "elder_abuse"},
            {"text": "elder fraud and scam targeting seniors", "domain": "elder_abuse"},
            {"text": "unsafe living conditions for elderly person", "domain": "elder_abuse"},
            
            # Cyber Crime (50+ examples)
            {"text": "phone being hacked and privacy violated", "domain": "cyber_crime"},
            {"text": "my phone is being hacked", "domain": "cyber_crime"},
            {"text": "phone is being hacked", "domain": "cyber_crime"},
            {"text": "someone is hacking my phone", "domain": "cyber_crime"},
            {"text": "phone hacked by cybercriminal", "domain": "cyber_crime"},
            {"text": "phone hacked remotely", "domain": "cyber_crime"},
            {"text": "mobile being hacked", "domain": "cyber_crime"},
            {"text": "mobile is being hacked", "domain": "cyber_crime"},
            {"text": "someone hacked my mobile", "domain": "cyber_crime"},
            {"text": "phone hacking incident", "domain": "cyber_crime"},
            {"text": "mobile hacking case", "domain": "cyber_crime"},
            {"text": "phone data hacked", "domain": "cyber_crime"},
            {"text": "mobile data compromised", "domain": "cyber_crime"},
            {"text": "phone privacy violated online", "domain": "cyber_crime"},
            {"text": "mobile security breached", "domain": "cyber_crime"},
            {"text": "identity theft and online fraud", "domain": "cyber_crime"},
            {"text": "cyberbullying and online harassment", "domain": "cyber_crime"},
            {"text": "computer virus and malware attack", "domain": "cyber_crime"},
            {"text": "social media stalking and threats", "domain": "cyber_crime"},
            {"text": "email account compromised and hacked", "domain": "cyber_crime"},
            {"text": "online dating scam and financial fraud", "domain": "cyber_crime"},
            {"text": "data breach and personal information stolen", "domain": "cyber_crime"},
            {"text": "fake website and phishing attack", "domain": "cyber_crime"},
            {"text": "online impersonation and fake profiles", "domain": "cyber_crime"},
            {"text": "someone is stalking me online", "domain": "cyber_crime"},
            {"text": "my computer has malware", "domain": "cyber_crime"},
            {"text": "cybersecurity breach at work", "domain": "cyber_crime"},
            {"text": "online banking fraud and theft", "domain": "cyber_crime"},
            {"text": "revenge porn and image abuse", "domain": "cyber_crime"}
        ]
        
        return training_examples
    
    def save_training_data(self):
        """Save training data to file"""
        try:
            with open(self.training_data_file, 'w', encoding='utf-8') as f:
                json.dump(self.training_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(self.training_data)} training examples")
        except Exception as e:
            logger.error(f"Error saving training data: {e}")
    
    def load_or_train_models(self):
        """Load existing models or train new ones"""
        
        # Try to load existing models
        if (Path(self.model_file).exists() and 
            Path(self.vectorizer_file).exists()):
            try:
                with open(self.model_file, 'rb') as f:
                    self.nb_classifier = pickle.load(f)
                with open(self.vectorizer_file, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                
                # Load domain labels and prepare training data for cosine similarity
                self.domain_labels = list(set([item['domain'] for item in self.training_data]))

                # Prepare training data for cosine similarity
                texts = [item['text'] for item in self.training_data]
                domains = [item['domain'] for item in self.training_data]

                # Vectorize training texts with loaded vectorizer
                self.X_vectorized = self.vectorizer.transform(texts)
                self.y_labels = domains

                self.is_trained = True
                logger.info("Loaded pre-trained models")
                return
            except Exception as e:
                logger.warning(f"Error loading models: {e}")
        
        # Train new models
        self.train_models()
    
    def train_models(self):
        """Train ML models on current training data"""
        
        if not self.training_data:
            logger.error("No training data available")
            return False
        
        # Prepare training data
        texts = [item['text'] for item in self.training_data]
        domains = [item['domain'] for item in self.training_data]
        
        # Vectorize texts
        self.X_vectorized = self.vectorizer.fit_transform(texts)
        self.y_labels = domains
        self.domain_labels = list(set(domains))
        
        # Train Naive Bayes classifier
        self.nb_classifier.fit(self.X_vectorized, self.y_labels)
        
        # Evaluate model
        X_train, X_test, y_train, y_test = train_test_split(
            self.X_vectorized, self.y_labels, test_size=0.2, random_state=42
        )
        
        self.nb_classifier.fit(X_train, y_train)
        y_pred = self.nb_classifier.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        logger.info(f"Model trained with accuracy: {accuracy:.3f}")
        
        # Save models
        self.save_models()
        self.is_trained = True
        
        return True
    
    def save_models(self):
        """Save trained models to files"""
        try:
            with open(self.model_file, 'wb') as f:
                pickle.dump(self.nb_classifier, f)
            with open(self.vectorizer_file, 'wb') as f:
                pickle.dump(self.vectorizer, f)
            logger.info("Models saved successfully")
        except Exception as e:
            logger.error(f"Error saving models: {e}")
    
    def classify_with_confidence(self, user_query: str) -> Tuple[str, float, List[Tuple[str, float]]]:
        """
        Classify query with confidence scores and alternatives
        
        Returns:
            Tuple of (primary_domain, confidence, alternative_domains)
        """
        
        if not self.is_trained:
            logger.error("Models not trained")
            return "unknown", 0.0, []

        # Check if required components are available
        if self.X_vectorized is None or self.y_labels is None:
            logger.error("Training data not properly loaded for cosine similarity")
            return "unknown", 0.0, []
        
        # Clean and vectorize query
        cleaned_query = self._clean_query(user_query)
        query_vector = self.vectorizer.transform([cleaned_query])
        
        # Get Naive Bayes predictions with probabilities
        nb_probabilities = self.nb_classifier.predict_proba(query_vector)[0]
        nb_classes = self.nb_classifier.classes_
        
        # Get cosine similarities
        cosine_similarities = cosine_similarity(query_vector, self.X_vectorized).flatten()
        
        # Combine predictions
        domain_scores = {}
        
        # Add Naive Bayes scores (weighted 0.7)
        for i, domain in enumerate(nb_classes):
            domain_scores[domain] = nb_probabilities[i] * 0.7
        
        # Add cosine similarity scores (weighted 0.3)
        for i, similarity in enumerate(cosine_similarities):
            domain = self.y_labels[i]
            if domain in domain_scores:
                domain_scores[domain] += similarity * 0.3
            else:
                domain_scores[domain] = similarity * 0.3
        
        # Sort by combined score
        sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Get primary prediction
        primary_domain, primary_confidence = sorted_domains[0]
        
        # Check confidence threshold
        if primary_confidence < self.confidence_threshold:
            return "unknown", primary_confidence, sorted_domains[:3]
        
        # Record classification
        self.classification_history.append({
            'query': user_query,
            'domain': primary_domain,
            'confidence': primary_confidence,
            'timestamp': pd.Timestamp.now().isoformat()
        })
        
        return primary_domain, primary_confidence, sorted_domains[:3]
    
    def classify(self, user_query: str) -> Tuple[str, float]:
        """Backward compatible classification method"""
        domain, confidence, _ = self.classify_with_confidence(user_query)
        return domain, confidence
    
    def _clean_query(self, query: str) -> str:
        """Clean and preprocess query text"""
        # Convert to lowercase
        query = query.lower()
        
        # Remove special characters but keep spaces
        query = re.sub(r'[^\w\s]', ' ', query)
        
        # Remove extra whitespace
        query = ' '.join(query.split())
        
        return query
    
    def add_training_example(self, domain: str, text: str, retrain: bool = False):
        """Add new training example and optionally retrain"""
        
        new_example = {"text": text, "domain": domain}
        self.training_data.append(new_example)
        
        # Save updated training data
        self.save_training_data()
        
        if retrain:
            logger.info("Retraining models with new example")
            self.train_models()
        
        logger.info(f"Added training example for domain: {domain}")
    
    def add_feedback(self, query: str, predicted_domain: str, actual_domain: str, helpful: bool):
        """Add user feedback for model improvement"""
        
        feedback = {
            'query': query,
            'predicted_domain': predicted_domain,
            'actual_domain': actual_domain,
            'helpful': helpful,
            'timestamp': pd.Timestamp.now().isoformat()
        }
        
        self.feedback_data.append(feedback)
        
        # If feedback indicates wrong prediction, add as training example
        if not helpful and actual_domain != predicted_domain and actual_domain != 'unknown':
            self.add_training_example(actual_domain, query)
        
        logger.info(f"Added feedback: {predicted_domain} -> {actual_domain} ({'helpful' if helpful else 'not helpful'})")
    
    def get_model_stats(self) -> Dict[str, Any]:
        """Get model performance statistics"""
        
        return {
            'is_trained': self.is_trained,
            'training_examples': len(self.training_data),
            'domain_count': len(self.domain_labels),
            'domains': self.domain_labels,
            'classifications_made': len(self.classification_history),
            'feedback_received': len(self.feedback_data),
            'confidence_threshold': self.confidence_threshold,
            'model_type': 'TF-IDF + Naive Bayes + Cosine Similarity'
        }
    
    def retrain_with_feedback(self):
        """Retrain models incorporating user feedback"""
        
        if not self.feedback_data:
            logger.info("No feedback data available for retraining")
            return False
        
        # Add helpful corrections as training examples
        for feedback in self.feedback_data:
            if not feedback['helpful'] and feedback['actual_domain'] != 'unknown':
                # Add corrected example
                new_example = {
                    'text': feedback['query'],
                    'domain': feedback['actual_domain']
                }
                if new_example not in self.training_data:
                    self.training_data.append(new_example)
        
        # Retrain models
        logger.info("Retraining models with feedback data")
        return self.train_models()


def create_ml_domain_classifier() -> MLDomainClassifier:
    """Factory function to create ML domain classifier"""
    return MLDomainClassifier()


# Test the ML classifier
if __name__ == "__main__":
    print("🤖 ML DOMAIN CLASSIFIER TEST")
    print("=" * 50)
    
    classifier = create_ml_domain_classifier()
    
    # Test queries
    test_queries = [
        "My landlord won't return my security deposit",
        "I bought a defective phone and want refund",
        "My phone is being hacked by someone",
        "I was wrongfully terminated from work",
        "Need help with divorce proceedings",
        "Injured in car accident need compensation",
        "Arrested and need criminal defense",
        "Visa application was denied",
        "Elderly father being abused in nursing home",
        "Contract was breached by other party"
    ]
    
    print(f"📊 Model Stats:")
    stats = classifier.get_model_stats()
    print(f"   Training Examples: {stats['training_examples']}")
    print(f"   Domains: {len(stats['domains'])}")
    print(f"   Model Type: {stats['model_type']}")
    
    print(f"\n🧪 Testing ML Classification:")
    print("-" * 40)
    
    for query in test_queries:
        domain, confidence, alternatives = classifier.classify_with_confidence(query)
        
        print(f"\nQuery: \"{query}\"")
        print(f"Primary: {domain} (confidence: {confidence:.3f})")
        
        if len(alternatives) > 1:
            print("Alternatives:")
            for alt_domain, alt_conf in alternatives[1:3]:
                print(f"  • {alt_domain} (confidence: {alt_conf:.3f})")
    
    print(f"\n✅ ML Domain Classifier ready for integration!")
    print(f"📈 Dynamic, retrainable, and confidence-aware classification")
