import asyncio
import pygame
import sys
import math
import random
from entities import Player, Ball
from physics import GoalNetPhysics, handle_ball_pitch_bounds
from ai import FootballAI

# ── re-use everything from game.py ──────────────────────────────────────────
from game import GameEngine, WIDTH, HEIGHT, FPS

async def main():
    game = GameEngine()

    while True:
        game.handle_events()
        game.update()
        game.draw()
        game.clock.tick(FPS)
        await asyncio.sleep(0)   # yield control back to the browser each frame

asyncio.run(main())
