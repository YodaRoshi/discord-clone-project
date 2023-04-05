console.log('Room.js loaded')


const roomName = JSON.parse(document.getElementById('json-roomname').textContent);
const userName = JSON.parse(document.getElementById('json-username').textContent);
const isSuperuser = JSON.parse(document.getElementById('json-superuser').textContent);

const chatSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/' +
    roomName +
    '/'
);
// 
function scrollToBottom() {
    console.log('Scrolling to bottom')
    const objDiv = document.querySelector('#threads-scroll');
    objDiv.scrollTop = objDiv.scrollHeight;

};


chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    if (data.body) {
        createThread(data);
        scrollToBottom();
    } else {
        console.log('The message was empty!')
    }
};
document.querySelector('#room-message-input').focus();


document.querySelector('#room-message-input').onkeyup = function (e) {
    e.preventDefault();
    if (e.keyCode === 13) {
        e.preventDefault();
        console.log('Submitting')
        const messageInputDom = document.querySelector('#room-message-input');
        const body = messageInputDom.value;

        chatSocket.send(JSON.stringify({
            'body': body,
            'username': userName,
            'room': roomName
        }));

        messageInputDom.value = '';

        return false;
    }
};


scrollToBottom()
chatSocket.onclose = function (e) {
    console.error('The socket closed unexpectedly');
};

function createThread(data) {
    // {% for message in room_messages %}
    let thread = `<div class="thread" id="thread">
                    <div class="thread__top">
                    <div class="thread__author">`
    // {% if message.user.is_active %}
    if (data.is_active) {
        thread += `<a href="/profile/${data.user_id}" class="thread__authorInfo">`
    } else {
        thread += `<a class = "thread__authorInfo disabled">`
    }

    thread += `<div class = "avatar avatar--small" >
                <img src="${data.avatar}"/>
                </div>
                <span>@${data.username}</span>
                </a>
                <span class="thread__date">${data.created} ago</span></div>`
    if (isSuperuser || data.username == userName) {
        thread += `<a href="/delete-message/${data.message_id}">
                    <div class="thread__delete">
                        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
                        <title>remove</title>
            <path
              d="M27.314 6.019l-1.333-1.333-9.98 9.981-9.981-9.981-1.333 1.333 9.981 9.981-9.981 9.98 1.333 1.333 9.981-9.98 9.98 9.98 1.333-1.333-9.98-9.98 9.98-9.981z">
            </path>
          </svg>
        </div>
      </a>`
    }
    // endif
    thread += `</div><div class="thread__details">${data.body}</div></div>`



    document.querySelector('#threads-scroll').innerHTML += thread;
}