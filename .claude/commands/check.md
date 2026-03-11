Check and verify an engineering solution for correctness.

Verification steps:
1. **Equilibrium check**: ΣFx = 0, ΣFy = 0, ΣM = 0 (must all be ≈ 0)
2. **Units check**: All values have consistent units, conversions are correct
3. **Sign convention check**: Forces, moments, stresses follow stated conventions
4. **Boundary conditions**: Support conditions are correctly applied
5. **Physical reasonableness**: Do the magnitudes make engineering sense?
6. **Numerical accuracy**: Using np.isclose() for comparisons, no floating-point traps
7. **Plot verification**: Diagrams match expected shapes (e.g., linear V → parabolic M)

Run the solution and add verification code:
```python
# Equilibrium check
print("\n--- Verification ---")
print(f"ΣFx = {sum_Fx:.6f} N  (should be ≈ 0)")
print(f"ΣFy = {sum_Fy:.6f} N  (should be ≈ 0)")
print(f"ΣM  = {sum_M:.6f} N·m (should be ≈ 0)")
assert np.isclose(sum_Fx, 0, atol=1e-6), "Equilibrium violated in x!"
assert np.isclose(sum_Fy, 0, atol=1e-6), "Equilibrium violated in y!"
assert np.isclose(sum_M, 0, atol=1e-6), "Moment equilibrium violated!"
print("✓ All checks passed")
```
