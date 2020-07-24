# -*- coding: utf-8 -*-
"""Orientation models."""
import numpy as np

from .closures import compute_closure


def jeffery_ode(a, t, xi, L, **kwargs):
    """ODE describing Jeffery's model.

    Arguments
    ---------
        a (9x1 doubles): Flattened fiber orientation tensor

        t (double): time of evaluation

        xi (double): Shape factor computed from aspect ratio

        L (function handle): function to compute velocity gradient at time t

    Reference:
    G.B. Jeffery, 'The motion of ellipsoidal particles immersed
    in a viscous fluid', Proceedings of the Royal Society A, 1922.
    https://doi.org/10.1098/rspa.1922.0078
    """
    a = np.reshape(a, (3, 3))
    A = compute_closure(a)
    D = 0.5 * (L(t) + np.transpose(L(t)))
    W = 0.5 * (L(t) - np.transpose(L(t)))

    dadt = (
        np.einsum("ik,kj->ij", W, a)
        - np.einsum("ik,kj->ij", a, W)
        + xi
        * (
            np.einsum("ik,kj->ij", D, a)
            + np.einsum("ik,kj->ij", a, D)
            - 2 * np.einsum("ijkl,kl->ij", A, D)
        )
    )
    return dadt.ravel()


def folgar_tucker_ode(a, t, xi, L, Ci=0.0, **kwargs):
    """ODE describing the Folgar-Tucker model.

    Arguments
    ---------
        a (9x1 doubles): Flattened fiber orientation tensor

        t (double): time of evaluation

        xi (double): Shape factor computed from aspect ratio

        L (function handle): function to compute velocity gradient at time t

        Ci (double): Fiber interaction constant (typically 0 < Ci < 0.1)

    Reference:
    F. Folgar, C.L. Tucker III, 'Orientation behavior of fibers in concentrated
    suspensions', Journal of Reinforced Plastic Composites 3, 98-119, 1984.
    https://doi.org/10.1177%2F073168448400300201
    """
    a = np.reshape(a, (3, 3))
    A = compute_closure(a)
    D = 0.5 * (L(t) + np.transpose(L(t)))
    W = 0.5 * (L(t) - np.transpose(L(t)))
    G = np.sqrt(2.0 * np.einsum("ij,ij", D, D))
    delta = np.eye(3)

    dadt = (
        np.einsum("ik,kj->ij", W, a)
        - np.einsum("ik,kj->ij", a, W)
        + xi
        * (
            np.einsum("ik,kj->ij", D, a)
            + np.einsum("ik,kj->ij", a, D)
            - 2 * np.einsum("ijkl,kl->ij", A, D)
        )
        + 2 * Ci * G * (delta - 3 * a)
    )
    return dadt.ravel()


def maier_saupe_ode(a, t, xi, L, Ci=0.0, U0=0.0, **kwargs):
    """ODE using Folgar-Tucker constant and Maier-Saupe potential.

    Arguments
    ---------
        a (9x1 doubles): Flattened fiber orientation tensor

        t (double): time of evaluation

        xi (double): Shape factor computed from aspect ratio

        L (function handle): function to compute velocity gradient at time t

        Ci (double): Fiber interaction constant (typically 0 < Ci < 0.1)

        U0 (double): Maier-Saupe Potential (in 3D stable for y U0 < 8 Ci)

    Reference:
    Arnulf Latz, Uldis Strautins, Dariusz Niedziela, 'Comparative numerical
    study of two concentrated fiber suspension models', Journal of
    Non-Newtonian Fluid Mechanics 165, 764-781, 2010.
    https://doi.org/10.1016/j.jnnfm.2010.04.001
    """
    a = np.reshape(a, (3, 3))
    A = compute_closure(a)
    D = 0.5 * (L(t) + np.transpose(L(t)))
    W = 0.5 * (L(t) - np.transpose(L(t)))
    G = np.sqrt(2.0 * np.einsum("ij,ij", D, D))
    delta = np.eye(3)

    dadt = (
        np.einsum("ik,kj->ij", W, a)
        - np.einsum("ik,kj->ij", a, W)
        + xi
        * (
            np.einsum("ik,kj->ij", D, a)
            + np.einsum("ik,kj->ij", a, D)
            - 2 * np.einsum("ijkl,kl->ij", A, D)
        )
        + 2
        * G
        * (
            Ci * (delta - 3 * a)
            + U0
            * (np.einsum("ik,kj->ij", a, a) - np.einsum("ijkl,kl->ij", A, a))
        )
    )
    return dadt.ravel()


