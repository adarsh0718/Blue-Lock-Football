# 🤖 SAP-CHAT-BOT: Smart AI Search Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-1.5%20Flash-4285F4?style=for-the-badge&logo=google-gemini&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**A modern, premium AI-powered chatbot assistant for the Blue Lock Football simulation codebase.**  
Featuring web search fallbacks, Gemini API integration, and self-healing configurations.

### 🌐 **[Click Here for the Active Live App Demo](https://noteflow-966730172656.asia-southeast1.run.app/)**

</div>

---

## 🎬 Overview

**SAP-CHAT-BOT** is a standalone, AI-enabled web assistant tailored for exploring, searching, and understanding the **Blue Lock Football** project codebase. It bridges web-based scraping engines, codebase parsing, and LLM text synthesis into a unified chat dashboard interface.

Built using **Flask** (backend) and a sleek **Glassmorphism Dark-Space** themed front-end, it offers multiple search modes to answer queries efficiently, even in offline environments.

---

## 🚀 Active Live Link
You can test the application live in production here:
👉 **[https://noteflow-966730172656.asia-southeast1.run.app/](https://noteflow-966730172656.asia-southeast1.run.app/)**

---

## ✨ Features

### 🔍 1. Multi-Mode Search Engine
Choose how the assistant answers your queries:
*   **Web Search Mode**: Uses a custom-built Mojeek parser to scrape active web results, providing real-time search without an API key.
*   **Codebase Search Mode**: Scans the core Pygame project files (`game.py`, `entities.py`, `physics.py`, `ai.py`) to give direct answers with line numbers and contexts.
*   **AI Mode (Google Gemini)**: Synthesizes retrieved codebase context and web results using `gemini-1.5-flash` for high-quality, smart responses.
*   **All Mode**: Combines web, codebase, and AI analysis for complete comprehensive answers.

### 🛠️ 2. Self-Healing & Validating API Key Management
*   An interactive **Settings Panel** allows users to input their own Google Gemini API keys.
*   A **Key Validator** tests the key against Google's API before saving.
*   **Self-Healing Fallback**: If an active API key is detected to be invalid or expired during chat, the backend automatically clears it from the user's settings and falls back to a offline/local synthesis engine seamlessly.

### 💬 3. Chat Session & Thread Manager
*   Maintains multiple distinct chat threads within a sidebar.
*   Uses `sessionStorage` to store conversation histories locally for enhanced security and privacy (cleared when the browser tab is closed).

### 🎨 4. Premium Responsive Design
*   **Space-Age Glassmorphism HUD**: Translucent dark-mode cards with custom neon borders.
*   **Micro-animations**: Smooth transitions, scale hover states, fading slide-ins, and active pulsing icons.
*   **Markdown Rendering**: Clean text synthesis with markdown lists, bold font, and code syntax highlighting.

---

## 📂 Project Architecture

```
Blue-Lock-Football/
│
├── chatbot/                 # Chatbot Application Core
│   ├── app.py               # Flask backend with /api/chat, /api/validate-key, /api/codebase-files
│   ├── search_engine.py     # Search engine API connector, Mojeek web parser, local greetings library
│   ├── templates/
│   │   └── index.html       # Single-page app layout with sidebar, chats, and settings panels
│   └── static/
│       ├── style.css        # Premium custom stylesheet, responsive layout, glassmorphism card designs
│       └── script.js        # UI state controller, session storage threads, key validation actions
│
├── game.py                  # Blue Lock Football: Core simulation entry (for codebase context)
├── entities.py              # Blue Lock Football: Ball and Player entities (for codebase context)
├── physics.py               # Blue Lock Football: Goal Net Spring Physics (for codebase context)
├── ai.py                    # Blue Lock Football: Goalkeeper and player AI scripts (for codebase context)
│
├── .gitignore               # Configured Git exclusion patterns (ignores cache and virtual envs)
├── GUIDE.md                 # Detailed project overview and learning guide
└── README.md                # Main project guide
```

---

## 🛠️ Local Setup & Installation

### Prerequisites
*   Python 3.8 or higher installed on your machine.
*   A valid Google Gemini API Key (get one from [Google AI Studio](https://aistudio.google.dev/)).

### 1. Clone your repository
```bash
git clone https://github.com/adarsh0718/Blue-Lock-Football.git
cd Blue-Lock-Football
```

### 2. Install required packages
Install Flask and standard packages:
```bash
pip install Flask requests
```

### 3. Run the Flask Web App
```bash
python chatbot/app.py
```

### 4. Access the web app
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser!
