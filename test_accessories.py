#!/usr/bin/env python3
"""
Test all accessories and components to ensure they are working properly
"""

def test_all_components():
    print("🧪 TESTING ALL ACCESSORIES AND COMPONENTS")
    print("=" * 50)
    
    # Test 1: ML Domain Classifier
    print("1. Testing ML Domain Classifier...")
    try:
        from ml_domain_classifier import create_ml_domain_classifier
        classifier = create_ml_domain_classifier()
        domain, confidence, alternatives = classifier.classify_with_confidence("my phone was stolen")
        print(f"   ✅ ML Classifier working: '{domain}' (confidence: {confidence:.3f})")
    except Exception as e:
        print(f"   ❌ ML Classifier failed: {e}")
        return False
    
    # Test 2: Working Enhanced Agent
    print("2. Testing Working Enhanced Agent...")
    try:
        from working_enhanced_agent import create_working_enhanced_agent
        agent = create_working_enhanced_agent()
        response = agent.process_query("my phone was stolen")
        print(f"   ✅ Enhanced Agent working: '{response.domain}' (confidence: {response.confidence:.3f})")
    except Exception as e:
        print(f"   ❌ Enhanced Agent failed: {e}")
        return False
    
    # Test 3: Ultimate Legal Agent
    print("3. Testing Ultimate Legal Agent...")
    try:
        from ultimate_legal_agent import UltimateLegalAgent
        agent = UltimateLegalAgent()
        response = agent.process_ultimate_query("my phone was stolen")
        print(f"   ✅ Ultimate Agent working: '{response.get('domain', 'N/A')}'")
    except Exception as e:
        print(f"   ❌ Ultimate Agent failed: {e}")
        return False
    
    # Test 4: Web Interface Components
    print("4. Testing Web Interface Components...")
    try:
        from simple_web_interface import initialize_agent
        if initialize_agent():
            print(f"   ✅ Web Interface Agent initialized")
        else:
            print(f"   ❌ Web Interface Agent failed to initialize")
            return False
    except Exception as e:
        print(f"   ❌ Web Interface test failed: {e}")
        return False
    
    # Test 5: Legal Database
    print("5. Testing Legal Database...")
    try:
        from complete_legal_database import create_complete_legal_database
        db = create_complete_legal_database()
        sections = db.get_all_sections_for_query("criminal_law", "theft", "my phone was stolen")
        total_sections = len(sections["bns_sections"]) + len(sections["ipc_sections"]) + len(sections["crpc_sections"])
        print(f"   ✅ Legal Database working: {total_sections} sections found")
    except Exception as e:
        print(f"   ❌ Legal Database failed: {e}")
        return False
    
    print("\n🎉 ALL ACCESSORIES AND COMPONENTS ARE WORKING PROPERLY!")
    return True

if __name__ == "__main__":
    success = test_all_components()
    if success:
        print("\n✅ System is ready for use!")
    else:
        print("\n❌ Some components need attention!")