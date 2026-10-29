"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame


# ============================================================
# WINDOW / TABLE SETTINGS
# ============================================================

WIDTH, HEIGHT = 800, 500

MARGIN = 20

GOAL_HEIGHT = 150

GOAL_TOP = HEIGHT / 2 - GOAL_HEIGHT / 2

GOAL_BOTTOM = HEIGHT / 2 + GOAL_HEIGHT / 2


# ============================================================
# COLORS
# ============================================================

COLOR_BG = (15, 15, 25)

COLOR_TABLE = (20, 60, 90)

COLOR_WALL = (200, 200, 210)

COLOR_CENTER_LINE = (90, 130, 150)

COLOR_PUCK = (240, 240, 240)

COLOR_PLAYER = (60, 140, 240)

COLOR_COMPUTER = (240, 80, 80)

COLOR_TEXT = (255, 255, 255)

COLOR_SCORE = (255, 255, 255)

COLOR_TIMER = (255, 255, 255)

COLOR_WINNER = (255, 220, 80)


# ============================================================
# WINDOW SIZE
# ============================================================

WINDOW_SIZE = (WIDTH, HEIGHT)


# ============================================================
# TABLE
# ============================================================

def draw_table(surface):
    """Draw the air hockey table."""

    surface.fill(COLOR_BG)

    # Main table
    pygame.draw.rect(
        surface,
        COLOR_TABLE,
        (
            MARGIN,
            MARGIN,
            WIDTH - 2 * MARGIN,
            HEIGHT - 2 * MARGIN
        )
    )

    # Center line
    pygame.draw.line(
        surface,
        COLOR_CENTER_LINE,
        (WIDTH / 2, MARGIN),
        (WIDTH / 2, HEIGHT - MARGIN),
        2
    )

    # Top wall
    pygame.draw.rect(
        surface,
        COLOR_WALL,
        (
            0,
            0,
            WIDTH,
            MARGIN
        )
    )

    # Bottom wall
    pygame.draw.rect(
        surface,
        COLOR_WALL,
        (
            0,
            HEIGHT - MARGIN,
            WIDTH,
            MARGIN
        )
    )

    # Left wall - above goal
    pygame.draw.rect(
        surface,
        COLOR_WALL,
        (
            0,
            MARGIN,
            MARGIN,
            GOAL_TOP - MARGIN
        )
    )

    # Left wall - below goal
    pygame.draw.rect(
        surface,
        COLOR_WALL,
        (
            0,
            GOAL_BOTTOM,
            MARGIN,
            HEIGHT - MARGIN - GOAL_BOTTOM
        )
    )

    # Right wall - above goal
    pygame.draw.rect(
        surface,
        COLOR_WALL,
        (
            WIDTH - MARGIN,
            MARGIN,
            MARGIN,
            GOAL_TOP - MARGIN
        )
    )

    # Right wall - below goal
    pygame.draw.rect(
        surface,
        COLOR_WALL,
        (
            WIDTH - MARGIN,
            GOAL_BOTTOM,
            MARGIN,
            HEIGHT - MARGIN - GOAL_BOTTOM
        )
    )


# ============================================================
# PUCK
# ============================================================

def draw_puck(surface, puck):
    """Draw the puck."""

    pygame.draw.circle(
        surface,
        COLOR_PUCK,
        (
            int(puck.x),
            int(puck.y)
        ),
        puck.radius
    )


# ============================================================
# PADDLE
# ============================================================

def draw_paddle(surface, paddle, color):
    """Draw a paddle."""

    pygame.draw.circle(
        surface,
        color,
        (
            int(paddle.x),
            int(paddle.y)
        ),
        int(paddle.radius)
    )


# ============================================================
# GENERAL TEXT
# ============================================================

def draw_text(
    surface,
    font,
    text,
    pos,
    color=COLOR_TEXT
):
    """Draw text at a specific position."""

    text_surface = font.render(
        text,
        True,
        color
    )

    surface.blit(
        text_surface,
        pos
    )


# ============================================================
# SCORE
# ============================================================

def draw_score(
    surface,
    font,
    player_score,
    computer_score
):
    """
    Draw the current score.

    Example:

        PLAYER  2    -    1  COMPUTER
    """

    score_text = (
        f"PLAYER  {player_score}"
        f"    -    "
        f"{computer_score}  COMPUTER"
    )

    text_surface = font.render(
        score_text,
        True,
        COLOR_SCORE
    )

    text_rect = text_surface.get_rect(
        center=(
            WIDTH // 2,
            MARGIN // 2
        )
    )

    surface.blit(
        text_surface,
        text_rect
    )


# ============================================================
# TIMER
# ============================================================

def draw_timer(
    surface,
    font,
    remaining_time
):
    """
    Draw the remaining match time.

    Example:

        TIME: 27
    """

    seconds = max(
        0,
        int(remaining_time + 0.999)
    )

    timer_text = f"TIME: {seconds}"

    text_surface = font.render(
        timer_text,
        True,
        COLOR_TIMER
    )

    text_rect = text_surface.get_rect(
        center=(
            WIDTH // 2,
            MARGIN + 20
        )
    )

    surface.blit(
        text_surface,
        text_rect
    )


# ============================================================
# WINNER BANNER
# ============================================================

def draw_banner(
    surface,
    font,
    text
):
    """Draw a winner/message banner in the center."""

    text_surface = font.render(
        text,
        True,
        COLOR_WINNER
    )

    text_rect = text_surface.get_rect(
        center=(
            surface.get_width() // 2,
            surface.get_height() // 2
        )
    )

    surface.blit(
        text_surface,
        text_rect
    )