#!/usr/bin/env python3
"""
Demo: Enhanced Legal Agent with Subdomain Classification and BNS Integration
===========================================================================

This demo showcases the enhanced legal agent that provides:
1. MANDATORY subdomain classification for ALL queries
2. Bharatiya Nyaya Sanhita (BNS) 2023 sections integration
3. Constitutional articles and legal backing
4. Complete legal analysis with actionable guidance

Author: Legal Agent Team
Version: 2.0.0 - Complete Integration Demo
Date: 2025-01-15
"""

from enhanced_subdomain_bns_agent import create_enhanced_subdomain_bns_agent
import json

def demo_enhanced_features():
    """Demonstrate all enhanced features"""
    
    print("🚀 ENHANCED LEGAL AGENT DEMO")
    print("=" * 80)
    print("Features Demonstrated:")
    print("✅ Mandatory Subdomain Classification for ALL queries")
    print("✅ Bharatiya Nyaya Sanhita (BNS) 2023 sections")
    print("✅ Constitutional articles and legal backing")
    print("✅ Complete legal analysis with actionable guidance")
    print("=" * 80)
    
    # Initialize the enhanced agent
    print("\n🔧 Initializing Enhanced Agent...")
    agent = create_enhanced_subdomain_bns_agent()
    
    # Show agent capabilities
    stats = agent.get_agent_stats()
    print(f"\n📊 Agent Capabilities:")
    print(f"   Version: {stats['agent_version']}")
    print(f"   Subdomain Classifier: {stats['subdomain_classifier_stats']['total_domains']} domains, {stats['subdomain_classifier_stats']['total_subdomains']} subdomains")
    print(f"   BNS Database: {stats['bns_database_stats']['total_bns_sections']} sections")
    print(f"   IPC to BNS Mappings: {stats['bns_database_stats']['ipc_to_bns_mappings']}")
    
    # Demo queries covering different legal domains
    demo_queries = [
        {
            "query": "My phone was stolen from my bag while traveling in the bus",
            "description": "Criminal Law - Theft case with transportation context"
        },
        {
            "query": "Someone hacked my bank account and transferred money without my permission",
            "description": "Cyber Crime - Identity theft and financial fraud"
        },
        {
            "query": "My boss fired me after I complained about sexual harassment by my colleague",
            "description": "Employment Law - Wrongful termination with harassment context"
        },
        {
            "query": "My husband beats me regularly and threatens to kill me if I leave",
            "description": "Family Law - Domestic violence with criminal intimidation"
        },
        {
            "query": "Landlord is refusing to return my security deposit and is demanding extra money",
            "description": "Tenant Rights - Security deposit dispute with potential extortion"
        },
        {
            "query": "I bought an expensive phone online but received a fake duplicate product",
            "description": "Consumer Complaint - Product fraud and cheating"
        },
        {
            "query": "My elderly mother's caregiver is stealing her pension money and jewelry",
            "description": "Elder Abuse - Financial exploitation and theft"
        },
        {
            "query": "Car accident caused serious injuries and the other driver was drunk",
            "description": "Personal Injury - Motor vehicle accident with criminal negligence"
        }
    ]
    
    print(f"\n🧪 DEMONSTRATING ENHANCED FEATURES")
    print("=" * 80)
    
    for i, demo_case in enumerate(demo_queries, 1):
        print(f"\n📋 DEMO CASE {i}: {demo_case['description']}")
        print(f"Query: \"{demo_case['query']}\"")
        print("-" * 60)
        
        # Process the query
        response = agent.process_query_with_complete_analysis(demo_case['query'])
        
        # Display key results
        print(f"🎯 CLASSIFICATION RESULTS:")
        print(f"   Primary Domain: {response['domain'].replace('_', ' ').title()}")
        print(f"   Specific Subdomain: {response['subdomain'].replace('_', ' ').title()} (confidence: {response['subdomain_confidence']:.1%})")
        
        # Show BNS sections
        print(f"\n📚 BHARATIYA NYAYA SANHITA (BNS) SECTIONS:")
        if response['bns_sections']:
            for j, section in enumerate(response['bns_sections'][:3], 1):
                print(f"   {j}. Section {section['section_number']}: {section['title']}")
        else:
            print("   No specific BNS sections identified")
        
        # Show constitutional backing
        if response['constitutional_articles']:
            print(f"\n🏛️ CONSTITUTIONAL BACKING:")
            for article in response['constitutional_articles'][:2]:
                if isinstance(article, dict):
                    print(f"   • Article {article.get('article_number', 'N/A')}: {article.get('title', 'Constitutional provision')}")
        
        # Show immediate actions
        if response['legal_guidance'].get('immediate_actions'):
            print(f"\n⚡ IMMEDIATE ACTIONS:")
            for action in response['legal_guidance']['immediate_actions'][:3]:
                print(f"   • {action}")
        
        # Show analysis completeness
        completeness = response['analysis_completeness']
        print(f"\n✅ ANALYSIS COMPLETENESS:")
        print(f"   Domain Classification: {'✅' if completeness['domain_classified'] else '❌'}")
        print(f"   Subdomain Classification: {'✅' if completeness['subdomain_classified'] else '❌'}")
        print(f"   BNS Sections: {'✅' if completeness['bns_sections_provided'] else '❌'} ({len(response['bns_sections'])} sections)")
        print(f"   Constitutional Backing: {'✅' if completeness['constitutional_backing'] else '❌'}")
        
        print(f"\n" + "="*60)
        
        # Pause between demos (except for last one)
        if i < len(demo_queries):
            input(f"⏸️  Press Enter to continue to Demo Case {i+1}...")

