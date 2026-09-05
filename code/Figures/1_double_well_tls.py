"""
TLS Double-Well Potential (Standard Tunneling Model)
E_L, E_R (well energies), V0 (barrier height, measured from well bottom),
d (well separation), Delta (asymmetry, flat-ended dimension line).
Delta_0 intentionally omitted (removed per final revision).
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

# ---------------------------------------------------------------
# Potential: asymmetric quartic double well
# ---------------------------------------------------------------
x = np.linspace(-3.2, 3.2, 2000)
a = 1.0
eps = 0.35  # asymmetry (tilt)
V = a * (x**2 - 1) ** 2 - eps * x

resL = minimize_scalar(lambda x: a * (x**2 - 1) ** 2 - eps * x, bounds=(-2, 0), method="bounded")
resR = minimize_scalar(lambda x: a * (x**2 - 1) ** 2 - eps * x, bounds=(0, 2), method="bounded")
xL, EL = resL.x, resL.fun
xR, ER = resR.x, resR.fun

resB = minimize_scalar(lambda x: -(a * (x**2 - 1) ** 2 - eps * x), bounds=(xL, xR), method="bounded")
xB, V0 = resB.x, -resB.fun

fig, ax = plt.subplots(figsize=(7.5, 5.5))
ax.plot(x, V, color="k", lw=2, zorder=1)

# ---------------------------------------------------------------
# Ground-state wavefunctions (schematic gaussians sitting on each well)
# ---------------------------------------------------------------
sigma = 0.35
amp = 0.35
psiL = amp * np.exp(-(x - xL) ** 2 / (2 * sigma**2)) + EL
psiR = amp * np.exp(-(x - xR) ** 2 / (2 * sigma**2)) + ER

ax.plot(x, psiL, color="tab:blue", lw=2, zorder=3)
ax.plot(x, psiR, color="tab:red", lw=2, zorder=3)
ax.fill_between(x, EL, psiL, color="tab:blue", alpha=0.15, zorder=2)
ax.fill_between(x, ER, psiR, color="tab:red", alpha=0.15, zorder=2)

ax.text(xL, EL + amp + 0.12, r"$|L\rangle$", ha="center", color="tab:blue", fontsize=13, zorder=6)
ax.text(xR, ER + amp + 0.12, r"$|R\rangle$", ha="center", color="tab:red", fontsize=13, zorder=6)

# ---------------------------------------------------------------
# E_L / E_R dashed reference lines (drawn on top of gaussians)
# ---------------------------------------------------------------
ax.hlines(EL, xL - 0.15, 2.9, color="tab:blue", lw=2, linestyle="--", zorder=4)
ax.hlines(ER, xR - 0.5, 2.9, color="tab:red", lw=2, linestyle="--", zorder=4)

ax.text(xL - 0.2, EL + 0.13, r"$E_L$", ha="right", va="bottom", color="tab:blue",
        fontsize=13, fontweight="bold", zorder=7)
ax.text(xR - 0.65, ER + 0.13, r"$E_R$", ha="right", va="bottom", color="tab:red",
        fontsize=13, fontweight="bold", zorder=7)

# ---------------------------------------------------------------
# Delta: flat-ended dimension-line arrow between the two levels
# ---------------------------------------------------------------
x_delta = 2.6
ax.annotate("", xy=(x_delta, ER), xytext=(x_delta, EL),
            arrowprops=dict(arrowstyle="|-|,widthA=0.5,widthB=0.5", color="k", lw=1.8))
ax.text(x_delta + 0.15, (EL + ER) / 2, r"$\Delta$", color="k", fontsize=15, ha="left", va="center")

# ---------------------------------------------------------------
# V0: barrier height, measured from the well bottom up to barrier top
# ---------------------------------------------------------------
Ebase = min(EL, ER)
ax.annotate("", xy=(xB, V0), xytext=(xB, Ebase),
            arrowprops=dict(arrowstyle="<->", color="purple", lw=1.8))
ax.text(xB + 0.18, (V0 + Ebase) / 2, r"$V_0$", color="purple", fontsize=15, fontweight="bold",
        bbox=dict(facecolor="white", edgecolor="none", pad=1, alpha=0.85), zorder=8)

# ---------------------------------------------------------------
# d: well separation
# ---------------------------------------------------------------
ybar = min(EL, ER) - 0.35
ax.annotate("", xy=(xL, ybar), xytext=(xR, ybar),
            arrowprops=dict(arrowstyle="<->", color="orange", lw=1.6))
ax.text(0, ybar - 0.22, r"$d$", color="orange", fontsize=13, ha="center")

# ---------------------------------------------------------------
# Axes styling: clean arrow-style axes like a textbook sketch
# ---------------------------------------------------------------
ax.set_xlabel("Configuration coordinate", fontsize=12)
ax.set_ylabel("Potential energy", fontsize=12)
ax.set_title("TLS Double-Well Potential (STM)", fontsize=13)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim(-3.15, 3.1)
ax.set_ylim(ybar - 0.55, V0 + 0.6)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_position(("data", -3.05))
ax.spines["bottom"].set_position(("data", ybar))
ax.plot(1, ybar, ">k", transform=ax.get_yaxis_transform(), clip_on=False, markersize=8)
ax.plot(-3.05, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False, markersize=8)

plt.tight_layout()
plt.savefig("/mnt/user-data/outputs/1_double_well_tls.png", dpi=200, bbox_inches="tight")
print("saved")
