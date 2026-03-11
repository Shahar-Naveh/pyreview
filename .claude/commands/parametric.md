Perform a parametric study on a structural engineering problem.

Steps:
1. Identify the parameter to vary (length, load, cross-section, material, etc.)
2. Define the range and number of points for the parameter
3. Calculate the response (stress, displacement, reactions, etc.) for each parameter value
4. Create clear visualizations showing how the response changes
5. Analyze trends and identify critical values
6. Summarize findings

Pattern:
```python
import numpy as np
import matplotlib.pyplot as plt

# Parameter range
L_values = np.linspace(1, 10, 50)  # beam length [m]
results = []

for L in L_values:
    # Calculate response for this parameter value
    result = some_calculation(L)
    results.append(result)

results = np.array(results)

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(L_values, results[:, 0], 'b-o', markersize=3)
axes[0].set_xlabel('Beam Length L [m]')
axes[0].set_ylabel('Max Deflection [mm]')
axes[0].set_title('Deflection vs Beam Length')
axes[0].grid(True)

axes[1].plot(L_values, results[:, 1], 'r-o', markersize=3)
axes[1].set_xlabel('Beam Length L [m]')
axes[1].set_ylabel('Max Stress [MPa]')
axes[1].set_title('Stress vs Beam Length')
axes[1].grid(True)

plt.tight_layout()
plt.savefig('parametric_study.png', dpi=150)
plt.show()
```

When using pandas for data analysis:
```python
import pandas as pd
df = pd.DataFrame({'L [m]': L_values, 'δ_max [mm]': results[:, 0], 'σ_max [MPa]': results[:, 1]})
print(df.describe())
```
