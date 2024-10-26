html_1 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebSocket Chat - User 1</title>
    <style>
        #chat-box {
            width: 100%;
            height: 300px;
            border: 1px solid #ddd;
            overflow-y: scroll;
            padding: 10px;
            background-color: #f9f9f9;
            margin-bottom: 10px;
        }
        #message-input {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
        }
        #send-button {
            padding: 10px 20px;
        }
    </style>
</head>
<body>
    <h2>WebSocket Chat - User 1</h2>
    <div id="chat-box"></div>
    <input type="text" id="message-input" placeholder="Type your message here...">
    <button id="send-button">Send</button>

    <script>
        const userId = 1;  // User ID untuk pengguna 1
        const receiverId = 2;  // ID penerima
        const socket = new WebSocket(`ws://127.0.0.1:8888/ws/${userId}`);
        const chatBox = document.getElementById('chat-box');
        const messageInput = document.getElementById('message-input');
        const sendButton = document.getElementById('send-button');

        socket.onopen = () => {
            console.log("Connected to WebSocket");
        };

        socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            const messageElement = document.createElement('div');
            messageElement.textContent = `User ${message.sender_id}: ${message.content}`;
            chatBox.appendChild(messageElement);
            chatBox.scrollTop = chatBox.scrollHeight;  // Scroll otomatis ke bawah
        };

        socket.onerror = (error) => {
            console.log("WebSocket Error: ", error);
        };

        socket.onclose = () => {
            console.log("WebSocket connection closed");
        };

        sendButton.addEventListener('click', () => {
            const message = {
                receiver_id: receiverId,
                content: messageInput.value,
            };
            socket.send(JSON.stringify(message));
            messageInput.value = '';  // Bersihkan input setelah mengirim
        });

        messageInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                sendButton.click();
            }
        });
    </script>
</body>
</html>
"""

html_2 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebSocket Chat - User 2</title>
    <style>
        #chat-box {
            width: 100%;
            height: 300px;
            border: 1px solid #ddd;
            overflow-y: scroll;
            padding: 10px;
            background-color: #f9f9f9;
            margin-bottom: 10px;
        }
        #message-input {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
        }
        #send-button {
            padding: 10px 20px;
        }
    </style>
</head>
<body>
    <h2>WebSocket Chat - User 2</h2>
    <div id="chat-box"></div>
    <input type="text" id="message-input" placeholder="Type your message here...">
    <button id="send-button">Send</button>

    <script>
        const userId = 2;  // User ID untuk pengguna 2
        const receiverId = 1;  // ID penerima
        const socket = new WebSocket(`ws://127.0.0.1:8888/ws/${userId}`);
        const chatBox = document.getElementById('chat-box');
        const messageInput = document.getElementById('message-input');
        const sendButton = document.getElementById('send-button');

        socket.onopen = () => {
            console.log("Connected to WebSocket");
        };

        socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            const messageElement = document.createElement('div');
            messageElement.textContent = `User ${message.sender_id}: ${message.content}`;
            chatBox.appendChild(messageElement);
            chatBox.scrollTop = chatBox.scrollHeight;  // Scroll otomatis ke bawah
        };

        socket.onerror = (error) => {
            console.log("WebSocket Error: ", error);
        };

        socket.onclose = () => {
            console.log("WebSocket connection closed");
        };

        sendButton.addEventListener('click', () => {
            const message = {
                receiver_id: receiverId,
                content: messageInput.value,
            };
            socket.send(JSON.stringify(message));
            messageInput.value = '';  // Bersihkan input setelah mengirim
        });

        messageInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                sendButton.click();
            }
        });
    </script>
</body>
</html>
"""