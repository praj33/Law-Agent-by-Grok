"""
Training Data Expander for ML Domain Classifier
==============================================

Adds harassment-related training examples to improve classification
accuracy for queries that currently fall into "unknown domain".
"""

import json
from typing import List, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class TrainingDataExpander:
    """Expands training data with harassment and edge case examples"""
    
    def __init__(self):
        """Initialize training data expander"""
        
        # New training examples for harassment cases
        self.harassment_training_data = [
            # Neighbor harassment -> Criminal Law
            {"text": "my neighbor is harassing me", "domain": "criminal_law"},
            {"text": "neighbor girl is being harassed", "domain": "criminal_law"},
            {"text": "neighbor constantly bothering me", "domain": "criminal_law"},
            {"text": "neighbor making inappropriate comments", "domain": "criminal_law"},
            {"text": "neighbor threatening me", "domain": "criminal_law"},
            {"text": "neighbor stalking me", "domain": "criminal_law"},
            {"text": "neighbor disturbing peace", "domain": "criminal_law"},
            
            # Sexual harassment -> Criminal Law
            {"text": "someone is sexually harassing me", "domain": "criminal_law"},
            {"text": "being sexually harassed at work", "domain": "employment_law"},
            {"text": "boss making sexual advances", "domain": "employment_law"},
            {"text": "colleague touching inappropriately", "domain": "employment_law"},
            {"text": "supervisor asking for sexual favors", "domain": "employment_law"},
            {"text": "workplace sexual harassment", "domain": "employment_law"},
            {"text": "eve teasing on street", "domain": "criminal_law"},
            {"text": "stranger following me", "domain": "criminal_law"},
            
            # Cyber harassment -> Cyber Crime
            {"text": "someone harassing me online", "domain": "cyber_crime"},
            {"text": "being cyberbullied on social media", "domain": "cyber_crime"},
            {"text": "receiving threatening messages online", "domain": "cyber_crime"},
            {"text": "someone stalking me on internet", "domain": "cyber_crime"},
            {"text": "fake profiles created to harass me", "domain": "cyber_crime"},
            {"text": "online harassment and threats", "domain": "cyber_crime"},
            {"text": "cyberstalking and online abuse", "domain": "cyber_crime"},
            
            # Domestic harassment -> Family Law
            {"text": "husband harassing me", "domain": "family_law"},
            {"text": "in-laws harassing for dowry", "domain": "family_law"},
            {"text": "domestic harassment by spouse", "domain": "family_law"},
            {"text": "family members threatening me", "domain": "family_law"},
            {"text": "emotional abuse by husband", "domain": "family_law"},
            {"text": "wife constantly harassing me", "domain": "family_law"},
            
            # Public harassment -> Criminal Law
            {"text": "harassment in public transport", "domain": "criminal_law"},
            {"text": "being harassed on street", "domain": "criminal_law"},
            {"text": "public harassment and catcalling", "domain": "criminal_law"},
            {"text": "harassment in market place", "domain": "criminal_law"},
            {"text": "stranger harassing me in public", "domain": "criminal_law"},
            
            # Tenant harassment -> Tenant Rights
            {"text": "landlord harassing me", "domain": "tenant_rights"},
            {"text": "property owner threatening tenant", "domain": "tenant_rights"},
            {"text": "harassment by building society", "domain": "tenant_rights"},
            {"text": "neighbor harassing about property", "domain": "tenant_rights"},
            
            # Consumer harassment -> Consumer Complaint
            {"text": "company representatives harassing me", "domain": "consumer_complaint"},
            {"text": "debt collectors harassing me", "domain": "consumer_complaint"},
            {"text": "service provider threatening me", "domain": "consumer_complaint"},
            
            # Elder harassment -> Elder Abuse
            {"text": "elderly person being harassed", "domain": "elder_abuse"},
            {"text": "harassment of senior citizen", "domain": "elder_abuse"},
            {"text": "old person being threatened", "domain": "elder_abuse"},
            
            # General harassment patterns
            {"text": "constant harassment and threats", "domain": "criminal_law"},
            {"text": "psychological harassment", "domain": "criminal_law"},
            {"text": "verbal harassment and abuse", "domain": "criminal_law"},
            {"text": "intimidation and harassment", "domain": "criminal_law"},
            {"text": "harassment causing mental trauma", "domain": "criminal_law"},
        ]
        
        # Edge cases and ambiguous queries
        self.edge_case_training_data = [
            # Property disputes
            {"text": "property boundary dispute with neighbor", "domain": "contract_dispute"},
            {"text": "land grabbing by neighbor", "domain": "criminal_law"},
            {"text": "illegal construction by neighbor", "domain": "tenant_rights"},
            
            # Noise complaints
            {"text": "neighbor making too much noise", "domain": "tenant_rights"},
            {"text": "loud music disturbing peace", "domain": "criminal_law"},
            
            # Relationship issues
            {"text": "boyfriend threatening to share photos", "domain": "cyber_crime"},
            {"text": "ex-girlfriend blackmailing me", "domain": "criminal_law"},
            {"text": "relationship dispute and threats", "domain": "criminal_law"},
            
            # Financial harassment
            {"text": "money lender harassing for payment", "domain": "consumer_complaint"},
            {"text": "bank officials threatening me", "domain": "consumer_complaint"},
            {"text": "loan recovery agents harassing", "domain": "consumer_complaint"},
            
            # Educational harassment
            {"text": "teacher harassing student", "domain": "criminal_law"},
            {"text": "college ragging and harassment", "domain": "criminal_law"},
            {"text": "school bullying and threats", "domain": "criminal_law"},
            
            # Medical harassment
            {"text": "doctor behaving inappropriately", "domain": "criminal_law"},
            {"text": "hospital staff harassing patient", "domain": "consumer_complaint"},
            
            # Transportation harassment
            {"text": "auto driver harassing me", "domain": "criminal_law"},
            {"text": "cab driver inappropriate behavior", "domain": "criminal_law"},
            {"text": "public transport harassment", "domain": "criminal_law"},
        ]
    
    def expand_training_data(self, existing_file: str = "training_data.json") -> bool:
        """Expand existing training data with harassment examples"""
        
        try:
            # Load existing training data
            existing_data = []
            if Path(existing_file).exists():
                with open(existing_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                logger.info(f"Loaded {len(existing_data)} existing training examples")
            
            # Combine with new data
            all_new_data = self.harassment_training_data + self.edge_case_training_data
            
            # Check for duplicates
            existing_texts = {item['text'].lower() for item in existing_data}
            new_examples = []
            
            for example in all_new_data:
                if example['text'].lower() not in existing_texts:
                    new_examples.append(example)
            
            # Add new examples
            expanded_data = existing_data + new_examples
            
            # Save expanded training data
            with open(existing_file, 'w', encoding='utf-8') as f:
                json.dump(expanded_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Added {len(new_examples)} new training examples")
            logger.info(f"Total training examples: {len(expanded_data)}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error expanding training data: {e}")
            return False
    
    def create_harassment_focused_dataset(self, output_file: str = "harassment_training_data.json") -> bool:
        """Create a focused dataset for harassment-related queries"""
        
        try:
            # Combine all harassment data
            harassment_dataset = self.harassment_training_data + self.edge_case_training_data
            
            # Add domain statistics
            domain_counts = {}
            for example in harassment_dataset:
                domain = example['domain']
                domain_counts[domain] = domain_counts.get(domain, 0) + 1
            
            dataset_info = {
                'metadata': {
                    'total_examples': len(harassment_dataset),
                    'domains_covered': list(domain_counts.keys()),
                    'domain_distribution': domain_counts,
                    'focus': 'harassment_and_edge_cases',
                    'created_for': 'improving_unknown_domain_classification'
                },
                'training_data': harassment_dataset
            }
            
            # Save harassment-focused dataset
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(dataset_info, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Created harassment-focused dataset with {len(harassment_dataset)} examples")
            logger.info(f"Domain distribution: {domain_counts}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating harassment dataset: {e}")
            return False
    
    def get_domain_suggestions_for_query(self, query: str) -> List[Dict[str, Any]]:
        """Get domain suggestions for a specific query based on training patterns"""
        
        query_lower = query.lower()
        suggestions = []
        
        # Check against harassment patterns
        for example in self.harassment_training_data + self.edge_case_training_data:
            example_words = set(example['text'].lower().split())
            query_words = set(query_lower.split())
            
            # Calculate word overlap
            overlap = len(example_words.intersection(query_words))
            if overlap >= 2:  # At least 2 words in common
                similarity = overlap / len(example_words.union(query_words))
                suggestions.append({
                    'domain': example['domain'],
                    'similarity': similarity,
                    'matching_example': example['text'],
                    'reason': f"Similar to: '{example['text']}'"
                })
        
        # Sort by similarity and remove duplicates
        suggestions.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Keep top unique domains
        seen_domains = set()
        unique_suggestions = []
        for suggestion in suggestions:
            if suggestion['domain'] not in seen_domains:
                unique_suggestions.append(suggestion)
                seen_domains.add(suggestion['domain'])
                if len(unique_suggestions) >= 3:
                    break
        
        return unique_suggestions


def retrain_ml_classifier_with_harassment_data():
    """Retrain the ML classifier with expanded harassment data"""
    
    try:
        from ml_domain_classifier import create_ml_domain_classifier
        
        # Expand training data
        expander = TrainingDataExpander()
        success = expander.expand_training_data()
        
        if not success:
            print("Failed to expand training data")
            return False
        
        # Create new classifier and retrain
        classifier = create_ml_domain_classifier()
        
        # Force retrain with new data
        classifier.train_models()
        classifier.save_models()
        
        print("✅ ML classifier retrained with harassment data")
        print(f"📊 New model stats: {classifier.get_model_stats()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error retraining classifier: {e}")
        return False


# Test the training data expander
if __name__ == "__main__":
    print("🔧 TRAINING DATA EXPANDER TEST")
    print("=" * 50)
    
    expander = TrainingDataExpander()
    
    # Test domain suggestions
    test_queries = [
        "my neighbor girl is being harassed",
        "boss sexually harassing me",
        "someone stalking me online",
        "landlord threatening me"
    ]
    
    for query in test_queries:
        print(f"\nQuery: \"{query}\"")
        suggestions = expander.get_domain_suggestions_for_query(query)
        
        print("Domain Suggestions:")
        for suggestion in suggestions:
            print(f"  • {suggestion['domain']} ({suggestion['similarity']:.2f}): {suggestion['reason']}")
    
    # Create harassment dataset
    print(f"\n🔧 Creating harassment-focused dataset...")
    success = expander.create_harassment_focused_dataset()
    
    if success:
        print("✅ Harassment dataset created successfully")
    else:
        print("❌ Failed to create harassment dataset")
    
    # Expand existing training data
    print(f"\n🔧 Expanding existing training data...")
    success = expander.expand_training_data()
    
    if success:
        print("✅ Training data expanded successfully")
        print("🔄 Ready to retrain ML classifier")
    else:
        print("❌ Failed to expand training data")
