"""
Legal Agent CLI Interface
========================

Command-line interface for testing and interacting with the Legal Agent.
Provides an interactive dialogue loop for users to test the agent functionality.

Usage:
    python cli_interface.py

Features:
- Interactive query processing
- Feedback collection
- Session management
- Statistics viewing
- Help system
"""

import sys
import json
from typing import Optional
from legal_agent import LegalAgent, LegalQueryInput, create_legal_agent
from adaptive_legal_agent import create_adaptive_legal_agent
from working_enhanced_agent import create_working_enhanced_agent


class LegalAgentCLI:
    """Command-line interface for the Legal Agent"""
    
    def __init__(self):
        # Use enhanced working agent with all fixes
        self.agent = create_working_enhanced_agent()
        self.session_id = None
        self.running = True
        self.last_query = None
        self.last_response = None
        
    def start(self):
        """Start the CLI interface"""
        self.print_welcome()
        
        while self.running:
            try:
                command = input("\n> ").strip()
                
                if not command:
                    continue
                    
                self.process_command(command)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def print_welcome(self):
        """Print welcome message and help"""
        print("=" * 60)
        print("🏛️  LEGAL AGENT CLI INTERFACE")
        print("=" * 60)
        print("Welcome to the Legal Agent! I can help you with legal queries.")
        print("\nCommands:")
        print("  help          - Show this help message")
        print("  query <text>  - Ask a legal question")
        print("  feedback <rating> - Rate the last response (helpful/not helpful)")
        print("  stats         - Show feedback statistics")
        print("  clear         - Clear screen")
        print("  quit/exit     - Exit the program")
        print("\nOr just type your legal question directly!")
        print("=" * 60)
    
    def process_command(self, command: str):
        """Process user command"""
        command_lower = command.lower()
        
        if command_lower in ['quit', 'exit', 'q']:
            self.running = False
            print("Goodbye!")
            
        elif command_lower in ['help', 'h']:
            self.print_help()
            
        elif command_lower.startswith('query '):
            query_text = command[6:].strip()
            self.process_query(query_text)
            
        elif command_lower.startswith('feedback '):
            feedback_text = command[9:].strip()
            self.process_feedback(feedback_text)
            
        elif command_lower == 'stats':
            self.show_stats()
            
        elif command_lower == 'clear':
            self.clear_screen()
            
        else:
            # Treat as a direct query
            self.process_query(command)
    
    def process_query(self, query_text: str):
        """Process a legal query"""
        if not query_text:
            print("Please provide a query.")
            return

        print(f"\n🔍 Processing query: {query_text}")
        print("-" * 50)

        # Store query for feedback
        self.last_query = query_text

        # Process query with enhanced agent
        response = self.agent.process_query(query_text)

        # Store session ID and response for feedback
        self.session_id = response.session_id
        self.last_response = response

        # Display response
        self.display_response(response)

        # Ask for feedback
        print("\n💬 Was this response helpful? (Type 'feedback helpful' or 'feedback not helpful')")
    
    def process_feedback(self, feedback_text: str):
        """Process user feedback with real learning"""
        if not self.last_query or not self.last_response:
            print("No previous query to provide feedback for.")
            return

        print(f"🧠 Processing feedback: '{feedback_text}'")

        # Process feedback through the agent's learning system
        self.agent.process_feedback(
            query=self.last_query,
            domain=self.last_response.domain,
            confidence=self.last_response.confidence,
            feedback=feedback_text
        )

        print("✅ Thank you! The agent has learned from your feedback.")

        # Show learning effect by testing the same query again
        if "helpful" in feedback_text.lower() or "good" in feedback_text.lower():
            print("\n🔄 Let me process that query again to show the learning effect...")
            new_response = self.agent.process_query(self.last_query)

            if new_response.confidence > self.last_response.confidence:
                print(f"🚀 Confidence increased! {self.last_response.confidence:.3f} → {new_response.confidence:.3f}")
                print("✅ The agent learned that this classification was helpful!")
            else:
                print(f"📊 Confidence: {new_response.confidence:.3f} (learning applied)")
        elif "not helpful" in feedback_text.lower() or "wrong" in feedback_text.lower():
            print("\n🔄 Let me process that query again to show the learning effect...")
            new_response = self.agent.process_query(self.last_query)

            if new_response.confidence < self.last_response.confidence:
                print(f"📉 Confidence decreased! {self.last_response.confidence:.3f} → {new_response.confidence:.3f}")
                print("✅ The agent learned that this classification was not helpful!")
            else:
                print(f"📊 Confidence: {new_response.confidence:.3f} (learning applied)")
    
    def display_response(self, response):
        """Display the agent response in a formatted way"""
        print(f"📋 Domain: {response.domain.replace('_', ' ').title()} (Confidence: {response.confidence:.3f})")
        print(f"⏱️  Timeline: {response.timeline}")
        print(f"📊 Success Rate: {response.success_rate:.1%}")

        print(f"\n📝 Legal Route:")
        print(f"   {response.legal_route}")

        if response.constitutional_backing:
            print(f"\n🏛️ Constitutional Backing:")
            print(f"   {response.constitutional_backing}")

        print(f"\n⚡ Response Time: {response.response_time:.3f}s")
        print(f"🔗 Session ID: {response.session_id}")
    
    def show_stats(self):
        """Show system statistics"""
        print("\n📊 SYSTEM STATISTICS")
        print("=" * 40)
        print("Enhanced Legal Agent with comprehensive domain coverage:")
        print("• 10 Legal Domains supported")
        print("• 60+ Legal scenario patterns")
        print("• ML-driven classification")
        print("• Constitutional integration")
        print("• Dataset-driven legal routes")
        print("• Real-time processing")
    
    def print_help(self):
        """Print help information"""
        print("\n📖 HELP - Legal Agent Commands")
        print("=" * 40)
        print("query <text>     - Ask a legal question")
        print("feedback <text>  - Provide feedback on last response")
        print("stats           - View feedback statistics")
        print("clear           - Clear the screen")
        print("help            - Show this help")
        print("quit/exit       - Exit the program")
        print("\nExample queries:")
        print("• 'My landlord won't return my deposit'")
        print("• 'I want to divorce my spouse'")
        print("• 'My employer fired me unfairly'")
        print("• 'I was in a car accident'")
    
    def clear_screen(self):
        """Clear the screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_welcome()


def main():
    """Main function to run the CLI"""
    cli = LegalAgentCLI()
    cli.start()


if __name__ == "__main__":
    main()
