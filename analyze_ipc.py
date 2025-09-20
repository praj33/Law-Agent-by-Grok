import sys
sys.path.append('.')

# Load part 1
from complete_ipc_sections_full import create_complete_ipc_database
data1 = create_complete_ipc_database()
print(f"Sections in part 1: {len(data1)}")

# Load part 2
with open('complete_ipc_sections.py2', 'r') as f:
    content = f.read()
    exec(content)
    data2 = create_complete_ipc_database_part2()
print(f"Sections in part 2: {len(data2)}")

# Combine all sections
all_sections = set(data1.keys()).union(set(data2.keys()))
print(f"Total unique sections: {len(all_sections)}")

# Check numeric sections
digit_sections = [s for s in all_sections if s.isdigit()]
numeric_sections = sorted([int(s) for s in digit_sections])
print(f"Numeric sections: {len(numeric_sections)}")
print(f"Range: {numeric_sections[0]} to {numeric_sections[-1]}")

# Check for gaps
missing = []
for i in range(1, 512):
    if str(i) not in all_sections:
        # Check if there are alphanumeric sections like 376A that would cover this
        covered = False
        for section in all_sections:
            if str(i) in section and section != str(i):
                covered = True
                break
        if not covered:
            missing.append(i)

print(f"Missing numeric sections: {missing}")

# Check what alphanumeric sections we have
alpha_sections = [s for s in all_sections if not s.isdigit()]
print(f"Alphanumeric sections: {len(alpha_sections)}")
print(f"Examples: {sorted(alpha_sections)[:20]}")