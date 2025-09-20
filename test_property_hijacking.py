#!/usr/bin/env python3
"""
Test Property Hijacking Query with Interactive Feedback
======================================================

This script tests the specific "property hijacking" query and waits for
interactive feedback to demonstrate the complete flow.
"""

from cli_interface import LegalAgentCLI

def main():
    """Test property hijacking query with interactive feedback"""
    
    print("🏠 TESTING PROPERTY HIJACKING QUERY")
    print("=" * 60)
    print("This will process your query and wait for interactive feedback")
    print("=" * 60)
    
    # Create CLI with adaptive agent
    try:
        cli = LegalAgentCLI(use_adaptive=True)
        print("✅ Using Adaptive Agent with constitutional analysis")
    except Exception as e:
        print(f"⚠️ Adaptive agent failed, using enhanced agent: {e}")
        cli = LegalAgentCLI(use_adaptive=False)
    
    # Test the specific query
    test_query = "My Property is Been Hijaced"
    
    print(f"\n🔍 Processing query: '{test_query}'")
    print("-" * 60)
    
    # Process the query
    cli.process_query(test_query)
    
    print(f"\n✅ Query processed successfully!")
    print(f"   Domain: {cli.last_response.domain}")
    print(f"   Confidence: {cli.last_response.confidence:.3f}")
    
    # Now start interactive feedback session
    print("\n" + "=" * 60)
    print("🎯 INTERACTIVE FEEDBACK SESSION")
    print("=" * 60)
    print("You can now give feedback or ask follow-up questions:")
    print("• Type 'helpful' or 'not helpful' for feedback")
    print("• Type any follow-up question")
    print("• Type 'quit' to exit")
    print("-" * 60)
    
    # Interactive loop for feedback and follow-up
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            # Process the input (feedback or new query)
            cli.process_command(user_input)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()