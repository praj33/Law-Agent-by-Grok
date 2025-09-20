from constitutional_integration import create_constitutional_advisor

advisor = create_constitutional_advisor()
result = advisor.get_constitutional_backing('cyber_crime', 'my phone is being hacked by someone')

print("Constitutional backing result:")
print("Articles:", [f"Article {art['article_number']}" for art in result.get('articles', [])])