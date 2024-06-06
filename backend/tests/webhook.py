import json
import urllib.request

def call_webhook(url, data):
    headers = {
        'Content-Type': 'application/json',
    }
    json_data_bytes = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=json_data_bytes, headers=headers)
    try:
        response = urllib.request.urlopen(req)
        print("Webhook response:", response.read().decode())
    except Exception as e:
        print(f"General error: {e}")

data = {"challenge": "tt", "category": "tt", "team": "fdzfzadf", "user": "aaa", "solve_id": 9, "scoreboard": [{"team": "r", "score": 10091.0, "num_solves": 3}, {"team": "y", "score": 10091.0, "num_solves": 3}, {"team": "a", "score": 10091.0, "num_solves": 3}, {"team": "z", "score": 10091.0, "num_solves": 3}, {"team": "u", "score": 10091.0, "num_solves": 3}, {"team": "q", "score": 10091.0, "num_solves": 3}, {"team": "aear", "score": 10091.0, "num_solves": 3}, {"team": "s", "score": 10091.0, "num_solves": 3}, {"team": "t", "score": 10090.0, "num_solves": 2}, {"team": "e", "score": 10090.0, "num_solves": 2}, {"team": "fdzfzadf", "score": 1.0, "num_solves": 1}]}
call_webhook('http://localhost:3000/webhook', data)