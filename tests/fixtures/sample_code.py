"""Sample Python file for testing pyreview.

This file deliberately contains various issues for the review agents to catch.
"""

import os
import pickle
import numpy as np


# Security issue: command injection
def run_user_command(user_input):
    os.system(user_input)


# Security issue: insecure deserialization
def load_data(filepath):
    with open(filepath, "rb") as f:
        return pickle.load(f)


# Performance issue: Python loop over numpy array
def calculate_total_force(forces):
    """Sum all force vectors (each is [Fx, Fy, Fz])."""
    total = np.zeros(3)
    for force in forces:
        for i in range(3):
            total[i] = total[i] + force[i]
    return total


# Style issue: magic numbers, no type hints, poor naming
def calc(a, b, c):
    x = a * 9.81
    y = b * 0.001
    z = c * 1000000
    if x > 100:
        if y < 0.5:
            if z > 500:
                return x + y + z
    return 0


# Architecture issue: god function doing too much
def process_everything(data, filepath, user_cmd):
    result = load_data(filepath)
    forces = [[d * 9.81, 0, 0] for d in data]
    total = calculate_total_force(forces)
    run_user_command(user_cmd)
    output = calc(total[0], total[1], total[2])
    with open("output.txt", "w") as f:
        f.write(str(output))
    return output


# Engineering issue: wrong moment calculation
def moment_about_point(force, position, point):
    """Calculate moment of force about a point.

    Should be M = r x F where r = position - point
    """
    r = position - point
    # Bug: should be cross product, not dot product
    moment = np.dot(r, force)
    return moment
