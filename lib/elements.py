"""
1D Element Analysis
===================
Functions for axial bar/rod analysis: stress, strain, elongation, thermal effects.
All formulas follow course conventions (tension = positive).
"""

import numpy as np


def axial_stress(N, A):
    """
    Normal stress in a bar.

    Parameters
    ----------
    N : float or array — internal axial force [N or kN]
    A : float or array — cross-sectional area [m² or mm²]
        (use consistent units with N)

    Returns
    -------
    float or array — normal stress σ = N/A [Pa or MPa]
    """
    return N / A


def axial_strain(sigma, E):
    """
    Normal strain from Hooke's law.

    Parameters
    ----------
    sigma : float or array — normal stress [Pa or MPa]
    E : float — Young's modulus [Pa or MPa] (same units as sigma)

    Returns
    -------
    float or array — normal strain ε = σ/E [dimensionless]
    """
    return sigma / E


def elongation(N, L, A, E):
    """
    Elongation of a prismatic bar under axial force.

    δ = NL / (AE)

    Parameters
    ----------
    N : float — axial force [N]
    L : float — length [m]
    A : float — cross-sectional area [m²]
    E : float — Young's modulus [Pa]

    Returns
    -------
    float — elongation δ [m]
    """
    return (N * L) / (A * E)


def elongation_composite(segments):
    """
    Total elongation of a bar with multiple segments (different N, L, A, or E).

    δ_total = Σ (Ni * Li) / (Ai * Ei)

    Parameters
    ----------
    segments : list of dicts, each with keys 'N', 'L', 'A', 'E'

    Returns
    -------
    float — total elongation [same units as L]
    """
    return sum(seg['N'] * seg['L'] / (seg['A'] * seg['E']) for seg in segments)


def thermal_strain(alpha, delta_T):
    """
    Thermal strain.

    Parameters
    ----------
    alpha : float — coefficient of thermal expansion [1/°C]
    delta_T : float — temperature change [°C]

    Returns
    -------
    float — thermal strain ε_T = α·ΔT [dimensionless]
    """
    return alpha * delta_T


def thermal_elongation(alpha, delta_T, L):
    """
    Thermal elongation of an unrestrained bar.

    δ_T = α · ΔT · L

    Parameters
    ----------
    alpha : float — coefficient of thermal expansion [1/°C]
    delta_T : float — temperature change [°C]
    L : float — original length [m]

    Returns
    -------
    float — thermal elongation [m]
    """
    return alpha * delta_T * L


def thermal_stress_restrained(E, alpha, delta_T):
    """
    Stress in a fully restrained bar due to temperature change.

    σ = E · α · ΔT

    Parameters
    ----------
    E : float — Young's modulus [Pa]
    alpha : float — coefficient of thermal expansion [1/°C]
    delta_T : float — temperature change [°C]

    Returns
    -------
    float — thermal stress [Pa] (compressive if heated, tensile if cooled)
    """
    return E * alpha * delta_T


def analyze_bar(N, L, A, E, name="Bar"):
    """
    Complete analysis of a prismatic bar: stress, strain, elongation.

    Returns a dict with all computed values and prints a summary.
    """
    sigma = axial_stress(N, A)
    eps = axial_strain(sigma, E)
    delta = elongation(N, L, A, E)

    result = {
        'name': name,
        'N': N, 'L': L, 'A': A, 'E': E,
        'stress': sigma,
        'strain': eps,
        'elongation': delta,
    }

    state = "tension" if N > 0 else "compression" if N < 0 else "unloaded"
    print(f"--- {name} ({state}) ---")
    print(f"  N = {N:.2f}")
    print(f"  σ = {sigma:.4f}")
    print(f"  ε = {eps:.6e}")
    print(f"  δ = {delta:.6e}")

    return result
