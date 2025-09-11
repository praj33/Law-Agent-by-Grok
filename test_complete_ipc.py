#!/usr/bin/env python3
"""
Test script for complete IPC sections integration
"""

from complete_legal_database import create_complete_legal_database
from complete_ipc_sections_full import create_complete_ipc_database


def test_complete_ipc_integration():
    """Test that complete IPC sections are properly integrated"""
    
    print("🔍 Testing Complete IPC Sections Integration")
    print("=" * 50)
    
    # Test 1: Check that complete IPC database has all 256 sections
    ipc_db = create_complete_ipc_database()
    print(f"✅ Complete IPC Database Sections: {len(ipc_db)}")
    
    # Display first 10 sections
    print("\n📋 First 10 IPC Sections:")
    for i, (section_num, section_data) in enumerate(list(ipc_db.items())[:10]):
        print(f"   {section_num}: {section_data['title']}")
    
    # Display last 10 sections
    print("\n📋 Last 10 IPC Sections:")
    for i, (section_num, section_data) in enumerate(list(ipc_db.items())[-10:]):
        print(f"   {section_num}: {section_data['title']}")
    
    # Test 2: Check that legal database uses complete IPC sections
    legal_db = create_complete_legal_database()
    print(f"\n✅ Legal Database IPC Sections: {len(legal_db.ipc_sections)}")
    
    # Test 3: Query test
    print("\n🔍 Query Test:")
    query_result = legal_db.get_all_sections_for_query("criminal_law", "theft", "Someone stole my phone")
    print(f"   BNS Sections Found: {len(query_result['bns_sections'])}")
    print(f"   IPC Sections Found: {len(query_result['ipc_sections'])}")
    print(f"   CrPC Sections Found: {len(query_result['crpc_sections'])}")
    
    # Show some IPC sections from query result
    if query_result['ipc_sections']:
        print("\n📋 IPC Sections from Query:")
        for section in query_result['ipc_sections'][:5]:
            print(f"   Section {section['section_number']}: {section['title']}")
    
    # Test 4: Specific section check
    print("\n🔍 Specific Section Check:")
    section_302 = ipc_db.get("302")
    if section_302:
        print(f"   Section 302: {section_302['title']}")
    else:
        print("   Section 302: NOT FOUND")
    
    section_124A = ipc_db.get("124A")
    if section_124A:
        print(f"   Section 124A: {section_124A['title']}")
    else:
        print("   Section 124A: NOT FOUND")
    
    section_228A = ipc_db.get("228A")
    if section_228A:
        print(f"   Section 228A: {section_228A['title']}")
    else:
        print("   Section 228A: NOT FOUND")
    
    print("\n✅ Integration Test Complete!")


if __name__ == "__main__":
    test_complete_ipc_integration()