def iard_ode(a, t, xi, L, Ci=0.0, Cm=0.0, **kwargs):
    """ODE describing iARD model.

    Arguments
    ---------
        a (9x1 doubles): Flattened fiber orientation tensor

        t (double): time of evaluation

        xi (double): Shape factor computed from aspect ratio

        L (function handle): function to compute velocity gradient at time t

        Ci (double): Fiber interaction constant (typically 0 < Ci < 0.05)

        Cm (double): anisotropy factor (0 < Cm < 1)

    Reference:
    Tseng, Huan-Chang; Chang, Rong-Yeu; Hsu, Chia-Hsiang, 'An objective tensor
    to predict anisotropic fiber orientation in concentrated suspensions',
    Journal of Rheology 60, 215, 2016.
    https://doi.org/10.1122/1.4939098
    """
    a = np.reshape(a, (3, 3))
    A = compute_closure(a)
    D = 0.5 * (L(t) + np.transpose(L(t)))
    W = 0.5 * (L(t) - np.transpose(L(t)))
    G = np.sqrt(2.0 * np.einsum("ij,ij", D, D))
    delta = np.eye(3)

    D2 = np.einsum("ik,kj->ij", D, D)
    D2_norm = np.sqrt(1.0 / 2.0 * np.einsum("ij,ij", D2, D2))

    Dr = Ci * (delta - Cm * D2 / D2_norm)

    dadt_HD = (
        np.einsum("ik,kj->ij", W, a)
        - np.einsum("ik,kj->ij", a, W)
        + xi
        * (
            np.einsum("ik,kj->ij", D, a)
            + np.einsum("ik,kj->ij", a, D)
            - 2 * np.einsum("ijkl,kl->ij", A, D)
        )
    )

    dadt_iard = G * (
        2 * Dr
        - 2 * np.trace(Dr) * a
        - 5 * np.einsum("ik,kj->ij", Dr, a)
        - 5 * np.einsum("ik,kj->ij", a, Dr)
        + 10 * np.einsum("ijkl,kl->ij", A, Dr)
    )

    dadt = dadt_HD + dadt_iard
    return dadt.ravel()


