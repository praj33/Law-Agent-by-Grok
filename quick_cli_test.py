#!/usr/bin/env python3
"""
Quick CLI Test for Constitutional Articles
==========================================

This script demonstrates the CLI interface showing constitutional articles
with meanings and confidence percentages.
"""

from cli_interface import LegalAgentCLI
import sys

def test_cli_with_constitutional_articles():
    """Test CLI with constitutional articles display"""
    
    print("=== CLI CONSTITUTIONAL ARTICLES TEST ===")
    print()
    
    # Create CLI with adaptive agent (which includes constitutional analysis)
    try:
        cli = LegalAgentCLI(use_adaptive=True)
        print("✅ CLI with adaptive agent created successfully")
    except Exception as e:
        print(f"❌ Failed to create CLI: {e}")
        # Fallback to regular CLI
        cli = LegalAgentCLI(use_adaptive=False)
        print("✅ CLI with regular agent created successfully")
    
    # Test queries
    test_queries = [
        "my coworker is sexually harassing me at workplace",
        "my phone is being hacked by someone",
        "landlord not returning my security deposit"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: Processing query '{query}'")
        print("-" * 60)
        
        try:
            # Simulate user input by directly calling process_command
            cli.process_query(query)
            
            # Check if constitutional articles are in the response
            if cli.last_response and hasattr(cli.last_response, 'constitutional_articles'):
                articles = cli.last_response.constitutional_articles
                if articles:
                    print(f"\n📋 Constitutional Articles Found: {len(articles)}")
                    for j, article in enumerate(articles[:2], 1):  # Show first 2
                        print(f"  {j}. Article {article.get('article_number', 'N/A')}")
                        print(f"     Title: {article.get('title', 'N/A')}")
                        if 'confidence_percentage' in article:
                            print(f"     Confidence: {article['confidence_percentage']}%")
                else:
                    print("❌ No constitutional articles found in response")
            else:
                print("❌ No constitutional articles attribute in response")
                
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            import traceback
            traceback.print_exc()
        
        print()

if __name__ == "__main__":
    test_cli_with_constitutional_articles()
    print("✅ CLI constitutional articles test completed!")