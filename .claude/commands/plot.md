Create engineering plots and diagrams using matplotlib.

Guidelines:
- Always label axes with variable name AND units: "Force F [kN]", "Position x [m]"
- Always include a title
- Use grid lines (ax.grid(True))
- Use tight_layout() to prevent label clipping
- Save to PNG with dpi=150 for good quality
- For structural diagrams: fill_between for shear/moment areas
- Use proper sign conventions in the plots

Common plot types for this course:
1. **Force diagrams**: Arrows showing force vectors on a structure
2. **SFD/BMD**: Shear force and bending moment diagrams (stacked subplots)
3. **Stress/strain**: σ-ε diagrams, stress distribution across cross-section
4. **Parametric**: Response vs parameter curves
5. **Deformed shape**: Original + deformed structure overlay

Template:
```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y, 'b-', linewidth=2, label='Result')
ax.set_xlabel('x [m]')
ax.set_ylabel('y [kN]')
ax.set_title('Descriptive Title')
ax.legend()
ax.grid(True)
ax.axhline(y=0, color='k', linewidth=0.5)
plt.tight_layout()
plt.savefig('plot_name.png', dpi=150, bbox_inches='tight')
plt.show()
```
