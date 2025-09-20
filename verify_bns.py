from bharatiya_nyaya_sanhita import create_bns_database

db = create_bns_database()
sections = db.bns_sections

print(f"Total sections: {len(sections)}")
print(f"Expected: 358")
print(f"Complete: {len(sections) == 358}")
print(f"No duplicates: {len(sections) == len(set(sections.keys()))}")
print(f"First: Section {min(sections.keys())} - {sections[min(sections.keys())]['title']}")
print(f"Last: Section {max(sections.keys())} - {sections[max(sections.keys())]['title']}")