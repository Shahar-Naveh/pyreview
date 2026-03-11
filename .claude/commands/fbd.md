Create a detailed Free Body Diagram description for the given structural problem.

Steps:
1. Identify the structure type (beam, truss, frame, bar, cable)
2. Identify and list all supports with their reaction components:
   - Pin support: Rx, Ry (2 reactions)
   - Roller support: R perpendicular to surface (1 reaction)
   - Fixed support: Rx, Ry, M (3 reactions)
3. Identify all applied loads:
   - Point forces: magnitude, direction, location
   - Distributed loads: intensity (w), type (uniform, triangular, trapezoidal), span
   - Concentrated moments: magnitude, direction (CW/CCW), location
4. Identify self-weight if relevant
5. Draw the FBD as structured comments in Python code
6. Check determinacy: count unknowns vs equations (3 for 2D)

Output format — describe the FBD as a structured Python comment block:
```python
# ============================================================
# FREE BODY DIAGRAM
# ============================================================
#
#     P = 10 kN
#     ↓
#     |
# ----+--------+--------+----
# ^                           ○
# Pin (A)                  Roller (B)
# Ax→, Ay↑                   By↑
#
# Applied loads:
#   - P = 10 kN downward at x = 2 m
#   - w = 5 kN/m uniform from x = 3 m to x = 6 m
#
# Support reactions:
#   - A (pin):    Ax [kN] →, Ay [kN] ↑
#   - B (roller): By [kN] ↑
#
# Unknowns: 3 (Ax, Ay, By)
# Equations: 3 (ΣFx, ΣFy, ΣM)
# → Statically determinate
# ============================================================
```

After describing the FBD, proceed to solve for reactions using equilibrium.

Common support symbols:
- Pin:    △ or ^  (provides Rx, Ry)
- Roller: ○      (provides R normal to surface)
- Fixed:  |||    (provides Rx, Ry, M)
- Hinge:  ●      (internal, M = 0 at this point)
