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
        self.confidence_threshold = 0.05  # Increased from 0.001 to better handle 30+ domains
        
        # Enhanced thresholds for better accuracy
        self.min_confidence_for_classification = 0.1
        self.high_confidence_threshold = 0.8
        
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
        """Load existing training data or create new comprehensive dataset"""
        try:
            # Try to load existing training data
            with open(self.training_data_file, 'r', encoding='utf-8') as f:
                self.training_data = json.load(f)
            logger.info(f"Loaded {len(self.training_data)} training examples from file")
        except FileNotFoundError:
            # Create comprehensive training data if file doesn't exist
            logger.info("Training data file not found, creating comprehensive dataset")
            self.training_data = self._create_comprehensive_training_data()
            self.save_training_data()
        except Exception as e:
            logger.error(f"Error loading training data: {e}")
            # Fallback to creating comprehensive data
            self.training_data = self._create_comprehensive_training_data()
            self.save_training_data()
    
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
            {"text": "need custody of my children", "domain": "family_law"},
            {"text": "fighting for child custody rights", "domain": "family_law"},
            {"text": "custody dispute with ex-spouse", "domain": "family_law"},
            {"text": "child custody legal proceedings", "domain": "family_law"},
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
            {"text": "child kidnapped for ransom", "domain": "criminal_law"},
            {"text": "daughter kidnapped for ransom", "domain": "criminal_law"},
            {"text": "son kidnapped for ransom", "domain": "criminal_law"},
            {"text": "family member kidnapped for ransom", "domain": "criminal_law"},
            {"text": "person kidnapped for ransom", "domain": "criminal_law"},
            {"text": "kidnapped for ransom by criminals", "domain": "criminal_law"},
            {"text": "raped by neighbor", "domain": "criminal_law"},
            {"text": "raped by family member", "domain": "criminal_law"},
            {"text": "raped by stranger", "domain": "criminal_law"},
            {"text": "sexual assault by coworker", "domain": "criminal_law"},
            {"text": "sexual abuse by relative", "domain": "criminal_law"},
            {"text": "molested by family friend", "domain": "criminal_law"},
            {"text": "someone is hacking my computer", "domain": "criminal_law"},
            {"text": "computer being hacked by someone", "domain": "criminal_law"},
            {"text": "hacking into my computer system", "domain": "criminal_law"},
            {"text": "unauthorized access to my computer", "domain": "criminal_law"},
            
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
            {"text": "phone being hacked and privacy violated", "domain": "criminal_law"},
            {"text": "my phone is being hacked", "domain": "criminal_law"},
            {"text": "phone is being hacked", "domain": "criminal_law"},
            {"text": "someone is hacking my phone", "domain": "criminal_law"},
            {"text": "phone hacked by cybercriminal", "domain": "criminal_law"},
            {"text": "phone hacked remotely", "domain": "criminal_law"},
            {"text": "mobile being hacked", "domain": "criminal_law"},
            {"text": "mobile is being hacked", "domain": "criminal_law"},
            {"text": "someone hacked my mobile", "domain": "criminal_law"},
            {"text": "phone hacking incident", "domain": "criminal_law"},
            {"text": "mobile hacking case", "domain": "criminal_law"},
            {"text": "phone data hacked", "domain": "criminal_law"},
            {"text": "mobile data compromised", "domain": "criminal_law"},
            {"text": "phone privacy violated online", "domain": "criminal_law"},
            {"text": "mobile security breached", "domain": "criminal_law"},
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
            {"text": "revenge porn and image abuse", "domain": "cyber_crime"},
            
            # Add examples for all expanded domains
            {"text": "cyber attack on my business network", "domain": "cyber_crime"},
            {"text": "data breach at my company", "domain": "cyber_crime"},
            {"text": "online harassment and cyberbullying", "domain": "cyber_crime"},
            {"text": "identity theft and financial fraud online", "domain": "cyber_crime"},
            {"text": "ransomware attack on hospital systems", "domain": "cyber_crime"},
            
            {"text": "drug trafficking across state borders", "domain": "drug_crimes"},
            {"text": "possession of narcotics with intent to distribute", "domain": "drug_crimes"},
            {"text": "manufacturing illegal substances in a lab", "domain": "drug_crimes"},
            {"text": "caught with drugs at airport customs", "domain": "drug_crimes"},
            {"text": "prescription fraud for controlled substances", "domain": "drug_crimes"},
            
            {"text": "financial fraud and embezzlement at corporation", "domain": "financial_crimes"},
            {"text": "insider trading of stocks for profit", "domain": "financial_crimes"},
            {"text": "tax evasion and money laundering schemes", "domain": "financial_crimes"},
            {"text": "ponzi scheme defrauding investors", "domain": "financial_crimes"},
            {"text": "bankruptcy fraud to avoid debts", "domain": "financial_crimes"},
            
            {"text": "public protest turning into violent riots", "domain": "public_order"},
            {"text": "sedition against government authorities", "domain": "public_order"},
            {"text": "terrorism and bomb threats in city", "domain": "public_order"},
            {"text": "hate speech inciting communal violence", "domain": "public_order"},
            {"text": "unlawful assembly disrupting public peace", "domain": "public_order"},
            
            {"text": "defective product causing consumer injury", "domain": "consumer_protection"},
            {"text": "false advertising of health products", "domain": "consumer_protection"},
            {"text": "warranty breach on electronic device", "domain": "consumer_protection"},
            {"text": "unfair business practices and scams", "domain": "consumer_protection"},
            {"text": "product recall due to safety concerns", "domain": "consumer_protection"},
            
            {"text": "medical malpractice during surgery", "domain": "medical_law"},
            {"text": "negligence by healthcare provider", "domain": "medical_law"},
            {"text": "wrongful death due to hospital error", "domain": "medical_law"},
            {"text": "informed consent violation by doctor", "domain": "medical_law"},
            {"text": "pharmaceutical company liability for side effects", "domain": "medical_law"},
            
            {"text": "real estate fraud in property transaction", "domain": "real_estate_law"},
            {"text": "landlord tenant dispute over lease terms", "domain": "real_estate_law"},
            {"text": "property boundary and ownership dispute", "domain": "real_estate_law"},
            {"text": "construction defect in new building", "domain": "real_estate_law"},
            {"text": "title dispute and adverse possession claim", "domain": "real_estate_law"},
            
            {"text": "breach of contract in business deal", "domain": "contract_law"},
            {"text": "contract formation and validity issues", "domain": "contract_law"},
            {"text": "performance and discharge of contractual obligations", "domain": "contract_law"},
            {"text": "contractual dispute over terms and conditions", "domain": "contract_law"},
            {"text": "specific performance of contractual agreement", "domain": "contract_law"},
            
            {"text": "patent infringement of innovative technology", "domain": "intellectual_property"},
            {"text": "trademark violation and brand counterfeiting", "domain": "intellectual_property"},
            {"text": "copyright infringement of creative work", "domain": "intellectual_property"},
            {"text": "trade secret misappropriation by competitor", "domain": "intellectual_property"},
            {"text": "intellectual property licensing dispute", "domain": "intellectual_property"},
            
            {"text": "environmental pollution affecting community", "domain": "environmental_law"},
            {"text": "industrial waste disposal violation", "domain": "environmental_law"},
            {"text": "wildlife protection and conservation", "domain": "environmental_law"},
            {"text": "climate change litigation against corporation", "domain": "environmental_law"},
            {"text": "environmental impact assessment compliance", "domain": "environmental_law"},
            
            {"text": "tax evasion and avoidance schemes", "domain": "tax_law"},
            {"text": "income tax assessment dispute", "domain": "tax_law"},
            {"text": "gst compliance and refund issues", "domain": "tax_law"},
            {"text": "customs duty evasion at border", "domain": "tax_law"},
            {"text": "tax audit and investigation procedures", "domain": "tax_law"},
            
            {"text": "visa application denial and appeal", "domain": "immigration_law"},
            {"text": "asylum and refugee protection claim", "domain": "immigration_law"},
            {"text": "deportation and removal proceedings", "domain": "immigration_law"},
            {"text": "immigration fraud and document forgery", "domain": "immigration_law"},
            {"text": "citizenship and naturalization process", "domain": "immigration_law"},
            
            {"text": "corporate governance and compliance", "domain": "corporate_law"},
            {"text": "merger and acquisition legal issues", "domain": "corporate_law"},
            {"text": "shareholder rights and disputes", "domain": "corporate_law"},
            {"text": "director liability and fiduciary duties", "domain": "corporate_law"},
            {"text": "corporate insolvency and bankruptcy", "domain": "corporate_law"},
            
            {"text": "banking fraud and financial crime", "domain": "banking_law"},
            {"text": "loan default and debt recovery", "domain": "banking_law"},
            {"text": "banking regulation and compliance", "domain": "banking_law"},
            {"text": "cheque bounce and negotiable instruments", "domain": "banking_law"},
            {"text": "bank customer protection rights", "domain": "banking_law"},
            
            {"text": "insurance claim denial and dispute", "domain": "insurance_law"},
            {"text": "insurance fraud and misrepresentation", "domain": "insurance_law"},
            {"text": "policy interpretation and coverage", "domain": "insurance_law"},
            {"text": "insurance regulation and compliance", "domain": "insurance_law"},
            {"text": "third party liability and indemnity", "domain": "insurance_law"},
            
            {"text": "student rights and educational discrimination", "domain": "education_law"},
            {"text": "academic misconduct and disciplinary action", "domain": "education_law"},
            {"text": "educational institution regulation", "domain": "education_law"},
            {"text": "special education and disability rights", "domain": "education_law"},
            {"text": "research ethics and intellectual property", "domain": "education_law"},
            
            {"text": "traffic violation and road accident", "domain": "transport_law"},
            {"text": "vehicle registration and licensing", "domain": "transport_law"},
            {"text": "transportation regulation and safety", "domain": "transport_law"},
            {"text": "commercial vehicle operation permit", "domain": "transport_law"},
            {"text": "public transport and infrastructure", "domain": "transport_law"},
            
            {"text": "sports doping and performance enhancement", "domain": "sports_law"},
            {"text": "sports betting and gambling regulation", "domain": "sports_law"},
            {"text": "athlete contract and endorsement deals", "domain": "sports_law"},
            {"text": "sports governance and regulatory compliance", "domain": "sports_law"},
            {"text": "event organization and spectator safety", "domain": "sports_law"},
            
            {"text": "media defamation and libel claims", "domain": "media_law"},
            {"text": "press freedom and censorship issues", "domain": "media_law"},
            {"text": "journalist rights and source protection", "domain": "media_law"},
            {"text": "broadcast regulation and licensing", "domain": "media_law"},
            {"text": "digital media and online content regulation", "domain": "media_law"},
            
            {"text": "human rights violation by state actors", "domain": "human_rights"},
            {"text": "freedom of expression and assembly", "domain": "human_rights"},
            {"text": "discrimination and equal protection", "domain": "human_rights"},
            {"text": "torture and cruel treatment prohibition", "domain": "human_rights"},
            {"text": "right to privacy and data protection", "domain": "human_rights"},
            
            {"text": "government regulation and administrative action", "domain": "administrative_law"},
            {"text": "public authority decision review", "domain": "administrative_law"},
            {"text": "administrative tribunal proceedings", "domain": "administrative_law"},
            {"text": "public information and transparency", "domain": "administrative_law"},
            {"text": "regulatory compliance and enforcement", "domain": "administrative_law"},
            
            {"text": "constitutional interpretation and judicial review", "domain": "constitutional_law"},
            {"text": "fundamental rights protection", "domain": "constitutional_law"},
            {"text": "separation of powers and checks", "domain": "constitutional_law"},
            {"text": "federal and state jurisdiction", "domain": "constitutional_law"},
            {"text": "constitutional amendment procedures", "domain": "constitutional_law"},
            
            {"text": "election fraud and voting rights", "domain": "election_law"},
            {"text": "campaign finance and expenditure", "domain": "election_law"},
            {"text": "electoral dispute and resolution", "domain": "election_law"},
            {"text": "candidate eligibility and nomination", "domain": "election_law"},
            {"text": "election commission authority and powers", "domain": "election_law"},
            
            {"text": "international treaty and agreement", "domain": "international_law"},
            {"text": "diplomatic immunity and privileges", "domain": "international_law"},
            {"text": "international criminal law and tribunals", "domain": "international_law"},
            {"text": "extradition and mutual legal assistance", "domain": "international_law"},
            {"text": "international trade and investment law", "domain": "international_law"}
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
        
        # Enhanced confidence handling
        if primary_confidence < self.min_confidence_for_classification:
            # For low confidence, return unknown but provide alternatives
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
        
        # Calculate accuracy if we have feedback data
        accuracy = 0.0
        if self.feedback_data:
            correct_feedback = sum(1 for feedback in self.feedback_data 
                                 if feedback.get('actual_domain') == feedback.get('predicted_domain')
                                 and feedback.get('helpful', False))
            accuracy = correct_feedback / len(self.feedback_data) if self.feedback_data else 0.0
        
        return {
            'is_trained': self.is_trained,
            'training_examples': len(self.training_data),
            'domain_count': len(self.domain_labels),
            'domains': self.domain_labels,
            'classifications_made': len(self.classification_history),
            'feedback_received': len(self.feedback_data),
            'model_accuracy': accuracy,
            'confidence_threshold': self.confidence_threshold,
            'min_confidence_for_classification': self.min_confidence_for_classification,
            'high_confidence_threshold': self.high_confidence_threshold,
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
