from constitutional_article_matcher import get_constitutional_articles_with_confidence

result = get_constitutional_articles_with_confidence('my phone is being hacked by someone')
print('Articles with confidence:')
for rec in result['recommendations'][:3]:
    print(f"Article {rec['article_number']}: {rec['confidence_percentage']}% - {rec['relevance_score']}")