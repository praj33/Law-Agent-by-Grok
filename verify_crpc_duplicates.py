#!/usr/bin/env python3
"""
Verification script for CrPC Sections - Check for Duplicates
==========================================================

This script verifies that there are no duplicate sections in the CrPC database.
"""

from complete_crpc_sections import create_complete_crpc_database


def verify_no_duplicates():
    print("=== Verifying CrPC Sections for Duplicates ===\n")
    
    # Load the CrPC database
    crpc_db = create_complete_crpc_database()
    print(f"Total CrPC sections: {len(crpc_db)}")
    
    # Get all section numbers
    section_numbers = list(crpc_db.keys())
    
    # Check for duplicates
    unique_sections = set(section_numbers)
    duplicate_count = len(section_numbers) - len(unique_sections)
    
    print(f"Unique section numbers: {len(unique_sections)}")
    print(f"Duplicate sections found: {duplicate_count}")
    
    if duplicate_count == 0:
        print("  ✓ NO DUPLICATES FOUND - All section numbers are unique")
    else:
        print("  ✗ DUPLICATES FOUND - Please check the database")
        # Find duplicates
        seen = set()
        duplicates = set()
        for section in section_numbers:
            if section in seen:
                duplicates.add(section)
            else:
                seen.add(section)
        print(f"  Duplicate section numbers: {duplicates}")
    
    # Show some statistics
    print("\n=== Section Number Analysis ===")
    numeric_sections = [sec for sec in section_numbers if sec.isdigit()]
    alphanumeric_sections = [sec for sec in section_numbers if not sec.isdigit()]
    
    print(f"Numeric sections (e.g., '1', '41'): {len(numeric_sections)}")
    print(f"Alphanumeric sections (e.g., '41A', '164A'): {len(alphanumeric_sections)}")
    
    if alphanumeric_sections:
        print(f"Alphanumeric section examples: {alphanumeric_sections[:10]}")
    
    print("\n=== Verification Complete ===")


if __name__ == "__main__":
    verify_no_duplicates()