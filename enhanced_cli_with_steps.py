"""
Enhanced CLI with Process Steps
===============================

A working CLI that shows detailed process steps for all legal queries
"""

import sys
import os
import uuid
from datetime import datetime

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        os.system("chcp 65001 > nul")
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

def safe_print(text):
    """Print text safely, handling Unicode encoding issues"""
    try:
        print(text)
    except UnicodeEncodeError:
        safe_text = text.replace('₹', 'Rs.').replace('✅', '[OK]').replace('❌', '[ERROR]').replace('⚠️', '[WARNING]')
        print(safe_text)

class ProcessStepsProvider:
    """Provides detailed process steps for all legal domains"""
    
    def __init__(self):
        self.process_mapping = {
            'tenant_rights': [
                "1. Document the issue (photos, receipts, communications with landlord)",
                "2. Review your lease agreement and local tenant protection laws",
                "3. Send written notice to landlord via certified mail with return receipt",
                "4. Wait for landlord response (typically 30 days as per local law)",
                "5. File complaint with local rent tribunal or housing court",
                "6. Attend mandatory mediation session if required by court",
                "7. Present evidence at formal hearing (photos, receipts, witnesses)",
                "8. Receive tribunal decision and follow enforcement procedures"
            ],
            'consumer_complaint': [
                "1. Collect all receipts, warranties, and purchase documentation",
                "2. Contact customer service and document all communications",
                "3. File complaint with consumer forum (District/State/National level)",
                "4. Pay prescribed fees and submit required forms",
                "5. Present evidence during hearing (receipts, photos, expert reports)",
                "6. Attend all scheduled hearings and follow court procedures",
                "7. Receive consumer forum order for replacement/refund/compensation",
                "8. Follow up on order execution within specified timeframe"
            ],
            'family_law': [
                "1. Consult qualified family lawyer for case assessment",
                "2. Gather marriage certificate, financial documents, property papers",
                "3. File divorce petition in appropriate family court jurisdiction",
                "4. Serve legal notice to spouse through court process",
                "5. Attend mandatory counseling sessions as directed by court",
                "6. Participate in mediation for mutual settlement attempts",
                "7. Present evidence during trial (if settlement fails)",
                "8. Receive final divorce decree with custody/alimony orders"
            ],
            'employment_law': [
                "1. Document workplace issues (emails, witnesses, incident reports)",
                "2. Review employment contract and company policies thoroughly",
                "3. File complaint with HR department and maintain written records",
                "4. Approach Labor Commissioner or appropriate labor authority",
                "5. Submit required forms with supporting evidence and documentation",
                "6. Attend conciliation meetings between employer and employee",
                "7. Present case at labor court hearing if conciliation fails",
                "8. Receive labor court order for reinstatement/compensation"
            ],
            'criminal_law': [
                "1. File First Information Report (FIR) at nearest police station immediately",
                "2. Provide detailed statement with all relevant facts and evidence",
                "3. Cooperate with police investigation and provide additional information",
                "4. Engage criminal lawyer for legal representation and guidance",
                "5. Attend court hearings as witness or complainant as required",
                "6. Present evidence and testimony during trial proceedings",
                "7. Follow up on case progress and court orders regularly",
                "8. Receive final judgment and follow appeal process if necessary"
            ],
            'cyber_crime': [
                "1. Preserve digital evidence (screenshots, emails, transaction records)",
                "2. File complaint with local Cyber Crime Cell or online portal",
                "3. Submit detailed complaint with all supporting digital evidence",
                "4. Provide access to affected accounts/devices for investigation",
                "5. Cooperate with cyber crime investigation team",
                "6. Attend hearings at designated cyber crime court",
                "7. Present technical evidence and expert testimony if required",
                "8. Follow court orders for recovery/compensation procedures"
            ],
            'personal_injury': [
                "1. Seek immediate medical attention and preserve medical records",
                "2. Document accident scene with photos and witness statements",
                "3. Report incident to police and obtain official accident report",
                "4. Notify insurance companies (yours and other party's) immediately",
                "5. Consult personal injury lawyer for case evaluation",
                "6. File insurance claims with comprehensive medical documentation",
                "7. Negotiate settlement with insurance companies through lawyer",
                "8. File civil lawsuit if fair settlement cannot be reached"
            ],
            'contract_dispute': [
                "1. Review contract terms and identify specific breach clauses",
                "2. Gather all contract-related documents and communications",
                "3. Send legal notice to defaulting party demanding performance",
                "4. Attempt negotiation and settlement through mutual discussion",
                "5. File civil suit in appropriate court for contract enforcement",
                "6. Present contract documents and evidence of breach in court",
                "7. Attend hearings and follow court procedures for resolution",
                "8. Receive court judgment for specific performance or damages"
            ],
            'elder_abuse': [
                "1. Document evidence of abuse (medical records, photos, witnesses)",
                "2. Contact Elder Helpline (14567) for immediate assistance",
                "3. File police complaint if physical/financial abuse is involved",
                "4. Approach Senior Citizen Tribunal for legal remedies",
                "5. Submit application with medical/financial evidence of abuse",
                "6. Attend tribunal hearings with supporting witnesses",
                "7. Present case for protection order or compensation",
                "8. Follow tribunal orders for elder protection and care"
            ],
            'immigration_law': [
                "1. Determine eligibility for desired immigration benefit or status",
                "2. Gather required documentation (passport, certificates, photos)",
                "3. Complete appropriate immigration forms accurately and completely",
                "4. Pay required government fees and submit application package",
                "5. Attend biometrics appointment at designated service center",
                "6. Participate in immigration interview if scheduled",
                "7. Respond promptly to any requests for additional evidence",
                "8. Receive decision and take appropriate next steps or appeals"
            ]
        }
    
    def get_process_steps(self, domain):
        """Get process steps for a domain"""
        return self.process_mapping.get(domain, [
            "1. Consult with qualified legal professional for case assessment",
            "2. Gather all relevant documents and evidence related to issue",
            "3. Research applicable laws and legal precedents",
            "4. Determine appropriate legal forum or authority for complaint",
            "5. File formal complaint or petition with supporting documentation",
            "6. Follow prescribed legal procedures and attend required hearings",
            "7. Present case with evidence and legal arguments",
            "8. Receive legal decision and follow enforcement procedures"
        ])

