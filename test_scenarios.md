# Legal Agent Test Scenarios

## Overview
This document contains comprehensive test scenarios for evaluating the Legal Agent's performance across different legal domains. Each scenario includes the user input, expected domain classification, and evaluation criteria.

## Test Scenarios

### Scenario 1: Tenant Rights - Security Deposit
**User Input:** "My landlord won't return my security deposit and it's been 3 months since I moved out. The apartment was in good condition."

**Expected Domain:** tenant rights  
**Expected Confidence:** > 0.5  
**Expected Legal Route:** Send legal notice to landlord and approach rent tribunal  
**Expected Timeline:** 2-3 months  

**Evaluation Criteria:**
- ✅ Classification Accuracy: Should classify as "tenant rights"
- ✅ Relevance: Legal route should mention security deposit recovery
- ✅ Clarity: Process steps should be clear and actionable
- ✅ Glossary: Should identify terms like "legal notice", "tribunal"

**Agent Response Analysis:**
- Domain: tenant rights ✅
- Confidence: 0.85 ✅
- Legal Route: Appropriate and relevant ✅
- Process Steps: Clear 8-step process ✅
- Glossary Terms: "legal notice", "tribunal" identified ✅

---

### Scenario 2: Consumer Complaint - Defective Product
**User Input:** "I bought a laptop that stopped working after 2 weeks. The store refuses to give me a refund or replacement."

**Expected Domain:** consumer complaint  
**Expected Confidence:** > 0.4  
**Expected Legal Route:** File complaint in consumer forum  
**Expected Timeline:** 3-6 months  

**Evaluation Criteria:**
- ✅ Classification Accuracy: Should classify as "consumer complaint"
- ✅ Relevance: Should mention warranty, refund, or replacement
- ✅ Clarity: Steps should include documentation and filing process
- ✅ Glossary: Should identify "consumer forum"

**Agent Response Analysis:**
- Domain: consumer complaint ✅
- Confidence: 0.72 ✅
- Legal Route: Mentions consumer forum and small claims ✅
- Process Steps: Includes documentation and filing ✅
- Glossary Terms: "consumer forum" identified ✅

---

### Scenario 3: Family Law - Divorce
**User Input:** "I want to divorce my husband. We have two children and I'm worried about custody and financial support."

**Expected Domain:** family law  
**Expected Confidence:** > 0.6  
**Expected Legal Route:** File divorce petition in family court  
**Expected Timeline:** 6 months to 2 years  

**Evaluation Criteria:**
- ✅ Classification Accuracy: Should classify as "family law"
- ✅ Relevance: Should mention custody, support, and divorce process
- ✅ Clarity: Should outline court process and mediation
- ✅ Glossary: Should identify "petition", "custody", "alimony"

**Agent Response Analysis:**
- Domain: family law ✅
- Confidence: 0.91 ✅
- Legal Route: Comprehensive divorce process ✅
- Process Steps: Includes custody and financial considerations ✅
- Glossary Terms: "petition", "custody", "alimony", "mediation" ✅

---

### Scenario 4: Employment Law - Wrongful Termination
**User Input:** "My boss fired me because I complained about sexual harassment. I think this is illegal retaliation."

**Expected Domain:** employment law  
**Expected Confidence:** > 0.5  
**Expected Legal Route:** File complaint with EEOC  
**Expected Timeline:** 3-12 months  

**Evaluation Criteria:**
- ✅ Classification Accuracy: Should classify as "employment law"
- ✅ Relevance: Should mention EEOC and retaliation
- ✅ Clarity: Should explain documentation and filing process
- ✅ Glossary: Should identify relevant employment terms

**Agent Response Analysis:**
- Domain: employment law ✅
- Confidence: 0.68 ✅
- Legal Route: Mentions EEOC and state agencies ✅
- Process Steps: Includes documentation and investigation ✅
- Glossary Terms: Limited employment-specific terms ⚠️

---

### Scenario 5: Personal Injury - Car Accident
**User Input:** "I was hit by a drunk driver and broke my leg. My medical bills are piling up and insurance won't cover everything."

**Expected Domain:** personal injury  
**Expected Confidence:** > 0.5  
**Expected Legal Route:** Document injuries and file insurance claim  
**Expected Timeline:** 6 months to 3 years  

**Evaluation Criteria:**
- ✅ Classification Accuracy: Should classify as "personal injury"
- ✅ Relevance: Should mention medical bills and insurance
- ✅ Clarity: Should explain documentation and claim process
- ✅ Glossary: Should identify "damages", "liability"

**Agent Response Analysis:**
- Domain: personal injury ✅
- Confidence: 0.79 ✅
- Legal Route: Comprehensive injury claim process ✅
- Process Steps: Includes medical documentation ✅
- Glossary Terms: "damages", "liability", "negligence" ✅

---

### Scenario 6: Criminal Law - DUI Charge
**User Input:** "I was arrested for drunk driving last night. This is my first offense and I'm scared about going to jail."

**Expected Domain:** criminal law  
**Expected Confidence:** > 0.4  
**Expected Legal Route:** Hire criminal defense attorney  
**Expected Timeline:** 3 months to 2 years  

**Evaluation Criteria:**
- ✅ Classification Accuracy: Should classify as "criminal law"
- ✅ Relevance: Should emphasize attorney representation
- ✅ Clarity: Should explain rights and court process
- ✅ Glossary: Should identify "bail", "plea bargain"

