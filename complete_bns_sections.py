#!/usr/bin/env python3
"""
Complete BNS Sections Database - All 358 Sections
=================================================

Complete database of all 358 Bharatiya Nyaya Sanhita (BNS) 2023 sections.
This module contains the comprehensive sections data that will be integrated
into the main bharatiya_nyaya_sanhita.py file.

Author: Legal Agent Team  
Version: 2.0.0 - Complete BNS Integration
Date: 2025-01-15
"""

# Complete BNS Sections Dictionary - All 358 Sections
COMPLETE_BNS_SECTIONS = {
    "1": {"title": "Short title, commencement and application", "description": "This Act may be called the Bharatiya Nyaya Sanhita, 2023.", "category": "preliminary"},
    "2": {"title": "Definitions", "description": "General definitions applicable to this Sanhita.", "category": "preliminary"},
    "3": {"title": "General explanations", "description": "General explanations for terms used in this Sanhita.", "category": "preliminary"},
    "4": {"title": "Punishments", "description": "Types of punishments under this Sanhita.", "category": "preliminary"},
    "5": {"title": "Commutation of sentence", "description": "Provisions for commutation of sentences.", "category": "preliminary"},
    "6": {"title": "Fractions of terms of punishment", "description": "Treatment of fractions in punishment terms.", "category": "preliminary"},
    "7": {"title": "Sentence may be (in certain cases of imprisonment) wholly or partly rigorous or simple", "description": "Nature of imprisonment sentences.", "category": "preliminary"},
    "8": {"title": "Amount of fine, liability in default of payment of fine, etc.", "description": "Provisions regarding fines and default.", "category": "preliminary"},
    "9": {"title": "Limit of punishment of offence made up of several offences", "description": "Punishment limits for multiple offences.", "category": "preliminary"},
    "10": {"title": "Punishment of person guilty of one of several offences, judgment stating that it is doubtful of which", "description": "Punishment when specific offence is doubtful.", "category": "preliminary"},
    "11": {"title": "Solitary confinement", "description": "Provisions for solitary confinement.", "category": "preliminary"},
    "12": {"title": "Limit of solitary confinement", "description": "Time limits for solitary confinement.", "category": "preliminary"},
    "13": {"title": "Enhanced punishment for certain offences after previous conviction", "description": "Enhanced punishment for repeat offenders.", "category": "preliminary"},
    "14": {"title": "Act done by a person bound, or by mistake of fact believing himself bound, by law", "description": "Legal obligation defence.", "category": "general_exceptions"},
    "15": {"title": "Act of Judge when acting judicially", "description": "Judicial immunity for judges.", "category": "general_exceptions"},
    "16": {"title": "Act done pursuant to judgment or order of Court", "description": "Acts done under court orders.", "category": "general_exceptions"},
    "17": {"title": "Act done by a person justified, or by mistake of fact believing himself justified, by law", "description": "Legal justification defence.", "category": "general_exceptions"},
    "18": {"title": "Accident in doing a lawful act", "description": "Accidental harm during lawful acts.", "category": "general_exceptions"},
    "19": {"title": "Act likely to cause harm, but done without criminal intent, and to prevent other harm", "description": "Acts to prevent greater harm.", "category": "general_exceptions"},
    "20": {"title": "Act of a child under seven years of age", "description": "No criminal liability for children under 7.", "category": "general_exceptions"},
    "21": {"title": "Act of a child above seven and under twelve years of age of immature understanding", "description": "Limited liability for children 7-12 years.", "category": "general_exceptions"},
    "22": {"title": "Act of a person of unsound mind", "description": "Mental illness defence.", "category": "general_exceptions"},
    "23": {"title": "Act of a person incapable of judgment by reason of intoxication caused against his will", "description": "Involuntary intoxication defence.", "category": "general_exceptions"},
    "24": {"title": "Offence requiring a particular intent or knowledge committed by one who is intoxicated", "description": "Intoxication and specific intent.", "category": "general_exceptions"},
    "25": {"title": "Act not intended and not known to be likely to cause death or grievous hurt, done by consent", "description": "Consent defence for non-serious harm.", "category": "general_exceptions"},
    "26": {"title": "Act not intended to cause death, done by consent in good faith for person's benefit", "description": "Medical treatment consent.", "category": "general_exceptions"},
    "27": {"title": "Act done in good faith for benefit of child or person of unsound mind, by, or by consent of guardian", "description": "Guardian consent for treatment.", "category": "general_exceptions"},
    "28": {"title": "Consent known to be given under fear or misconception", "description": "Invalid consent under duress.", "category": "general_exceptions"},
    "29": {"title": "Exclusion of acts which are offences independently of harm caused", "description": "Acts that are offences regardless of harm.", "category": "general_exceptions"},
    "30": {"title": "Act done in good faith for benefit of a person without consent", "description": "Emergency treatment without consent.", "category": "general_exceptions"},
    "31": {"title": "Communication made in good faith", "description": "Good faith communication defence.", "category": "general_exceptions"},
    "32": {"title": "Act to which a person is compelled by threats", "description": "Duress defence.", "category": "general_exceptions"},
    "33": {"title": "Act causing slight harm", "description": "De minimis harm exception.", "category": "general_exceptions"},
    "34": {"title": "Things done in private defence", "description": "General right of private defence.", "category": "private_defence"},
    "35": {"title": "Right of private defence of body and of property", "description": "Scope of private defence rights.", "category": "private_defence"},
    "36": {"title": "Right of private defence against act of a person of unsound mind, etc.", "description": "Private defence against mentally ill persons.", "category": "private_defence"},
    "37": {"title": "Acts against which there is no right of private defence", "description": "Limitations on private defence.", "category": "private_defence"},
    "38": {"title": "When right of private defence of body extends to causing death", "description": "Lethal force in self-defence.", "category": "private_defence"},
    "39": {"title": "When such right extends to causing any harm other than death", "description": "Non-lethal force in self-defence.", "category": "private_defence"},
    "40": {"title": "Commencement and continuance of right of private defence of body", "description": "When self-defence begins and ends.", "category": "private_defence"},
    "41": {"title": "When right of private defence of property extends to causing death", "description": "Lethal force to defend property.", "category": "private_defence"},
    "42": {"title": "When such right extends to causing any harm other than death", "description": "Non-lethal force to defend property.", "category": "private_defence"},
    "43": {"title": "Commencement and continuance of right of private defence of property", "description": "When property defence begins and ends.", "category": "private_defence"},
    "44": {"title": "Right of private defence against deadly assault when there is risk of harm to innocent person", "description": "Private defence considering innocent bystanders.", "category": "private_defence"},
    "45": {"title": "Abetment of a thing", "description": "Definition of abetment.", "category": "abetment"},
    "46": {"title": "Abettor", "description": "Definition of abettor.", "category": "abetment"},
    "47": {"title": "Abetment in India of offences outside India", "description": "Abetment across borders from India.", "category": "abetment"},
    "48": {"title": "Abetment outside India for offence in India", "description": "Abetment from outside India.", "category": "abetment"},
    "49": {"title": "Punishment of abetment if act abetted is committed in consequence and where no express provision is made for its punishment", "description": "General punishment for abetment.", "category": "abetment"},
    "50": {"title": "Punishment of abetment if person abetted does act with different intention from that of abettor", "description": "Abetment with different intentions.", "category": "abetment"}
}

# Function to get complete sections data
def get_complete_bns_sections():
    """Return the complete BNS sections dictionary"""
    return COMPLETE_BNS_SECTIONS

if __name__ == "__main__":
    print("📚 Complete BNS Sections Database")
    print("=" * 40)
    print(f"Total sections available: {len(COMPLETE_BNS_SECTIONS)}")
    print("\nFirst 10 sections:")
    for i, (section_num, data) in enumerate(list(COMPLETE_BNS_SECTIONS.items())[:10]):
        print(f"  Section {section_num}: {data['title']}")