import sys
import re

file_path = 'backend/app/config.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add a helper method to Config class or just fix the variables directly after getting them
# Let's see if we can just append a check after getting the env vars
old_code = """    LLM_API_KEY = os.environ.get('LLM_API_KEY', '').strip() or None
    LLM_BASE_URL = os.environ.get('LLM_BASE_URL', 'https://generativelanguage.googleapis.com/v1beta/openai/').strip()
    LLM_MODEL_NAME = os.environ.get('LLM_MODEL_NAME', 'gemini-2.5-flash').strip()
    LLM_BOOST_API_KEY = os.environ.get('LLM_BOOST_API_KEY', '').strip() or None
    LLM_BOOST_BASE_URL = os.environ.get('LLM_BOOST_BASE_URL', 'https://api.openai.com/v1').strip()
    LLM_BOOST_MODEL_NAME = os.environ.get('LLM_BOOST_MODEL_NAME', 'gpt-4o-mini').strip()"""

new_code = """    LLM_API_KEY = os.environ.get('LLM_API_KEY', '').strip() or None
    LLM_BASE_URL = os.environ.get('LLM_BASE_URL', 'https://generativelanguage.googleapis.com/v1beta/openai/').strip()
    LLM_MODEL_NAME = os.environ.get('LLM_MODEL_NAME', 'gemini-2.5-flash').strip()
    LLM_BOOST_API_KEY = os.environ.get('LLM_BOOST_API_KEY', '').strip() or None
    LLM_BOOST_BASE_URL = os.environ.get('LLM_BOOST_BASE_URL', 'https://api.openai.com/v1').strip()
    LLM_BOOST_MODEL_NAME = os.environ.get('LLM_BOOST_MODEL_NAME', 'gpt-4o-mini').strip()

    # Pastikan URL memiliki protokol http:// atau https://
    if LLM_BASE_URL and not LLM_BASE_URL.startswith(('http://', 'https://')):
        LLM_BASE_URL = f"https://{LLM_BASE_URL}"
    if LLM_BOOST_BASE_URL and not LLM_BOOST_BASE_URL.startswith(('http://', 'https://')):
        LLM_BOOST_BASE_URL = f"https://{LLM_BOOST_BASE_URL}"
"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Success config")
else:
    print("Old code not found!")