def iardrpr_ode(a, t, xi, L, Ci=0.0, Cm=0.0, alpha=0.0, beta=0.0, **kwargs):
    """ODE describing iARD-RPR model.

    Arguments
    ---------
        a (9x1 doubles): Flattened fiber orientation tensor

        t (double): time of evaluation

        xi (double): Shape factor computed from aspect ratio

        L (function handle): function to compute velocity gradient at time t

        Ci (double): Fiber interaction constant (typically 0 < Ci < 0.05)

        Cm (double): anisotropy factor (0 < Cm < 1)

        alpha (double): retardance rate (0 < alpha < 1)

        beta (double):  retardance tuning factor (0< beta < 1)

    Reference:
    Tseng, Huan-Chang; Chang, Rong-Yeu; Hsu, Chia-Hsiang, 'An objective tensor
    to predict anisotropic fiber orientation in concentrated suspensions',
    Journal of Rheology 60, 215, 2016.
    https://doi.org/10.1122/1.4939098
    """
    a = np.reshape(a, (3, 3))
    A = compute_closure(a)
    D = 0.5 * (L(t) + np.transpose(L(t)))
    W = 0.5 * (L(t) - np.transpose(L(t)))
    G = np.sqrt(2.0 * np.einsum("ij,ij", D, D))
    delta = np.eye(3)

    D2 = np.einsum("ik,kj->ij", D, D)
    D2_norm = np.sqrt(1.0 / 2.0 * np.einsum("ij,ij", D2, D2))

    Dr = Ci * (delta - Cm * D2 / D2_norm)

    dadt_HD = (
        np.einsum("ik,kj->ij", W, a)
        - np.einsum("ik,kj->ij", a, W)
        + xi
        * (
            np.einsum("ik,kj->ij", D, a)
            + np.einsum("ik,kj->ij", a, D)
            - 2.0 * np.einsum("ijkl,kl->ij", A, D)
        )
    )

    dadt_iard = G * (
        2.0 * Dr
        - 2.0 * np.trace(Dr) * a
        - 5.0 * np.einsum("ik,kj->ij", Dr, a)
        - 5.0 * np.einsum("ik,kj->ij", a, Dr)
        + 10.0 * np.einsum("ijkl,kl->ij", A, Dr)
    )

    dadt_temp = dadt_HD + dadt_iard

    # Spectral Decomposition
    eigenValues, eigenVectors = np.linalg.eig(a)
    idx = eigenValues.argsort()[::-1]
    R = eigenVectors[:, idx]

    # Estimation of eigenvalue rates (rotated back)
    dadt_diag = np.einsum("ik, kl, lj->ij", np.transpose(R), dadt_temp, R)

    lbd0 = dadt_diag[0, 0]
    lbd1 = dadt_diag[1, 1]
    lbd2 = dadt_diag[2, 2]

    # Computation of IOK tensor by rotation
    IOK = np.zeros((3, 3))
    IOK[0, 0] = alpha * (lbd0 - beta * (lbd0 ** 2.0 + 2.0 * lbd1 * lbd2))
    IOK[1, 1] = alpha * (lbd1 - beta * (lbd1 ** 2.0 + 2.0 * lbd0 * lbd2))
    IOK[2, 2] = alpha * (lbd2 - beta * (lbd2 ** 2.0 + 2.0 * lbd0 * lbd1))

    dadt_rpr = -np.einsum("ik, kl, lj->ij", R, IOK, np.transpose(R))

    dadt = dadt_temp + dadt_rpr
    return dadt.ravel()


def mrd_ode(a, t, xi, L, Ci=0.0, D1=1.0, D2=0.8, D3=0.15, **kwargs):
    u"""ODE describing MRD model.

    Arguments
    ---------
        a (9x1 doubles): Flattened fiber orientation tensor

        t (double): time of evaluation

        xi (double): Shape factor computed from aspect ratio

        L (function handle): function to compute velocity gradient at time t

        Ci (double): Fiber interaction constant (typically 0 < Ci < 0.05)

        D1,D2,D3 (double): anisotropy factors (0 < D1, D2, D3)

    Reference:
    A. Bakharev, H. Yu, R. Speight and J. Wang, “Using New Anisotropic Rotational
    Diffusion Model To Improve Prediction Of Short Fibers in Thermoplastic Injection
    Molding," in ANTEC, Orlando, 2018.
    """
    a = np.reshape(a, (3, 3))
    A = compute_closure(a)
    D = 0.5 * (L(t) + np.transpose(L(t)))
    W = 0.5 * (L(t) - np.transpose(L(t)))
    G = np.sqrt(2.0 * np.einsum("ij,ij", D, D))

    C_hat = np.array([[D1, 0.0, 0.0], [0.0, D2, 0.0], [0.0, 0.0, D3]])

    # Spectral Decomposition
    eigenValues, eigenVectors = np.linalg.eig(a)
    idx = eigenValues.argsort()[::-1]
    R = eigenVectors[:, idx]

    C = Ci * np.einsum("ij,jk,kl->il", R, C_hat, np.transpose(R))

    dadt_HD = (
        np.einsum("ik,kj->ij", W, a)
        - np.einsum("ik,kj->ij", a, W)
        + xi
        * (
            np.einsum("ik,kj->ij", D, a)
            + np.einsum("ik,kj->ij", a, D)
            - 2 * np.einsum("ijkl,kl->ij", A, D)
        )
    )

    dadt_mrd = G * (
        2 * C
        - 2 * np.trace(C) * a
        - 5 * np.einsum("ik,kj->ij", C, a)
        - 5 * np.einsum("ik,kj->ij", a, C)
        + 10 * np.einsum("ijkl,kl->ij", A, C)
    )

    dadt = dadt_HD + dadt_mrd
    return dadt.ravel()


