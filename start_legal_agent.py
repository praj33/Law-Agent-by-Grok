#!/usr/bin/env python3
"""
Enhanced Legal Agent Starter
===========================

Quick start script for the enhanced Legal Agent with all features:
- Enhanced feedback learning
- Comprehensive legal guidance
- Query storage system
- Terminal format output

Usage: python start_legal_agent.py
"""

def main():
    """Start the enhanced legal agent"""
    
    print("🏛️ ENHANCED LEGAL AGENT SYSTEM")
    print("=" * 50)
    print("Features:")
    print("✅ Enhanced feedback learning")
    print("✅ Comprehensive legal guidance")  
    print("✅ Query storage system")
    print("✅ Constitutional articles")
    print("=" * 50)
    
    try:
        # Import the enhanced adaptive agent
        from adaptive_agent import create_adaptive_agent
        from legal_agent import LegalQueryInput
        
        # Create the agent with all enhancements
        agent = create_adaptive_agent()
        print("✅ Enhanced Legal Agent initialized successfully!")
        
        # Interactive mode
        print("\n🔍 INTERACTIVE MODE")
        print("Type your legal questions below (or 'quit' to exit)")
        print("-" * 50)
        
        session_id = "interactive_session"
        
        while True:
            try:
                # Get user input
                user_input = input("\n📋 Your legal question: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                # Process query with all enhancements
                query_input = LegalQueryInput(
                    user_input=user_input,
                    session_id=session_id
                )
                
                print("\n⏳ Processing with enhanced features...")
                
                # Get terminal formatted response
                response = agent.process_query_with_terminal_format(query_input)
                print(response)
                
                # Ask for feedback
                print("\n" + "="*50)
                feedback = input("💬 Feedback (helpful/not helpful/skip): ").strip()
                
                if feedback.lower() not in ['', 'skip']:
                    # Process feedback for learning
                    feedback_input = LegalQueryInput(
                        user_input=user_input,
                        feedback=feedback,
                        session_id=session_id
                    )
                    
                    agent.process_query_with_learning(feedback_input)
                    print("✅ Feedback recorded - agent will learn from this!")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
                
    except ImportError as e:
        print(f"❌ Error importing enhanced agent: {e}")
        print("💡 Make sure all required files are present")
    except Exception as e:
        print(f"❌ Error starting agent: {e}")


if __name__ == "__main__":
    main()