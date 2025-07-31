"""
Simple CLI for Testing
======================

A simple CLI interface to test the enhanced agent directly
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

def main():
    """Simple CLI for testing enhanced agent"""
    
    safe_print("🏛️ ENHANCED LEGAL AGENT - SIMPLE CLI")
    safe_print("=" * 50)
    safe_print("Loading enhanced agent...")
    
    try:
        from working_enhanced_agent import create_working_enhanced_agent
        agent = create_working_enhanced_agent()
        safe_print("✅ Enhanced agent loaded successfully!")
        
    except Exception as e:
        safe_print(f"❌ Error loading agent: {e}")
        return
    
    safe_print("\nType your legal query (or 'quit' to exit):")
    safe_print("=" * 50)
    
    while True:
        try:
            query = input("\n> ").strip()
            
            if not query:
                continue
                
            if query.lower() in ['quit', 'exit', 'q']:
                safe_print("Goodbye!")
                break
            
            safe_print(f"\n🔍 Processing: {query}")
            safe_print("-" * 40)
            
            # Process query
            response = agent.process_query(query)
            
            # Display results
            safe_print(f"📋 Domain: {response.domain.replace('_', ' ').title()}")
            safe_print(f"🎯 Confidence: {response.confidence:.3f}")
            safe_print(f"⏱️ Timeline: {response.timeline}")
            safe_print(f"📊 Success Rate: {response.success_rate:.1%}")
            safe_print(f"📝 Legal Route: {response.legal_route}")

            # Display detailed process steps
            if hasattr(response, 'process_steps') and response.process_steps:
                safe_print(f"\n📋 Detailed Process Steps:")
                for step in response.process_steps:
                    safe_print(f"   {step}")

            if response.constitutional_backing:
                safe_print(f"\n🏛️ Constitutional Backing: Available")

            safe_print(f"⚡ Response Time: {response.response_time:.3f}s")
            
        except KeyboardInterrupt:
            safe_print("\n\nGoodbye!")
            break
        except Exception as e:
            safe_print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