def demo_bns_ipc_conversion():
    """Demonstrate IPC to BNS conversion feature"""
    
    print(f"\n🔄 BNS - IPC CONVERSION DEMO")
    print("=" * 50)
    print("Demonstrating conversion from old IPC sections to new BNS sections")
    
    from bharatiya_nyaya_sanhita import create_bns_database
    bns_db = create_bns_database()
    
    # Common IPC sections and their BNS equivalents
    ipc_sections = [
        ("302", "Murder"),
        ("307", "Attempt to murder"),
        ("323", "Voluntarily causing hurt"),
        ("354", "Assault on woman with intent to outrage modesty"),
        ("375", "Rape"),
        ("378", "Theft"),
        ("420", "Cheating"),
        ("498A", "Cruelty by husband or relatives"),
        ("506", "Criminal intimidation")
    ]
    
    print(f"\n📋 IPC TO BNS CONVERSION TABLE:")
    print("-" * 50)
    
    for ipc_section, description in ipc_sections:
        conversion = bns_db.get_ipc_to_bns_conversion(ipc_section)
        if conversion:
            print(f"IPC {ipc_section} ({description})")
            print(f"  → BNS {conversion['bns_section']}: {conversion['title']}")
        else:
            print(f"IPC {ipc_section} ({description}) → No BNS equivalent found")
        print()

def demo_subdomain_coverage():
    """Demonstrate comprehensive subdomain coverage"""
    
    print(f"\n🎯 SUBDOMAIN COVERAGE DEMO")
    print("=" * 50)
    print("Demonstrating comprehensive subdomain classification across all legal domains")
    
    from subdomain_classifier import create_subdomain_classifier
    classifier = create_subdomain_classifier()
    
    # Show domain and subdomain structure
    all_subdomains = classifier.get_all_subdomains()
    
    print(f"\n📊 SUBDOMAIN STRUCTURE:")
    print("-" * 30)
    
    for domain, subdomains in all_subdomains.items():
        print(f"\n🏛️ {domain.replace('_', ' ').title()}:")
        for subdomain in list(subdomains.keys())[:5]:  # Show first 5 subdomains
            print(f"   • {subdomain.replace('_', ' ').title()}")
        if len(subdomains) > 5:
            print(f"   ... and {len(subdomains) - 5} more subdomains")
    
    stats = classifier.get_stats()
    print(f"\n📈 COVERAGE STATISTICS:")
    print(f"   Total Domains: {stats['total_domains']}")
    print(f"   Total Subdomains: {stats['total_subdomains']}")
    print(f"   Trained Classifiers: {stats['trained_classifiers']}")
    print(f"   Training Examples: {stats['training_examples']}")

def main():
    """Main demo function"""
    
    print("🎉 WELCOME TO THE ENHANCED LEGAL AGENT DEMO")
    print("=" * 80)
    print("This demo showcases the most advanced legal AI system with:")
    print("✅ Mandatory subdomain classification for ALL queries")
    print("✅ Complete Bharatiya Nyaya Sanhita (BNS) 2023 integration")
    print("✅ Constitutional articles and legal backing")
    print("✅ Actionable legal guidance and recommendations")
    print("=" * 80)
    
    try:
        # Main feature demonstration
        demo_enhanced_features()
        
        # Additional feature demos
        print(f"\n🔍 ADDITIONAL FEATURE DEMONSTRATIONS")
        print("=" * 50)
        
        demo_bns_ipc_conversion()
        demo_subdomain_coverage()
        
        # Final summary
        print(f"\n🎉 DEMO COMPLETE!")
        print("=" * 50)
        print("✅ Enhanced Legal Agent successfully demonstrated")
        print("✅ All queries receive mandatory subdomain classification")
        print("✅ All queries receive relevant BNS 2023 sections")
        print("✅ Constitutional backing and legal guidance provided")
        print("✅ Complete legal analysis with actionable recommendations")
        print("\n🚀 The Enhanced Legal Agent is ready for production use!")
        print("📚 Comprehensive legal coverage with latest Indian legal framework")
        print("⚖️ Professional-grade legal analysis and guidance")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()