import sys
import re

file_path = 'backend/app/api/simulation.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find the assignment max_rounds = None right after platform assignment
pattern = r"(platform = data\.get\('platform', 'parallel'\).*?)max_rounds = None"
new_content = re.sub(pattern, r"\1max_rounds = data.get('max_rounds')", content, flags=re.DOTALL)

if content != new_content:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Success")
else:
    print("Old code not found!")
