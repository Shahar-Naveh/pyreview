"""
Equilibrium Utilities
=====================
Functions for checking and solving static equilibrium in 2D and 3D.
"""

import numpy as np


def check_equilibrium_2d(forces, moments_about_origin=None, tol=1e-6):
    """
    Check if a 2D system is in static equilibrium.

    Parameters
    ----------
    forces : array of shape (n, 2) — each row is [Fx, Fy] in [N] or [kN]
    moments_about_origin : array of shape (n,) — moment contributions about origin [N·m or kN·m]
        If None, only force equilibrium is checked.
    tol : float — tolerance for equilibrium check

    Returns
    -------
    dict with keys: 'Fx_sum', 'Fy_sum', 'M_sum', 'in_equilibrium'
    """
    forces = np.atleast_2d(forces)
    fx_sum = np.sum(forces[:, 0])
    fy_sum = np.sum(forces[:, 1])

    result = {
        'Fx_sum': fx_sum,
        'Fy_sum': fy_sum,
        'in_equilibrium': np.isclose(fx_sum, 0, atol=tol) and np.isclose(fy_sum, 0, atol=tol),
    }

    if moments_about_origin is not None:
        m_sum = np.sum(moments_about_origin)
        result['M_sum'] = m_sum
        result['in_equilibrium'] = result['in_equilibrium'] and np.isclose(m_sum, 0, atol=tol)

    return result


def solve_reactions_simply_supported(L, loads):
    """
    Solve reactions for a simply supported beam (pin at x=0, roller at x=L).

    Parameters
    ----------
    L : float — beam length [m]
    loads : list of dicts, each with:
        - 'type': 'point' or 'distributed'
        - For 'point': 'P' (force, downward positive) [kN], 'x' (location) [m]
        - For 'distributed': 'w' (intensity, downward positive) [kN/m],
          'x_start' [m], 'x_end' [m]
        - For 'moment': 'M' (moment, CCW positive) [kN·m], 'x' (location) [m]

    Returns
    -------
    dict: {'Ay': float, 'By': float} — vertical reactions at A (x=0) and B (x=L) [kN]
    """
    # Sum moments about A (x=0) to find By
    moment_about_A = 0.0
    total_Fy = 0.0

    for load in loads:
        if load['type'] == 'point':
            P = load['P']
            x = load['x']
            moment_about_A += P * x
            total_Fy += P
        elif load['type'] == 'distributed':
            w = load['w']
            x_start = load['x_start']
            x_end = load['x_end']
            resultant = w * (x_end - x_start)
            centroid = (x_start + x_end) / 2.0
            moment_about_A += resultant * centroid
            total_Fy += resultant
        elif load['type'] == 'moment':
            moment_about_A += load['M']

    By = moment_about_A / L
    Ay = total_Fy - By

    return {'Ay': Ay, 'By': By}


def moment_about_point(forces, positions, point):
    """
    Compute total moment of a set of 2D forces about a given point.

    Parameters
    ----------
    forces : array of shape (n, 2) — [Fx, Fy] per force
    positions : array of shape (n, 2) — [x, y] application points
    point : array of shape (2,) — [x, y] of the moment center

    Returns
    -------
    float — total moment (positive = CCW)
    """
    forces = np.atleast_2d(forces)
    positions = np.atleast_2d(positions)
    point = np.asarray(point)

    r = positions - point  # position vectors from point
    # M = r × F = rx*Fy - ry*Fx (scalar for 2D)
    moments = r[:, 0] * forces[:, 1] - r[:, 1] * forces[:, 0]
    return np.sum(moments)


def moment_about_point_3d(forces, positions, point):
    """
    Compute total moment of 3D forces about a given point.

    Parameters
    ----------
    forces : array of shape (n, 3) — [Fx, Fy, Fz] per force
    positions : array of shape (n, 3) — [x, y, z] application points
    point : array of shape (3,) — moment center

    Returns
    -------
    array of shape (3,) — moment vector [Mx, My, Mz]
    """
    forces = np.atleast_2d(forces)
    positions = np.atleast_2d(positions)
    point = np.asarray(point)

    r = positions - point
    moments = np.cross(r, forces)
    return np.sum(moments, axis=0)
