import os
import json
import difflib
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

DATA_FILE = 'data/training_data.json'

# Load initial training data
if not os.path.exists(DATA_FILE):
    initial_data = {"conversations": []}
    with open(DATA_FILE, 'w') as f:
        json.dump(initial_data, f, indent=4)

with open(DATA_FILE) as f:
    data = json.load(f)

# Configure Google Gemini API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Function to find a response with a similarity threshold
def find_response(question, threshold=0.8):
    closest_matches = difflib.get_close_matches(question.lower(), [q.lower() for entry in data['conversations'] for q in entry['questions']], n=1)
    if closest_matches:
        best_match = closest_matches[0]
        similarity_ratio = difflib.SequenceMatcher(None, question.lower(), best_match).ratio()
        if similarity_ratio >= threshold:
            for entry in data['conversations']:
                if best_match in [q.lower() for q in entry['questions']]:
                    return entry['answer']
    return None

# Route to handle chat
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = find_response(user_input)
    if response:
        return jsonify({'response': response})
    else:
        # Use Google Gemini API for response
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )

        chat_session = model.start_chat(
            history=[user_input]
        )

        gemini_response = chat_session.send_message(user_input)

        return jsonify({'response': gemini_response.text})

# Route to train the bot
@app.route('/train', methods=['POST'])
def train():
    question = request.json.get('question').lower()
    answer = request.json.get('answer')

    # Check if the question already exists
    for entry in data['conversations']:
        if any(question in q for q in entry['questions']):
            entry['answer'] = answer
            break
    else:
        # If it does not exist, add a new entry
        data['conversations'].append({
            'questions': [question],
            'answer': answer
        })

    # Save the updated training data
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify({'response': 'Thank you for teaching me!'})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
