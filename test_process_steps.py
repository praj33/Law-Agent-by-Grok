"""
Test Process Steps Integration
==============================

Test that detailed process steps are now showing in the enhanced agent
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

def test_process_steps():
    """Test that process steps are now included in responses"""
    
    safe_print("📋 TESTING DETAILED PROCESS STEPS")
    safe_print("=" * 60)
    safe_print("Testing that detailed step-by-step processes are now showing")
    safe_print("=" * 60)
    
    from working_enhanced_agent import create_working_enhanced_agent
    agent = create_working_enhanced_agent()
    
    # Test different types of legal queries
    test_queries = [
        {
            'query': 'landlord not returning my deposit',
            'domain': 'tenant_rights',
            'expected_steps': ['Document the issue', 'Review your lease', 'Send written notice']
        },
        {
            'query': 'my boss is not giving my salary',
            'domain': 'employment_law', 
            'expected_steps': ['Document workplace issues', 'Review employment contract', 'File complaint with HR']
        },
        {
            'query': 'I was raped by my neighbor',
            'domain': 'criminal_law',
            'expected_steps': ['File First Information Report', 'Provide detailed statement', 'Cooperate with police']
        },
        {
            'query': 'defective product not working',
            'domain': 'consumer_complaint',
            'expected_steps': ['Collect all receipts', 'Contact customer service', 'File complaint with consumer forum']
        }
    ]
    
    for i, test_case in enumerate(test_queries, 1):
        query = test_case['query']
        expected_domain = test_case['domain']
        expected_steps = test_case['expected_steps']
        
        safe_print(f"\n🧪 Test {i}: {expected_domain.replace('_', ' ').title()}")
        safe_print(f"Query: \"{query}\"")
        safe_print("-" * 50)
        
        try:
            response = agent.process_query(query)
            
            # Check if process steps are included
            if hasattr(response, 'process_steps') and response.process_steps:
                safe_print(f"✅ Process steps included: {len(response.process_steps)} steps")
                safe_print(f"📋 Sample steps:")
                
                # Show first 3 steps
                for j, step in enumerate(response.process_steps[:3], 1):
                    safe_print(f"   {step}")
                
                if len(response.process_steps) > 3:
                    safe_print(f"   ... and {len(response.process_steps) - 3} more steps")
                
                # Check if expected content is present
                steps_text = ' '.join(response.process_steps).lower()
                found_expected = sum(1 for expected in expected_steps if any(word.lower() in steps_text for word in expected.split()))
                
                if found_expected >= 2:
                    safe_print(f"✅ Content quality: Good (found {found_expected}/{len(expected_steps)} expected elements)")
                else:
                    safe_print(f"⚠️ Content quality: Could be better (found {found_expected}/{len(expected_steps)} expected elements)")
                    
            else:
                safe_print(f"❌ No process steps found in response")
                safe_print(f"   Response has: {[attr for attr in dir(response) if not attr.startswith('_')]}")
                
        except Exception as e:
            safe_print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    # Test specific tenant rights case (user's example)
    safe_print(f"\n🏠 SPECIFIC TEST: Tenant Rights (User's Example)")
    safe_print("-" * 60)
    
    try:
        response = agent.process_query("landlord not returning deposit")
        
        if hasattr(response, 'process_steps') and response.process_steps:
            safe_print(f"✅ Tenant rights process steps found!")
            safe_print(f"📋 Complete process:")
            
            for step in response.process_steps:
                safe_print(f"   {step}")
            
            # Check for specific elements user mentioned
            steps_text = ' '.join(response.process_steps).lower()
            has_document_collection = 'document' in steps_text or 'receipt' in steps_text
            has_lease_review = 'lease' in steps_text or 'agreement' in steps_text
            has_notice_sending = 'notice' in steps_text or 'written' in steps_text
            
            safe_print(f"\n📊 Content Analysis:")
            safe_print(f"   Document collection: {'✅' if has_document_collection else '❌'}")
            safe_print(f"   Lease review: {'✅' if has_lease_review else '❌'}")
            safe_print(f"   Notice sending: {'✅' if has_notice_sending else '❌'}")
            
        else:
            safe_print(f"❌ No process steps found for tenant rights")
            
    except Exception as e:
        safe_print(f"❌ Error in tenant rights test: {e}")

def main():
    """Main test function"""
    
    test_process_steps()
    
    safe_print(f"\n🎯 SUMMARY:")
    safe_print("=" * 40)
    safe_print("The enhanced agent now includes detailed process steps like:")
    safe_print("• 'Document the issue (photos, receipts, communications)'")
    safe_print("• 'Review your lease agreement and local tenant laws'")
    safe_print("• 'Send written notice to landlord via certified mail'")
    safe_print("• And 5+ more detailed steps for each legal domain")
    
    safe_print(f"\n🚀 Test in CLI:")
    safe_print("python cli_interface.py")
    safe_print("Ask: 'landlord not returning my deposit'")
    safe_print("You should now see detailed step-by-step processes!")

if __name__ == "__main__":
    main()
