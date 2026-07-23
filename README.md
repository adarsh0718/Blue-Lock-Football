# ⚽ Championship Football 1978 — Blue Lock Edition

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-00B140?style=for-the-badge&logo=pygame&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-gold?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**A retro-styled, feature-rich 2D football game built with Python & Pygame.**  
Inspired by the raw intensity of *Blue Lock* — a vintage 5v5 experience dripping in 1970s football aesthetics.

[🎮 Getting Started](#-installation) · [🕹️ Controls](#%EF%B8%8F-controls) · [🌦️ Weather Modes](#%EF%B8%8F-weather-system) · [🧠 AI System](#-ai-system) · [📂 Project Structure](#-project-structure)

</div>

---

## 🎬 Overview

**Championship Football 1978** is a fully-featured, physics-driven 2D football simulation written entirely in Python using Pygame. It captures the look and feel of vintage 1970s football — complete with muted olive-green grass stripes, CRT scanline overlays, leather ball seams, and sepia-toned stadium lighting.

The game features **two modes** — play solo against AI-controlled opponents, or go head-to-head in local **2-player** mode. With 4 distinct weather conditions, spring-physics goal nets, stamina management, charge-shot mechanics, and a role-based AI engine, every match feels alive and dynamic.

> ⚡ *"The era of a chosen striker has begun."*

---

## ✨ Features

### 🖼️ Visual Style
- **Vintage 1970s Aesthetic** — muted olive-green grass strips, chalk-cream field markings, sepia gold HUD
- **CRT Scanline Overlay** — subtle horizontal scanline filter applied every frame for a retro TV look
- **Dynamic Screen Shake** — camera trembles on powerful shots and goal celebrations
- **Leather Ball Rendering** — classic tan leather football with rotating curved seam lines
- **Sprint Ghost Trails** — motion-blur trails appear behind sprinting players
- **Confetti Celebration** — goal events spawn 100 colored confetti particles with gravity and spin

### 🌦️ Weather System
Four fully simulated weather conditions, each affecting visuals and physics:

| Weather | Visual Effect | Physics Effect |
|---------|--------------|----------------|
| ☀️ **Sunny** | Crisp, dark player & ball shadows | Standard friction & acceleration |
| 🌇 **Evening** | Amber sunset tint overlay, stretched long shadows | Standard physics |
| 🌧️ **Raining** | Raindrop particles with splash ripples, faint shadows | Wet grass: higher ball slide, reduced player grip & sprint speed |
| 🌙 **Night** | Deep dark blue stadium overlay with soft spotlight halos | Standard physics |

### ⚽ Ball Physics
- Full **3-axis physics** (X, Y, Z) — the ball can be lofted into the air
- **Air resistance** and **gravity** simulate realistic ball arc and bounce
- **Spin speed** affects visual seam rotation based on kick velocity
- **Weather-adjusted friction** — wet conditions make the ball slide further
- **Vintage dust trail** — subtle beige particle trail when ball exceeds speed threshold

### 👥 Player Mechanics
- **Stamina system** — sprinting drains stamina; depleted players slow down
- **Role-specific speeds** — GKs, DEFs, MIDs, and ATTs all move consistently
- **Active player indicator** — animated bouncing triangle marks your controlled player
- **Auto-switch on ball pickup** — control automatically shifts to the player who collects the ball

### 🎯 Shooting & Passing
- **Charge shot** — hold the shoot key to build power; a gold pulsing bar shows charge level
- **Shot deviation** — underpowered shots deviate from target; full-charge shots are accurate
- **Smart pass** — auto-aims at the best-aligned teammate in your facing direction
- **Lofted passes** — long-distance passes have a 25% chance of being lobbed automatically

### 🥅 Goal Net Physics
- Goal nets are built from **8 spring-physics nodes**
- Each node uses Hooke's Law spring force with damping to snap back to rest
- Ball impact deflects the nearest node; structural springs maintain net shape
- Wooden goalpost bounce with high restitution and heavy damping on post hits

---

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Python 3.8+** | Core game logic and systems |
| **Pygame 2.x** | Rendering, event handling, audio surface |
| **OOP / Class Design** | `Ball`, `Player`, `GoalNetPhysics`, `FootballAI`, `GameEngine` |
| **Spring Physics** | Goal net deformation and restitution |
| **Vector Mathematics** | Movement, collision, AI targeting, shot deviation |
| **Particle System** | Rain, splash ripples, kick dust, sprint trails, confetti |

---

## 📂 Project Structure

```
Blue-Lock-Football/
│
├── game.py          # Core GameEngine — main loop, input, states, rendering
│   ├── GameEngine   # Central controller: menu, match, goal, game-over states
│   ├── Particle     # Particle class — dust, rain, splash, confetti
│   └── draw_*       # Rendering methods: pitch, HUD, nets, overlays, menus
│
├── entities.py      # Game objects — Ball and Player classes
│   ├── Ball         # 3-axis physics, spin, weather friction, trail, rendering
│   └── Player       # Movement, stamina, weather effects, jersey rendering
│
├── physics.py       # Collision and net simulation
│   ├── NetNode      # Spring-physics node for goal net deformation
│   ├── GoalNetPhysics   # Full net with structural spring constraints
│   └── handle_ball_pitch_bounds  # Boundary reflection and post collision
│
└── ai.py            # FootballAI — role-based decision engine
    ├── update_goalkeeper        # GK tracking, rush-out, distribution
    ├── handle_offense_ball_carrier  # Shoot, pass, dribble with dodge
    ├── handle_offense_support   # Role-based positioning off the ball
    └── handle_defense_or_loose  # Press, mark space, recover shape
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (comes bundled with Python)

### 1. Clone the Repository

```bash
git clone https://github.com/adarsh0718/Blue-Lock-Football.git
cd Blue-Lock-Football
```

### 2. Install Dependencies

```bash
pip install pygame
```

### 3. Run the Game

```bash
python game.py
```

---

## 🕹️ Controls

### Main Menu Navigation

| Key | Action |
|-----|--------|
| `W` / `↑` | Move selection up |
| `S` / `↓` | Move selection down |
| `A` / `←` | Cycle option left (mode/weather) |
| `D` / `→` | Cycle option right (mode/weather) |
| `Enter` | Confirm selection |

### In-Match — Player 1 (Blue Team)

| Key | Action |
|-----|--------|
| `W A S D` | Move player |
| `Left Shift` | Sprint (drains stamina) |
| `F` | Pass ball / Switch to nearest player |
| `Hold G` | Charge shot |
| `Release G` | Release shot |

### In-Match — Player 2 (Red Team, 2-Player Mode)

| Key | Action |
|-----|--------|
| `↑ ↓ ← →` | Move player |
| `Right Shift` | Sprint (drains stamina) |
| `K` | Pass ball / Switch to nearest player |
| `Hold L` | Charge shot |
| `Release L` | Release shot |

### General

| Key | Action |
|-----|--------|
| `Escape` | Return to menu |
| `Enter` | Restart (on Game Over screen) |

---

## ⚙️ Game Mechanics — Deep Dive

### Match Flow

```
MENU → (mode + weather select) → MATCH → GOAL_SCB (3s celebration) → MATCH
                                       ↘ GAME_OVER (90-min timer ends) → MENU
```

### Player Roles (5v5 Formation)

Each team fields 5 players in a **1-2-1-1** formation:

| # | Role | Behaviour |
|---|------|-----------|
| GK | Goalkeeper | Tracks ball Y-axis, rushes out within 70px, distributes to furthest free teammate |
| DEF | Defender (×2) | Retreats to protect penalty box, spreads wide to cover Y-axis |
| MID | Midfielder | Positions 60–100px behind/ahead of ball carrier, blocks passing lanes |
| ATT | Attacker | Pushes high for 1v1 opportunities, counter-attacks from advanced position |

### AI Decision Tree (Outfield Players)

```
Ball owner == this player?
  ├── YES → Shoot if within 230px, else pass to open teammate, else dribble with dodge
  ├── TEAMMATE has ball → Move to role-based support position
  └── OPPONENT/LOOSE ball
        ├── Closest player → Press ball aggressively
        └── Others → Mark space / recover defensive shape
```

### Tackling
- **Player-initiated**: Press `F` / `K` when close to an opponent — range tightened in rain
- **AI auto-tackle**: 8% chance per frame when within contact range (6% in rain)
- Successful tackle scatters the ball with random velocity and triggers a brief screen shake

### Charge Shot Mechanics
- Charge builds at `+1.0 / frame` up to max `30.0`
- **Power**: `5.8 + (charge_ratio × 6.0)` — max power ≈ 11.8
- **Loft (Z)**: `charge_ratio × 4.4` — full charge lofts the ball high
- **Deviation**: `(1 - charge_ratio) × 0.16 radians` — full charge = laser accuracy

---

## 🧠 AI System

The `FootballAI` class (`ai.py`) manages the decision-making of all 8 AI-controlled players (4 per team). Each player is evaluated independently every frame.

### Goalkeeper Intelligence
- Maintains a safe position **18px in front of** the goal mouth
- Tracks ball Y position clamped to the goal range
- **Rushes out** if ball is free and within 70px range
- On ball pickup: finds the **furthest open teammate** and kicks with `power=7.2`

### Outfield Intelligence
- **Ball carrier**: Prioritises shoot → find open forward pass → dribble with vertical dodge around defenders
- **Supporting attacker**: Pushes 130px forward of carrier towards goal center
- **Supporting midfielder**: Flanks 60px off carrier to create passing triangle
- **Supporting defenders**: Hold shape 90px behind, spread vertically
- **Defensive press**: Closest non-GK to ball sprints to press at full speed
- **Defensive recovery**: DEF retreats to box, MID fills space 100px behind ball, ATT holds high for counter

---

## 🔮 Roadmap

- [ ] Sound effects (kick, goal, crowd roar)
- [ ] Background music (vintage stadium ambience)
- [ ] Pause menu
- [ ] Team & jersey colour selection
- [ ] Match timer display in real-time clock format
- [ ] Tournament bracket mode
- [ ] Improved AI with pressure and pressing triggers
- [ ] Animated player sprites
- [ ] Online multiplayer support

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a new feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit** your changes with a clear message
   ```bash
   git commit -m "feat: add your feature description"
   ```
4. **Push** to your fork
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a **Pull Request** describing your changes

---

## 👨‍💻 Author

**Adarsh Peddada**  
Electronics and Computer Engineering Student  
Passionate about Python, Artificial Intelligence, Game Development & Software Engineering.

[![GitHub](https://img.shields.io/badge/GitHub-adarsh0718-181717?style=flat-square&logo=github)](https://github.com/adarsh0718)

---

## 📜 License

This project is licensed under the **MIT License** — free to use, modify, and distribute for educational and personal purposes.

---

<div align="center">

⭐ **If you enjoyed this project, please consider giving it a star on GitHub!** ⭐

*"The only one who can make himself a weapon is himself."* — Jinpachi Ego

</div>
