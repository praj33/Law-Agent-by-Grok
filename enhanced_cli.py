#!/usr/bin/env python3
"""
Enhanced CLI Interface with Detailed Legal Provisions
====================================================

Simple CLI interface for the enhanced legal agent that provides
comprehensive legal analysis with IPC sections, CrPC sections,
and detailed legal processes.
"""

import sys
from enhanced_working_agent import create_enhanced_working_agent

def print_banner():
    """Print the enhanced CLI banner"""
    print("🏛️" + "="*70 + "🏛️")
    print("    ENHANCED LEGAL AGENT - DETAILED LEGAL PROVISIONS")
    print("    Advanced AI Legal Assistant with Comprehensive Analysis")
    print("🏛️" + "="*70 + "🏛️")
    print()
    print("✅ IPC Sections with detailed descriptions")
    print("✅ CrPC Sections for procedural guidance") 
    print("✅ Constitutional Articles with relevance")
    print("✅ Step-by-step legal processes")
    print("✅ Timeline and success rate analysis")
    print("✅ Emergency contacts and important notes")
    print()

def print_help():
    """Print help information"""
    print("💡 HELP - Available Commands:")
    print("-" * 35)
    print("• Type your legal question in plain English")
    print("• Examples:")
    print("  - 'my phone is stolen'")
    print("  - 'my phone is being hacked'")
    print("  - 'boss not paying salary'")
    print("  - 'husband beats me daily'")
    print("  - 'landlord not returning deposit'")
    print("• Commands:")
    print("  - 'help' - Show this help")
    print("  - 'exit' or 'quit' - Exit the program")
    print()

def main():
    """Main CLI interface"""
    
    print_banner()
    
    # Initialize enhanced agent
    print("🔧 Initializing Enhanced Legal Agent...")
    try:
        agent = create_enhanced_working_agent()
        print("✅ Enhanced Legal Agent ready!")
        print()
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        print("Please check your installation and try again.")
        return
    
    print("💬 Ask your legal question (type 'help' for examples, 'exit' to quit)")
    print("-" * 70)
    
    while True:
        try:
            # Get user input
            user_input = input("\n🏛️ Legal Query: ").strip()
            
            # Handle commands
            if not user_input:
                continue
            elif user_input.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Thank you for using Enhanced Legal Agent!")
                print("🚀 Stay legally informed and protected!")
                break
            elif user_input.lower() in ['help', 'h']:
                print_help()
                continue
            
            # Process legal query
            print(f"\n🔍 Processing: '{user_input}'...")
            print("⏳ Analyzing legal provisions...")
            
            try:
                # Get enhanced response
                response = agent.process_query_with_enhanced_provisions(user_input)
                
                # Display the enhanced response
                agent.display_enhanced_response(response)
                
                # Ask for feedback
                print("\n💭 Was this analysis helpful?")
                feedback = input("   Type 'helpful', 'not helpful', or press Enter to continue: ").strip().lower()
                
                if feedback:
                    agent.process_feedback(
                        user_input, 
                        response['domain'], 
                        response['confidence'], 
                        feedback
                    )
                    if 'helpful' in feedback:
                        print("✅ Thank you! Your feedback helps improve the system.")
                    else:
                        print("📝 Thank you for the feedback. We'll work on improvements.")
                
            except Exception as e:
                print(f"❌ Error processing query: {e}")
                print("Please try rephrasing your question or contact support.")
                continue
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Stay legally protected!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            continue

if __name__ == "__main__":
    main()