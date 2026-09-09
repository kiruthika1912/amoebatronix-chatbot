// =====================================================
// ENTERPRISE AI ASSISTANT
// FRONTEND → FASTAPI → RAG → KNOWLEDGE BASE
// =====================================================


const projectSelect = document.getElementById("projectSelect");

const questionInput = document.getElementById("questionInput");

const sendButton = document.getElementById("sendButton");

const chatMessages = document.getElementById("chatMessages");

const quickQuestions =
    document.querySelectorAll(".quick-question");

const menuItems =
    document.querySelectorAll(".menu-item");


// FastAPI backend URL (works whether hosted together or separately)
const API_URL = window.location.origin.startsWith("http")
    ? `${window.location.origin}/ask`
    : "http://127.0.0.1:8000/ask";


// =====================================================
// PROJECT SELECT
// =====================================================

projectSelect.addEventListener("change", function () {

    console.log(
        "Selected project:",
        projectSelect.value
    );

});


// =====================================================
// SEND BUTTON
// =====================================================

sendButton.addEventListener(
    "click",
    askQuestion
);


// =====================================================
// ENTER KEY
// =====================================================

questionInput.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {

            event.preventDefault();

            askQuestion();

        }

    }
);


// =====================================================
// QUICK QUESTIONS
// =====================================================

quickQuestions.forEach(function (button) {

    button.addEventListener(
        "click",
        function () {

            questionInput.value =
                button.textContent.trim();

            questionInput.focus();

            askQuestion();

        }
    );

});


// =====================================================
// ASK QUESTION
// =====================================================

async function askQuestion() {

    const question =
        questionInput.value.trim();


    // Don't send empty question
    if (!question) {

        questionInput.focus();

        return;

    }


    // Remove welcome message
    const emptyChat =
        document.querySelector(".empty-chat");

    if (emptyChat) {

        emptyChat.remove();

    }


    // Display user question
    addMessage(
        "You",
        question,
        "user-message"
    );


    // Clear input
    questionInput.value = "";


    // Disable button
    sendButton.disabled = true;

    sendButton.innerHTML =
        "⏳ Sending...";


    // Loading message
    const loadingId =
        "loading-" + Date.now();


    chatMessages.innerHTML += `

        <div
            class="chat-message ai-message loading-message"
            id="${loadingId}"
        >

            <div class="message-label">
                AI Assistant
            </div>

            Searching the knowledge base...

        </div>

    `;


    scrollToBottom();


    try {

        console.log(
            "Sending request to:",
            API_URL
        );

        console.log(
            "Question:",
            question
        );


        // Send request to FastAPI
        const response =
            await fetch(API_URL, {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"

                },

                body: JSON.stringify({

                    question: question

                })

            });


        // Check HTTP response
        if (!response.ok) {

            throw new Error(
                "Server returned status " +
                response.status
            );

        }


        // Convert response to JSON
        const data =
            await response.json();


        console.log(
            "Backend response:",
            data
        );


        // Remove loading message
        const loadingMessage =
            document.getElementById(
                loadingId
            );

        if (loadingMessage) {

            loadingMessage.remove();

        }


        // Display AI response
        displayBackendResponse(data);


    } catch (error) {

        console.error(
            "API Error:",
            error
        );


        // Remove loading message
        const loadingMessage =
            document.getElementById(
                loadingId
            );

        if (loadingMessage) {

            loadingMessage.remove();

        }


        addMessage(
            "AI Assistant",
            "Unable to connect to the FastAPI backend. Please make sure the server is running on http://127.0.0.1:8000.",
            "ai-message"
        );

    }


    // Enable button
    sendButton.disabled = false;

    sendButton.innerHTML =
        "<span>➤</span> Send";


    // Put cursor back in input
    questionInput.focus();


    scrollToBottom();

}


// =====================================================
// ADD MESSAGE
// =====================================================

function addMessage(
    sender,
    message,
    className
) {

    const messageElement =
        document.createElement("div");


    messageElement.className =
        "chat-message " +
        className;


    const label =
        document.createElement("div");


    label.className =
        "message-label";


    label.textContent =
        sender;


    const content =
        document.createElement("div");


    content.textContent =
        message;


    messageElement.appendChild(label);

    messageElement.appendChild(content);


    chatMessages.appendChild(
        messageElement
    );


    scrollToBottom();

}


// =====================================================
// DISPLAY BACKEND RESPONSE
// =====================================================

function displayBackendResponse(data) {

    let answer = "";


    // Current backend format
    if (
        data.results &&
        Array.isArray(data.results)
    ) {

        data.results.forEach(
            function (result, index) {

                if (result.text) {

                    answer +=
                        result.text;

                } else {

                    answer +=
                        JSON.stringify(
                            result
                        );

                }


                if (
                    index <
                    data.results.length - 1
                ) {

                    answer +=
                        "\n\n";

                }

            }
        );

    }


    // Other possible formats
    else if (data.answer) {

        answer = data.answer;

    }

    else if (data.response) {

        answer = data.response;

    }

    else if (data.text) {

        answer = data.text;

    }

    else {

        answer =
            JSON.stringify(
                data,
                null,
                2
            );

    }


    addMessage(
        "AI Assistant",
        answer,
        "ai-message"
    );

}


// =====================================================
// SCROLL CHAT
// =====================================================

function scrollToBottom() {

    chatMessages.scrollTop =
        chatMessages.scrollHeight;

}


// =====================================================
// SIDEBAR MENU
// =====================================================

menuItems.forEach(function (item) {

    item.addEventListener(
        "click",
        function () {

            menuItems.forEach(
                function (button) {

                    button.classList.remove(
                        "active"
                    );

                }
            );


            item.classList.add(
                "active"
            );

        }
    );

});


// =====================================================
// PAGE LOADED
// =====================================================

console.log(
    "Enterprise AI Assistant frontend loaded."
);

console.log(
    "FastAPI API:",
    API_URL
);


// Automatically focus the question box
questionInput.focus();