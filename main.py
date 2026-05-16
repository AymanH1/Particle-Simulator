import pygame
import random
import math

dt = 0.016


class Particle:
    def __init__(self, name, velocity, position, mass, charge, radius):
        self.name = name
        self.velocity = pygame.Vector2(velocity)
        self.position = pygame.Vector2(position)
        self.mass = mass
        self.charge = charge
        self.radius = radius
        self.color = None


class Nucleus:
    def __init__(self, particles):
        self.particles = particles
        self.position = sum((p.position for p in particles), pygame.Vector2()) / len(particles)
        self.velocity = sum((p.velocity for p in particles), pygame.Vector2()) / len(particles)
        self.mass = sum(p.mass for p in particles)
        self.radius = 25
        self.color = (160, 0, 255)

class Hydrogen:
    def __init__(self, particles):
        self.particles = particles
        self.position = sum((p.position for p in particles), pygame.Vector2()) / len(particles)
        self.velocity = sum((p.velocity for p in particles), pygame.Vector2()) / len(particles)
        self.mass = sum(p.mass for p in particles)
        self.radius = 17
        self.color = (255, 255, 0)


class Photon:
    def __init__(self, position, velocity):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.lifetime = 3.0
        self.radius = 2


def random_velocity(min_speed, max_speed):
    return random.choice([-1, 1]) * random.uniform(min_speed, max_speed)


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 16)

button_electron = pygame.Rect(1170, 10, 100, 40)
button_proton   = pygame.Rect(1170, 60, 100, 40)
button_neutron  = pygame.Rect(1170, 110, 100, 40)
button_positron = pygame.Rect(1170, 160, 100, 40)

text_electron = font.render("Add Electron", True, (255, 255, 255))
text_proton   = font.render("Add Proton", True, (255, 255, 255))
text_neutron  = font.render("Add Neutron", True, (255, 255, 255))
text_positron = font.render("Add Positron", True, (255, 255, 255))

text_rect_electron = text_electron.get_rect(center=button_electron.center)
text_rect_proton   = text_proton.get_rect(center=button_proton.center)
text_rect_neutron  = text_neutron.get_rect(center=button_neutron.center)
text_rect_positron = text_positron.get_rect(center=button_positron.center)

# ---------------- CONSTANTS ----------------
ELECTRON_MASS = 1
POSITRON_MASS = 1
PROTON_MASS   = 1836
NEUTRON_MASS  = 1839

ELECTRON_CHARGE = -1
POSITRON_CHARGE = 1
PROTON_CHARGE   = 1
NEUTRON_CHARGE  = 0

ELECTRON_RADIUS = 8
POSITRON_RADIUS = 8
PROTON_RADIUS   = 18
NEUTRON_RADIUS  = 17

electrons = []
positrons = []
protons = []
neutrons = []
nuclei = []
photons = []
hydrogens = []

