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
from working_enhanced_agent import create_working_enhanced_agent

# Try to import adaptive agent (Task 2)
try:
    from adaptive_agent import create_adaptive_agent
    ADAPTIVE_AGENT_AVAILABLE = True
except ImportError:
    create_adaptive_agent = None
    ADAPTIVE_AGENT_AVAILABLE = False


class LegalAgentCLI:
    """Command-line interface for the Legal Agent"""

    def __init__(self, use_adaptive=False):
        # Choose agent type
        if use_adaptive and ADAPTIVE_AGENT_AVAILABLE and create_adaptive_agent is not None:
            print("🧠 Using Adaptive Agent (Task 2) with learning capabilities")
            self.adaptive_agent = create_adaptive_agent()
            self.agent = self.adaptive_agent.base_agent  # Use base agent for display
        else:
            print("🔧 Using Enhanced Working Agent")
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
        
        if ADAPTIVE_AGENT_AVAILABLE and hasattr(self, 'adaptive_agent'):
            print("🏛️ CONSTITUTIONAL ANALYSIS ENABLED!")
            print("   • Specific constitutional articles with confidence percentages")
            print("   • Searches through 140+ constitutional articles")
            print("   • Enhanced legal guidance with constitutional backing")
            print()
        
        print("Welcome to the Legal Agent! I can help you with legal queries.")
        print("\nCommands:")
        print("  help          - Show this help message")
        print("  query <text>  - Ask a legal question")
        print("  feedback <rating> - Rate the last response (helpful/not helpful)")
        print("  stats         - Show feedback statistics")
        print("  clear         - Clear screen")
        print("  quit/exit     - Exit the program")
        print("\nOr just type your legal question directly!")
        
        if ADAPTIVE_AGENT_AVAILABLE and hasattr(self, 'adaptive_agent'):
            print("\n🎯 TRY: 'Employee discloses all the company secrets to another company'")
            print("     to see constitutional articles with confidence percentages!")
        
        print("=" * 60)
    
    def is_feedback_response(self, command_lower: str) -> bool:
        """Check if the command is likely feedback on the previous response"""
        if not self.last_query or not self.last_response:
            return False

        # Exact feedback keywords (single words)
        exact_feedback_keywords = [
            'helpful', 'unhelpful', 'good', 'bad', 'wrong', 'correct',
            'excellent', 'poor', 'great', 'terrible', 'useful', 'useless',
            'perfect', 'awful', 'thanks', 'yes', 'no', 'right', 'incorrect',
            'accurate', 'inaccurate'
        ]

        # Multi-word feedback phrases
        feedback_phrases = [
            'not helpful', 'thank you', 'very good', 'very bad', 'not good',
            'not useful', 'very helpful', 'not correct', 'completely wrong'
        ]

        # Check if the entire command is just a feedback keyword
        command_stripped = command_lower.strip()
        if command_stripped in exact_feedback_keywords:
            return True

        # Check for multi-word feedback phrases
        if command_stripped in feedback_phrases:
            return True

        # Check if it's a very short response (1-2 words) with feedback keywords
        words = command_stripped.split()
        if len(words) <= 2:
            for keyword in exact_feedback_keywords:
                if keyword in command_stripped:
                    return True

        # Exclude obvious questions/queries even if they contain feedback words
        question_indicators = ['what', 'how', 'when', 'where', 'why', 'can', 'should', 'will', 'do', 'does', 'is', 'are']
        if any(word in words for word in question_indicators):
            return False

        return False

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

        # Check if it's feedback without the "feedback" prefix
        elif self.is_feedback_response(command_lower):
            print(f"🧠 Detected as FEEDBACK: '{command}'")
            self.process_feedback(command)

        else:
            # Treat as a direct query
            print(f"🔍 Detected as QUERY: '{command}'")
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

        # Process query differently based on agent type
        if ADAPTIVE_AGENT_AVAILABLE and hasattr(self, 'adaptive_agent'):
            # Use adaptive agent with structured output and constitutional articles
            from legal_agent import LegalQueryInput
            query_input = LegalQueryInput(
                user_input=query_text,
                session_id=self.session_id or "cli_session"
            )
            
            # Get structured response with constitutional articles
            if hasattr(self.adaptive_agent, 'process_query_with_structured_output'):
                structured_response = self.adaptive_agent.process_query_with_structured_output(query_input)
                print(structured_response)
                
                # Also get the base response for feedback
                response = self.adaptive_agent.process_query_with_learning(query_input)
                self.session_id = response.session_id
                self.last_response = response
            else:
                response = self.adaptive_agent.process_query_with_learning(query_input)
                self.session_id = response.session_id
                self.last_response = response
                self.display_response(response)
        else:
            # Use enhanced agent with string input
            response = self.agent.process_query(query_text)
            self.session_id = response.session_id
            self.last_response = response
            self.display_response(response)

        # Ask for feedback
        print("\n💬 Was this response helpful?")
        print("   You can simply type: 'helpful', 'not helpful', 'good', 'bad', etc.")
        print("   Or use: 'feedback <your rating>')")
    
    def process_feedback(self, feedback_text: str):
        """Process user feedback with real learning"""
        if not self.last_query or not self.last_response:
            print("No previous query to provide feedback for.")
            return

        print(f"🧠 Processing feedback: '{feedback_text}'")

        # Try adaptive agent first (Task 2), then fall back to enhanced agent
        if ADAPTIVE_AGENT_AVAILABLE and hasattr(self, 'adaptive_agent'):
            # Use adaptive agent for Task 2 learning
            from legal_agent import LegalQueryInput
            feedback_query = LegalQueryInput(
                user_input=self.last_query,
                feedback=feedback_text,
                session_id=self.session_id
            )
            self.adaptive_agent.process_query_with_learning(feedback_query)
        else:
            # Use enhanced agent feedback system
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

        # Timeline - handle different response types
        if hasattr(response, 'timeline'):
            print(f"⏱️  Timeline: {response.timeline}")

        # Success rate - only if available
        if hasattr(response, 'success_rate'):
            print(f"📊 Success Rate: {response.success_rate:.1%}")

        # Legal route
        if hasattr(response, 'legal_route'):
            print(f"\n📝 Legal Route:")
            print(f"   {response.legal_route}")

        # Display detailed process steps
        if hasattr(response, 'process_steps') and response.process_steps:
            print(f"\n📋 Detailed Process Steps:")
            for step in response.process_steps:
                print(f"   {step}")

        # Constitutional backing - ENHANCED with proper legal acts
        if hasattr(response, 'constitutional_backing') and response.constitutional_backing:
            print(f"\n🏛️ CONSTITUTIONAL & LEGAL BACKING:")
            print(f"   {response.constitutional_backing}")
            
            # Display constitutional articles WITHOUT misleading confidence percentages
            if hasattr(response, 'constitutional_articles') and response.constitutional_articles:
                print(f"\n📜 RELEVANT CONSTITUTIONAL ARTICLES:")
                for i, article in enumerate(response.constitutional_articles, 1):
                    article_num = article.get('article_number', 'N/A')
                    title = article.get('title', 'N/A')
                    relevance_type = article.get('relevance_type', article.get('is_primary', False))
                    
                    # Use relevance type instead of misleading confidence percentages
                    if relevance_type == 'PRIMARY' or relevance_type == True:
                        priority_icon = "🔴"  # Red for primary
                    elif relevance_type == 'SUPPORTING':
                        priority_icon = "🟡"  # Yellow for supporting
                    else:
                        priority_icon = "🟢"  # Green for relevant
                    
                    priority_text = "PRIMARY" if (relevance_type == 'PRIMARY' or relevance_type == True) else "SUPPORTING" if relevance_type == 'SUPPORTING' else "RELEVANT"
                    print(f"   {priority_icon} Article {article_num}: {title} ({priority_text})")
                    
                    # Show relevance reason instead of summary
                    if article.get('content_summary'):
                        print(f"     Relevance: {article['content_summary']}")
                    elif article.get('summary'):
                        summary = article['summary'][:100] + "..." if len(article.get('summary', '')) > 100 else article.get('summary')
                        print(f"     Summary: {summary}")
            
            # Display applicable legal acts (NEW FEATURE)
            if hasattr(response, 'legal_acts') and response.legal_acts:
                print(f"\n⚖️ APPLICABLE LEGAL FRAMEWORK:")
                for act in response.legal_acts:
                    print(f"   📜 {act.get('act_name', 'Legal Act')}:")
                    for section in act.get('sections', []):
                        print(f"     - {section}")
                    if act.get('relevance_reason'):
                        print(f"     Relevance: {act['relevance_reason']}")
                    print()  # Add spacing between acts

        # Response time
        if hasattr(response, 'response_time'):
            print(f"\n⚡ Response Time: {response.response_time:.3f}s")

        # Session ID
        if hasattr(response, 'session_id'):
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
    import sys

    # Check for adaptive agent option
    use_adaptive = '--adaptive' in sys.argv or '-a' in sys.argv

    if use_adaptive and not ADAPTIVE_AGENT_AVAILABLE:
        print("❌ Adaptive agent not available. Using enhanced agent instead.")
        use_adaptive = False

    cli = LegalAgentCLI(use_adaptive=use_adaptive)
    cli.start()


if __name__ == "__main__":
    print("🏛️ Legal Agent CLI")
    print("Usage: python cli_interface.py [--adaptive|-a]")
    print("  --adaptive: Use Task 2 Adaptive Agent with learning")
    print()
    main()