def pard_ode(a, t, xi, L, Ci=0.0, Omega=0.0, **kwargs):
    """ODE describing pARD model.

    Arguments
    ---------
        a (9x1 doubles): Flattened fiber orientation tensor

        t (double): time of evaluation

        xi (double): Shape factor computed from aspect ratio

        L (function handle): function to compute velocity gradient at time t

        Ci (double): Fiber interaction constant (typically 0 < Ci < 0.05)

        Omega (double): anisotropy factor (0.5 < Omega < 1)

    Reference:
    Tseng, Huan-Chang; Chang, Rong-Yeu; Hsu, Chia-Hsiang, 'The use of principal spatial
    tensor to predict anisotropic fiber orientation in concentrated fiber suspensions',
    Journal of Rheology 62, 313, 2017.
    https://doi.org/10.1122/1.4998520
    """
    a = np.reshape(a, (3, 3))
    A = compute_closure(a)
    D = 0.5 * (L(t) + np.transpose(L(t)))
    W = 0.5 * (L(t) - np.transpose(L(t)))
    G = np.sqrt(2.0 * np.einsum("ij,ij", D, D))

    C_hat = np.array(
        [[1.0, 0.0, 0.0], [0.0, Omega, 0.0], [0.0, 0.0, 1.0 - Omega]]
    )

    # Spectral Decomposition
    eigenValues, eigenVectors = np.linalg.eig(a)
    idx = eigenValues.argsort()[::-1]
    R = eigenVectors[:, idx]

    C = Ci * np.einsum("ij,jk,kl->il", R, C_hat, np.transpose(R))

    dadt_HD = (
        np.einsum("ik,kj->ij", W, a)
        - np.einsum("ik,kj->ij", a, W)
        + xi
        * (
            np.einsum("ik,kj->ij", D, a)
            + np.einsum("ik,kj->ij", a, D)
            - 2 * np.einsum("ijkl,kl->ij", A, D)
        )
    )

    dadt_pard = G * (
        2 * C
        - 2 * np.trace(C) * a
        - 5 * np.einsum("ik,kj->ij", C, a)
        - 5 * np.einsum("ik,kj->ij", a, C)
        + 10 * np.einsum("ijkl,kl->ij", A, C)
    )

    dadt = dadt_HD + dadt_pard
    return dadt.ravel()


