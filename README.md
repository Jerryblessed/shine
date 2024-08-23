# ✨ Shine

Shine is an educational platform that allows users to post and retrieve content for studies. The platform supports various file formats, including images, documents, and others. The architecture of Shine integrates TiDB, SQLite, and AI search to enable efficient content management and retrieval.

## 🛠 Architectural Diagram

![Shine Architectural Diagram](https://i.ibb.co/LvZR3jC/shine-architectural-diagram.png)

## 🌟 Features

- **📁 File Upload and Retrieval:** Users can upload various file formats, which are transformed into vector embeddings for storage.
- **🔍 AI-Powered Search:** The platform supports advanced search functionalities using AI, allowing users to query and retrieve content effectively.
- **🔢 Vector Embeddings:** Content is stored as vector embeddings, enabling efficient similarity searches through top-k nearest neighbor algorithms.
- **💾 Database Integration:** Shine uses TiDB for vector embedding management and SQLite for interaction with user queries.

- **Admin Panel**
- **Comment**
  - Comment Delete
- **Custom Profile Picture**
- **Dashboard Page**
- **Dark/Light Themes**
- **Database Checker**
- **Debug Messages**
- **Docker**
- **Google reCAPTCHA v3**
- **Logging**
- **Multi Language Support**
- **Password**
  - Password Change
  - Password Reset
- **Post**
  - Post Banner Photos
  - Post Categories
  - Post Creation
  - Post Delete
  - Post Edit
  - Post Views
- **Responsive Design w/TailwindCSS**
- **Search Bar**
- **Summer Note Editor**
- **Testing w/PlayWright**
- **Time Zone Awareness**
- **User**
  - User Delete
  - User Login
  - User Log Out
  - User Name Change
  - User Page
  - User Points
  - User Profile Pictures
  - User Settings Page
  - User Sign Up
  - User Verification

## 📦 Requirements for flask app

- Flask
- Passlib
- WTForms
- Requests
- Flask-WTF
- Playwright
- Pipenv
- Python 3.10 or newer
- google.generativeai
- peewee
- tidb-vector

## 📦 Requirements for next.js app
For the next.js app's requirement, please visit [shine's chat](https://github.com/Jerryblessed/shine/blob/main/light_chat/package.json) project requirement page

## 🧑🏻‍💻 Languages

- Python
- HTML | Jinja
- CSS
- JavaScript
- TypeScript

## 📚 Technologies

### ⚙️ Backend

- SQLite3
- Passlib
- Flask
- WTForms
- Flask_WTF
- Requests
- Playwright
- node.js

### 🔮 Frontend

- jQuery
- TailwindCSS
- Tabler Icons
- Summer Note Editor
- JavaScript
- TypeScript

### 🔨 Tools

- Black formatter
- Prettier formatter
- VSCode editor
- Docker
- Pipenv
- Git

## 🚦 Running the Project

1. **Download source code from GitHub** 💾
   ```bash
   https://github.com/Jerryblessed/shine.git   
For shine flask app (main app), run the following commands

-   cd ./shine
-   pip install requirements.txt
-   python run app.py


 For shine Generative Assistance, run the following commands
-   cd ./light_chat
-   npm i
-   npm run dev

## Special Thanks! 🎉

We would like to extend a heartfelt thanks to [DogukanUrker](https://github.com/DogukanUrker) for the incredible work on the [FlaskBlog](https://github.com/DogukanUrker/flaskBlog) project!


## 📜 License

```text
MIT License

Copyright (c) 2024 Shine Educational Platform

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



