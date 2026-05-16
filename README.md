A 2D particle simulation built in Python using PyGame that models motion using Newtonian mechanics. 
Particles have mass, charge, velocity, and radius, and interact through simplified classical forces.

Long-range interactions are handled using Coulomb’s law to simulate electromagnetic attraction and repulsion between charged particles. 
In addition, a short-range exponential attraction term is used as a custom cohesion rule to encourage clustering when particles are very close, 
rather than representing any real nuclear force.

The system also includes rule-based event behaviour: electron–positron collisions produce photon particles to represent energy release,
while proton–electron and proton–neutron interactions can form stable grouped states when particles are close together and have low 
relative velocity. These grouped states (“hydrogen” and “nuclei”) are simplified composite objects used for visual and behavioural structure, 
not physically accurate atomic or nuclear models.

Overall, the simulation is a deterministic classical sandbox designed to produce emergent behaviour like orbiting, clustering, 
and collision-based transformations, rather than to replicate real quantum mechanics, chemistry, or nuclear physics.
