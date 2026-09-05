"""
Max deviation from the mean, per power level.
Three panels (one per device power), each showing repeated time-sweep
scans of fitted Qi with the maximum-deviation scan flagged.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

OI = {
    "orange": "#E69F00",
    "skyblue": "#56B4E9",
    "green": "#009E73",
    "black": "#000000",
    "gray": "#999999",
}

rng = np.random.default_rng(3)

plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
})

n_scans = 6
t = np.arange(1, n_scans + 1)

# three illustrative repeated-scan sets, increasing scatter with power
powers = [-112, -108, -105]
spreads = [0.10, 0.07, 0.045]
colors = [OI["skyblue"], OI["green"], OI["orange"]]
markers = ["o", "^", "s"]

fig, axes = plt.subplots(1, 3, figsize=(14, 4.4), sharey=True)

Qi_mean = 1.00e5

for ax, P, spread, color, marker in zip(axes, powers, spreads, colors, markers):
    Qi = Qi_mean * (1 + rng.normal(0, spread, n_scans))
    i_max = np.argmax(np.abs(Qi - Qi_mean))

    ax.axhline(Qi_mean, color=OI["gray"], ls="--", lw=1.2)
    ax.plot(t, Qi, marker, color=color, ms=8)

    arrow = FancyArrowPatch(
        (t[i_max], Qi_mean), (t[i_max], Qi[i_max]),
        arrowstyle="<->", mutation_scale=13, color=color, lw=1.5,
    )
    ax.add_patch(arrow)
    dy = 2200 if Qi[i_max] > Qi_mean else -3200
    ax.annotate(
        r"$\Delta Q_i^{\max}$",
        xy=(t[i_max], (Qi_mean + Qi[i_max]) / 2),
        xytext=(t[i_max] + 0.3, (Qi_mean + Qi[i_max]) / 2 + dy),
        fontsize=11, color=color,
    )

    ax.set_xlabel("Scan number (joint fit)")
    ax.set_title(f"{P} dBm")
    ax.set_xlim(0.5, n_scans + 0.5)

axes[0].set_ylabel(r"Fitted $Q_i$")

fig.suptitle(
    "Max deviation from the mean, per power level",
    fontsize=13, y=1.03,
)
fig.tight_layout()
fig.savefig("/mnt/user-data/outputs/3_time_sweep_max_fluctuation.png",
            dpi=200, bbox_inches="tight")
print("saved")
