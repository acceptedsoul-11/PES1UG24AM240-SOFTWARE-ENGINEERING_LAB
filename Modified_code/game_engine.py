"""
GameEngine: owns the puck, both paddles, and the computer AI, and runs
one frame's worth of game logic.

Implemented tasks:
- Paddle collision handling
- Match scoring
- 30-second match timer
- Winner detection
- Draw detection
- Clean puck reset after every goal
"""

import random
import time

from game.puck import Puck
from game.paddle import Paddle
from game.ai import ComputerAI
from game.collisions import handle_paddle_collision
from game.renderer import WIDTH, HEIGHT, MARGIN, GOAL_TOP, GOAL_BOTTOM


PLAYER_SPEED = 6
PUCK_RADIUS = 12
PADDLE_RADIUS = 28
INITIAL_PUCK_SPEED = 4.5

MATCH_DURATION = 30
WINNING_SCORE = 5


class GameEngine:
    def __init__(self):
        # ----------------------------------------------------
        # Puck
        # ----------------------------------------------------

        self.puck = Puck(
            WIDTH / 2,
            HEIGHT / 2,
            PUCK_RADIUS
        )

        self._launch_puck()

        # ----------------------------------------------------
        # Player paddle
        # ----------------------------------------------------

        self.player = Paddle(
            x=WIDTH * 0.15,
            y=HEIGHT / 2,
            radius=PADDLE_RADIUS,
            min_x=MARGIN + PADDLE_RADIUS,
            max_x=WIDTH / 2 - PADDLE_RADIUS,
            min_y=MARGIN + PADDLE_RADIUS,
            max_y=HEIGHT - MARGIN - PADDLE_RADIUS,
        )

        # ----------------------------------------------------
        # Computer paddle
        # ----------------------------------------------------

        self.computer = Paddle(
            x=WIDTH * 0.85,
            y=HEIGHT / 2,
            radius=PADDLE_RADIUS,
            min_x=WIDTH / 2 + PADDLE_RADIUS,
            max_x=WIDTH - MARGIN - PADDLE_RADIUS,
            min_y=MARGIN + PADDLE_RADIUS,
            max_y=HEIGHT - MARGIN - PADDLE_RADIUS,
        )

        # ----------------------------------------------------
        # AI
        # ----------------------------------------------------

        self.ai = ComputerAI()

        # ----------------------------------------------------
        # Scores
        # ----------------------------------------------------

        self.player_score = 0
        self.computer_score = 0

        # None while playing.
        # "PLAYER", "COMPUTER", or "DRAW" after match ends.
        self.winner = None

        # ----------------------------------------------------
        # Match timer
        # ----------------------------------------------------

        self.match_start_time = time.monotonic()
        self.remaining_time = MATCH_DURATION

    def _launch_puck(self):
        """
        Give the puck its starting velocity for a new point.
        """

        angle_choices = [
            0.3,
            0.6,
            -0.3,
            -0.6
        ]

        direction = random.choice([-1, 1])
        vy_factor = random.choice(angle_choices)

        self.puck.vx = INITIAL_PUCK_SPEED * direction
        self.puck.vy = INITIAL_PUCK_SPEED * vy_factor

    def handle_input(self, keys_pressed):
        """Handle keyboard input for the human player."""

        import pygame

        # Do not allow movement after match ends.
        if self.winner is not None:
            return

        dx = 0
        dy = 0

        if keys_pressed[pygame.K_UP]:
            dy -= PLAYER_SPEED

        if keys_pressed[pygame.K_DOWN]:
            dy += PLAYER_SPEED

        if keys_pressed[pygame.K_LEFT]:
            dx -= PLAYER_SPEED

        if keys_pressed[pygame.K_RIGHT]:
            dx += PLAYER_SPEED

        self.player.move_by(dx, dy)

    def update(self):
        """Run one frame of game logic."""

        # ----------------------------------------------------
        # Match already finished
        # ----------------------------------------------------

        if self.winner is not None:
            return

        # ----------------------------------------------------
        # Update timer
        # ----------------------------------------------------

        elapsed_time = time.monotonic() - self.match_start_time

        self.remaining_time = max(
            0,
            MATCH_DURATION - elapsed_time
        )

        # Time expired.
        if self.remaining_time <= 0:
            self.remaining_time = 0
            self._finish_by_score()
            return

        # ----------------------------------------------------
        # Update AI
        # ----------------------------------------------------

        self.ai.update(
            self.computer,
            self.puck
        )

        # ----------------------------------------------------
        # Move puck
        # ----------------------------------------------------

        self.puck.move()

        # ----------------------------------------------------
        # Wall collisions
        # ----------------------------------------------------

        self.puck.bounce_off_walls(
            HEIGHT,
            MARGIN
        )

        # ----------------------------------------------------
        # Paddle collisions
        # ----------------------------------------------------

        handle_paddle_collision(
            self.puck,
            self.player
        )

        handle_paddle_collision(
            self.puck,
            self.computer
        )

        # ----------------------------------------------------
        # Goal detection
        # ----------------------------------------------------

        self._handle_goals()

    def _handle_goals(self):
        """
        Detect goals.

        Left goal:
            Computer scores.

        Right goal:
            Player scores.
        """

        # ====================================================
        # LEFT GOAL
        # ====================================================

        if self.puck.x - self.puck.radius < MARGIN:

            if GOAL_TOP < self.puck.y < GOAL_BOTTOM:

                # Computer scores.
                self.computer_score += 1

                # Check for immediate match win.
                self._check_winner()

                # If match is still active,
                # reset the puck for the next point.
                if self.winner is None:
                    self._reset_puck()

            else:
                # Not inside goal opening.
                # Bounce from wall.
                self.puck.x = MARGIN + self.puck.radius
                self.puck.vx = -self.puck.vx

        # ====================================================
        # RIGHT GOAL
        # ====================================================

        elif self.puck.x + self.puck.radius > WIDTH - MARGIN:

            if GOAL_TOP < self.puck.y < GOAL_BOTTOM:

                # Player scores.
                self.player_score += 1

                # Check for immediate match win.
                self._check_winner()

                # If match is still active,
                # reset the puck for the next point.
                if self.winner is None:
                    self._reset_puck()

            else:
                # Not inside goal opening.
                # Bounce from wall.
                self.puck.x = WIDTH - MARGIN - self.puck.radius
                self.puck.vx = -self.puck.vx

    def _check_winner(self):
        """Check whether somebody reached the winning score."""

        if self.player_score >= WINNING_SCORE:
            self.winner = "PLAYER"

        elif self.computer_score >= WINNING_SCORE:
            self.winner = "COMPUTER"

    def _finish_by_score(self):
        """Determine the result when the timer expires."""

        if self.player_score > self.computer_score:
            self.winner = "PLAYER"

        elif self.computer_score > self.player_score:
            self.winner = "COMPUTER"

        else:
            self.winner = "DRAW"

    def _reset_puck(self):
        """
        Completely reset the puck after a goal.

        This ensures every new point starts from a clean state.
        """

        # ----------------------------------------------------
        # Reset position
        # ----------------------------------------------------

        self.puck.x = WIDTH / 2
        self.puck.y = HEIGHT / 2

        # ----------------------------------------------------
        # Clear old velocity first
        # ----------------------------------------------------

        self.puck.vx = 0
        self.puck.vy = 0

        # ----------------------------------------------------
        # Launch with a fresh direction
        # ----------------------------------------------------

        self._launch_puck()

    def draw(self, surface, font):
        """Draw the complete game."""

        from game import renderer

        # Table
        renderer.draw_table(surface)

        # Player paddle
        renderer.draw_paddle(
            surface,
            self.player,
            renderer.COLOR_PLAYER
        )

        # Computer paddle
        renderer.draw_paddle(
            surface,
            self.computer,
            renderer.COLOR_COMPUTER
        )

        # Puck
        renderer.draw_puck(
            surface,
            self.puck
        )

        # Score
        renderer.draw_score(
            surface,
            font,
            self.player_score,
            self.computer_score
        )

        # Timer
        renderer.draw_timer(
            surface,
            font,
            self.remaining_time
        )

        # Match result
        if self.winner == "PLAYER":

            renderer.draw_banner(
                surface,
                font,
                "PLAYER WINS!"
            )

        elif self.winner == "COMPUTER":

            renderer.draw_banner(
                surface,
                font,
                "COMPUTER WINS!"
            )

        elif self.winner == "DRAW":

            renderer.draw_banner(
                surface,
                font,
                "DRAW!"
            )