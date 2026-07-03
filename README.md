# ⚽ Championship Football 1978 — Blue Lock Edition

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-00B140?style=for-the-badge&logo=pygame&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-1.5%20Flash-4285F4?style=for-the-badge&logo=google-gemini&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-gold?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**A retro-styled, physics-driven 2D football simulation built with Python & Pygame, integrated with an AI-powered Codebase Search Chatbot.**  
Inspired by the raw intensity of *Blue Lock* — a vintage 5v5 experience dripping in 1970s football aesthetics combined with modern search tech.

### 🌐 [▶ Open Live Chatbot App](https://sraadaly-966730172656.asia-southeast1.run.app/) &nbsp;&nbsp; [📂 View Code](https://github.com/adarsh0718/Blue-Lock-Football)

</div>

---

## 🎬 Overview

**Championship Football 1978** is a hybrid project featuring:
1.  **Retro Game Simulation**: A fully-featured, physics-driven 2D football simulation written in Python using Pygame. It captures the look and feel of vintage 1970s football — complete with muted olive-green grass stripes, CRT scanline overlays, leather ball seams, and sepia-toned stadium lighting.
2.  **SAP-CHAT-BOT (Smart AI Search Assistant)**: An interactive AI-powered assistant deployed via Flask and Google Gemini to help explore the codebase, answer game logic questions, and perform web searches.

The game features **two modes** — play solo against AI-controlled opponents, or go head-to-head in local **2-player** mode. With 4 distinct weather conditions, spring-physics goal nets, stamina management, charge-shot mechanics, and a role-based AI engine, every match feels alive and dynamic.

---

## 🛠️ How I Created This

This project was built from scratch to combine vintage game engineering with modern web architecture:

### 1. Game Mechanics & Simulation (Pygame & Vector Math)
*   **Vector Kinematics**: Used `pygame.math.Vector2` to handle player motion, acceleration, friction, and ball trajectory. The ball handles full 3D coordinates ($X, Y, Z$) to allow lob passes and high shots, factoring in gravity ($g$) and wind resistance.
*   **CRT Television Rendering**: Created custom pixel shader filters in Pygame to render vintage horizontal lines and a slight color bleed to mimic cathode-ray tube monitors.
*   **Hooke's Law Net Physics**: Implemented spring-mass systems to calculate goal net elastic deformation:
    \[F = -k \cdot x - c \cdot v\]
    where $k$ represents spring stiffness, $c$ is the damping coefficient, and $x$ is displacement.

### 2. Smart AI Decision Engine (`ai.py`)
*   Designed a state-machine AI controller with role allocations (Goalkeeper, Defender, Midfielder, Attacker). 
*   **Goalkeeper AI**: Automatically calculates ball interception vectors and restricts movements to the box.
*   **Offensive/Defensive States**: AI players switch behavior based on ball possession, utilizing charge shots, dodging tackles, and executing smart pass selection.

### 3. AI Chatbot Assistant (Flask & Google Gemini API)
*   **Flask Web Server**: Created REST endpoints to validate keys and coordinate search engines.
*   **Search Hybrid Engine**: Created a custom Mojeek scraping parser for live search results. If the user provides a Gemini API key, the chatbot feeds local files and web search results into `gemini-1.5-flash` to synthesize accurate code answers.
*   **Self-Healing State Management**: Designed JS/Flask interactions to auto-clear invalid settings in `localStorage` and fall back to local offline synthesis on authentication errors.

---

## ✨ Features

### 🎮 Pygame Football Simulation
*   **Vintage Styling**: Olive-green grass panels, chalk-cream lines, custom sepia HUD, and sprint ghost trails.
*   **Weather Engine**: sunny, evening, rain (with water drop splash particles and slippery grass physics), and night modes.
*   **Player Attributes**: Stamina limits, player switching logic, auto-aimed passing, and power-charged shots.
*   **Visual Flair**: Exploding particle confetti on goals, camera shake, and rotating 3D leather ball seams.

### 🤖 Smart Chatbot Assistant
*   **Interactive Search**: Instantly queries Web, local Codebase files (`game.py`, `entities.py`, etc.), or AI models.
*   **Self-Healing Keys**: Automatic credentials clearance and fail-safes.
*   **Premium Web UI**: Responsive glassmorphic layout, session sidebar thread manager, and Markdown text renderer.

---

## 📂 Project Structure

```
Blue-Lock-Football/
│
├── game.py              # Main loop, visual state renderer, CRT scanlines, confetti, UI menus
├── entities.py          # Player class (stamina, movement, trails) and Ball class (3D space, bounce)
├── physics.py           # Hooke's Law spring net simulation (8 nodes, elastic deformation)
├── ai.py                # Computer player decision tree (defender, midfielder, attacker, goalkeeper roles)
│
├── chatbot/             # SAP-CHAT-BOT: ChatGPT Mini Assistant
│   ├── app.py           # Flask server, /api/chat & /api/validate-key endpoints, self-healing keys
│   ├── search_engine.py # Gemini API betav1 connector, Mojeek web parser, offline greetings library
│   ├── templates/
│   │   └── index.html   # Sidebar layout, conversation history panels, settings modal
│   └── static/
│       ├── style.css    # Dark tech styling, fade-in animations, responsive panels
│       └── script.js    # Client state machine, sessionStorage threads, key validator
│
├── .gitignore           # Ignores python cache and virtual environments
├── GUIDE.md             # In-depth technical breakdown and architecture manual
├── CHATBOT.md           # Chatbot specific specifications
└── README.md            # Main project document
```

---

## 🚀 Installation & Setup

### Prerequisites
*   Python 3.8+
*   pip

### 1. Clone the Repository
```bash
git clone https://github.com/adarsh0718/Blue-Lock-Football.git
cd Blue-Lock-Football
```

### 2. Install Dependencies
```bash
pip install pygame Flask requests
```

### 3. Run the Retro Game
```bash
python game.py
```

### 4. Run the Chatbot Assistant
```bash
python chatbot/app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser!

---

## 🕹️ Controls

### Match Gameplay

| Player | Movement | Shoot (Charge) | Pass | Sprint |
|--------|----------|----------------|------|--------|
| **Player 1** | Arrow Keys | `M` | `N` | `Space` |
| **Player 2** | `W, A, S, D` | `F` | `G` | `Left Shift` |

---

## 👨‍💻 Author

**Adarsh Peddada**  
Electronics and Computer Engineering Student  
Passionate about Machine Learning, Data Analytics & Web Development.

[![GitHub](https://img.shields.io/badge/GitHub-adarsh0718-181717?style=flat-square&logo=github)](https://github.com/adarsh0718)
