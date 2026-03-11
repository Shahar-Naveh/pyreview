# Python for Civil Engineering — Workspace

## Context
This is a course workspace for **Computer Applications in Civil Engineering** (SCE, 2025-2026).
The student is learning Python for engineering calculations. All problems involve structural/civil engineering.

## Course Topics (in order)
1. **Python refresher** — basics, functions, loops, lists
2. **Vector calculus with numpy** — force summation, moments about a point, moments about an axis
3. **1D element** — internal forces, stresses, strains, elongation formula
4. **Plotting** — matplotlib diagrams for engineering results
5. **Statically determinate beams** — reactions, shear force diagrams (SFD), bending moment diagrams (BMD)
6. **Frames** — internal forces in statically determinate frames
7. **Parametric studies** — varying parameters, data analysis, visualization

## How to Help
- When given a problem: solve it step-by-step with clear Python code
- Always use **numpy** for vector/matrix operations
- Always use **matplotlib** for plots
- Use proper engineering conventions (sign conventions, units, free body diagrams described in comments)
- Write clean, well-commented code that a student can learn from
- If a Jupyter notebook is needed, create it in `notebooks/`
- Homework solutions go in `homework/hw1/`, `homework/hw2/`, `homework/hw3/`

## Engineering Conventions
- Forces: positive = tension, negative = compression (for axial)
- Beams: positive shear = clockwise rotation, positive moment = sagging (concave up)
- Units: always state units in comments and plot labels (N, kN, m, mm, Pa, MPa)
- Coordinate system: x = horizontal (right+), y = vertical (up+)

## Code Style
- Use numpy vectorized operations, not Python loops over arrays
- Include docstrings explaining the engineering problem
- Label all plot axes with units
- Use `np.isclose()` for floating-point comparisons, never `==`

## Project Structure
```
homework/       — Homework solutions (hw1, hw2, hw3)
notebooks/      — Jupyter notebooks for exercises
docker/         — Docker setup for running Python + Jupyter
project-tasks.md — Course syllabus and requirements
```

## Docker
Run `docker compose up` to start a Jupyter Lab environment with all dependencies.
Access at http://localhost:8888

## Testing
Run solutions with: `python homework/hw1/solution.py`
Run in Docker: `docker compose run python python homework/hw1/solution.py`
