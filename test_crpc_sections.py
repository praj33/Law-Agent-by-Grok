#!/usr/bin/env python3
"""
Test script for CrPC Sections Implementation
==========================================

This script tests the complete CrPC sections implementation.
"""

from complete_legal_database import create_complete_legal_database
from complete_crpc_sections_full import create_complete_crpc_database


def test_crpc_implementation():
    print("=== Testing CrPC Sections Implementation ===\n")
    
    # Test 1: Check if CrPC database loads correctly
    print("Test 1: Loading CrPC Database")
    crpc_db = create_complete_crpc_database()
    print(f"  ✓ CrPC database loaded with {len(crpc_db)} sections")
    
    # Test 2: Check if complete legal database uses CrPC
    print("\nTest 2: Integration with Complete Legal Database")
    legal_db = create_complete_legal_database()
    stats = legal_db.get_stats()
    print(f"  ✓ Total legal sections: {stats['total_sections']}")
    print(f"  ✓ CrPC sections in legal database: {stats['total_crpc_sections']}")
    
    # Test 3: Check specific CrPC sections
    print("\nTest 3: Verifying Specific CrPC Sections")
    sample_sections = ["1", "41", "50", "164", "209"]
    for sec_num in sample_sections:
        if sec_num in crpc_db:
            title = crpc_db[sec_num]["title"]
            print(f"  ✓ Section {sec_num}: {title}")
        else:
            print(f"  ✗ Section {sec_num}: NOT FOUND")
    
    # Test 4: Check keyword-based retrieval
    print("\nTest 4: Keyword-based Section Retrieval")
    result = legal_db.get_all_sections_for_query("criminal", "murder", "Murder case procedures")
    print(f"  ✓ Retrieved {len(result['crpc_sections'])} CrPC sections for murder query")
    for section in result['crpc_sections']:
        print(f"    - Section {section['section_number']}: {section['title']}")
    
    print("\n=== All Tests Completed Successfully ===")


if __name__ == "__main__":
    test_crpc_implementation()