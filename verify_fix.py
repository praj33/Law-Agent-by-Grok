"""
Quick Verification of Phone Theft Fix
=====================================

This script quickly verifies that "My phone is stolen" is now 
correctly classified as "criminal_law" instead of "cyber_crime".
"""

def verify_phone_theft_fix():
    """Verify the specific query that was problematic"""
    
    print("🔍 VERIFYING PHONE THEFT CLASSIFICATION FIX")
    print("=" * 50)
    
    try:
        from ml_domain_classifier import create_ml_domain_classifier
        classifier = create_ml_domain_classifier()
        
        # Test the exact query from the user's issue
        query = "My phone is stolen"
        domain, confidence, alternatives = classifier.classify_with_confidence(query)
        
        print(f"Query: \"{query}\"")
        print(f"Classification: {domain}")
        print(f"Confidence: {confidence:.3f}")
        
        if domain == "criminal_law":
            print("✅ SUCCESS! Query is now correctly classified as criminal_law")
            print("   The fix is working properly!")
            return True
        elif domain == "cyber_crime":
            print("❌ ISSUE: Query is still being classified as cyber_crime")
            print("   The fix may not be working properly")
            return False
        else:
            print(f"⚠️  UNEXPECTED: Query classified as {domain}")
            print("   This is neither the old nor expected classification")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


if __name__ == "__main__":
    success = verify_phone_theft_fix()
    
    if success:
        print("\n🎉 Your terminal should now work correctly!")
        print("   Try typing 'My phone is stolen' in your terminal.")
    else:
        print("\n❌ The fix may need additional work.")