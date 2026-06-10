import os
import requests
import json

url = 'https://generativelanguage.googleapis.com/v1beta/openai/chat/completions'
headers = {
    'Authorization': 'Bearer AIzaSyBItq4UkWDEVU8qPT41-SxmHqm-BMSfMDs',
    'Content-Type': 'application/json'
}
payload = {
    'model': 'gemini-2.5-flash',
    'response_format': {'type': 'json_object'},
    'messages': [
        {'role': 'system', 'content': 'You are a helpful assistant. Output a JSON object with a single key "numbers" containing an array of numbers from 1 to 200.'},
        {'role': 'user', 'content': 'Generate the JSON.'}
    ],
    'max_tokens': 4096
}
response = requests.post(url, headers=headers, json=payload)
print(response.status_code)
content = response.json()
print('Finish reason:', content.get('choices', [{}])[0].get('finish_reason'))
