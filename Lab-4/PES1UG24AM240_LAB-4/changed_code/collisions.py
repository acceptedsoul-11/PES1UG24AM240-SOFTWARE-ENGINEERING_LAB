"""
collisions: puck-vs-paddle collision handling.
"""


def handle_paddle_collision(puck, paddle):
    """
    Handle a circular puck colliding with a circular paddle.

    The puck is reflected along the collision normal and then moved
    outside the paddle to prevent it from getting stuck.

    Returns True if a collision was handled this frame.
    """

    dx = puck.x - paddle.x
    dy = puck.y - paddle.y

    distance_sq = dx * dx + dy * dy
    min_distance = puck.radius + paddle.radius

    # No collision
    if distance_sq >= min_distance * min_distance:
        return False

    # Avoid division by zero if centers are exactly identical.
    if distance_sq == 0:
        nx = 1.0
        ny = 0.0
        distance = 0.0
    else:
        distance = distance_sq ** 0.5
        nx = dx / distance
        ny = dy / distance

    # ---------------------------------------------------------
    # 1. Push puck outside the paddle
    # ---------------------------------------------------------
    overlap = min_distance - distance

    puck.x += nx * overlap
    puck.y += ny * overlap

    # ---------------------------------------------------------
    # 2. Reflect velocity around collision normal
    # ---------------------------------------------------------
    velocity_normal = puck.vx * nx + puck.vy * ny

    # Only bounce if the puck is moving INTO the paddle.
    if velocity_normal < 0:
        puck.vx -= 2 * velocity_normal * nx
        puck.vy -= 2 * velocity_normal * ny

    return True
