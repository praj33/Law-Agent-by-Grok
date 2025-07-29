"""
Test Specific Query Fixes
=========================

Test the specific fixes for:
1. Salary-related queries (should be employment_law)
2. Phone stolen at airport (should be criminal_law, not cyber_crime)
"""

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

def test_specific_fixes():
    """Test the specific query fixes"""
    
    safe_print("🔧 TESTING SPECIFIC QUERY FIXES")
    safe_print("=" * 50)
    safe_print("Testing fixes for salary queries and theft classification")
    safe_print("=" * 50)
    
    from working_enhanced_agent import create_working_enhanced_agent
    agent = create_working_enhanced_agent()
    
    # Test cases with expected results
    test_cases = [
        # Salary issues (should be employment_law)
        {
            'query': 'my boss is not giving my salary',
            'expected_domain': 'employment_law',
            'issue': 'Salary not being paid'
        },
        {
            'query': 'my boss is not increasing my salary', 
            'expected_domain': 'employment_law',
            'issue': 'Salary increment denied'
        },
        {
            'query': 'company not paying wages for 3 months',
            'expected_domain': 'employment_law', 
            'issue': 'Unpaid wages'
        },
        {
            'query': 'employer withholding my salary',
            'expected_domain': 'employment_law',
            'issue': 'Salary withheld'
        },
        
        # Physical theft (should be criminal_law, not cyber_crime)
        {
            'query': 'my phone got stolen at airport',
            'expected_domain': 'criminal_law',
            'issue': 'Physical theft misclassified as cyber crime'
        },
        {
            'query': 'wallet stolen from my pocket in bus',
            'expected_domain': 'criminal_law',
            'issue': 'Physical theft'
        },
        {
            'query': 'bag snatched on street',
            'expected_domain': 'criminal_law',
            'issue': 'Street crime'
        },
        {
            'query': 'phone stolen at office',
            'expected_domain': 'criminal_law',
            'issue': 'Workplace theft'
        },
        
        # Cyber crimes (should remain cyber_crime)
        {
            'query': 'my online account was hacked',
            'expected_domain': 'cyber_crime',
            'issue': 'Account hacking'
        },
        {
            'query': 'someone stole my password online',
            'expected_domain': 'cyber_crime',
            'issue': 'Digital credential theft'
        }
    ]
    
    safe_print(f"\n🧪 Testing {len(test_cases)} specific cases:")
    safe_print("-" * 60)
    
    fixed_count = 0
    total_count = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        query = test_case['query']
        expected = test_case['expected_domain']
        issue = test_case['issue']
        
        safe_print(f"\n{i}. Issue: {issue}")
        safe_print(f"   Query: \"{query}\"")
        
        try:
            response = agent.process_query(query)
            actual_domain = response.domain
            confidence = response.confidence
            
            if actual_domain == expected:
                safe_print(f"   ✅ FIXED: {actual_domain} (confidence: {confidence:.3f})")
                safe_print(f"   📋 Route: {response.legal_route[:50]}...")
                fixed_count += 1
            else:
                safe_print(f"   ❌ ISSUE: Got {actual_domain}, expected {expected}")
                safe_print(f"   📋 Route: {response.legal_route[:50]}...")
                
        except Exception as e:
            safe_print(f"   ❌ ERROR: {e}")
    
    # Summary
    success_rate = (fixed_count / total_count) * 100
    safe_print(f"\n📊 FIX RESULTS SUMMARY")
    safe_print("=" * 40)
    safe_print(f"Total Test Cases: {total_count}")
    safe_print(f"Successfully Fixed: {fixed_count}")
    safe_print(f"Still Need Work: {total_count - fixed_count}")
    safe_print(f"Fix Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        safe_print(f"🎉 EXCELLENT! Almost all issues fixed")
    elif success_rate >= 80:
        safe_print(f"✅ VERY GOOD! Most issues resolved")
    elif success_rate >= 70:
        safe_print(f"👍 GOOD! Majority of issues fixed")
    else:
        safe_print(f"⚠️ NEEDS MORE WORK! Some issues remain")
    
    safe_print(f"\n🎯 KEY FIXES IMPLEMENTED:")
    safe_print("✅ Enhanced employment law patterns for salary issues")
    safe_print("✅ Added specific salary-related keywords")
    safe_print("✅ Improved theft vs cyber crime distinction")
    safe_print("✅ Added physical location context detection")
    safe_print("✅ Implemented scenario prioritization logic")

def main():
    """Main test function"""
    
    test_specific_fixes()
    
    safe_print(f"\n🚀 TEST YOUR FIXES:")
    safe_print("=" * 30)
    safe_print("python cli_interface.py")
    safe_print("")
    safe_print("Try these queries:")
    safe_print("• 'my boss is not giving my salary'")
    safe_print("• 'my boss is not increasing my salary'") 
    safe_print("• 'my phone got stolen at airport'")
    safe_print("")
    safe_print("Expected results:")
    safe_print("• Salary queries → employment_law")
    safe_print("• Phone stolen at airport → criminal_law")

if __name__ == "__main__":
    main()
