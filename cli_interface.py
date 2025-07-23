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


class LegalAgentCLI:
    """Command-line interface for the Legal Agent"""
    
    def __init__(self):
        # Use adaptive agent for real learning
        self.agent = create_adaptive_legal_agent()
        self.session_id = None
        self.running = True
        self.last_query = None
        
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
        
        # Create query input
        query_input = LegalQueryInput(
            user_input=query_text,
            session_id=self.session_id
        )
        
        # Store query for feedback
        self.last_query = query_text

        # Process query with learning
        response = self.agent.process_query_with_learning(query_input)
        
        # Store session ID for feedback
        self.session_id = response.session_id
        
        # Display response
        self.display_response(response)
        
        # Ask for feedback
        print("\n💬 Was this response helpful? (Type 'feedback helpful' or 'feedback not helpful')")
    
    def process_feedback(self, feedback_text: str):
        """Process user feedback with real learning"""
        if not self.last_query or not self.session_id:
            print("No previous query to provide feedback for.")
            return

        print(f"🧠 Processing feedback: '{feedback_text}'")

        # Create feedback query for learning
        feedback_query = LegalQueryInput(
            user_input=self.last_query,
            feedback=feedback_text,
            session_id=self.session_id
        )

        # Process feedback (triggers learning)
        self.agent.process_query_with_learning(feedback_query)

        print("✅ Thank you! The agent has ACTUALLY learned from your feedback.")

        # Test the same query again to show learning
        if "not helpful" in feedback_text.lower() or "wrong" in feedback_text.lower():
            print("\n🔄 Let me try that query again with the new learning...")
            test_query = LegalQueryInput(user_input=self.last_query)
            new_response = self.agent.process_query_with_learning(test_query)
            print(f"🎯 Updated response: {new_response.domain} (confidence: {new_response.confidence:.3f})")
            print("✅ See the difference? The agent learned!")
    
    def display_response(self, response):
        """Display the agent response in a formatted way"""
        print(f"📋 Domain: {response.domain.title()} (Confidence: {response.confidence:.2f})")
        print(f"⏱️  Timeline: {response.timeline}")
        print(f"🎯 Expected Outcome: {response.outcome}")
        
        print(f"\n📝 Legal Route:")
        print(f"   {response.legal_route}")
        
        print(f"\n📋 Process Steps:")
        for i, step in enumerate(response.process_steps, 1):
            print(f"   {step}")
        
        if response.glossary:
            print(f"\n📚 Legal Terms Found:")
            for term, definition in response.glossary.items():
                print(f"   • {term.title()}: {definition}")
        
        print(f"\n🔗 Session ID: {response.session_id}")
    
    def show_stats(self):
        """Show feedback statistics"""
        print("\n📊 FEEDBACK STATISTICS")
        print("=" * 40)
        
        stats = self.agent.get_feedback_stats()
        
        print(f"Total Feedback Entries: {stats['total_feedback']}")
        print(f"Positive Feedback: {stats['positive_percentage']:.1f}%")
        
        if stats['domains']:
            print("\nDomain Distribution:")
            for domain, count in stats['domains'].items():
                print(f"  • {domain.title()}: {count}")
        
        if stats['domain_feedback']:
            print("\nDomain-Specific Feedback:")
            for domain, data in stats['domain_feedback'].items():
                print(f"  • {domain.title()}: {data['positive_percentage']:.1f}% positive ({data['total']} total)")
        
        if stats['recent_feedback']:
            print("\nRecent Feedback (last 5):")
            for feedback in stats['recent_feedback'][-5:]:
                print(f"  • {feedback['domain']}: {feedback['feedback']}")
    
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
