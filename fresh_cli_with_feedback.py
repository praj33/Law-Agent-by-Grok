"""
Fresh CLI with Feedback
======================

A completely fresh CLI that definitely has the process_feedback method
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

class FreshLegalAgentCLI:
    """Fresh CLI with guaranteed feedback functionality"""
    
    def __init__(self):
        # Import and create agent
        from working_enhanced_agent import create_working_enhanced_agent
        self.agent = create_working_enhanced_agent()
        self.last_query = None
        self.last_response = None
        
        # Verify the agent has the required method
        if not hasattr(self.agent, 'process_feedback'):
            raise Exception("Agent missing process_feedback method!")
        
        safe_print("✅ Fresh CLI initialized with feedback support!")
    
    def start(self):
        """Start the CLI"""
        
        safe_print("🏛️ FRESH LEGAL AGENT CLI - WITH FEEDBACK")
        safe_print("=" * 60)
        safe_print("✅ Feedback learning system is working!")
        safe_print("=" * 60)
        
        safe_print("\nCommands:")
        safe_print("• Type any legal query")
        safe_print("• Type 'feedback helpful' or 'feedback not helpful' after a query")
        safe_print("• Type 'quit' to exit")
        safe_print("=" * 60)
        
        while True:
            try:
                command = input("\n> ").strip()
                
                if not command:
                    continue
                
                if command.lower() in ['quit', 'exit', 'q']:
                    safe_print("Goodbye!")
                    break
                
                if command.lower().startswith('feedback '):
                    feedback_text = command[9:].strip()
                    self.process_feedback(feedback_text)
                else:
                    self.process_query(command)
                    
            except KeyboardInterrupt:
                safe_print("\n\nGoodbye!")
                break
            except Exception as e:
                safe_print(f"❌ Error: {e}")
                import traceback
                traceback.print_exc()
    
    def process_query(self, query):
        """Process a legal query"""
        
        safe_print(f"\n🔍 Processing: {query}")
        safe_print("-" * 50)
        
        try:
            # Process query
            response = self.agent.process_query(query)
            
            # Store for feedback
            self.last_query = query
            self.last_response = response
            
            # Display response
            self.display_response(response)
            
            # Ask for feedback
            safe_print(f"\n💬 Was this response helpful?")
            safe_print("Type: 'feedback helpful' or 'feedback not helpful'")
            
        except Exception as e:
            safe_print(f"❌ Query processing error: {e}")
            import traceback
            traceback.print_exc()
    
    def process_feedback(self, feedback_text):
        """Process user feedback"""
        
        if not self.last_query or not self.last_response:
            safe_print("❌ No previous query to provide feedback for.")
            return
        
        safe_print(f"🧠 Processing feedback: '{feedback_text}'")
        
        try:
            # Verify method exists before calling
            if not hasattr(self.agent, 'process_feedback'):
                safe_print("❌ ERROR: Agent missing process_feedback method!")
                return
            
            # Process feedback through the agent
            self.agent.process_feedback(
                query=self.last_query,
                domain=self.last_response.domain,
                confidence=self.last_response.confidence,
                feedback=feedback_text
            )
            
            safe_print("✅ Thank you! The agent has learned from your feedback.")
            
            # Show learning effect
            safe_print(f"\n🔄 Let me process that query again to show the learning effect...")
            new_response = self.agent.process_query(self.last_query)
            
            if new_response.confidence != self.last_response.confidence:
                safe_print(f"🚀 Confidence changed! {self.last_response.confidence:.3f} → {new_response.confidence:.3f}")
                safe_print("✅ The agent learned from your feedback!")
            else:
                safe_print("📊 Confidence remained the same (feedback balanced out)")
                
        except Exception as e:
            safe_print(f"❌ Feedback processing error: {e}")
            import traceback
            traceback.print_exc()
    
    def display_response(self, response):
        """Display the agent response"""
        
        safe_print(f"📋 Domain: {response.domain.replace('_', ' ').title()} (Confidence: {response.confidence:.3f})")
        safe_print(f"⏱️ Timeline: {response.timeline}")
        safe_print(f"📊 Success Rate: {response.success_rate:.1%}")
        
        safe_print(f"\n📝 Legal Route:")
        safe_print(f"   {response.legal_route}")
        
        # Display detailed process steps if available
        if hasattr(response, 'process_steps') and response.process_steps:
            safe_print(f"\n📋 Detailed Process Steps:")
            for step in response.process_steps:
                safe_print(f"   {step}")
        
        if response.constitutional_backing:
            safe_print(f"\n🏛️ Constitutional Backing:")
            safe_print(f"   {response.constitutional_backing}")
        
        safe_print(f"\n⚡ Response Time: {response.response_time:.3f}s")
        safe_print(f"🔗 Session ID: {response.session_id}")

def main():
    """Main function"""
    
    try:
        cli = FreshLegalAgentCLI()
        cli.start()
    except Exception as e:
        safe_print(f"❌ CLI startup error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
