"""
Beam Analysis Utilities
=======================
Functions for computing shear force and bending moment distributions
in statically determinate beams.
"""

import numpy as np


def shear_moment_simply_supported(L, loads, n_points=1000):
    """
    Compute V(x) and M(x) for a simply supported beam (pin at A, roller at B).

    Parameters
    ----------
    L : float — beam length [m]
    loads : list of dicts, each with:
        - 'type': 'point', 'distributed', or 'moment'
        - 'point':       {'P': float [kN], 'x': float [m]}
        - 'distributed': {'w': float [kN/m], 'x_start': float, 'x_end': float}
        - 'moment':      {'M': float [kN·m], 'x': float [m]}
    n_points : int — number of evaluation points

    Returns
    -------
    x : array — positions [m]
    V : array — shear force [kN]
    M : array — bending moment [kN·m]
    reactions : dict — {'Ay': float, 'By': float}
    """
    from .equilibrium import solve_reactions_simply_supported

    reactions = solve_reactions_simply_supported(L, loads)
    Ay, By = reactions['Ay'], reactions['By']

    x = np.linspace(0, L, n_points)
    V = np.zeros_like(x)
    M = np.zeros_like(x)

    # Add reaction at A
    V += Ay

    for load in loads:
        if load['type'] == 'point':
            P = load['P']
            x_load = load['x']
            # Point load: subtract P after x_load
            V -= P * (x >= x_load)
            M += Ay * x  # will be overwritten below
        elif load['type'] == 'distributed':
            w = load['w']
            x_start = load['x_start']
            x_end = load['x_end']
            # Distributed load contribution
            in_load = (x >= x_start) & (x <= x_end)
            past_load = x > x_end
            V -= w * np.where(in_load, x - x_start, 0)
            V -= w * (x_end - x_start) * past_load
        elif load['type'] == 'moment':
            M_applied = load['M']
            x_load = load['x']
            V += 0  # moments don't affect shear
            # Moment causes a jump in M (handled below)

    # Recompute M by integrating V (more reliable)
    dx = x[1] - x[0]
    M = np.cumsum(V) * dx

    # Apply moment jumps
    for load in loads:
        if load['type'] == 'moment':
            M_applied = load['M']
            x_load = load['x']
            M -= M_applied * (x >= x_load)

    return x, V, M, reactions


def shear_moment_cantilever(L, loads, n_points=1000):
    """
    Compute V(x) and M(x) for a cantilever beam (fixed at x=0, free at x=L).

    Parameters
    ----------
    L : float — beam length [m]
    loads : list of dicts (same format as shear_moment_simply_supported)
    n_points : int — number of evaluation points

    Returns
    -------
    x, V, M, reactions (reactions include 'Ay' and 'MA')
    """
    x = np.linspace(0, L, n_points)

    # Calculate reactions: ΣFy = 0 and ΣM_A = 0
    total_force = 0.0
    total_moment = 0.0  # about fixed end (x=0)

    for load in loads:
        if load['type'] == 'point':
            total_force += load['P']
            total_moment += load['P'] * load['x']
        elif load['type'] == 'distributed':
            w = load['w']
            x_start = load['x_start']
            x_end = load['x_end']
            resultant = w * (x_end - x_start)
            centroid = (x_start + x_end) / 2.0
            total_force += resultant
            total_moment += resultant * centroid
        elif load['type'] == 'moment':
            total_moment += load['M']

    Ay = total_force  # reaction force (upward)
    MA = total_moment  # reaction moment (CCW)

    reactions = {'Ay': Ay, 'MA': MA}

    # Build V(x) starting from fixed end
    V = np.full_like(x, Ay)
    for load in loads:
        if load['type'] == 'point':
            V -= load['P'] * (x >= load['x'])
        elif load['type'] == 'distributed':
            w = load['w']
            x_start = load['x_start']
            x_end = load['x_end']
            in_load = (x >= x_start) & (x <= x_end)
            past_load = x > x_end
            V -= w * np.where(in_load, x - x_start, 0)
            V -= w * (x_end - x_start) * past_load

    # M(x) by integration
    dx = x[1] - x[0]
    M = np.cumsum(V) * dx - MA

    # Apply moment jumps
    for load in loads:
        if load['type'] == 'moment':
            M -= load['M'] * (x >= load['x'])

    return x, V, M, reactions


def find_max_shear_moment(x, V, M):
    """
    Find maximum absolute values of shear and moment with their locations.

    Returns
    -------
    dict with: V_max, V_max_x, M_max, M_max_x
    """
    v_idx = np.argmax(np.abs(V))
    m_idx = np.argmax(np.abs(M))

    return {
        'V_max': V[v_idx],
        'V_max_x': x[v_idx],
        'M_max': M[m_idx],
        'M_max_x': x[m_idx],
    }
