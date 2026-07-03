# 📘 Blue Lock Football Project Guide & Learning Manual

Welcome to the comprehensive learning and setup guide for the **Blue Lock Football** project! This document outlines everything you built, how the systems work (game physics, AI, and chatbot), and how to manage the project using Git.

---

## 🛠️ Technology Stack

This project is split into two major components: a **2D Pygame Football Simulation** and a **ChatGPT Mini Web Assistant**.

### 1. Retro Game Simulation (Python & Pygame)
- **Language**: Python 3.8+
- **Graphics & Sound**: [Pygame 2.x](https://www.pygame.org/) — a library used for rendering 2D shapes, handling keyboard events, framing the game loop, and playing retro audio effects.
- **Mathematics**: Vector math (`pygame.math.Vector2`) for directional movement, player-to-ball collisions, field bounds, and AI paths.
- **Physics**: Hooke's Law for spring-damping net mechanics, gravity, air resistance, and kinetic momentum.

### 2. Chatbot Web Assistant (Flask & Gemini AI)
- **Backend Framework**: [Flask (Python)](https://flask.palletsprojects.com/) — serves the web app endpoints and handles server-side request routing.
- **Frontend Framework**: Vanilla HTML5, CSS3 (universal Dark Space Tech theme with glassmorphism), and Javascript (state-driven UI, session thread management).
- **AI Integration**: [Google Gemini API](https://ai.google.dev/) (specifically `gemini-1.5-flash`) via direct HTTP requests using the `v1beta` endpoint.
- **Web Search**: Mojeek search engine scraping as a fallback when offline or without an API key.

---

## 📂 Project Architecture

```
Blue-Lock-Football/
│
├── game.py              # Main loop, visual state renderer, CRT scanlines, confetti, UI menus
├── entities.py          # Player class (stamina, movement, trails) and Ball class (3D space, bounce)
├── physics.py           # Hooke's Law spring net simulation (8 nodes, elastic deformation)
├── ai.py                # Computer player decision tree (defender, midfielder, attacker, goalkeeper roles)
│
└── chatbot/             # SAP-CHAT-BOT: ChatGPT Mini Assistant
    ├── app.py           # Flask server, /api/chat & /api/validate-key endpoints, self-healing keys
    ├── search_engine.py # Gemini API betav1 connector, Mojeek web parser, offline greetings library
    ├── templates/
    │   └── index.html   # Sidebar layout, conversation history panels, settings modal
    └── static/
        ├── style.css    # Dark tech styling, fade-in animations, responsive panels
        └── script.js    # Client state machine, sessionStorage threads, key validator
```

### File-by-File Breakdown

#### 1. [game.py](file:///d:/Blue-Lock-Football/game.py)
This is the heart of the game. It controls the main game loop, which runs at a locked **60 Frames Per Second (FPS)**.
- **State Machine**: Toggles between `MENU`, `MATCH`, `GOAL` (celebration), and `GAMEOVER` screens.
- **CRT Filter**: Draws faint horizontal lines across the screen every frame to mimic a 1970s CRT television display.
- **Confetti & Dust Particles**: Manages visual particles when goals are scored or players sprint.
- **Camera Shake**: Briefly shifts the screen viewport offset based on shot power.

#### 2. [entities.py](file:///d:/Blue-Lock-Football/entities.py)
Defines the actors inside the simulation:
- **Ball Class**: Models coordinate systems in 3D space (`x, y, z`). It tracks height (`z`), velocity, and spin. When kicked high, gravity pulls it back down, and air resistance slows it down over time.
- **Player Class**: Manages player speed, stamina reserves, active selection indicators, and kick range detection. It renders motion blur "sprint trails" when players move at maximum speed.

#### 3. [physics.py](file:///d:/Blue-Lock-Football/physics.py)
Handles the goal net physics using **Spring-Mass systems**. The net is represented by 8 interconnected points (nodes).
- **Hooke's Law**: When the ball collides with a net node, the net deflects. The connecting springs pull it back to its original shape using the formula:
  \[F = -k \cdot x\]
  where \(k\) is the spring stiffness and \(x\) is the displacement.
- **Damping**: Applied to slow down the motion so the net doesn't wiggle forever:
  \[F_{\text{damping}} = -c \cdot v\]
  where \(c\) is the damping coefficient and \(v\) is the node's velocity.

#### 4. [ai.py](file:///d:/Blue-Lock-Football/ai.py)
Determines how the computer-controlled players behave:
- **Goalkeeper**: Constantly adjusts its y-coordinate to align with the ball's trajectory while remaining inside the goal area.
- **Defenders**: Position themselves between the ball and their own goal, tackling any opponent who gets close.
- **Midfielders**: Distribute passes to forwards and intercept opponent passes.
- **Attackers**: Run towards the ball, charge their shots, and try to shoot towards the opponent's goal corners.

#### 5. [chatbot/](file:///d:/Blue-Lock-Football/chatbot/)
A standalone ChatGPT-like assistant:
- **Session Thread Manager**: The sidebar lists recent conversations. This session data is saved in `sessionStorage` (cleared on tab close) for privacy.
- **Self-Healing API Keys**: If you enter an invalid API key, the chatbot automatically detects the authentication failure, clears it from `localStorage`, and falls back to a friendly conversational search layer without throwing recurring error popups.

---

## 🚀 Running & Using the Project

### Playing the Football Game
1. Open a terminal/command prompt.
2. Run the game:
   ```bash
   python game.py
   ```
3. **Controls**:
   - **Player 1**: Arrow keys (Move), `M` (Shoot/Charge), `N` (Pass), `Space` (Sprint).
   - **Player 2**: `W, A, S, D` (Move), `F` (Shoot/Charge), `G` (Pass), `Shift` (Sprint).

### Launching the Chatbot
1. Run the Flask server:
   ```bash
   python chatbot/app.py
   ```
2. Open your browser and go to **[http://127.0.0.1:5000](http://127.0.0.1:5000)**.
3. Configure your API key by opening the settings (⚙️) panel and paste a Gemini key from **[Google AI Studio](https://aistudio.google.dev/)**. Click **Test & Validate Key** to check its status.

---

## 📂 Managing the Project with Git & GitHub

Here is how you push and update your changes on GitHub step-by-step:

### 1. Initialize Git (If not already set up)
```bash
git init
git remote add origin https://github.com/adarsh0718/Blue-Lock-Football.git
```

### 2. Check Working Status
See what files are modified or untracked:
```bash
git status
```

### 3. Stage Changes
Add modified or new files to the commit staging area:
```bash
# Add the entire chatbot folder
git add chatbot/

# Add specific files
git add game.py entities.py physics.py ai.py

# Or add all changes at once
git add .
```

### 4. Create a Commit
Write a descriptive message detailing the changes you are saving:
```bash
git commit -m "feat: integrate chatbot assistant and Hooke's Law goal net physics"
```

### 5. Push to GitHub
Upload your local commits to your online repository:
```bash
git push -u origin main
```
