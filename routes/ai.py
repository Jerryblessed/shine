

from flask import Flask, render_template, render_template_string, request, Response, stream_with_context, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import io
import os
import google.generativeai as genai


# Import the necessary modules and functions
from modules import (
    Log,  # A class for logging messages
    Blueprint,  # A class for creating Flask blueprints
    render_template,  # A function for rendering Jinja templates
)


from werkzeug.utils import secure_filename
from PIL import Image
import io
import os
import google.generativeai as genai


# Create a blueprint for the search bar route
AIBlueprint = Blueprint(
    "ai", __name__
)  # Pass the name of the blueprint and the current module name as arguments



# Configuration
GOOGLE_API_KEY = 'AIzaSyDDEdN89laTbTO8JEHJULde5fPm-h1GRGY'
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

chat_session = model.start_chat(history=[])
next_message = ""
next_image = None

def allowed_file(filename):
    """Returns if a filename is supported via its extension"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@AIBlueprint.route("/upload", methods=["POST"])
def upload_file():
    """Takes in a file, checks if it is valid, and saves it for the next request to the API"""
    global next_image

    if "file" not in request.files:
        return jsonify(success=False, message="No file part")

    file = request.files["file"]

    if file.filename == "":
        return jsonify(success=False, message="No selected file")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        try:
            # Read the file stream into a BytesIO object
            file_stream = io.BytesIO(file.read())
            file_stream.seek(0)
            next_image = Image.open(file_stream)
            return jsonify(
                success=True,
                message="File uploaded successfully and added to the conversation",
                filename=filename,
            )
        except Exception as e:
            return jsonify(success=False, message=f"Error processing file: {str(e)}")
    return jsonify(success=False, message="File type not allowed")

@AIBlueprint.route("/ai", methods=["GET"])
def ai():
    """Renders the main homepage for the app"""
    return render_template_string('''
                           
<!doctype html>
<html>
  <head>
    <title>Gemini API Chat</title>
    <link
      rel="stylesheet"
      href="{{ url_for('static', filename='css/main.css') }}"
    />
  </head>
  <body>
    <div id="upload-banner">
      <!-- Success message will be inserted here -->
    </div>
    <div class="main-content">
      <div class="file-upload-section">
        <div class="header">
          <img
            src="{{ url_for('static', filename='css/icon.png') }}"
            alt="Google Gemini Logo"
          />
          <div class="demo-text">AI Chat...</div>
<br/>

          <a href="/" class="block">
          <div class="demo-text">  Go back home</div>
        </a>

      </div>
        <div id="filesList">
          <p id="filesPlaceholder" class="hidden">Files</p>
        </div>
        <div class="centered-text">
          <svg
            width="39"
            height="38"
            viewBox="0 0 39 38"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fill-rule="evenodd"
              clip-rule="evenodd"
              d="M30.5641 4.04786C29.9974 4.00156 29.2529 4.00001 28.0998 4.00001H17.5002C17.0998 6 16.6975 7.82282 16.2803 9.70819C16.0173 10.8991 15.7862 11.9461 15.2348 12.828C14.7521 13.6002 14.0999 14.2524 13.3277 14.7351C12.4458 15.2864 11.3989 15.5176 10.2079 15.7805C10.1253 15.7988 10.0419 15.8172 9.95788 15.8359L4.93362 16.9524C4.78815 16.9847 4.64286 17.0003 4.49976 17.0004V27.6C4.49976 28.7531 4.50131 29.4977 4.54761 30.0643C4.59201 30.6077 4.66736 30.8091 4.71775 30.908C4.90949 31.2843 5.21545 31.5903 5.59178 31.782C5.69067 31.8324 5.89211 31.9078 6.43543 31.9521C7.00211 31.9984 7.74665 32 8.89976 32H14.4998C15.6043 32 16.4998 32.8954 16.4998 34C16.4998 35.1046 15.6043 36 14.4998 36H8.82263C7.76835 36 6.85884 36.0001 6.1097 35.9389C5.31901 35.8743 4.53258 35.7316 3.77582 35.346C2.64684 34.7708 1.72896 33.8529 1.15372 32.7239C0.768132 31.9672 0.6255 31.1807 0.560898 30.3901C0.499691 29.6409 0.499722 28.7314 0.499758 27.6771L0.499759 16C0.499759 11.8495 2.55485 7.86649 5.46055 4.96079C8.36624 2.0551 12.3493 7.44227e-06 16.4998 7.44227e-06L28.1768 5.53492e-06C29.2311 -3.02279e-05 30.1407 -6.12214e-05 30.8898 0.0611463C31.6805 0.125748 32.4669 0.26838 33.2237 0.653969C34.3527 1.22921 35.2706 2.14709 35.8458 3.27606C36.2314 4.03282 36.374 4.81926 36.4386 5.60995C36.4998 6.35908 36.4998 7.2686 36.4998 8.32287V14C36.4998 15.1046 35.6043 16 34.4998 16C33.3952 16 32.4998 15.1046 32.4998 14V8.40001C32.4998 7.2469 32.4982 6.50235 32.4519 5.93568C32.4075 5.39235 32.3322 5.19091 32.2818 5.09203C32.09 4.7157 31.7841 4.40974 31.4077 4.21799C31.3089 4.16761 31.1074 4.09225 30.5641 4.04786ZM5.06003 12.8267L9.09016 11.9311C10.677 11.5785 10.9859 11.4818 11.2074 11.3433C11.4648 11.1824 11.6822 10.965 11.8431 10.7076C11.9815 10.4862 12.0783 10.1772 12.4309 8.5904L13.3265 4.56028C11.52 5.18578 9.77023 6.30796 8.28897 7.78922C6.80771 9.27048 5.68553 11.0203 5.06003 12.8267ZM28.4998 24C28.4998 22.8954 29.3952 22 30.4998 22C31.6043 22 32.4998 22.8954 32.4998 24V28H36.4998C37.6043 28 38.4998 28.8954 38.4998 30C38.4998 31.1046 37.6043 32 36.4998 32H32.4998V36C32.4998 37.1046 31.6043 38 30.4998 38C29.3952 38 28.4998 37.1046 28.4998 36V32H24.4998C23.3952 32 22.4998 31.1046 22.4998 30C22.4998 28.8954 23.3952 28 24.4998 28H28.4998V24Z"
              fill="#6E6E80"
            />
          </svg>
          <p>Attach files to make them available to Gemini</p>
        </div>
        <input
          type="file"
          id="file-upload"
          name="file-upload"
          class="file-upload-input"
          multiple
        />
        <label for="file-upload" class="file-upload-btn">Attach files</label>
      </div>
      <div class="chat-container">
        <div class="messages">
          {% for message in chat_history %}
          <div
            class="message-role {{ 'user' if message.role == 'user' else '' }}"
          >
            {{ message.role.capitalize() }}
          </div>
          <div
            class="{{ 'user-message' if message.role == 'user' else 'assistant-message' }}"
          >
            {{ message.content }}
          </div>
          {% endfor %}
        </div>
        <div class="message-input-container">
          <form action="/chat" method="post">
           <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
            <textarea
              name="message"
              placeholder="Chat with Gemini"
              required
            ></textarea>
            <div class="button-group">
              <button type="submit" id="send-btn">&#x2191;</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <script>
      document
        .querySelector("form")
        .addEventListener("submit", function (event) {
          event.preventDefault();
          const messageInput = document.querySelector(
            'textarea[name="message"]'
          );
          const message = messageInput.value.trim();
          const chatContainer = document.querySelector(".messages");

          // Append the user's message to the chat container
          if (message) {
            const roleDiv = document.createElement("div");
            roleDiv.classList.add("message-role");
            roleDiv.classList.add("user");

            roleDiv.textContent = "User";
            chatContainer.appendChild(roleDiv);

            const userMessageDiv = document.createElement("div");
            userMessageDiv.classList.add("user-message");
            userMessageDiv.textContent = message;
            chatContainer.appendChild(userMessageDiv);
          }

          // Clear the message input
          messageInput.value = "";

          // Send the user's message to the server using AJAX
          fetch("/chat", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: message }),
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.success) {
                const roleDiv = document.createElement("div");
                roleDiv.classList.add("message-role");
                roleDiv.classList.add("assistant");

                roleDiv.textContent = "Model";
                chatContainer.appendChild(roleDiv);

                // Prepare the model message container
                const assistantMessageDiv = document.createElement("div");
                assistantMessageDiv.classList.add("assistant-message");
                chatContainer.appendChild(assistantMessageDiv);

                // Open a connection to receive streamed responses
                const eventSource = new EventSource("/stream");
                eventSource.onmessage = function (event) {
                  const currentText = assistantMessageDiv.textContent;
                  const newText = event.data;
                  const lastChar = currentText.slice(-1);

                  // Check if we need to add a space (streamed chunks might be missing it)
                  if (/[.,!?]/.test(lastChar) && newText.charAt(0) !== " ") {
                    assistantMessageDiv.textContent += " " + newText;
                  } else {
                    assistantMessageDiv.textContent += newText;
                  }

                  // Scroll to the bottom of the chat container
                  chatContainer.scrollTop = chatContainer.scrollHeight;
                };
                eventSource.onerror = function () {
                  eventSource.close();
                };
              }
            });
        });
      
      // Add event listener for file uploads
      document
        .getElementById("file-upload")
        .addEventListener("change", function (event) {
          const file = event.target.files[0];
          if (!file) {
            return;
          }
          const formData = new FormData();
          formData.append("file", file);

          fetch("/upload", {
            method: "POST",
            body: formData,
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.success) {
                // Update and show the banner
                const banner = document.getElementById("upload-banner");
                banner.textContent = data.message;
                banner.style.display = "block";

                // Hide the banner after 3 seconds
                setTimeout(() => {
                  banner.style.display = "none";
                }, 3000);

                fetch("/get_files")
                  .then((response) => response.json())
                  .then((data) => {
                    populateFiles(data.assistant_files);
                  });
              } else {
                console.error("Upload failed:", data.message);
                // Update and show the banner
                const banner = document.getElementById("upload-banner");
                banner.textContent = data.message;
                banner.style.display = "block";
                banner.style.color = "red";

                // Hide the banner after 3 seconds
                setTimeout(() => {
                  banner.style.display = "none";
                }, 3500);
              }
            })
            .catch((error) => {
              console.error("Error uploading file:", error);
            });
        });
    </script>
  </body>
</html>



                           
                           ''', chat_history=chat_session.history)

@AIBlueprint.route("/chat", methods=["POST"])
def chat():
    """Takes in the message the user wants to send to the Gemini API, saves it"""
    global next_message
    next_message = request.json.get("message", "")
    return jsonify(success=True)

@AIBlueprint.route("/stream", methods=["GET"])
def stream():
    """Streams the response from the server for both multi-modal and plain text requests"""
    def generate():
        global next_message
        global next_image
        assistant_response_content = ""

        try:
            if next_image:
                # This only works with `gemini-1.5-pro-latest`
                response = chat_session.send_message([next_message, next_image], stream=True)
                next_image = None
            else:
                response = chat_session.send_message(next_message, stream=True)
                next_message = ""
            
            for chunk in response:
                assistant_response_content += chunk.text
                yield f"data: {chunk.text}\n\n"
        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream")

