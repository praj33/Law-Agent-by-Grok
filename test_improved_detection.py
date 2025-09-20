"""
Test Improved Feedback Detection
================================

Tests the improved feedback detection system to ensure
"what about filing a complaint" is correctly detected as a query.
"""

from cli_interface import LegalAgentCLI

def main():
    print('🧪 TESTING IMPROVED FEEDBACK DETECTION')
    print('=' * 50)

    # Create CLI instance
    cli = LegalAgentCLI()

    # Set up context (simulate previous query)
    cli.last_query = 'my phone got stolen in market'
    cli.last_response = type('obj', (object,), {'domain': 'criminal_law'})()

    print('\nTesting key scenarios:')
    print('=' * 30)

    # Test the exact user scenario
    test_cases = [
        ('helpful', 'Should be FEEDBACK'),
        ('what about filing a complaint', 'Should be QUERY'),
        ('how do I file a police report', 'Should be QUERY'),
        ('good', 'Should be FEEDBACK'),
        ('bad', 'Should be FEEDBACK'),
        ('what good options do I have', 'Should be QUERY (contains good but is question)'),
        ('can I get help', 'Should be QUERY'),
        ('thank you', 'Should be FEEDBACK'),
        ('what should I do next', 'Should be QUERY'),
        ('not helpful', 'Should be FEEDBACK'),
    ]

    correct = 0
    total = len(test_cases)

    for test_input, description in test_cases:
        result = cli.is_feedback_response(test_input.lower())
        detection = 'FEEDBACK' if result else 'QUERY'
        
        # Determine if this is correct
        expected_feedback = 'FEEDBACK' in description
        is_correct = (result == expected_feedback)
        
        status = '✅' if is_correct else '❌'
        if is_correct:
            correct += 1
            
        print(f'  {status} "{test_input}" -> {detection}')
        print(f'      {description}')

    print(f'\nAccuracy: {correct}/{total} ({(correct/total)*100:.1f}%)')

    print('\n🎯 SPECIFIC USER SCENARIO TEST:')
    print('=' * 40)
    print('Scenario: Phone theft -> feedback -> follow-up')
    
    # Test exact sequence
    helpful_result = cli.is_feedback_response('helpful')
    complaint_result = cli.is_feedback_response('what about filing a complaint')
    
    print(f'1. "helpful" -> {"FEEDBACK" if helpful_result else "QUERY"} {"✅" if helpful_result else "❌"}')
    print(f'2. "what about filing a complaint" -> {"FEEDBACK" if complaint_result else "QUERY"} {"✅" if not complaint_result else "❌"}')
    
    if helpful_result and not complaint_result:
        print('\n🎉 USER SCENARIO: WORKING PERFECTLY!')
        print('✅ "helpful" correctly detected as feedback')
        print('✅ "what about filing a complaint" correctly detected as query')
    else:
        print('\n❌ USER SCENARIO: NEEDS FIXING!')
        if not helpful_result:
            print('❌ "helpful" should be detected as feedback')
        if complaint_result:
            print('❌ "what about filing a complaint" should be detected as query')

if __name__ == "__main__":
    main()
