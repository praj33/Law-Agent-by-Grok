"""
Enhanced Legal Agent - Simple Startup Script
============================================

This script provides a simple way to start using the enhanced Legal Agent
with IPC/CrPC/Special Acts sections.

Usage:
1. Run this script: python start_enhanced_legal_agent.py
2. Enter your legal questions
3. Get structured responses with all legal sections

Author: Legal Agent Team
Date: 2025-01-XX
"""

from updated_main_agent import process_legal_query, create_updated_legal_agent
import sys

def interactive_legal_agent():
    """Interactive legal agent session"""
    
    print("🏛️ ENHANCED LEGAL AI ASSISTANT")
    print("=" * 60)
    print("✅ Includes Constitutional Articles, IPC Sections, CrPC Sections, and Special Acts")
    print("💡 Type 'quit' to exit, 'help' for examples")
    print("=" * 60)
    
    # Initialize agent
    print("🔄 Initializing Enhanced Legal Agent...")
    try:
        agent = create_updated_legal_agent()
        print("✅ Legal Agent ready!")
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        return
    
    print("\n💬 Enter your legal question:")
    
    while True:
        try:
            # Get user input
            user_input = input("\n⚖️  Legal Query: ").strip()
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using Enhanced Legal AI Assistant!")
                print("⚖️  Remember: This is for informational purposes only.")
                print("📞 Always consult a qualified lawyer for legal advice.")
                break
            
            elif user_input.lower() == 'help':
                show_examples()
                continue
            
            elif not user_input:
                print("💡 Please enter a legal question.")
                continue
            
            # Process the query
            print(f"\n🔍 Processing: \"{user_input}\"")
            print("⏳ Analyzing legal aspects...")
            
            try:
                response = agent.process_query(user_input)
                print("\n" + "="*60)
                print(response)
                print("="*60)
                
            except Exception as e:
                print(f"\n❌ Error processing query: {e}")
                print("Please try rephrasing your question.")
        
        except KeyboardInterrupt:
            print(f"\n\n⏹️  Session interrupted by user")
            print("👋 Thank you for using Enhanced Legal AI Assistant!")
            break
        
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("🔄 Continuing with session...")

def show_examples():
    """Show example legal queries"""
    print("\n📝 EXAMPLE LEGAL QUERIES:")
    print("-" * 40)
    examples = [
        "My phone is stolen",
        "My coworker is sexually harassing me at workplace",
        "My landlord is not returning my security deposit",
        "My husband is beating me and threatening violence",
        "Someone hacked my bank account and stole money",
        "My employer fired me without proper notice",
        "I bought a defective product and want refund",
        "My elderly father is being abused by caretaker"
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example}")
    
    print("\n💡 Try typing any of these or your own legal question!")

def quick_demo():
    """Quick demonstration of the enhanced legal agent"""
    print("🚀 QUICK DEMO - Enhanced Legal Agent")
    print("=" * 50)
    
    demo_queries = [
        "My phone is stolen",
        "My coworker is harassing me at work"
    ]
    
    for query in demo_queries:
        print(f"\n📝 Demo Query: \"{query}\"")
        print("-" * 30)
        
        try:
            response = process_legal_query(query)
            print(response)
            
            input("\nPress Enter to continue to next demo...")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n✅ Demo completed!")

def single_query_mode():
    """Process a single query and exit"""
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"🔍 Processing: \"{query}\"")
        print("-" * 50)
        
        try:
            response = process_legal_query(query)
            print(response)
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("Usage: python start_enhanced_legal_agent.py \"your legal question\"")

def main():
    """Main function"""
    print("🏛️ ENHANCED LEGAL AGENT STARTUP")
    print("=" * 40)
    print("Choose an option:")
    print("1. Interactive Mode (recommended)")
    print("2. Quick Demo")
    print("3. Single Query Mode")
    print("=" * 40)
    
    try:
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            interactive_legal_agent()
        elif choice == "2":
            quick_demo()
        elif choice == "3":
            single_query_mode()
        else:
            print("Invalid choice. Starting interactive mode...")
            interactive_legal_agent()
            
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Startup interrupted")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()