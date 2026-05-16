from vpython import *

# Set up the visual display
scene = canvas(title="Proton Repulsion Simulation")

# Define proton properties (charge and mass)
q_proton = 1.6e-19  # Coulombs
m_proton = 1.67e-27 # kg
k_coulomb = 8.99e9  # N*m^2/C^2

# Create two protons in the 3D space
proton1 = sphere(pos=vector(-1e-10, 0, 0), radius=1e-11, color=color.red, make_trail=True)
proton2 = sphere(pos=vector(1e-10, 0, 0), radius=1e-11, color=color.red, make_trail=True)

# Give them an initial velocity of zero
proton1.velocity = vector(0, 0, 0)
proton2.velocity = vector(0, 0, 0)

dt = 1e-20 # Time step for the simulation

while True:
    rate(100) # Frames per second limit
    
    # Calculate the vector distance and magnitude between the two protons
    r_vec = proton2.pos - proton1.pos
    r_mag = mag(r_vec)
    
    # Calculate Coulomb's Force
    force_mag = (k_coulomb * q_proton**2) / (r_mag**2)
    
    # Determine the force vectors (pushing away from each other)
    force_vec = force_mag * norm(r_vec)
    
    # Apply Newton's Second Law: F = ma (acceleration = Force / mass)
    acc1 = -force_vec / m_proton
    acc2 = force_vec / m_proton
    
    # Update velocity and position
    proton1.velocity = proton1.velocity + acc1 * dt
    proton1.pos = proton1.pos + proton1.velocity * dt
    
    proton2.velocity = proton2.velocity + acc2 * dt
    proton2.pos = proton2.pos + proton2.velocity * dt