def pardrpr_ode(a, t, xi, L, Ci=0.0, Omega=0.0, alpha=0.0, **kwargs):
    """ODE describing pARD model.

    Arguments
    ---------
        a (9x1 doubles): Flattened fiber orientation tensor

        t (double): time of evaluation

        xi (double): Shape factor computed from aspect ratio

        L (function handle): function to compute velocity gradient at time t

        Ci (double): Fiber interaction constant (typically 0 < Ci < 0.05)

        Omega (double): anisotropy factor (0.5 < Omega < 1)

        alpha (double): retardance rate (0 < alpha < 1)

    Reference:
    Tseng, Huan-Chang; Chang, Rong-Yeu; Hsu, Chia-Hsiang, 'The use of principal spatial
    tensor to predict anisotropic fiber orientation in concentrated fiber suspensions',
    Journal of Rheology 62, 313, 2017.
    https://doi.org/10.1122/1.4998520
    """
    a = np.reshape(a, (3, 3))
    A = compute_closure(a)
    D = 0.5 * (L(t) + np.transpose(L(t)))
    W = 0.5 * (L(t) - np.transpose(L(t)))
    G = np.sqrt(2.0 * np.einsum("ij,ij", D, D))

    C_hat = np.array(
        [[1.0, 0.0, 0.0], [0.0, Omega, 0.0], [0.0, 0.0, 1.0 - Omega]]
    )

    # Spectral Decomposition
    eigenValues, eigenVectors = np.linalg.eig(a)
    idx = eigenValues.argsort()[::-1]
    R = eigenVectors[:, idx]

    C = Ci * np.einsum("ij,jk,kl->il", R, C_hat, np.transpose(R))

    dadt_HD = (
        np.einsum("ik,kj->ij", W, a)
        - np.einsum("ik,kj->ij", a, W)
        + xi
        * (
            np.einsum("ik,kj->ij", D, a)
            + np.einsum("ik,kj->ij", a, D)
            - 2 * np.einsum("ijkl,kl->ij", A, D)
        )
    )

    dadt_pard = G * (
        2 * C
        - 2 * np.trace(C) * a
        - 5 * np.einsum("ik,kj->ij", C, a)
        - 5 * np.einsum("ik,kj->ij", a, C)
        + 10 * np.einsum("ijkl,kl->ij", A, C)
    )

    dadt_temp = dadt_HD + dadt_pard

    # Estimation of eigenvalue rates (rotated back)
    dadt_diag = np.einsum("ik, kl, lj->ij", np.transpose(R), dadt_temp, R)

    lbd0 = dadt_diag[0, 0]
    lbd1 = dadt_diag[1, 1]
    lbd2 = dadt_diag[2, 2]

    # Computation of IOK tensor by rotation
    IOK = np.zeros((3, 3))
    IOK[0, 0] = alpha * lbd0
    IOK[1, 1] = alpha * lbd1
    IOK[2, 2] = alpha * lbd2

    dadt_rpr = -np.einsum("ik, kl, lj->ij", R, IOK, np.transpose(R))

    dadt = dadt_temp + dadt_rpr
    return dadt.ravel()


def rsc_ode(a, t, xi, L, Ci=0.0, kappa=1.0, **kwargs):
    """ODE describing RSC model.

    Arguments
    ---------
        a (9x1 doubles): Flattened fiber orientation tensor

        t (double): time of evaluation

        xi (double): Shape factor computed from aspect ratio

        L (function handle): function to compute velocity gradient at time t

        Ci (double): Fiber interaction constant (typically 0 < Ci < 0.1)

        kappa (double): strain reduction factor (0 < kappa < 1)

    Reference:
    Jin Wang, John F. O'Gara, and Charles L. Tucker, 'An objective model
    for slow orientation kinetics in concentrated fiber suspensions:
    Theory and rheological evidence', Journal of Rheology 52, 1179, 2008.
    https://doi.org/10.1122/1.2946437
    """
    a = np.reshape(a, (3, 3))
    A = compute_closure(a)
    D = 0.5 * (L(t) + np.transpose(L(t)))
    W = 0.5 * (L(t) - np.transpose(L(t)))
    G = np.sqrt(2.0 * np.einsum("ij,ij", D, D))
    delta = np.eye(3)

    w, v = np.linalg.eig(a)
    L = (
        w[0] * np.einsum("i,j,k,l->ijkl", v[:, 0], v[:, 0], v[:, 0], v[:, 0])
        + w[1] * np.einsum("i,j,k,l->ijkl", v[:, 1], v[:, 1], v[:, 1], v[:, 1])
        + w[2] * np.einsum("i,j,k,l->ijkl", v[:, 2], v[:, 2], v[:, 2], v[:, 2])
    )
    M = (
        np.einsum("i,j,k,l->ijkl", v[:, 0], v[:, 0], v[:, 0], v[:, 0])
        + np.einsum("i,j,k,l->ijkl", v[:, 1], v[:, 1], v[:, 1], v[:, 1])
        + np.einsum("i,j,k,l->ijkl", v[:, 2], v[:, 2], v[:, 2], v[:, 2])
    )

    tensor4 = A + (1.0 - kappa) * (L - np.einsum("ijmn,mnkl->ijkl", M, A))

    dadt = (
        np.einsum("ik,kj->ij", W, a)
        - np.einsum("ik,kj->ij", a, W)
        + xi
        * (
            np.einsum("ik,kj->ij", D, a)
            + np.einsum("ik,kj->ij", a, D)
            - 2 * np.einsum("ijkl,kl->ij", tensor4, D)
        )
        + 2 * kappa * Ci * G * (delta - 3 * a)
    )
    return dadt.ravel()


