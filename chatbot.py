from flask import Flask, request, jsonify, render_template
import json
import os
import difflib

app = Flask(__name__)

DATA_FILE = 'data/training_data.json'

# Load initial training data
if not os.path.exists(DATA_FILE):
    initial_data = {"conversations": []}
    with open(DATA_FILE, 'w') as f:
        json.dump(initial_data, f, indent=4)

with open(DATA_FILE) as f:
    data = json.load(f)

# Function to find a response
def find_response(question):
    closest_matches = difflib.get_close_matches(question.lower(), [q.lower() for entry in data['conversations'] for q in entry['questions']])
    if closest_matches:
        for entry in data['conversations']:
            if closest_matches[0] in [q.lower() for q in entry['questions']]:
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
    app.run(debug=True)
