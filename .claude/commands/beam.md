Analyze a statically determinate beam problem.

Steps to follow:
1. Parse the beam geometry: length, supports (pin, roller, fixed), loads (point, distributed, moment)
2. Draw a free body diagram (describe in comments)
3. Calculate support reactions using equilibrium equations:
   - ΣFx = 0
   - ΣFy = 0
   - ΣM = 0 (about a convenient point)
4. Calculate internal forces along the beam using the method of sections:
   - Shear force V(x)
   - Bending moment M(x)
5. Plot the Shear Force Diagram (SFD) and Bending Moment Diagram (BMD)
6. Find and label maximum values of V and M
7. Print all results with units

Plotting conventions:
- Positive shear: causes clockwise rotation
- Positive moment: causes sagging (concave up)
- BMD is typically drawn on the tension side
- Use matplotlib with proper labels, units, and grid

Code pattern:
```python
import numpy as np
import matplotlib.pyplot as plt

L = 6.0  # beam length [m]
x = np.linspace(0, L, 1000)

# After calculating V(x) and M(x):
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

ax1.plot(x, V, 'b-', linewidth=2)
ax1.fill_between(x, V, alpha=0.3)
ax1.set_ylabel('Shear Force V [kN]')
ax1.set_title('Shear Force Diagram (SFD)')
ax1.grid(True)
ax1.axhline(y=0, color='k', linewidth=0.5)

ax2.plot(x, M, 'r-', linewidth=2)
ax2.fill_between(x, M, alpha=0.3)
ax2.set_ylabel('Bending Moment M [kN·m]')
ax2.set_xlabel('Position x [m]')
ax2.set_title('Bending Moment Diagram (BMD)')
ax2.grid(True)
ax2.axhline(y=0, color='k', linewidth=0.5)

plt.tight_layout()
plt.savefig('beam_diagrams.png', dpi=150)
plt.show()
```
