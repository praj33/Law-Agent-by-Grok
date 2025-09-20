#!/usr/bin/env python3

from ultimate_legal_agent import create_ultimate_legal_agent

def test_hacking_query():
    agent = create_ultimate_legal_agent()
    result = agent.process_ultimate_query('My phone is hacked')
    print('Domain:', result['domain'])
    print('Subdomain:', result['subdomain'])
    print('Domain Confidence:', result['domain_confidence'])
    print('Subdomain Confidence:', result['subdomain_confidence'])
    print('Total Sections:', result['total_sections'])
    
    # Also check the taxonomy classification
    taxonomy_domain, taxonomy_subdomain, taxonomy_confidence = agent.classify_query_according_to_taxonomy('My phone is hacked')
    print('Taxonomy Domain:', taxonomy_domain)
    print('Taxonomy Subdomain:', taxonomy_subdomain)
    print('Taxonomy Confidence:', taxonomy_confidence)
    
    # Check constitutional articles
    print('Constitutional Articles:', len(result.get('constitutional_articles', [])))
    if result.get('constitutional_articles'):
        for article in result['constitutional_articles']:
            print(f"  - Article {article['article_number']}: {article['title']} ({article['confidence_percentage']}%)")

if __name__ == "__main__":
    test_hacking_query()