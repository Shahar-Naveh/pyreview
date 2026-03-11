"""
Engineering Plotting Utilities
==============================
Standard plot functions with consistent styling for structural engineering.
All plots follow course conventions: labeled axes with units, grids, proper titles.
"""

import numpy as np
import matplotlib.pyplot as plt


# Default style for all engineering plots
STYLE = {
    'linewidth': 2,
    'grid': True,
    'dpi': 150,
    'figsize_single': (10, 5),
    'figsize_double': (10, 8),
    'figsize_triple': (12, 10),
    'fill_alpha': 0.3,
}


def plot_sfd_bmd(x, V, M, title="Beam Diagrams", save_path=None):
    """
    Plot Shear Force Diagram and Bending Moment Diagram.

    Parameters
    ----------
    x : array — positions along beam [m]
    V : array — shear force values [kN]
    M : array — bending moment values [kN·m]
    title : str — overall figure title
    save_path : str or None — if given, saves the figure to this path
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=STYLE['figsize_double'], sharex=True)
    fig.suptitle(title, fontsize=14, fontweight='bold')

    # SFD
    ax1.plot(x, V, 'b-', linewidth=STYLE['linewidth'])
    ax1.fill_between(x, V, alpha=STYLE['fill_alpha'], color='blue')
    ax1.set_ylabel('Shear Force V [kN]')
    ax1.set_title('Shear Force Diagram (SFD)')
    ax1.grid(STYLE['grid'])
    ax1.axhline(y=0, color='k', linewidth=0.5)

    # Annotate max/min shear
    v_max_idx = np.argmax(np.abs(V))
    ax1.annotate(f'V_max = {V[v_max_idx]:.2f} kN',
                 xy=(x[v_max_idx], V[v_max_idx]),
                 fontsize=9, ha='center',
                 xytext=(0, 15), textcoords='offset points',
                 arrowprops=dict(arrowstyle='->', color='blue'))

    # BMD
    ax2.plot(x, M, 'r-', linewidth=STYLE['linewidth'])
    ax2.fill_between(x, M, alpha=STYLE['fill_alpha'], color='red')
    ax2.set_ylabel('Bending Moment M [kN·m]')
    ax2.set_xlabel('Position x [m]')
    ax2.set_title('Bending Moment Diagram (BMD)')
    ax2.grid(STYLE['grid'])
    ax2.axhline(y=0, color='k', linewidth=0.5)

    # Annotate max/min moment
    m_max_idx = np.argmax(np.abs(M))
    ax2.annotate(f'M_max = {M[m_max_idx]:.2f} kN·m',
                 xy=(x[m_max_idx], M[m_max_idx]),
                 fontsize=9, ha='center',
                 xytext=(0, 15), textcoords='offset points',
                 arrowprops=dict(arrowstyle='->', color='red'))

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=STYLE['dpi'], bbox_inches='tight')
    plt.show()
    return fig


def plot_internal_forces(x, N, V, M, title="Internal Force Diagrams", save_path=None):
    """
    Plot Normal force, Shear force, and Bending moment diagrams (for frames/bars).

    Parameters
    ----------
    x : array — position along member [m]
    N : array — normal (axial) force [kN]
    V : array — shear force [kN]
    M : array — bending moment [kN·m]
    """
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=STYLE['figsize_triple'], sharex=True)
    fig.suptitle(title, fontsize=14, fontweight='bold')

    for ax, data, label, color in [
        (ax1, N, 'Normal Force N [kN]', 'green'),
        (ax2, V, 'Shear Force V [kN]', 'blue'),
        (ax3, M, 'Bending Moment M [kN·m]', 'red'),
    ]:
        ax.plot(x, data, color=color, linewidth=STYLE['linewidth'])
        ax.fill_between(x, data, alpha=STYLE['fill_alpha'], color=color)
        ax.set_ylabel(label)
        ax.grid(STYLE['grid'])
        ax.axhline(y=0, color='k', linewidth=0.5)

    ax3.set_xlabel('Position x [m]')
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=STYLE['dpi'], bbox_inches='tight')
    plt.show()
    return fig


def plot_diagram(x, y, xlabel, ylabel, title, save_path=None, color='b'):
    """
    Generic single engineering diagram with standard styling.
    """
    fig, ax = plt.subplots(figsize=STYLE['figsize_single'])
    ax.plot(x, y, color=color, linewidth=STYLE['linewidth'])
    ax.fill_between(x, y, alpha=STYLE['fill_alpha'], color=color)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(STYLE['grid'])
    ax.axhline(y=0, color='k', linewidth=0.5)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=STYLE['dpi'], bbox_inches='tight')
    plt.show()
    return fig


def plot_parametric(param_values, results, param_name, result_name,
                    title="Parametric Study", save_path=None):
    """
    Plot results of a parametric study.

    Parameters
    ----------
    param_values : array — the varying parameter values
    results : array — computed results for each parameter value
    param_name : str — label for x-axis (include units)
    result_name : str — label for y-axis (include units)
    """
    fig, ax = plt.subplots(figsize=STYLE['figsize_single'])
    ax.plot(param_values, results, 'bo-', linewidth=STYLE['linewidth'], markersize=6)
    ax.set_xlabel(param_name)
    ax.set_ylabel(result_name)
    ax.set_title(title)
    ax.grid(STYLE['grid'])
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=STYLE['dpi'], bbox_inches='tight')
    plt.show()
    return fig
