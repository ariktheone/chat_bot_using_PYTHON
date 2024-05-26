function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() === '') return;

    appendMessage('user', userInput);
    document.getElementById('user-input').value = '';

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        appendMessage('bot', data.response);
        if (data.response === "I don't know the answer to that. Can you teach me?") {
            const question = userInput;
            const answer = prompt('Please provide the correct answer to tain this model based on your QUESTION:');
            if (answer) {
                trainBot(question, answer);
            }
        }
    });
}

function appendMessage(sender, message) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('p');
    messageElement.textContent = message;
    messageElement.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function trainBot(question, answer) {
    fetch('/train', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: question, answer: answer })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.response);
    });
}

function checkEnter(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function clearChat() {
    document.getElementById('chat-box').innerHTML = '';
}
