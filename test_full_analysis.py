from ultimate_legal_agent import create_ultimate_legal_agent

agent = create_ultimate_legal_agent()
result = agent.process_ultimate_query('My phone is hacked')

print('Domain:', result['domain'])
print('Subdomain:', result['subdomain'])
print('Confidence:', result['subdomain_confidence'])
print()

print('Constitutional Articles:')
for article in result.get('constitutional_articles', [])[:3]:
    print(f'  Article {article["article_number"]}: {article["title"]} ({article["confidence_percentage"]}% confidence)')

print()
print('BNS Sections:', len(result['bns_sections']))
print('IPC Sections:', len(result['ipc_sections']))
print('CrPC Sections:', len(result['crpc_sections']))