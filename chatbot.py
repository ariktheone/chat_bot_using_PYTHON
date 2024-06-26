import os
import json
import difflib
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

DATA_FILE = 'data/training_data.json'

# Load initial training data
if not os.path.exists(DATA_FILE):
    initial_data = {"conversations": []}
    with open(DATA_FILE, 'w') as f:
        json.dump(initial_data, f, indent=4)

with open(DATA_FILE) as f:
    data = json.load(f)

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
        return jsonify({'response': "I don't know the answer to that. Can you teach me?"})

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
