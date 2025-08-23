"""
Debug Constitutional Articles
============================

This script will help us debug exactly what constitutional articles
are being shown to the user for workplace harassment queries.
"""

def test_all_agents():
    """Test all available agents to see which one has the wrong articles"""
    
    print("🔍 DEBUGGING CONSTITUTIONAL ARTICLES")
    print("=" * 60)
    
    query = "my coworker is sexually harassing me at work"
    print(f"Query: {query}")
    
    # Test 1: Working Enhanced Agent
    print("\n1. TESTING WORKING ENHANCED AGENT:")
    print("-" * 40)
    try:
        from working_enhanced_agent import create_working_enhanced_agent
        agent1 = create_working_enhanced_agent()
        response1 = agent1.process_query(query)
        print(f"Constitutional backing: {response1.constitutional_backing}")
        
        # Check for wrong articles
        if "Article 3" in response1.constitutional_backing:
            print("❌ FOUND Article 3 (wrong!)")
        if "Article 6" in response1.constitutional_backing:
            print("❌ FOUND Article 6 (wrong!)")
        if "Article 14" in response1.constitutional_backing:
            print("✅ FOUND Article 14 (correct!)")
        if "Article 15" in response1.constitutional_backing:
            print("✅ FOUND Article 15 (correct!)")
            
    except Exception as e:
        print(f"Error with working enhanced agent: {e}")
    
    # Test 2: Basic Legal Agent
    print("\n2. TESTING BASIC LEGAL AGENT:")
    print("-" * 40)
    try:
        from legal_agent import create_legal_agent, LegalQueryInput
        agent2 = create_legal_agent()
        query_input = LegalQueryInput(user_input=query, session_id="debug")
        response2 = agent2.process_query(query_input)
        print(f"Constitutional backing: {response2.constitutional_backing}")
        
        # Check for wrong articles
        if response2.constitutional_backing:
            if "Article 3" in response2.constitutional_backing:
                print("❌ FOUND Article 3 (wrong!) - THIS IS THE PROBLEM!")
            if "Article 6" in response2.constitutional_backing:
                print("❌ FOUND Article 6 (wrong!) - THIS IS THE PROBLEM!")
            if "Article 14" in response2.constitutional_backing:
                print("✅ FOUND Article 14 (correct!)")
            if "Article 15" in response2.constitutional_backing:
                print("✅ FOUND Article 15 (correct!)")
        else:
            print("No constitutional backing provided")
            
    except Exception as e:
        print(f"Error with basic legal agent: {e}")
    
    # Test 3: Enhanced Legal Agent
    print("\n3. TESTING ENHANCED LEGAL AGENT:")
    print("-" * 40)
    try:
        from enhanced_legal_agent import EnhancedLegalAgent
        agent3 = EnhancedLegalAgent()
        response3 = agent3.process_query(query)
        print(f"Constitutional backing: {response3.constitutional_backing}")
        
        # Check for wrong articles
        if response3.constitutional_backing:
            if "Article 3" in response3.constitutional_backing:
                print("❌ FOUND Article 3 (wrong!) - THIS IS THE PROBLEM!")
            if "Article 6" in response3.constitutional_backing:
                print("❌ FOUND Article 6 (wrong!) - THIS IS THE PROBLEM!")
            if "Article 14" in response3.constitutional_backing:
                print("✅ FOUND Article 14 (correct!)")
            if "Article 15" in response3.constitutional_backing:
                print("✅ FOUND Article 15 (correct!)")
        else:
            print("No constitutional backing provided")
            
    except Exception as e:
        print(f"Error with enhanced legal agent: {e}")

def test_constitutional_database():
    """Test the constitutional database directly"""
    
    print("\n4. TESTING CONSTITUTIONAL DATABASE DIRECTLY:")
    print("-" * 50)
    
    try:
        from constitutional_integration import ConstitutionalDatabase
        db = ConstitutionalDatabase()
        
        print(f"Total articles loaded: {len(db.articles)}")
        print("Available articles:")
        for article_num in sorted(db.articles.keys(), key=lambda x: int(x) if x.isdigit() else 999):
            article = db.articles[article_num]
            print(f"  Article {article_num}: {article.title[:50]}...")
        
        # Test search for harassment
        print("\nSearching for 'harassment':")
        harassment_articles = db.search_articles("harassment", limit=3)
        for article in harassment_articles:
            print(f"  Found: Article {article.article_number}: {article.title[:50]}...")
            
        # Test domain mapping
        print("\nEmployment law domain articles:")
        employment_articles = db.get_articles_for_domain("employment law")
        for article in employment_articles:
            print(f"  Domain: Article {article.article_number}: {article.title[:50]}...")
            
    except Exception as e:
        print(f"Error testing constitutional database: {e}")

def test_cli_agent():
    """Test the exact agent that CLI uses"""
    
    print("\n5. TESTING CLI AGENT (EXACT SAME AS CLI):")
    print("-" * 50)
    
    try:
        from cli_interface import LegalAgentCLI
        cli = LegalAgentCLI()
        
        # Process the query exactly as CLI does
        cli.process_query("my coworker is sexually harassing me at work")
        
        if cli.last_response:
            print(f"Constitutional backing: {cli.last_response.constitutional_backing}")
            
            # Check for wrong articles
            if cli.last_response.constitutional_backing:
                if "Article 3" in cli.last_response.constitutional_backing:
                    print("❌ CLI SHOWS Article 3 (wrong!) - FOUND THE PROBLEM!")
                if "Article 6" in cli.last_response.constitutional_backing:
                    print("❌ CLI SHOWS Article 6 (wrong!) - FOUND THE PROBLEM!")
                if "Article 14" in cli.last_response.constitutional_backing:
                    print("✅ CLI SHOWS Article 14 (correct!)")
                if "Article 15" in cli.last_response.constitutional_backing:
                    print("✅ CLI SHOWS Article 15 (correct!)")
        else:
            print("No response generated")
            
    except Exception as e:
        print(f"Error testing CLI agent: {e}")

def main():
    """Run all debugging tests"""
    
    test_all_agents()
    test_constitutional_database()
    test_cli_agent()
    
    print("\n" + "=" * 60)
    print("🎯 DEBUGGING COMPLETE")
    print("=" * 60)
    print("This will help identify which agent is showing wrong articles.")

if __name__ == "__main__":
    main()
