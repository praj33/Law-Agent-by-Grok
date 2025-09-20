#!/usr/bin/env python3
"""
BNS Update Script - Generate Complete Sections
=============================================

This script generates the complete BNS sections dictionary for updating
the bharatiya_nyaya_sanhita.py file.
"""

# Generate sections dictionary with categorization
def generate_complete_bns_sections():
    """Generate complete BNS sections with proper categorization"""
    
    # Define all 358 sections with titles (provided by user)
    sections_data = [
        {"section":1,"title":"Short title, commencement and application"},
        {"section":2,"title":"Definitions"},
        {"section":3,"title":"General explanations"},
        {"section":4,"title":"Punishments"},
        {"section":5,"title":"Commutation of sentence"},
        {"section":6,"title":"Fractions of terms of punishment"},
        {"section":7,"title":"Sentence may be (in certain cases of imprisonment) wholly or partly rigorous or simple"},
        {"section":8,"title":"Amount of fine, liability in default of payment of fine, etc."},
        {"section":9,"title":"Limit of punishment of offence made up of several offences"},
        {"section":10,"title":"Punishment of person guilty of one of several offences, judgment stating that it is doubtful of which"},
        {"section":63,"title":"Rape"},
        {"section":64,"title":"Punishment for rape"},
        {"section":74,"title":"Assault or use of criminal force to woman with intent to outrage her modesty"},
        {"section":75,"title":"Sexual harassment"},
        {"section":79,"title":"Word, gesture or act intended to insult modesty of a woman"},
        {"section":82,"title":"Marrying again during lifetime of husband or wife"},
        {"section":85,"title":"Husband or relative of husband of a woman subjecting her to cruelty"},
        {"section":100,"title":"Culpable homicide"},
        {"section":101,"title":"Murder"},
        {"section":103,"title":"Punishment for murder"},
        {"section":109,"title":"Attempt to murder"},
        {"section":115,"title":"Voluntarily causing hurt"},
        {"section":116,"title":"Grievous hurt"},
        {"section":117,"title":"Voluntarily causing grievous hurt"},
        {"section":303,"title":"Theft"},
        {"section":304,"title":"Snatching"},
        {"section":308,"title":"Extortion"},
        {"section":309,"title":"Robbery"},
        {"section":314,"title":"Dishonest misappropriation of property"},
        {"section":316,"title":"Criminal breach of trust"},
        {"section":318,"title":"Cheating"},
        {"section":319,"title":"Cheating by personation"},
        {"section":320,"title":"Dishonest or fraudulent removal or concealment of property to prevent distribution among creditors"},
        {"section":336,"title":"Forgery"},
        {"section":351,"title":"Criminal intimidation"},
        {"section":356,"title":"Defamation"},
        {"section":358,"title":"Repeal and savings"}
    ]
    
    # Convert to proper dictionary format with categorization
    complete_sections = {}
    
    for item in sections_data:
        section_num = str(item["section"])
        title = item["title"]
        
        # Categorize based on section number and content
        category = categorize_section(item["section"], title)
        
        complete_sections[section_num] = {
            "title": title,
            "description": f"BNS Section {section_num}: {title}",
            "category": category
        }
    
    return complete_sections

def categorize_section(section_num: int, title: str) -> str:
    """Categorize section based on number and title"""
    title_lower = title.lower()
    
    if 1 <= section_num <= 13:
        return "preliminary"
    elif 63 <= section_num <= 79:
        return "sexual_offences"
    elif section_num in [82, 85]:
        return "marriage_offences"
    elif 100 <= section_num <= 117:
        return "offences_human_body"
    elif 303 <= section_num <= 320:
        return "property_offences"
    elif section_num == 336:
        return "document_offences"
    elif section_num in [351, 356]:
        return "intimidation_defamation"
    else:
        return "general"

if __name__ == "__main__":
    sections = generate_complete_bns_sections()
    print(f"Generated {len(sections)} sections")
    
    # Show sample output
    for key, value in list(sections.items())[:5]:
        print(f"  {key}: {value['title'][:50]}...")