class EnhancedCLIWithSteps:
    """Enhanced CLI that shows process steps"""
    
    def __init__(self):
        self.process_provider = ProcessStepsProvider()
        
    def process_query(self, query):
        """Process a query and return response with steps"""
        
        # Simple domain classification (you can replace this with the ML classifier)
        domain = self.classify_domain(query)
        
        # Get process steps
        process_steps = self.process_provider.get_process_steps(domain)
        
        # Generate response
        response = {
            'domain': domain,
            'confidence': 0.85,  # Example confidence
            'legal_route': f"File complaint with appropriate {domain.replace('_', ' ')} authority",
            'timeline': "30-180 days",
            'success_rate': 0.70,
            'process_steps': process_steps,
            'constitutional_backing': "Available",
            'session_id': f"enhanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
        }
        
        return response
    
    def classify_domain(self, query):
        """Simple domain classification"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['landlord', 'rent', 'deposit', 'tenant', 'lease']):
            return 'tenant_rights'
        elif any(word in query_lower for word in ['boss', 'salary', 'fired', 'work', 'job', 'employment']):
            return 'employment_law'
        elif any(word in query_lower for word in ['rape', 'murder', 'theft', 'robbery', 'crime', 'police']):
            return 'criminal_law'
        elif any(word in query_lower for word in ['defective', 'refund', 'warranty', 'consumer', 'product']):
            return 'consumer_complaint'
        elif any(word in query_lower for word in ['divorce', 'marriage', 'custody', 'family', 'spouse']):
            return 'family_law'
        elif any(word in query_lower for word in ['hacked', 'cyber', 'online', 'internet', 'digital']):
            return 'cyber_crime'
        elif any(word in query_lower for word in ['elderly', 'senior', 'old', 'grandmother', 'grandfather']):
            return 'elder_abuse'
        elif any(word in query_lower for word in ['accident', 'injury', 'medical', 'doctor', 'hospital']):
            return 'personal_injury'
        elif any(word in query_lower for word in ['contract', 'agreement', 'breach', 'business']):
            return 'contract_dispute'
        elif any(word in query_lower for word in ['visa', 'immigration', 'passport', 'citizenship']):
            return 'immigration_law'
        else:
            return 'criminal_law'  # Default
    
    def display_response(self, response):
        """Display response with process steps"""
        
        safe_print(f"📋 Domain: {response['domain'].replace('_', ' ').title()} (Confidence: {response['confidence']:.3f})")
        safe_print(f"⏱️ Timeline: {response['timeline']}")
        safe_print(f"📊 Success Rate: {response['success_rate']:.1%}")
        
        safe_print(f"\n📝 Legal Route:")
        safe_print(f"   {response['legal_route']}")
        
        # Display detailed process steps
        safe_print(f"\n📋 Detailed Process Steps:")
        for step in response['process_steps']:
            safe_print(f"   {step}")
        
        if response['constitutional_backing']:
            safe_print(f"\n🏛️ Constitutional Backing: {response['constitutional_backing']}")
        
        safe_print(f"\n🔗 Session ID: {response['session_id']}")

def main():
    """Main CLI function"""
    
    safe_print("🏛️ ENHANCED LEGAL AGENT - WITH DETAILED PROCESS STEPS")
    safe_print("=" * 70)
    safe_print("Now showing detailed step-by-step legal processes!")
    safe_print("=" * 70)
    
    cli = EnhancedCLIWithSteps()
    
    safe_print("\nType your legal query (or 'quit' to exit):")
    safe_print("Try: 'landlord not returning my deposit'")
    safe_print("Try: 'my boss is not giving my salary'")
    safe_print("Try: 'I was raped by my neighbor'")
    safe_print("=" * 70)
    
    while True:
        try:
            query = input("\n> ").strip()
            
            if not query:
                continue
                
            if query.lower() in ['quit', 'exit', 'q']:
                safe_print("Goodbye!")
                break
            
            safe_print(f"\n🔍 Processing: {query}")
            safe_print("-" * 50)
            
            # Process query
            response = cli.process_query(query)
            
            # Display results with process steps
            cli.display_response(response)
            
        except KeyboardInterrupt:
            safe_print("\n\nGoodbye!")
            break
        except Exception as e:
            safe_print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
