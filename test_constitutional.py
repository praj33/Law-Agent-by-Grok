from constitutional_article_matcher import get_constitutional_articles_with_confidence

result = get_constitutional_articles_with_confidence('My phone is hacked')
print('Matching articles:', result['matching_articles'])
print('Top 3 recommendations:')
for r in result['recommendations'][:3]:
    print(f"  Article {r['article_number']} - {r['confidence_percentage']}% confidence")