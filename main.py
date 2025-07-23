from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from typing import Dict, Optional
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv

# FastAPI app setup
app = FastAPI(
    title="Legal Agent API",
    description="An integrated FastAPI-based legal assistant for classifying legal queries, providing legal routes, process steps, and glossary terms.",
    version="1.0.0"
)

# Pydantic schemas
class LegalQuery(BaseModel):
    user_input: str
    feedback: Optional[str] = None

class LegalResponse(BaseModel):
    domain: str
    confidence: float
    legal_route: str
    timeline: str
    outcome: str
    process_steps: str
    glossary: Dict[str, str]

# Query handler
def clean_query(query):
    return query.strip().lower()

# Domain classifier
domain_data = pd.DataFrame({
    'domain': ['tenant rights', 'consumer complaint', 'family law'],
    'example_query': [
        'my landlord is not returning deposit',
        'i received a faulty product',
        'i want a divorce from my husband'
    ]
})

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(domain_data['example_query'])

def classify_query(user_query):
    user_vec = vectorizer.transform([user_query])
    sims = cosine_similarity(user_vec, X)
    best_match = sims.argmax()
    confidence = float(sims[0][best_match])
    if confidence < 0.2:
        return "unknown", confidence
    return domain_data['domain'][best_match], confidence

# Legal route engine
def get_legal_route(domain):
    mapping = {
        'tenant rights': {
            'summary': 'Send legal notice to landlord and approach rent tribunal.',
            'timeline': '2-3 months',
            'outcome': 'Deposit refund or rent reduction.'
        },
        'consumer complaint': {
            'summary': 'File complaint in consumer forum.',
            'timeline': '3-6 months',
            'outcome': 'Replacement or refund of product.'
        },
        'family law': {
            'summary': 'File divorce petition in family court.',
            'timeline': '6 months to 1 year',
            'outcome': 'Legal separation, child custody, alimony if applicable.'
        },
        'unknown': {
            'summary': 'No legal route found for the given input.',
            'timeline': 'N/A',
            'outcome': 'Please consult a legal expert.'
        }
    }
    return mapping.get(domain, mapping['unknown'])

# Glossary engine
glossary_db = {
    'legal notice': 'A formal written communication from one party to another.',
    'tribunal': 'A special court that handles particular legal matters.',
    'alimony': 'Money paid to a former spouse after divorce.',
    'consumer forum': 'A court that handles cases related to consumer complaints.',
    'petition': 'A formal written request to a court.'
}

def find_legal_terms(text):
    found = {}
    for term in glossary_db:
        if term in text.lower():
            found[term] = glossary_db[term]
    return found

# Process explainer
def explain_process(domain):
    steps_mapping = {
        'tenant rights': '1. Draft legal notice → 2. Send to landlord → 3. File complaint in rent tribunal → 4. Attend hearings → 5. Get decision.',
        'consumer complaint': '1. Collect receipts → 2. File complaint in consumer forum → 3. Present evidence → 4. Attend hearings → 5. Get resolution.',
        'family law': '1. Consult family lawyer → 2. File divorce petition → 3. Attend mediation → 4. Go through court proceedings → 5. Final decision.',
        'unknown': 'No process steps found. Please consult a lawyer.'
    }
    return steps_mapping.get(domain, steps_mapping['unknown'])

# Feedback collector
def collect_feedback(query, domain, feedback, file='feedback.csv'):
    with open(file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([query, domain, feedback])

# API endpoint
@app.post("/legal-query", response_model=LegalResponse)
async def process_legal_query(query: LegalQuery):
    # Clean query
    cleaned_query = clean_query(query.user_input)
    
    # Classify domain
    domain, confidence = classify_query(cleaned_query)
    
    # Get legal route
    route = get_legal_route(domain)
    
    # Get process steps
    steps = explain_process(domain)
    
    # Find glossary terms
    glossary = find_legal_terms(query.user_input + ' ' + route['summary'])
    
    # Collect feedback
    feedback = query.feedback if query.feedback else "not provided"
    collect_feedback(cleaned_query, domain, feedback)
    
    # Return response
    return LegalResponse(
        domain=domain,
        confidence=confidence,
        legal_route=route['summary'],
        timeline=route['timeline'],
        outcome=route['outcome'],
        process_steps=steps,
        glossary=glossary
    )

# Custom OpenAPI schema for Swagger UI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Legal Agent API",
        version="1.0.0",
        description="An integrated FastAPI-based legal assistant for classifying legal queries, providing legal routes, process steps, and glossary terms.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = custom_openapi