particles_to_remove = set()

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if button_electron.collidepoint(event.pos):
                electrons.append(Particle(
                    "electron",
                    (random_velocity(200, 250), random_velocity(200, 250)),
                    (random.randint(0, 1280), random.randint(0, 720)),
                    ELECTRON_MASS,
                    ELECTRON_CHARGE,
                    ELECTRON_RADIUS
                ))

            if button_positron.collidepoint(event.pos):
                positrons.append(Particle(
                    "positron",
                    (random_velocity(200, 250), random_velocity(200, 250)),
                    (random.randint(0, 1280), random.randint(0, 720)),
                    POSITRON_MASS,
                    POSITRON_CHARGE,
                    POSITRON_RADIUS
                ))

            if button_proton.collidepoint(event.pos):
                protons.append(Particle(
                    "proton",
                    (random_velocity(20, 50), random_velocity(20, 50)),
                    (random.randint(0, 1280), random.randint(0, 720)),
                    PROTON_MASS,
                    PROTON_CHARGE,
                    PROTON_RADIUS
                ))

            if button_neutron.collidepoint(event.pos):
                neutrons.append(Particle(
                    "neutron",
                    (random_velocity(20, 50), random_velocity(20, 50)),
                    (random.randint(0, 1280), random.randint(0, 720)),
                    NEUTRON_MASS,
                    NEUTRON_CHARGE,
                    NEUTRON_RADIUS
                ))

    screen.fill("white")

    pygame.draw.rect(screen, 'black', button_electron)
    pygame.draw.rect(screen, 'black', button_positron)
    pygame.draw.rect(screen, 'black', button_proton)
    pygame.draw.rect(screen, 'black', button_neutron)

    screen.blit(text_electron, text_rect_electron)
    screen.blit(text_positron, text_rect_positron)
    screen.blit(text_proton, text_rect_proton)
    screen.blit(text_neutron, text_rect_neutron)

    all_particles = electrons + positrons + protons + neutrons + nuclei + hydrogens

    particles_to_remove.clear()

    # ---------------- PHYSICS ----------------
    for i in range(len(all_particles)):
        for j in range(i + 1, len(all_particles)):

            p1 = all_particles[i]
            p2 = all_particles[j]

            direction = p1.position - p2.position
            distance = direction.length()

            if distance == 0:
                continue

            normal = direction.normalize()

            # ---------------- ANNIHILATION ----------------
            if isinstance(p1, Particle) and isinstance(p2, Particle):

                if (p1.name == "electron" and p2.name == "positron") or \
                   (p1.name == "positron" and p2.name == "electron"):

                    if distance <= (p1.radius + p2.radius):

                        spawn = (p1.position + p2.position) * 0.5

                        photons.append(Photon(spawn, normal * 300))
                        photons.append(Photon(spawn, -normal * 300))

                        particles_to_remove.add(p1)
                        particles_to_remove.add(p2)
                        continue

            # ---------------- NUCLEAR BINDING ----------------
            if isinstance(p1, Particle) and isinstance(p2, Particle):

                if {p1.name, p2.name} == {"proton", "neutron"}:

                    rel_speed = (p1.velocity - p2.velocity).length()

                    if distance < 80:

                        force_magnitude = -8000000 * math.exp(-distance / 35) / (distance + 0.1)

                        if rel_speed < 20 and distance < 40:

                            nuclei.append(Nucleus([p1, p2]))

                            particles_to_remove.add(p1)
                            particles_to_remove.add(p2)

                            continue

                if {p1.name, p2.name} == {"proton", "electron"}:
                    rel_speed = (p1.velocity - p2.velocity).length()

                    if distance < 80:

                        force_magnitude = -1200000 * math.exp(-distance / 45) / (distance + 5)

                        # energy loss near proton (this is what actually matters)
                        if distance < 60:
                            p1.velocity *= 0.995
                            p2.velocity *= 0.995

                        # binding condition (now stable)
                        if distance < 25 and rel_speed < 220:

                            hydrogens.append(Hydrogen([p1, p2]))

                            particles_to_remove.add(p1)
                            particles_to_remove.add(p2)

                            continue


            # ---------------- FORCES ----------------
            force_magnitude = 0

            if isinstance(p1, Particle) and isinstance(p2, Particle):

                if p1.name in ["electron", "positron"] or p2.name in ["electron", "positron"]:
                    force_magnitude = 8000000 * (p1.charge * p2.charge) / (distance ** 2 + 100)

                elif p1.name == "proton" and p2.name == "proton":
                    force_magnitude = 200000000 / (distance ** 2 + 1)

                elif "neutron" in [p1.name, p2.name]:
                    force_magnitude = -6000000 * math.exp(-distance / 35) / (distance + 0.1)

            # ---------------- NUCLEUS INTERACTION ----------------
            if isinstance(p1, Nucleus) and isinstance(p2, Particle):
                force_magnitude = -5000000 * math.exp(-distance / 40) / (distance + 0.1)

            if isinstance(p2, Nucleus) and isinstance(p1, Particle):
                force_magnitude = -5000000 * math.exp(-distance / 40) / (distance + 0.1)

            force = force_magnitude * normal

            if isinstance(p1, Particle):
                p1.velocity += (force / p1.mass) * dt
            if isinstance(p2, Particle):
                p2.velocity -= (force / p2.mass) * dt

    # ---------------- REMOVE ----------------
    electrons = [p for p in electrons if p not in particles_to_remove]
    positrons = [p for p in positrons if p not in particles_to_remove]
    protons   = [p for p in protons if p not in particles_to_remove]
    neutrons  = [p for p in neutrons if p not in particles_to_remove]

    # ---------------- UPDATE + DRAW PARTICLES ----------------
    for p in all_particles:

        if p.color is None:
            if p.name == "electron":
                p.color = (255, 0, 0)
            elif p.name == "positron":
                p.color = (255, 165, 0)
            elif p.name == "proton":
                p.color = (0, 255, 0)
            elif p.name == "neutron":
                p.color = (0, 0, 255)

        pygame.draw.circle(screen, p.color, p.position, p.radius)
        p.position += p.velocity * dt

        if p.position.x <= p.radius or p.position.x >= 1280 - p.radius:
            p.velocity.x *= -1
        if p.position.y <= p.radius or p.position.y >= 720 - p.radius:
            p.velocity.y *= -1

    # ---------------- NUCLEI ----------------
    for n in nuclei:
        pygame.draw.circle(screen, n.color, n.position, n.radius)
        n.position += n.velocity * dt

    # --------------- HYDROGEN ----------------

    for h in hydrogens:
        pygame.draw.circle(screen, h.color, h.position, h.radius)
        h.position += h.velocity * dt

    # ---------------- PHOTONS ----------------
    for ph in photons:
        pygame.draw.circle(screen, "grey", ph.position, ph.radius)
        ph.position += ph.velocity * dt
        ph.lifetime -= dt

    photons = [ph for ph in photons if ph.lifetime > 0]

    pygame.display.flip()
    clock.tick(60)

pygame.quit()