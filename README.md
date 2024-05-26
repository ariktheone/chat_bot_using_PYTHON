# Advanced Chatbot

This is an advanced chatbot application built with Flask, HTML, CSS, and JavaScript. The bot is trained using a JSON file and can learn new responses dynamically from user input.

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/chatbot.git
    cd chatbot
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install flask
    ```

4. Run the Flask application:
    ```bash
    python chatbot.py
    ```

5. Open a web browser and go to `http://127.0.0.1:5000`.

## Usage

- Type a message in the input box and press "Send".
- If the bot doesn't know the answer, it will ask you to teach it.
- Provide the correct answer when prompted, and the bot will learn from it.

## Files

- `chatbot.py`: The main Flask application.
- `templates/index.html`: The HTML file for the frontend.
- `static/css/styles.css`: The CSS file for styling.
- `static/js/script.js`: The JavaScript file for client-side logic.
- `data/training_data.json`: The initial training data for the chatbot.
