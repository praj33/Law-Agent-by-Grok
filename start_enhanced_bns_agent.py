#!/usr/bin/env python3
"""
Enhanced BNS Legal Agent Starter
===============================

Start the Enhanced Legal Agent with:
✅ BNS (Bharatiya Nyaya Sanhita) 2023 sections
✅ Enhanced feedback learning
✅ Comprehensive legal guidance (100% coverage)
✅ Query storage system
✅ Subdomain classification

This preserves the BNS interface you want while adding all enhanced features.

Usage: python start_enhanced_bns_agent.py
"""

def main():
    """Start the enhanced BNS legal agent"""
    
    print("🏛️ ENHANCED LEGAL AGENT WITH BNS INTEGRATION")
    print("=" * 60)
    print("Enhanced Features:")
    print("✅ Bharatiya Nyaya Sanhita (BNS) 2023 sections")
    print("✅ Enhanced feedback learning")
    print("✅ Comprehensive legal guidance")  
    print("✅ Query storage system")
    print("✅ Subdomain classification")
    print("✅ Constitutional articles")
    print("=" * 60)
    
    try:
        # Import the enhanced BNS agent
        from enhanced_subdomain_bns_agent import create_enhanced_subdomain_bns_agent, LegalQueryInput
        
        # Create the BNS agent with all enhancements
        agent = create_enhanced_subdomain_bns_agent()
        print("✅ Enhanced BNS Legal Agent initialized successfully!")
        
        # Interactive mode
        print("\n🔍 INTERACTIVE MODE")
        print("Type your legal questions below (or 'quit' to exit)")
        print("-" * 60)
        
        session_id = "interactive_bns_session"
        
        while True:
            try:
                # Get user input
                user_input = input("\n📋 Your legal question: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                # Process query with BNS integration and enhanced features
                query_input = LegalQueryInput(
                    user_input=user_input,
                    session_id=session_id
                )
                
                print("\n⏳ Processing with BNS sections and enhanced features...")
                
                # Get terminal formatted response with BNS sections
                response = agent.process_query_with_terminal_format(query_input)
                print(response)
                
                # Ask for feedback for learning
                print("\n" + "="*60)
                feedback = input("💬 Feedback (helpful/not helpful/skip): ").strip()
                
                if feedback.lower() not in ['', 'skip']:
                    # Process feedback for enhanced learning
                    feedback_input = LegalQueryInput(
                        user_input=user_input,
                        feedback=feedback,
                        session_id=session_id
                    )
                    
                    agent.process_query_with_enhanced_learning(feedback_input)
                    print("✅ Feedback recorded - BNS agent will learn from this!")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
                
    except ImportError as e:
        print(f"❌ Error importing BNS agent: {e}")
        print("💡 Make sure all required files are present")
        print("Required files:")
        print("  - enhanced_subdomain_bns_agent.py")
        print("  - bharatiya_nyaya_sanhita.py")
        print("  - subdomain_classifier.py")
        print("  - adaptive_agent.py")
        print("  - query_storage.py")
    except Exception as e:
        print(f"❌ Error starting BNS agent: {e}")


if __name__ == "__main__":
    main()