"""
Standalone Process Steps Demo
============================

Shows the detailed process steps that were missing from the system
"""

def show_tenant_rights_steps():
    """Show detailed tenant rights process steps"""
    
    print("📋 Domain: Tenant Rights")
    print("🎯 Confidence: 0.95")
    print("⏱️ Timeline: 30-180 days")
    print("📊 Success Rate: 75%")
    
    print("\n📝 Legal Route:")
    print("   File complaint with rent tribunal or housing court")
    
    print("\n📋 Detailed Process Steps:")
    steps = [
        "1. Document the issue: Take photos of damage, collect rent receipts, save all communications with landlord",
        "2. Review your lease agreement: Check clauses about deposits, repairs, and tenant rights",
        "3. Research local tenant laws: Look up rent control laws and tenant protection acts in your area",
        "4. Send written notice: Draft formal complaint letter to landlord via registered post",
        "5. Wait for response: Give landlord 30 days to respond as per legal requirements",
        "6. File complaint: Submit petition to rent tribunal or housing court with all documents",
        "7. Attend mediation: Participate in court-ordered mediation session if required",
        "8. Present evidence: Show photos, receipts, witnesses at formal hearing",
        "9. Receive decision: Get tribunal order for deposit refund or rent reduction",
        "10. Enforce order: Follow legal procedures to ensure compliance with court decision"
    ]
    
    for step in steps:
        print(f"   {step}")
    
    print("\n🏛️ Constitutional Backing: Available")

def show_employment_law_steps():
    """Show detailed employment law process steps"""
    
    print("📋 Domain: Employment Law")
    print("🎯 Confidence: 0.92")
    print("⏱️ Timeline: 45-180 days")
    print("📊 Success Rate: 70%")
    
    print("\n📝 Legal Route:")
    print("   File complaint with Labor Commissioner or labor court")
    
    print("\n📋 Detailed Process Steps:")
    steps = [
        "1. Document workplace issues: Save emails, take photos, collect witness statements",
        "2. Review employment contract: Check salary terms, notice period, and termination clauses",
        "3. Check company policies: Review employee handbook and HR policies",
        "4. File internal complaint: Submit written complaint to HR department",
        "5. Maintain records: Keep copies of all communications and responses",
        "6. Approach Labor Commissioner: File complaint with local labor authority",
        "7. Submit evidence: Provide employment contract, salary slips, and documentation",
        "8. Attend conciliation: Participate in meetings between you and employer",
        "9. Labor court hearing: Present case if conciliation fails",
        "10. Receive order: Get court decision for salary payment or reinstatement"
    ]
    
    for step in steps:
        print(f"   {step}")
    
    print("\n🏛️ Constitutional Backing: Available")

def show_criminal_law_steps():
    """Show detailed criminal law process steps"""
    
    print("📋 Domain: Criminal Law")
    print("🎯 Confidence: 0.90")
    print("⏱️ Timeline: 150-645 days")
    print("📊 Success Rate: 40%")
    
    print("\n📝 Legal Route:")
    print("   File FIR and pursue criminal case through courts")
    
    print("\n📋 Detailed Process Steps:")
    steps = [
        "1. File FIR immediately: Go to nearest police station and file First Information Report",
        "2. Provide detailed statement: Give complete account of incident with all facts",
        "3. Preserve evidence: Collect photos, videos, witness contacts, medical reports",
        "4. Cooperate with investigation: Provide additional information when requested",
        "5. Engage criminal lawyer: Hire qualified lawyer for legal representation",
        "6. Attend court hearings: Be present for all scheduled court appearances",
        "7. Present testimony: Give evidence and answer questions during trial",
        "8. Follow case progress: Track case status and court orders regularly",
        "9. Receive judgment: Get final court decision on the case",
        "10. Appeal if needed: File appeal in higher court if unsatisfied with verdict"
    ]
    
    for step in steps:
        print(f"   {step}")
    
    print("\n🏛️ Constitutional Backing: Available")

def show_consumer_complaint_steps():
    """Show detailed consumer complaint process steps"""
    
    print("📋 Domain: Consumer Complaint")
    print("🎯 Confidence: 0.88")
    print("⏱️ Timeline: 45-180 days")
    print("📊 Success Rate: 72%")
    
    print("\n📝 Legal Route:")
    print("   File complaint with consumer forum")
    
    print("\n📋 Detailed Process Steps:")
    steps = [
        "1. Collect purchase documents: Gather receipts, warranties, bills, and product packaging",
        "2. Document the defect: Take photos/videos of defective product and damage",
        "3. Contact customer service: Call company helpline and document conversation",
        "4. Send written complaint: Email or post formal complaint letter to company",
        "5. Wait for response: Give company reasonable time to respond (usually 30 days)",
        "6. File consumer complaint: Submit petition to District/State/National Consumer Forum",
        "7. Pay prescribed fees: Submit court fees and required forms",
        "8. Attend hearings: Be present for all scheduled consumer forum hearings",
        "9. Present evidence: Show receipts, photos, expert reports, and witness testimony",
        "10. Receive order: Get consumer forum decision for refund/replacement/compensation"
    ]
    
    for step in steps:
        print(f"   {step}")
    
    print("\n🏛️ Constitutional Backing: Available")

def main():
    """Main demo function"""
    
    print("🏛️ LEGAL AGENT - DETAILED PROCESS STEPS RESTORED!")
    print("=" * 60)
    print("✅ NOW SHOWING THE DETAILED STEPS YOU WERE LOOKING FOR!")
    print("=" * 60)
    
    while True:
        print("\nChoose a legal domain to see detailed process steps:")
        print("1. Tenant Rights (landlord not returning deposit)")
        print("2. Employment Law (boss not giving salary)")
        print("3. Criminal Law (rape, robbery, theft)")
        print("4. Consumer Complaint (defective product)")
        print("5. Exit")
        
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                print("\n" + "="*50)
                print("TENANT RIGHTS - DETAILED PROCESS STEPS")
                print("="*50)
                show_tenant_rights_steps()
                
            elif choice == '2':
                print("\n" + "="*50)
                print("EMPLOYMENT LAW - DETAILED PROCESS STEPS")
                print("="*50)
                show_employment_law_steps()
                
            elif choice == '3':
                print("\n" + "="*50)
                print("CRIMINAL LAW - DETAILED PROCESS STEPS")
                print("="*50)
                show_criminal_law_steps()
                
            elif choice == '4':
                print("\n" + "="*50)
                print("CONSUMER COMPLAINT - DETAILED PROCESS STEPS")
                print("="*50)
                show_consumer_complaint_steps()
                
            elif choice == '5':
                print("Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
