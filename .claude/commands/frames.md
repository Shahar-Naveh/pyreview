Analyze a statically determinate frame for internal forces.

Steps to follow:
1. Parse the frame geometry: members, joints, supports (pin, roller, fixed)
2. Identify loads: point forces, distributed loads, moments on members
3. Draw a free body diagram of the entire frame (describe in comments)
4. Calculate support reactions using global equilibrium:
   - ΣFx = 0
   - ΣFy = 0
   - ΣM = 0 (about a convenient point)
5. Isolate each member and solve for internal forces at joints:
   - Normal force N (axial)
   - Shear force V
   - Bending moment M
6. If the frame has an internal hinge: use the hinge condition (M = 0 at hinge) as an additional equation
7. Plot internal force diagrams (N, V, M) along each member
8. Print all results with units

Analysis approach:
- For each member, set up a local coordinate system along the member axis
- Use the method of sections or member equilibrium to find N(x), V(x), M(x)
- At joints: ensure equilibrium of forces and moments

Key concepts:
- Three-hinged frames: statically determinate, use hinge condition
- L-frames and portal frames: common configurations
- Rigid joints transfer moment; hinged joints do not

Sign convention:
- Positive N = tension
- Positive V = clockwise rotation (same as beams)
- Positive M = sagging (concave up, tension on bottom)

Code pattern:
```python
import numpy as np
import matplotlib.pyplot as plt

# Define frame geometry
# Example: L-frame with vertical column and horizontal beam
col_height = 4.0   # column height [m]
beam_length = 6.0   # beam length [m]

# After solving reactions and internal forces:
fig, axes = plt.subplots(1, 3, figsize=(15, 6))

titles = ['Normal Force N [kN]', 'Shear Force V [kN]', 'Bending Moment M [kN·m]']
for ax, title in zip(axes, titles):
    ax.set_title(title)
    ax.grid(True)
    ax.set_aspect('equal')
    ax.axhline(y=0, color='k', linewidth=0.5)

plt.tight_layout()
plt.savefig('frame_diagrams.png', dpi=150)
plt.show()
```
