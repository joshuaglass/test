const { Room, RoomEvent, DataPacket_Kind } = livekit;

const chatHistory = document.getElementById('chat-history');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const connectBtn = document.getElementById('connect-btn');
const tokenInput = document.getElementById('token-input');
const statusText = document.getElementById('status-text');
const chatContainer = document.getElementById('chat-container');

let room;

function appendMessage(sender, message) {
    const messageElement = document.createElement('p');
    messageElement.innerHTML = `<b>${sender}:</b> ${message}`;
    chatHistory.appendChild(messageElement);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

async function connectToRoom() {
    const token = tokenInput.value;
    if (!token) {
        alert('Please enter a LiveKit token.');
        return;
    }

    room = new Room();

    room.on(RoomEvent.DataReceived, (payload, participant) => {
        const text = new TextDecoder().decode(payload);
        appendMessage('Agent', text);
    });

    try {
        await room.connect(
            "wss://sleep-xtck33ja.livekit.cloud",
            token,
            { autoSubscribe: true }
        );
        statusText.textContent = 'Connected';
        connectBtn.disabled = true;
        tokenInput.disabled = true;
        chatContainer.style.display = 'block';
        chatInput.disabled = false;
        sendBtn.disabled = false;
        appendMessage('System', 'Connected to the room.');
    } catch (error) {
        console.error('Failed to connect to the room:', error);
        statusText.textContent = 'Connection Failed';
    }
}

async function sendMessage() {
    const message = chatInput.value;
    if (!message) return;

    appendMessage('You', message);
    chatInput.value = '';

    const data = new TextEncoder().encode(message);
    await room.localParticipant.publishData(data, DataPacket_Kind.RELIABLE);
}

connectBtn.addEventListener('click', connectToRoom);
sendBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});