import os
import re

files = [
    'backend/scripts/run_twitter_simulation.py',
    'backend/scripts/run_reddit_simulation.py'
]

for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # We find os.environ["OPENAI_API_BASE_URL"] = llm_base_url
        new_content = re.sub(
            r'(if llm_base_url:\s+)(os\.environ\["OPENAI_API_BASE_URL"\] = llm_base_url)',
            r'\1if not llm_base_url.startswith(("http://", "https://")):\n            llm_base_url = f"https://{llm_base_url}"\n        \2',
            content
        )
        
        if content != new_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed {file_path}")
        else:
            print(f"Nothing changed in {file_path}")
