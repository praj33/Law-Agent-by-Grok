"""
Structured Legal Agent CLI Interface
===================================

Interactive command-line interface for the Enhanced Structured Legal Agent
that provides responses in the format:

1. Constitutional Articles
2. IPC Sections (Indian Penal Code, 1860)
3. CrPC Sections (Code of Criminal Procedure, 1973)
4. Special Acts (if applicable)

Author: Legal Agent Team
Date: 2025-01-XX
"""

import sys
import os
from enhanced_structured_legal_agent import create_structured_legal_agent, get_structured_legal_advice

def print_banner():
    """Print the application banner"""
    print("=" * 70)
    print("⚖️  STRUCTURED LEGAL AI ASSISTANT")
    print("=" * 70)
    print("🏛️ Provides structured legal responses with:")
    print("   1. Constitutional Articles")
    print("   2. IPC Sections (Indian Penal Code, 1860)")
    print("   3. CrPC Sections (Code of Criminal Procedure, 1973)")
    print("   4. Special Acts (if applicable)")
    print("=" * 70)
    print("💡 Type 'help' for commands, 'quit' to exit")
    print("=" * 70)

def print_help():
    """Print help information"""
    print("\n📋 AVAILABLE COMMANDS:")
    print("-" * 30)
    print("help     - Show this help message")
    print("examples - Show example queries")
    print("stats    - Show database statistics")
    print("clear    - Clear the screen")
    print("quit     - Exit the application")
    print("\n💬 Or simply type your legal question to get structured advice!")

def print_examples():
    """Print example queries"""
    print("\n📝 EXAMPLE LEGAL QUERIES:")
    print("-" * 40)
    examples = [
        "My coworker is sexually harassing me at workplace",
        "My landlord is not returning my security deposit",
        "My husband is beating me and threatening violence",
        "Someone hacked my bank account and stole money",
        "My employer fired me without proper notice",
        "I bought a defective product and want refund",
        "My elderly father is being abused by caretaker",
        "Someone broke into my house and stole jewelry"
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example}")
    
    print("\n💡 Try typing any of these or your own legal question!")

def print_stats(agent):
    """Print database statistics"""
    print("\n📊 LEGAL DATABASE STATISTICS:")
    print("-" * 40)
    print(f"📚 IPC Sections: {len(agent.legal_db.ipc_sections)}")
    print(f"📚 CrPC Sections: {len(agent.legal_db.crpc_sections)}")
    print(f"📚 Special Acts: {len(agent.legal_db.special_acts)}")
    print(f"🎯 Legal Domains: {len(agent.legal_db.domain_mappings)}")
    
    print(f"\n🎯 SUPPORTED LEGAL DOMAINS:")
    for domain in agent.legal_db.domain_mappings.keys():
        print(f"   • {domain.replace('_', ' ').title()}")

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def process_user_query(agent, query):
    """Process user query and display structured response"""
    print(f"\n🔍 Processing query: \"{query}\"")
    print("⏳ Analyzing legal aspects...")
    
    try:
        # Get structured response
        response = agent.process_structured_query(query)
        
        # Display classification info
        print(f"\n✅ CLASSIFICATION COMPLETE:")
        print(f"   Domain: {response.domain.title()}")
        print(f"   Confidence: {response.confidence:.2f}")
        print(f"   Session: {response.session_id}")
        
        # Display structured response
        print(f"\n{response.to_formatted_response()}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("Please try rephrasing your question or contact support.")

def main():
    """Main CLI application loop"""
    
    # Print banner
    clear_screen()
    print_banner()
    
    # Initialize agent
    print("🔄 Initializing Legal Agent...")
    try:
        agent = create_structured_legal_agent()
        print("✅ Legal Agent initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize Legal Agent: {e}")
        return
    
    # Main interaction loop
    while True:
        try:
            # Get user input
            print(f"\n{'='*70}")
            user_input = input("⚖️  Enter your legal question (or command): ").strip()
            
            # Handle empty input
            if not user_input:
                print("💡 Please enter a legal question or command.")
                continue
            
            # Handle commands
            command = user_input.lower()
            
            if command in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using Structured Legal AI Assistant!")
                print("⚖️  Remember: This is for informational purposes only.")
                print("📞 Always consult a qualified lawyer for legal advice.")
                break
            
            elif command == 'help':
                print_help()
                continue
            
            elif command == 'examples':
                print_examples()
                continue
            
            elif command == 'stats':
                print_stats(agent)
                continue
            
            elif command == 'clear':
                clear_screen()
                print_banner()
                continue
            
            # Process as legal query
            else:
                process_user_query(agent, user_input)
        
        except KeyboardInterrupt:
            print(f"\n\n⏹️  Application interrupted by user")
            print("👋 Thank you for using Structured Legal AI Assistant!")
            break
        
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("🔄 Continuing with application...")

if __name__ == "__main__":
    main()