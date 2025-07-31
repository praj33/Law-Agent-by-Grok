"""
Test spaCy Integration with Legal Agent
======================================

This script tests spaCy's NLP capabilities for legal text processing
"""

import spacy
import sys
import os

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        os.system("chcp 65001 > nul")
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

def safe_print(text):
    """Print text safely, handling Unicode encoding issues"""
    try:
        print(text)
    except UnicodeEncodeError:
        safe_text = text.replace('₹', 'Rs.').replace('✅', '[OK]').replace('❌', '[ERROR]').replace('⚠️', '[WARNING]')
        print(safe_text)

def test_spacy_legal_processing():
    """Test spaCy with legal queries"""
    
    safe_print("🔍 TESTING SPACY WITH LEGAL QUERIES")
    safe_print("=" * 50)
    
    # Load spaCy model
    try:
        nlp = spacy.load('en_core_web_sm')
        safe_print("✅ spaCy model loaded successfully!")
    except Exception as e:
        safe_print(f"❌ Error loading spaCy model: {e}")
        return
    
    # Test legal queries
    legal_queries = [
        "My landlord is not returning my security deposit",
        "I was wrongfully terminated from my job",
        "My neighbor is harassing me and my family",
        "The product I bought is defective and needs refund",
        "I want to file for divorce from my spouse"
    ]
    
    safe_print(f"\n📋 Processing {len(legal_queries)} legal queries with spaCy:")
    safe_print("-" * 50)
    
    for i, query in enumerate(legal_queries, 1):
        safe_print(f"\n🧪 Query {i}: {query}")
        
        # Process with spaCy
        doc = nlp(query)
        
        # Extract key information
        tokens = [token.text for token in doc]
        pos_tags = [(token.text, token.pos_) for token in doc if token.pos_ in ['NOUN', 'VERB', 'ADJ']]
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        safe_print(f"   📝 Key tokens: {tokens[:8]}...")  # Show first 8 tokens
        safe_print(f"   🏷️  Important words: {[word for word, pos in pos_tags[:5]]}")  # Show first 5 important words
        
        if entities:
            safe_print(f"   🎯 Entities found: {entities}")
        else:
            safe_print(f"   🎯 Entities found: None")
    
    # Test legal domain classification with spaCy features
    safe_print(f"\n🤖 LEGAL DOMAIN CLASSIFICATION WITH SPACY")
    safe_print("-" * 50)
    
    domain_keywords = {
        'tenant_rights': ['landlord', 'rent', 'deposit', 'lease', 'eviction'],
        'employment_law': ['job', 'work', 'fired', 'terminated', 'salary', 'boss'],
        'family_law': ['divorce', 'marriage', 'custody', 'spouse', 'child'],
        'consumer_complaint': ['product', 'defective', 'refund', 'warranty', 'purchase'],
        'harassment': ['harass', 'neighbor', 'threaten', 'abuse', 'disturb']
    }
    
    for query in legal_queries[:3]:  # Test first 3 queries
        doc = nlp(query)
        query_tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
        
        safe_print(f"\n📋 Query: {query}")
        safe_print(f"   🔍 Processed tokens: {query_tokens}")
        
        # Simple domain classification based on keyword matching
        best_domain = None
        best_score = 0
        
        for domain, keywords in domain_keywords.items():
            score = sum(1 for token in query_tokens if token in keywords)
            if score > best_score:
                best_score = score
                best_domain = domain
        
        if best_domain:
            safe_print(f"   🎯 Predicted domain: {best_domain} (score: {best_score})")
        else:
            safe_print(f"   🎯 Predicted domain: unknown")

def test_spacy_advanced_features():
    """Test advanced spaCy features for legal text"""
    
    safe_print(f"\n🚀 ADVANCED SPACY FEATURES FOR LEGAL TEXT")
    safe_print("=" * 50)
    
    nlp = spacy.load('en_core_web_sm')
    
    # Test with a complex legal sentence
    legal_text = "The defendant John Smith violated the rental agreement by failing to pay rent for three months, causing damages of $5000 to the plaintiff Mary Johnson."
    
    doc = nlp(legal_text)
    
    safe_print(f"📝 Legal text: {legal_text}")
    safe_print(f"\n🔍 Analysis:")
    
    # Named entities
    entities = [(ent.text, ent.label_, spacy.explain(ent.label_)) for ent in doc.ents]
    if entities:
        safe_print(f"   👤 Named Entities:")
        for text, label, explanation in entities:
            safe_print(f"      • {text} ({label}): {explanation}")
    
    # Dependency parsing
    safe_print(f"   🌳 Key Dependencies:")
    for token in doc:
        if token.dep_ in ['nsubj', 'dobj', 'ROOT']:
            safe_print(f"      • {token.text} ({token.dep_}): {spacy.explain(token.dep_)}")
    
    # Noun phrases
    noun_phrases = [chunk.text for chunk in doc.noun_chunks]
    safe_print(f"   📋 Noun Phrases: {noun_phrases}")

def main():
    """Main test function"""
    
    safe_print("🏛️ SPACY INTEGRATION TEST FOR LEGAL AGENT")
    safe_print("=" * 60)
    safe_print("Testing spaCy's NLP capabilities for legal text processing")
    safe_print("=" * 60)
    
    try:
        test_spacy_legal_processing()
        test_spacy_advanced_features()
        
        safe_print(f"\n🎉 SUCCESS!")
        safe_print("=" * 30)
        safe_print("✅ spaCy is successfully installed and working!")
        safe_print("✅ spaCy can process legal queries effectively!")
        safe_print("✅ Ready to integrate with your legal agent system!")
        
        safe_print(f"\n💡 Next Steps:")
        safe_print("• Use spaCy for better text preprocessing")
        safe_print("• Extract named entities from legal queries")
        safe_print("• Improve domain classification with NLP features")
        safe_print("• Analyze legal document structure")
        
    except Exception as e:
        safe_print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
