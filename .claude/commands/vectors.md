Help with vector calculus for structural engineering using numpy.

Capabilities:
- Define force vectors in 2D [Fx, Fy] and 3D [Fx, Fy, Fz]
- Sum of forces in a system: resultant force R = sum(Fi)
- Moment about a point: M = r × F (cross product)
- Moment about an axis: M_axis = (r × F) · unit_axis
- Unit vectors and direction cosines
- Resolve forces into components
- Check equilibrium conditions

Always use numpy arrays for vectors. Show the mathematical formulation in comments before the code.

Example pattern:
```python
import numpy as np

# Define force vectors [Fx, Fy, Fz] in Newtons
F1 = np.array([100, 200, 0])  # N
F2 = np.array([-50, 150, 0])  # N

# Resultant force
R = F1 + F2
print(f"Resultant: R = {R} N")
print(f"|R| = {np.linalg.norm(R):.2f} N")

# Moment about origin: M = r × F
r1 = np.array([2, 0, 0])  # m (position of F1)
M = np.cross(r1, F1)
print(f"Moment about O: M = {M} N·m")
```
