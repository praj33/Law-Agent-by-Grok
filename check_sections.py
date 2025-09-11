import sys
sys.path.append('.')
from complete_ipc_sections_full import create_complete_ipc_database

# Load part 1
data1 = create_complete_ipc_database()
print(f"Sections in part 1: {len(data1)}")

# Load part 2 using exec
with open('complete_ipc_sections.py2', 'r') as f:
    content = f.read()
    exec(content)
    data2 = create_complete_ipc_database_part2()
print(f"Sections in part 2: {len(data2)}")

# Get section numbers
sections1 = set(data1.keys())
sections2 = set(data2.keys())

print(f"First 10 sections in part 1: {sorted(list(sections1))[:10]}")
print(f"Last 10 sections in part 1: {sorted(list(sections1))[-10:]}")
print(f"First 10 sections in part 2: {sorted(list(sections2))[:10]}")
print(f"Last 10 sections in part 2: {sorted(list(sections2))[-10:]}")

# Check for overlap
overlap = sections1.intersection(sections2)
print(f"Overlapping sections: {len(overlap)}")

# Check total unique sections
all_sections = sections1.union(sections2)
print(f"Total unique sections: {len(all_sections)}")