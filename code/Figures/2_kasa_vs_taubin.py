"""
Algebraic Circle-Fit Bias in Resonator Seeding: Kasa vs. Taubin on a Truncated Arc
Two-panel comparison: a well-sampled high-SNR arc vs a truncated low-power arc,
fit with Kasa (standardLSQ) and Taubin (taubinSVD) algebraic circle fits.
"""
import numpy as np
import matplotlib.pyplot as plt
from circle_fit import standardLSQ, taubinSVD

rng = np.random.default_rng(0)


def notch_resonator_iq(Ql, Qc, phi0, fr=1.0, y_half_range=6.0, n=401):
    """Synthetic asymmetric notch resonator S21 arc (Probst et al. model),
    parameterized by a normalized detuning range in units of half-linewidths."""
    y = np.linspace(-y_half_range, y_half_range, n)  # y = 2 Ql (f - fr)/fr
    Qc_complex = Qc * np.exp(-1j * phi0)
    S21 = 1 - (Ql / np.abs(Qc_complex)) * np.exp(1j * phi0) / (1 + 2j * y)
    return S21


def add_noise(S21, snr):
    sigma = 1.0 / snr
    noise = sigma * (rng.normal(size=S21.shape) + 1j * rng.normal(size=S21.shape))
    return S21 + noise


def fit_and_plot(ax, title, Ql, Qc, phi0, y_half_range, n, snr):
    S21_clean = notch_resonator_iq(Ql, Qc, phi0, y_half_range=y_half_range, n=n)
    S21 = add_noise(S21_clean, snr)

    xdata, ydata = S21.real, S21.imag
    xk, yk, rk, _ = standardLSQ(np.column_stack([xdata, ydata]))
    xt, yt, rt, _ = taubinSVD(np.column_stack([xdata, ydata]))

    # true circle from the noiseless arc (algebraic fit on clean data)
    xdata0, ydata0 = S21_clean.real, S21_clean.imag
    x0, y0, radius, _ = taubinSVD(np.column_stack([xdata0, ydata0]))

    ax.plot(xdata, ydata, ".", color="0.6", ms=3, alpha=0.6, label="noisy IQ data")

    theta = np.linspace(0, 2 * np.pi, 400)
    ax.plot(x0 + radius * np.cos(theta), y0 + radius * np.sin(theta),
            "k--", lw=1.3, label=r"true circle ($r_0$)")
    ax.plot(xk + rk * np.cos(theta), yk + rk * np.sin(theta),
            color="tab:red", lw=1.8, label="Kåsa fit")
    ax.plot(xt + rt * np.cos(theta), yt + rt * np.sin(theta),
            color="tab:blue", lw=1.8, label=f"Taubin fit")

    ax.set_aspect("equal")
    ax.set_xlabel("Re(S21)")
    ax.set_ylabel("Im(S21)")
    ax.set_title(f"{title}\n" + rf"$r_0$: Kåsa={rk:.4f}, Taubin={rt:.4f}, true={radius:.4f}",
                 fontsize=9.5)
    ax.legend(frameon=False, fontsize=8, loc="best")


cases = [
    ("Well-sampled arc (SNR=200)", dict(Ql=6.2e5, Qc=2.3e6, phi0=0.05, y_half_range=6.0, n=401, snr=200.0)),
    ("Truncated arc, low-power sweep (SNR=5)", dict(Ql=6.2e5, Qc=2.3e6, phi0=0.05, y_half_range=1.5, n=200, snr=5.0)),
]

fig, axes = plt.subplots(1, 2, figsize=(11, 5))
for ax, (title, params) in zip(axes, cases):
    fit_and_plot(ax, title, **params)

fig.suptitle("Algebraic Circle-Fit Bias in Resonator Seeding: K\u00e5sa vs. Taubin on a Truncated Arc",
             fontsize=12)
fig.tight_layout()
fig.savefig("/mnt/user-data/outputs/2_kasa_vs_taubin.png", dpi=200, bbox_inches="tight")
print("saved")
