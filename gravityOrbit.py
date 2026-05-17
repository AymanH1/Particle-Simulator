import pygame
import math
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

class Thing:
    def __init__(self, position, velocity, mass):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.mass = mass

running = True

things = []

# camera
cam_x, cam_y = 640, 360
zoom = 1.0

def world_to_screen(wx, wy):
    sx = (wx - cam_x) * zoom + 640
    sy = (wy - cam_y) * zoom + 360
    return sx, sy

while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            dx = mx - 1250
            dy = my - 20

            if dx*dx + dy*dy <= 10*10:
                things.append(
                    Thing(
                        (random.randint(0, 1280), random.randint(0, 720)),
                        (random.randint(-200,200), random.randint(-200,200)),
                        20
                    )
                )

    keys = pygame.key.get_pressed()
    cam_speed = 300 / zoom
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        cam_x -= cam_speed * dt
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        cam_x += cam_speed * dt
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        cam_y -= cam_speed * dt
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        cam_y += cam_speed * dt
    if keys[pygame.K_EQUALS] or keys[pygame.K_PLUS]:
        zoom *= 1 + dt
    if keys[pygame.K_MINUS]:
        zoom /= 1 + dt

    things = [
        t for t in things
        if (t.position.x - 640)**2 + (t.position.y - 360)**2 > 100**2
    ]

    screen.fill("white")

    px, py = world_to_screen(640, 360)
    pygame.draw.circle(screen, "green", (px, py), int(100 * zoom))
    #pygame.draw.circle(screen, (0,0,0), (640, 360), 150, 2)

    for t in things:
        sx, sy = world_to_screen(t.position.x, t.position.y)
        pygame.draw.circle(screen, "black", (sx, sy), max(1, int(10 * zoom)))

    for t in things:
        # expected velocity
        dx = t.position.x - 640
        dy = t.position.y - 360
        r = math.sqrt(dx*dx + dy*dy)

        expected_speed = math.sqrt((9.81 * 400) / r)

        vx = t.velocity.x
        vy = t.velocity.y
        speed = math.sqrt(vx*vx + vy*vy)

        dot = dx * vx + dy * vy

        if abs(dot) < 1e-2 and abs(speed - expected_speed) < 0.1:
            print("orbit")

        # acceleration due to gravity
        # a = G(m/r^2)

        force = -9.81 * (400000 / (r**2))
        direction = pygame.Vector2(dx, dy).normalize()
        acceleration = direction * force
        t.velocity += acceleration * dt
        t.position += t.velocity * dt

    # fixed UI on top
    pygame.draw.circle(screen, "black", (1250, 20), 10)

    pygame.display.flip()