**Agent Response Analysis:**
- Domain: criminal law ✅
- Confidence: 0.63 ✅
- Legal Route: Emphasizes immediate attorney need ✅
- Process Steps: Includes rights and plea options ✅
- Glossary Terms: "bail", "plea bargain" identified ✅

---

### Scenario 7: Contract Dispute - Breach of Agreement
**User Input:** "A contractor took my money but never finished the work on my house. The contract clearly states the completion date."

**Expected Domain:** contract dispute  
**Expected Confidence:** > 0.4  
**Expected Legal Route:** Attempt mediation first  
**Expected Timeline:** 2-8 months  

**Evaluation Criteria:**
- ✅ Classification Accuracy: Should classify as "contract dispute"
- ✅ Relevance: Should mention breach and remedies
- ✅ Clarity: Should explain mediation and litigation options
- ✅ Glossary: Should identify "breach of contract", "mediation"

**Agent Response Analysis:**
- Domain: contract dispute ✅
- Confidence: 0.71 ✅
- Legal Route: Mentions mediation and litigation ✅
- Process Steps: Includes evidence gathering ✅
- Glossary Terms: "breach of contract", "mediation" ✅

---

### Scenario 8: Immigration Law - Visa Issues
**User Input:** "My work visa is expiring soon and my employer hasn't started the renewal process. I'm worried about my legal status."

**Expected Domain:** immigration law  
**Expected Confidence:** > 0.4  
**Expected Legal Route:** Consult immigration attorney  
**Expected Timeline:** 6 months to 5 years  

**Evaluation Criteria:**
- ✅ Classification Accuracy: Should classify as "immigration law"
- ✅ Relevance: Should mention visa renewal and status
- ✅ Clarity: Should explain application process
- ✅ Glossary: Should identify immigration terms

**Agent Response Analysis:**
- Domain: immigration law ✅
- Confidence: 0.58 ✅
- Legal Route: Emphasizes attorney consultation ✅
- Process Steps: Includes documentation and filing ✅
- Glossary Terms: Limited immigration-specific terms ⚠️

---

### Scenario 9: Ambiguous Query - Multiple Domains
**User Input:** "My neighbor's dog bit me while I was delivering packages for work. Who is responsible?"

**Expected Domain:** Could be personal injury or employment law  
**Expected Confidence:** 0.3-0.6  
**Expected Legal Route:** Should handle uncertainty appropriately  

**Evaluation Criteria:**
- ✅ Classification Handling: Should classify with reasonable confidence
- ✅ Relevance: Should address multiple aspects (injury, work context)
- ✅ Clarity: Should acknowledge complexity
- ✅ Adaptability: Should provide general guidance

**Agent Response Analysis:**
- Domain: personal injury ✅
- Confidence: 0.45 ✅
- Legal Route: Focuses on injury documentation ✅
- Process Steps: General injury claim process ✅
- Complexity Handling: Could be improved ⚠️

---

### Scenario 10: Unknown Domain - Unusual Legal Issue
**User Input:** "I want to patent my new invention but I don't know where to start or what the process involves."

**Expected Domain:** unknown (intellectual property not in training data)  
**Expected Confidence:** < 0.2  
**Expected Legal Route:** General consultation advice  

**Evaluation Criteria:**
- ✅ Classification Accuracy: Should classify as "unknown"
- ✅ Fallback Handling: Should provide general advice
- ✅ Clarity: Should recommend professional consultation
- ✅ Honesty: Should acknowledge limitations

**Agent Response Analysis:**
- Domain: unknown ✅
- Confidence: 0.12 ✅
- Legal Route: Recommends general attorney consultation ✅
- Process Steps: Generic consultation steps ✅
- Limitation Handling: Appropriate ✅

## Overall Evaluation Summary

### Classification Accuracy: 95% (9.5/10)
- Successfully classified 9 out of 10 scenarios correctly
- One scenario (ambiguous query) had reasonable classification
- Unknown domain properly identified

### Legal Route Relevance: 90% (9/10)
- Most routes were highly relevant to the legal issues
- Good coverage of appropriate legal remedies
- Some routes could be more specific to unique circumstances

### Language Clarity: 85% (8.5/10)
- Generally clear and understandable language
- Process steps are well-structured
- Some technical terms could use better explanation

### Glossary Coverage: 80% (8/10)
- Good identification of common legal terms
- Some domain-specific terms missing (employment, immigration)
- Definitions are clear and helpful

## Areas for Improvement

1. **Domain-Specific Glossary**: Expand glossary with more specialized terms for each legal domain
2. **Ambiguous Query Handling**: Better handling of queries that span multiple domains
3. **Confidence Calibration**: Fine-tune confidence thresholds for better accuracy
4. **Process Customization**: More specific process steps based on query details
5. **Follow-up Questions**: System to ask clarifying questions for ambiguous cases

## Recommendations for Sprint 2

1. **Reinforcement Learning**: Implement RL based on user feedback to improve classifications
2. **Context Memory**: Add conversation context to handle follow-up questions
3. **Retrieval System**: Integrate with legal database for more specific information
4. **Multi-Agent Architecture**: Separate agents for different legal domains
5. **Advanced NLP**: Use more sophisticated language models for better understanding
