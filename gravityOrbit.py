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

def draw_grid(screen, spacing, color=(100,100,100)):
    width, height = screen.get_size()

    for x in range(0, width, spacing):
        pygame.draw.line(screen, color, (x, 0), (x, height))

    for y in range(0, height, spacing):
        pygame.draw.line(screen, color, (0, y), (width, y))

running = True

things = []

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

    screen.fill((18, 24, 38))
    draw_grid(screen,50)

    px, py = world_to_screen(640, 360)
    pygame.draw.circle(screen, (255, 180, 60), (px, py), int(100 * zoom))
    #pygame.draw.circle(screen, (0,0,0), (640, 360), 150, 2)

    for t in things:
        sx, sy = world_to_screen(t.position.x, t.position.y)
        pygame.draw.circle(screen, (120, 200, 255), (sx, sy), max(1, int(10 * zoom)))

    for t in things:
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

        r_vec = pygame.Vector2(dx, dy)
        v_vec = pygame.Vector2(vx, vy)

        # a = -GM / (v² - 2GM/r)
        semi_major_axis = (-9.81 * 400000) / ((speed**2) - (2 * 9.81 * 400000) / r)

        # e_vec = (v²/GM - 1/r) * r_vec - (r_dot_v/GM) * v_vec
        e_vec = (speed**2/(9.81*400000) - 1/r) * r_vec - (dot/(9.81*400000)) * v_vec
        e = math.sqrt(e_vec.x**2 + e_vec.y**2)

        if semi_major_axis > 0 and e < 1:
            # b = semi_major_axis * sqrt(1 - e^2)
            semi_minor_axis = semi_major_axis * math.sqrt(1 - e**2)

            # angle = tan(e_vec.y, e_vec.x)
            angle = math.atan2(e_vec.y, e_vec.x)

            center_x = 640 - e_vec.x / e * semi_major_axis * e
            center_y = 360 - e_vec.y / e * semi_major_axis * e

            points = []
            for i in range(360):
                theta = math.radians(i)
                x = semi_major_axis * math.cos(theta)
                y = semi_minor_axis * math.sin(theta)
                rx = x * math.cos(angle) - y * math.sin(angle)
                ry = x * math.sin(angle) + y * math.cos(angle)
                sx, sy = world_to_screen(center_x + rx, center_y + ry)
                points.append((sx, sy))

            pygame.draw.lines(screen, "white", True, points, 1)

        # acceleration due to gravity
        # a = G(m/r^2)
        force = -9.81 * (400000 / (r**2))
        direction = pygame.Vector2(dx, dy).normalize()
        acceleration = direction * force
        t.velocity += acceleration * dt
        t.position += t.velocity * dt

    pygame.draw.circle(screen, (120, 200, 255), (1250, 20), 10)

    pygame.display.flip()