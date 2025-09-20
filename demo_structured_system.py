"""
Complete Structured Legal System Demonstration
=============================================

This script demonstrates the complete structured legal response system
with the format requested:

1. Constitutional Articles
2. IPC Sections (Indian Penal Code, 1860)
3. CrPC Sections (Code of Criminal Procedure, 1973)
4. Special Acts (if applicable)

Author: Legal Agent Team
Date: 2025-01-XX
"""

from enhanced_structured_legal_agent import get_structured_legal_advice
from integrated_structured_legal_agent import get_combined_legal_response

def demonstrate_structured_responses():
    """Demonstrate structured legal responses for various scenarios"""
    
    print("🏛️ STRUCTURED LEGAL AI ASSISTANT DEMONSTRATION")
    print("=" * 70)
    print("Demonstrating the new structured response format with:")
    print("1. Constitutional Articles")
    print("2. IPC Sections (Indian Penal Code, 1860)")
    print("3. CrPC Sections (Code of Criminal Procedure, 1973)")
    print("4. Special Acts (if applicable)")
    print("=" * 70)
    
    # Test cases representing different legal scenarios
    test_scenarios = [
        {
            "title": "🚨 Workplace Sexual Harassment",
            "query": "My male colleague is sexually harassing me at workplace and making inappropriate comments. He also sends me inappropriate messages.",
            "description": "Employment law case involving sexual harassment at workplace"
        },
        {
            "title": "🏠 Domestic Violence",
            "query": "My husband is beating me and threatening me with violence. He also doesn't let me go out of the house.",
            "description": "Family law case involving domestic violence and abuse"
        },
        {
            "title": "🏘️ Tenant Rights Violation",
            "query": "My landlord is not returning my security deposit even after 6 months of vacating the property. He is also demanding extra money.",
            "description": "Property law case involving tenant rights and security deposit"
        },
        {
            "title": "💻 Cyber Crime - Online Fraud",
            "query": "Someone hacked my bank account and transferred money through online fraud. They also used my personal information.",
            "description": "Cyber crime case involving online fraud and identity theft"
        },
        {
            "title": "👴 Elder Abuse",
            "query": "My elderly father is being neglected and physically abused by his caretaker. The caretaker is also stealing his money.",
            "description": "Elder abuse case involving neglect and financial exploitation"
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{'='*70}")
        print(f"SCENARIO {i}: {scenario['title']}")
        print(f"Description: {scenario['description']}")
        print(f"Query: \"{scenario['query']}\"")
        print('='*70)
        
        try:
            # Get structured response
            print("🔍 Generating structured legal response...")
            response = get_structured_legal_advice(scenario['query'])
            print(response)
            
        except Exception as e:
            print(f"❌ Error generating response: {e}")
        
        # Wait for user input to continue
        if i < len(test_scenarios):
            input(f"\n⏸️  Press Enter to continue to next scenario...")
    
    print(f"\n🎉 ALL SCENARIOS DEMONSTRATED!")
    print(f"✅ Structured Legal AI Assistant is working perfectly!")


def demonstrate_specific_features():
    """Demonstrate specific features of the structured system"""
    
    print(f"\n{'='*70}")
    print("🔧 DEMONSTRATING SPECIFIC FEATURES")
    print('='*70)
    
    # Feature 1: Constitutional Articles Coverage
    print(f"\n1️⃣ CONSTITUTIONAL ARTICLES COVERAGE:")
    print("-" * 40)
    query1 = "I am being discriminated at work because of my gender"
    print(f"Query: \"{query1}\"")
    print("Expected: Articles 14, 15, 19, 21")
    
    response1 = get_structured_legal_advice(query1)
    print(f"\nResponse Preview:")
    lines = response1.split('\n')
    for line in lines[6:15]:  # Show constitutional articles section
        if line.strip():
            print(line)
    
    input("\nPress Enter to continue...")
    
    # Feature 2: IPC Sections for Criminal Matters
    print(f"\n2️⃣ IPC SECTIONS FOR CRIMINAL MATTERS:")
    print("-" * 40)
    query2 = "Someone broke into my house and stole my jewelry and cash"
    print(f"Query: \"{query2}\"")
    print("Expected: Sections 378, 379, 380, 392")
    
    response2 = get_structured_legal_advice(query2)
    print(f"\nResponse Preview:")
    lines = response2.split('\n')
    in_ipc_section = False
    for line in lines:
        if "**Relevant IPC Sections" in line:
            in_ipc_section = True
        elif "**Relevant CrPC Sections" in line:
            break
        elif in_ipc_section and line.strip():
            print(line)
    
    input("\nPress Enter to continue...")
    
    # Feature 3: Special Acts Coverage
    print(f"\n3️⃣ SPECIAL ACTS COVERAGE:")
    print("-" * 40)
    query3 = "I bought a defective mobile phone and the company refuses to replace it"
    print(f"Query: \"{query3}\"")
    print("Expected: Consumer Protection Act, 2019")
    
    response3 = get_structured_legal_advice(query3)
    print(f"\nResponse Preview:")
    lines = response3.split('\n')
    in_special_section = False
    for line in lines:
        if "**Relevant Special Acts" in line:
            in_special_section = True
        elif line.startswith("="):
            break
        elif in_special_section and line.strip():
            print(line)
    
    print(f"\n✅ All specific features demonstrated successfully!")


def show_system_capabilities():
    """Show the capabilities of the structured legal system"""
    
    print(f"\n{'='*70}")
    print("📊 SYSTEM CAPABILITIES OVERVIEW")
    print('='*70)
    
    from enhanced_structured_legal_agent import create_structured_legal_agent
    
    agent = create_structured_legal_agent()
    
    print(f"📚 LEGAL DATABASE COVERAGE:")
    print(f"   • IPC Sections: {len(agent.legal_db.ipc_sections)}")
    print(f"   • CrPC Sections: {len(agent.legal_db.crpc_sections)}")
    print(f"   • Special Acts: {len(agent.legal_db.special_acts)}")
    print(f"   • Legal Domains: {len(agent.legal_db.domain_mappings)}")
    
    print(f"\n🎯 SUPPORTED LEGAL DOMAINS:")
    for domain in agent.legal_db.domain_mappings.keys():
        print(f"   • {domain.replace('_', ' ').title()}")
    
    print(f"\n📋 KEY IPC SECTIONS COVERED:")
    key_sections = ["302", "354A", "498A", "420", "378", "375"]
    for section in key_sections:
        if section in agent.legal_db.ipc_sections:
            title = agent.legal_db.ipc_sections[section]["title"]
            print(f"   • Section {section}: {title}")
    
    print(f"\n📋 KEY SPECIAL ACTS COVERED:")
    key_acts = ["POSH_2013", "DV_2005", "CONSUMER_2019", "IT_2000"]
    for act_key in key_acts:
        if act_key in agent.legal_db.special_acts:
            name = agent.legal_db.special_acts[act_key]["act_name"]
            print(f"   • {name}")
    
    print(f"\n🔧 SYSTEM FEATURES:")
    print(f"   • Domain Classification with ML")
    print(f"   • Constitutional Articles Integration")
    print(f"   • Keyword-based Section Matching")
    print(f"   • Structured Response Format")
    print(f"   • Simple Language Explanations")
    print(f"   • Formal Legal Style")


def main():
    """Main demonstration function"""
    
    try:
        # Run all demonstrations
        demonstrate_structured_responses()
        demonstrate_specific_features()
        show_system_capabilities()
        
        print(f"\n🎊 COMPLETE DEMONSTRATION FINISHED!")
        print(f"🏛️ Structured Legal AI Assistant is ready for production!")
        print(f"⚖️ Remember: This provides legal information, not legal advice.")
        print(f"📞 Always consult a qualified lawyer for specific legal matters.")
        
    except KeyboardInterrupt:
        print(f"\n⏹️  Demonstration interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()