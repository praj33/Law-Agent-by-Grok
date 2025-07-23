"""
Adaptive Legal Agent CLI
========================

Interactive CLI for the self-training legal agent.
Shows learning in real-time as you provide feedback.

Usage: python adaptive_cli.py
"""

from adaptive_legal_agent import create_adaptive_legal_agent, LegalQueryInput
import json

class AdaptiveLegalAgentCLI:
    """CLI for the adaptive legal agent"""
    
    def __init__(self):
        self.agent = create_adaptive_legal_agent()
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
        """Print welcome message"""
        print("=" * 70)
        print("🧠 ADAPTIVE LEGAL AGENT CLI - SELF-TRAINING VERSION")
        print("=" * 70)
        print("This agent LEARNS from your feedback and improves over time!")
        print("\nCommands:")
        print("  help          - Show help")
        print("  query <text>  - Ask a legal question")
        print("  feedback <rating> - Rate the last response")
        print("  learning      - Show learning statistics")
        print("  reset         - Reset learning data")
        print("  quit/exit     - Exit")
        print("\nOr just type your legal question directly!")
        print("=" * 70)
    
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
            
        elif command_lower == 'learning':
            self.show_learning_stats()
            
        elif command_lower == 'reset':
            self.reset_learning()
            
        else:
            # Treat as a direct query
            self.process_query(command)
    
    def process_query(self, query_text: str):
        """Process a legal query"""
        if not query_text:
            print("Please provide a query.")
            return
            
        print(f"\n🔍 Processing: {query_text}")
        print("-" * 50)
        
        # Store for feedback
        self.last_query = query_text
        
        # Create query input
        query_input = LegalQueryInput(
            user_input=query_text,
            session_id=self.session_id
        )
        
        # Process with learning
        response = self.agent.process_query_with_learning(query_input)
        self.last_response = response
        
        # Store session ID
        self.session_id = response.session_id
        
        # Display response
        self.display_response(response)
        
        # Ask for feedback
        print("\n💬 How was this response?")
        print("Type: 'feedback helpful' or 'feedback not helpful' or 'feedback wrong domain'")
    
    def process_feedback(self, feedback_text: str):
        """Process user feedback"""
        if not self.last_query or not self.last_response:
            print("No previous query to provide feedback for.")
            return
        
        print(f"\n🧠 Processing feedback: '{feedback_text}'")
        print("-" * 30)
        
        # Create feedback query
        feedback_query = LegalQueryInput(
            user_input=self.last_query,
            feedback=feedback_text,
            session_id=self.session_id
        )
        
        # Process feedback (this triggers learning)
        self.agent.process_query_with_learning(feedback_query)
        
        print("✅ Thank you! The agent has learned from your feedback.")
        
        # Show what changed
        self.show_learning_impact(feedback_text)
        
        # Test the same query again to show improvement
        if "not helpful" in feedback_text.lower() or "wrong" in feedback_text.lower():
            print("\n🔄 Let me try that query again with the new learning...")
            self.test_learning_improvement()
    
    def show_learning_impact(self, feedback: str):
        """Show how the feedback impacted learning"""
        stats = self.agent.get_learning_stats()
        
        is_positive = "helpful" in feedback.lower() and "not helpful" not in feedback.lower()
        
        if is_positive:
            print(f"📈 Reinforced '{self.last_response.domain}' classification")
            print(f"✅ Positive feedback count: {stats['positive_feedback_count']}")
        else:
            print(f"📉 Penalized '{self.last_response.domain}' classification")
            print(f"❌ Negative feedback count: {stats['negative_feedback_count']}")
            print(f"🔄 Classifications improved: {stats['classifications_improved']}")
    
    def test_learning_improvement(self):
        """Test if the agent improved after negative feedback"""
        if not self.last_query:
            return
        
        # Test the same query again
        test_query = LegalQueryInput(user_input=self.last_query)
        new_response = self.agent.process_query_with_learning(test_query)
        
        print(f"🔄 Same query result after learning:")
        print(f"   Before: {self.last_response.domain} (confidence: {self.last_response.confidence:.3f})")
        print(f"   After:  {new_response.domain} (confidence: {new_response.confidence:.3f})")
        
        if new_response.domain != self.last_response.domain:
            print("🎯 ✅ Domain changed - Agent learned!")
        elif abs(new_response.confidence - self.last_response.confidence) > 0.01:
            print("📊 ✅ Confidence adjusted - Agent learned!")
        else:
            print("⚠️ No immediate change - learning may take more feedback")
    
    def display_response(self, response):
        """Display agent response"""
        print(f"🏛️  Domain: {response.domain.title()} (Confidence: {response.confidence:.3f})")
        print(f"⏱️  Timeline: {response.timeline}")
        print(f"🎯 Expected Outcome: {response.outcome}")
        
        print(f"\n📝 Legal Route:")
        print(f"   {response.legal_route}")
        
        print(f"\n📋 Process Steps:")
        for i, step in enumerate(response.process_steps[:3], 1):  # Show first 3 steps
            print(f"   {step}")
        if len(response.process_steps) > 3:
            print(f"   ... and {len(response.process_steps) - 3} more steps")
        
        if response.glossary:
            print(f"\n📚 Legal Terms:")
            for term, definition in list(response.glossary.items())[:2]:  # Show first 2 terms
                print(f"   • {term.title()}: {definition[:60]}...")
        
        if response.data_driven_advice:
            print(f"\n📊 Data-Driven Insight:")
            print(f"   Risk Level: {response.risk_assessment}")
            print(f"   {response.data_driven_advice[:100]}...")
    
    def show_learning_stats(self):
        """Show learning statistics"""
        print("\n🧠 LEARNING STATISTICS")
        print("=" * 40)
        
        stats = self.agent.get_learning_stats()
        
        print(f"📊 Total Feedback Processed: {stats['total_feedback_processed']}")
        print(f"✅ Positive Feedback: {stats['positive_feedback_count']}")
        print(f"❌ Negative Feedback: {stats['negative_feedback_count']}")
        print(f"🔄 Classifications Improved: {stats['classifications_improved']}")
        print(f"🧠 Learning Data Size: {stats['learning_data_size']}")
        
        if stats['confidence_adjustments']:
            print(f"\n🎯 Domain Confidence Adjustments:")
            for domain, adjustment in stats['confidence_adjustments'].items():
                direction = "📈" if adjustment > 0 else "📉"
                print(f"   {domain}: {adjustment:+.3f} {direction}")
        
        # Show some learned queries
        if hasattr(self.agent.domain_classifier, 'negative_feedback_queries'):
            neg_queries = self.agent.domain_classifier.negative_feedback_queries
            if neg_queries:
                print(f"\n❌ Queries with Negative Feedback:")
                for query in neg_queries[-3:]:  # Show last 3
                    print(f"   • {query}")
        
        if hasattr(self.agent.domain_classifier, 'positive_feedback_queries'):
            pos_queries = self.agent.domain_classifier.positive_feedback_queries
            if pos_queries:
                print(f"\n✅ Queries with Positive Feedback:")
                for query in pos_queries[-3:]:  # Show last 3
                    print(f"   • {query}")
    
    def reset_learning(self):
        """Reset learning data"""
        confirm = input("⚠️ Reset all learning data? This cannot be undone. (yes/no): ")
        if confirm.lower() == 'yes':
            # Clear learning data
            self.agent.domain_classifier.feedback_weights.clear()
            self.agent.domain_classifier.confidence_adjustments.clear()
            self.agent.domain_classifier.negative_feedback_queries.clear()
            self.agent.domain_classifier.positive_feedback_queries.clear()
            
            # Save empty learning data
            self.agent.domain_classifier.save_learning_data()
            
            # Reset stats
            self.agent.learning_stats = {
                'total_feedback_processed': 0,
                'positive_feedback_count': 0,
                'negative_feedback_count': 0,
                'classifications_improved': 0
            }
            
            print("✅ Learning data reset. Agent is back to initial state.")
        else:
            print("❌ Reset cancelled.")
    
    def print_help(self):
        """Print help information"""
        print("\n📖 ADAPTIVE LEGAL AGENT HELP")
        print("=" * 40)
        print("This agent learns from your feedback!")
        print("\nCommands:")
        print("  query <text>     - Ask a legal question")
        print("  feedback <text>  - Give feedback on last response")
        print("  learning         - View learning statistics")
        print("  reset           - Reset all learning data")
        print("  help            - Show this help")
        print("  quit            - Exit")
        print("\nFeedback Examples:")
        print("  'feedback helpful' - Reinforces the classification")
        print("  'feedback not helpful' - Penalizes the classification")
        print("  'feedback wrong domain' - Tries alternative classification")
        print("  'feedback this should be family law' - Specific correction")
        print("\nExample Session:")
        print("  > My landlord won't return deposit")
        print("  > feedback not helpful, this is consumer issue")
        print("  > My landlord won't return deposit  # Will be different now!")


def main():
    """Main function"""
    cli = AdaptiveLegalAgentCLI()
    cli.start()


if __name__ == "__main__":
    main()
