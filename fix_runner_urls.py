import os

files = [
    'backend/scripts/run_parallel_simulation.py',
    'backend/scripts/run_twitter_simulation.py',
    'backend/scripts/run_reddit_simulation.py'
]

for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the assignment to os.environ["OPENAI_API_BASE_URL"] with a check
        old_code = 'if llm_base_url:\n        os.environ["OPENAI_API_BASE_URL"] = llm_base_url'
        new_code = '''if llm_base_url:
        # Auto-append https:// if missing
        if not llm_base_url.startswith(('http://', 'https://')):
            llm_base_url = f"https://{llm_base_url}"
        os.environ["OPENAI_API_BASE_URL"] = llm_base_url'''
        
        if old_code in content:
            content = content.replace(old_code, new_code)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed {file_path}")
        else:
            print(f"Old code not found in {file_path}")
    else:
        print(f"File not found {file_path}")
