"""
Enhanced Legal Agent CLI with Constitutional Integration
======================================================

Interactive command-line interface for the Legal Agent with constitutional backing.
Now includes Indian Constitutional articles for enhanced legal advice.

Features:
- 10 legal domain classification
- Enhanced crime data integration (3 datasets)
- Constitutional article references
- Location-based insights
- Self-learning capabilities

Usage: python constitutional_cli.py
"""

import sys
from typing import Optional
from legal_agent import create_legal_agent, LegalQueryInput
from adaptive_legal_agent import create_adaptive_legal_agent

class ConstitutionalLegalCLI:
    """Enhanced CLI with constitutional integration"""
    
    def __init__(self):
        """Initialize the enhanced CLI"""
        self.agent = None
        self.adaptive_agent = None
        self.use_adaptive = False
        self.session_count = 0
        
    def initialize_agents(self):
        """Initialize legal agents"""
        print("🔄 Initializing Enhanced Legal Agent with Constitutional Integration...")
        
        try:
            # Initialize basic agent
            self.agent = create_legal_agent()
            print("✅ Basic Legal Agent initialized")
            
            # Initialize adaptive agent
            self.adaptive_agent = create_adaptive_legal_agent()
            print("✅ Adaptive Legal Agent initialized")
            
            return True
        except Exception as e:
            print(f"❌ Error initializing agents: {e}")
            return False
    
    def display_welcome(self):
        """Display welcome message with constitutional features"""
        print("\n" + "="*80)
        print("🏛️  ENHANCED LEGAL AGENT - Constitutional Integration")
        print("    AI-Powered Legal Assistance with Indian Constitutional Backing")
        print("="*80)
        
        print("\n📊 System Capabilities:")
        print("   • 10 Legal Domains: Tenant Rights, Consumer, Family, Employment, etc.")
        print("   • 11 Constitutional Articles: Citizenship, Fundamental Rights")
        print("   • 3 Crime Datasets: 36 States/UTs with historical trends")
        print("   • Enhanced Data Integration: Location-based insights")
        print("   • Self-Learning: Adaptive responses based on feedback")
        
        print("\n🏛️ Constitutional Features:")
        print("   • Constitutional backing for all legal advice")
        print("   • Relevant article references (Articles 1-10)")
        print("   • Citizenship law support (Articles 5-10)")
        print("   • Enhanced credibility with constitutional basis")
        
        print("\n💡 Example Queries:")
        print("   • 'My phone is being hacked' → Cyber Crime + Constitutional privacy rights")
        print("   • 'I was arrested without warrant' → Criminal Law + Articles 20-22")
        print("   • 'Need citizenship help' → Immigration + Articles 5-10")
        print("   • 'Elderly abuse in Delhi' → Elder Abuse + Crime data + Article 21")
        
        print("\n⚙️ Commands:")
        print("   • Type your legal question")
        print("   • 'adaptive' - Switch to adaptive mode")
        print("   • 'basic' - Switch to basic mode")
        print("   • 'stats' - View system statistics")
        print("   • 'help' - Show this help")
        print("   • 'quit' - Exit")
        
        print("\n" + "="*80)
    
    def process_query(self, user_input: str) -> bool:
        """Process user query and display enhanced response"""
        
        if not user_input.strip():
            return True
        
        # Handle commands
        command = user_input.lower().strip()
        
        if command == 'quit':
            return False
        elif command == 'help':
            self.display_welcome()
            return True
        elif command == 'adaptive':
            self.use_adaptive = True
            print("✅ Switched to Adaptive Mode (self-learning enabled)")
            return True
        elif command == 'basic':
            self.use_adaptive = False
            print("✅ Switched to Basic Mode")
            return True
        elif command == 'stats':
            self.display_stats()
            return True
        
        # Process legal query
        self.session_count += 1
        
        print(f"\n🔍 Processing Query #{self.session_count}...")
        print("-" * 60)
        
        try:
            query_input = LegalQueryInput(user_input=user_input)
            
            if self.use_adaptive:
                response = self.adaptive_agent.process_query_with_learning(query_input)
                print("🧠 Mode: Adaptive (Self-Learning)")
            else:
                response = self.agent.process_query(query_input)
                print("⚙️ Mode: Basic")
            
            # Display core response
            self.display_core_response(response)
            
            # Display constitutional backing
            self.display_constitutional_backing(response)
            
            # Display enhanced features
            self.display_enhanced_features(response)
            
            # Ask for feedback
            self.collect_feedback(response)
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            print("Please try rephrasing your question or contact support.")
        
        return True
    
    def display_core_response(self, response):
        """Display core legal response"""
        print(f"\n🎯 Legal Analysis:")
        print(f"   Domain: {response.domain.title()} (Confidence: {response.confidence:.3f})")
        print(f"   Legal Route: {response.legal_route}")
        print(f"   Timeline: {response.timeline}")
        print(f"   Expected Outcome: {response.outcome}")
    
    def display_constitutional_backing(self, response):
        """Display constitutional backing if available"""
        if hasattr(response, 'constitutional_backing') and response.constitutional_backing:
            print(f"\n🏛️ Constitutional Backing:")
            print(f"   {response.constitutional_backing}")
            
            if hasattr(response, 'constitutional_articles') and response.constitutional_articles:
                print(f"\n📜 Relevant Constitutional Articles:")
                for article in response.constitutional_articles:
                    print(f"   • Article {article['article_number']}: {article['title'][:60]}...")
                    if article.get('summary'):
                        print(f"     {article['summary'][:80]}...")
        else:
            print(f"\n🏛️ Constitutional Backing: Not available for this query")
    
    def display_enhanced_features(self, response):
        """Display enhanced features (crime data, location insights)"""
        
        # Location-based insights
        if hasattr(response, 'location_insights') and response.location_insights:
            print(f"\n📍 Location-Based Insights:")
            if response.location_insights.get('location_found'):
                print(f"   Location: {response.location_insights.get('location', 'Unknown')}")
                print(f"   Risk Level: {response.risk_assessment or 'Unknown'}")
                
                if hasattr(response, 'data_driven_advice') and response.data_driven_advice:
                    print(f"   Enhanced Advice: {response.data_driven_advice[:100]}...")
        
        # Process steps
        if hasattr(response, 'process_steps') and response.process_steps:
            print(f"\n📋 Process Steps:")
            for i, step in enumerate(response.process_steps[:3], 1):
                print(f"   {i}. {step}")
            if len(response.process_steps) > 3:
                print(f"   ... and {len(response.process_steps) - 3} more steps")
        
        # Glossary terms
        if hasattr(response, 'glossary') and response.glossary:
            print(f"\n📚 Key Legal Terms:")
            for term, definition in list(response.glossary.items())[:2]:
                print(f"   • {term}: {definition[:60]}...")
    
    def collect_feedback(self, response):
        """Collect user feedback"""
        if self.use_adaptive:
            print(f"\n💬 Feedback (for learning):")
            print("   Was this response helpful? (yes/no/skip)")
            
            try:
                feedback_input = input("   Your feedback: ").strip().lower()
                
                if feedback_input in ['yes', 'y']:
                    print("   ✅ Thank you! This helps improve the system.")
                elif feedback_input in ['no', 'n']:
                    print("   📝 Thank you for the feedback. The system will learn from this.")
                else:
                    print("   ⏭️ Feedback skipped.")
            except KeyboardInterrupt:
                print("\n   ⏭️ Feedback skipped.")
    
    def display_stats(self):
        """Display system statistics"""
        print(f"\n📊 System Statistics:")
        print("-" * 30)
        print(f"   Queries Processed: {self.session_count}")
        print(f"   Current Mode: {'Adaptive' if self.use_adaptive else 'Basic'}")
        print(f"   Constitutional Articles: 11 loaded")
        print(f"   Crime Data Coverage: 36 states/UTs")
        print(f"   Legal Domains: 10 supported")
        
        if self.agent:
            try:
                feedback_stats = self.agent.get_feedback_stats()
                print(f"   Total Feedback: {feedback_stats.get('total_feedback', 0)}")
                print(f"   Positive Feedback: {feedback_stats.get('positive_feedback', 0)}")
            except:
                print(f"   Feedback Stats: Not available")
    
    def run(self):
        """Run the enhanced CLI"""
        
        # Initialize agents
        if not self.initialize_agents():
            print("❌ Failed to initialize agents. Exiting.")
            return
        
        # Display welcome
        self.display_welcome()
        
        print(f"\n🚀 Enhanced Legal Agent Ready!")
        print("Type your legal question or 'help' for assistance.")
        
        # Main interaction loop
        while True:
            try:
                print(f"\n{'🧠 Adaptive' if self.use_adaptive else '⚙️ Basic'} Mode | Query #{self.session_count + 1}")
                user_input = input("❓ Your legal question: ").strip()
                
                if not self.process_query(user_input):
                    break
                    
            except KeyboardInterrupt:
                print(f"\n\n👋 Thank you for using Enhanced Legal Agent!")
                print("Your queries help improve the system through constitutional integration.")
                break
            except EOFError:
                break
        
        print(f"\n📊 Session Summary:")
        print(f"   Queries Processed: {self.session_count}")
        print(f"   Constitutional Backing: Provided for applicable queries")
        print(f"   Enhanced Features: Crime data + Constitutional articles")
        print("\n🏛️ Enhanced Legal Agent - Constitutional Integration Complete")


def main():
    """Main function"""
    cli = ConstitutionalLegalCLI()
    cli.run()


if __name__ == "__main__":
    main()
