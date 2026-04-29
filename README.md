[README.md](https://github.com/user-attachments/files/27188174/README.md)
# VOID-RUNNER# VOID RUNNER

**VOID RUNNER** is a minimalist 2D arcade survival game for desktop.  
The player controls a small glowing white dot and avoids falling red blocks in a dark neon environment. The goal is simple: survive as long as possible and beat the high score.

---

## Preview

> Add your screenshots inside `assets/screenshots/` and update these paths if needed.

| Home Screen | Gameplay |
|---|---|
| ![Home Screen](assets/screenshots/home.png) | ![Gameplay](assets/screenshots/gameplay.png) |

| How To Play | Game Over |
|---|---|
| ![How To Play](assets/screenshots/how-to-play.png) | ![Game Over](assets/screenshots/game-over.png) |

---

## Game Concept

VOID RUNNER is built around one simple mechanic:

> Move the white dot. Avoid the red blocks. Survive as long as possible.

The game uses a clean minimalist visual style with:
- Dark background
- White glowing player
- Red neon obstacles
- Simple geometric UI
- Score and high score system
- Desktop `.exe` support

---

## Features

- Minimalist home menu
- Smooth player movement
- Falling obstacle system
- Collision detection
- Score system
- High score saving
- Game over screen
- Retry / Home / Exit actions
- How To Play screen
- Pause support
- Windows executable build support

---

## Screens

### Home Screen

The home screen contains the main navigation:

- `PLAY`
- `HOW TO PLAY`
- `SETTINGS`
- `EXIT`

### Gameplay Screen

The gameplay screen includes:

- Player dot
- Falling red blocks
- Current score
- Best score
- Pause button

### How To Play Screen

Shows the basic controls and rules:

1. Move with `WASD` or arrow keys
2. Avoid falling red blocks
3. Survive as long as possible
4. Beat your high score

### Game Over Screen

Displayed when the player hits an obstacle.

Includes:

- Final score
- Best score
- Retry button
- Home button
- Exit button

---

## Controls

| Key | Action |
|---|---|
| `W` / `Arrow Up` | Move up |
| `S` / `Arrow Down` | Move down |
| `A` / `Arrow Left` | Move left |
| `D` / `Arrow Right` | Move right |
| `ESC` | Pause / Back |
| Mouse Click | Select menu buttons |

---

## Tech Stack

- **Python**
- **Pygame**
- **PyInstaller**

---

## Project Structure

```text
void-runner/
│
├── main.py
├── README.md
├── requirements.txt
│
├── assets/
│   ├── fonts/
│   ├── sounds/
│   ├── images/
│   └── screenshots/
│       ├── home.png
│       ├── gameplay.png
│       ├── how-to-play.png
│       └── game-over.png
│
├── data/
│   └── highscore.txt
│
└── src/
    ├── settings.py
    ├── game.py
    ├── player.py
    ├── obstacle.py
    ├── ui.py
    ├── screens.py
    └── storage.py
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/void-runner.git
cd void-runner
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Game

```bash
python main.py
```

---

## Build Windows EXE

Install PyInstaller:

```bash
pip install pyinstaller
```

Build the game:

```bash
pyinstaller --onefile --windowed --name VoidRunner main.py
```

The executable file will be generated here:

```text
dist/VoidRunner.exe
```

---

## Requirements

`requirements.txt`

```text
pygame
pyinstaller
```

---

## Gameplay Rules

- The player starts near the bottom of the screen.
- Red blocks fall from the top.
- The player must avoid all red blocks.
- Score increases over time.
- The longer the player survives, the harder the game becomes.
- If the player touches a red block, the game ends.
- The best score is saved locally.

---

## Team Roles

This project was designed to be developed by two people.

### Gameplay Developer

Responsible for:

- Player movement
- Obstacle movement
- Collision detection
- Score system
- Difficulty scaling
- High score save/load
- Game loop logic

### UI / UX Developer

Responsible for:

- Home screen
- Buttons
- HUD
- How To Play screen
- Game Over screen
- Pause screen
- Visual polish
- Sound/UI feedback

---

## Development Checklist

- [ ] Create Pygame window
- [ ] Add game state system
- [ ] Add home screen
- [ ] Add player movement
- [ ] Add falling obstacles
- [ ] Add collision detection
- [ ] Add score system
- [ ] Add high score saving
- [ ] Add game over screen
- [ ] Add retry system
- [ ] Add how to play screen
- [ ] Add pause screen
- [ ] Add settings screen
- [ ] Add sound effects
- [ ] Polish UI
- [ ] Test gameplay
- [ ] Build `.exe`

---

## Final Version Goals

The final version should include:

- Complete menu flow
- Playable main game
- High score persistence
- Clean visual design
- Smooth controls
- Working retry system
- Windows executable file
- README documentation
- Screenshots for presentation

---

## License

This project is for learning and portfolio/demo purposes.  
You can update the license depending on your repository usage.

---

## Project Summary

VOID RUNNER is a simple but polished minimalist arcade game.  
It focuses on fast reflexes, clean UI, and a complete desktop game experience using only basic 2D shapes and lightweight game logic.