def ard_rsc_ode(
    a, t, xi, L, b1=0.0, kappa=1.0, b2=0, b3=0, b4=0, b5=0, **kwargs
):
    """ODE describing ARD-RSC model.

    Arguments
    ---------
        a (9x1 doubles): Flattened fiber orientation tensor

        t (double): time of evaluation

        xi (double): Shape factor computed from aspect ratio

        L (function handle): function to compute velocity gradient at time t

        b1 (double): First parameter of rotary diffusion tensor (0 < b1 < 0.1)

        kappa (double): strain reduction factor (0 < kappa < 1)

        b2 (double): Second parameter of rotary diffusion tensor

        b3 (double): Third parameter of rotary diffusion tensor

        b4 (double): Fourth parameter of rotary diffusion tensor

        b5 (double): Fifth parameter of rotary diffusion tensor

    Reference:
    J. H. Phelps,  C. L. Tucker, 'An anisotropic rotary diffusion model for
    fiber orientation in short- and long-fiber thermoplastics', Journal of
    Non-Newtonian Fluid Mechanics 156, 165-176, 2009.
    https://doi.org/10.1016/j.jnnfm.2008.08.002
    """
    a = np.reshape(a, (3, 3))
    A = compute_closure(a)
    D = 0.5 * (L(t) + np.transpose(L(t)))
    W = 0.5 * (L(t) - np.transpose(L(t)))
    G = np.sqrt(2.0 * np.einsum("ij,ij", D, D))
    delta = np.eye(3)

    w, v = np.linalg.eig(a)
    L = (
        w[0] * np.einsum("i,j,k,l->ijkl", v[:, 0], v[:, 0], v[:, 0], v[:, 0])
        + w[1] * np.einsum("i,j,k,l->ijkl", v[:, 1], v[:, 1], v[:, 1], v[:, 1])
        + w[2] * np.einsum("i,j,k,l->ijkl", v[:, 2], v[:, 2], v[:, 2], v[:, 2])
    )
    M = (
        np.einsum("i,j,k,l->ijkl", v[:, 0], v[:, 0], v[:, 0], v[:, 0])
        + np.einsum("i,j,k,l->ijkl", v[:, 1], v[:, 1], v[:, 1], v[:, 1])
        + np.einsum("i,j,k,l->ijkl", v[:, 2], v[:, 2], v[:, 2], v[:, 2])
    )
    if G > 0.0:
        C = (
            b1 * delta
            + b2 * a
            + b3 * np.einsum("ik,kj->ij", a, a)
            + b4 * D / G
            + b5 * np.einsum("ik,kj->ij", D, D) / (G * G)
        )
    else:
        C = np.eye(3)

    tensor4 = A + (1.0 - kappa) * (L - np.einsum("ijmn,mnkl->ijkl", M, A))

    dadt = (
        np.einsum("ik,kj->ij", W, a)
        - np.einsum("ik,kj->ij", a, W)
        + xi
        * (
            np.einsum("ik,kj->ij", D, a)
            + np.einsum("ik,kj->ij", a, D)
            - 2 * np.einsum("ijkl,kl->ij", tensor4, D)
        )
        + G
        * (
            2 * (C - (1 - kappa) * np.einsum("ijkl,kl->ij", M, C))
            - 2 * kappa * np.trace(C) * a
            - 5 * (np.einsum("ik,kj->ij", C, a) + np.einsum("ik,kj->ij", a, C))
            + 10 * np.einsum("ijkl,kl->ij", tensor4, C)
        )
    )
    return dadt.ravel()
