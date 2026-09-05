"""
Empirical (power, max relative deviation) anchor points mapped onto a
fitted log-linear scaling law: log10(delta) = a + b * P_dBm.
"""
import numpy as np
import matplotlib.pyplot as plt

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

# ---------------------------------------------------------------
# Two anchor measurements: repeated time-sweep scans at each power
# ---------------------------------------------------------------
n_scans = 6
t = np.arange(1, n_scans + 1)
Qi_mean = 1.00e5

P_low_dBm, P_high_dBm = -112, -105
Qi_low = Qi_mean * (1 + rng.normal(0, 0.10, n_scans))
Qi_high = Qi_mean * (1 + rng.normal(0, 0.045, n_scans))

max_dev_low = np.max(np.abs(Qi_low - Qi_mean)) / Qi_mean
max_dev_high = np.max(np.abs(Qi_high - Qi_mean)) / Qi_mean

powers = np.array([P_low_dBm, P_high_dBm])
devs = np.array([max_dev_low, max_dev_high])

# ---------------------------------------------------------------
# Linear scaling law in dBm, fit exactly through the two anchor points
# log10(delta) = a + b * P_dBm
# ---------------------------------------------------------------
log_devs = np.log10(devs)
b, a = np.polyfit(powers, log_devs, 1)  # slope, intercept

P_line = np.linspace(-118, -98, 100)
dev_line = 10 ** (a + b * P_line)

fig, axB = plt.subplots(figsize=(6.5, 5))

axB.plot(P_line, dev_line, color=OI["gray"], lw=1.8,
         label=r"scaling law: $\log_{10}\Delta = a + bP$")
axB.plot(powers, devs, "o", color=OI["black"], ms=9, zorder=5,
         label="empirical anchor points")
axB.annotate(f"{P_low_dBm} dBm", (powers[0], devs[0]),
             textcoords="offset points", xytext=(8, -14), fontsize=9)
axB.annotate(f"{P_high_dBm} dBm", (powers[1], devs[1]),
             textcoords="offset points", xytext=(8, 6), fontsize=9)

axB.set_yscale("log")
axB.set_xlabel("Device power (dBm)")
axB.set_ylabel(r"Max relative deviation $\Delta Q_i^{\max}/Q_i$")
axB.set_title("Empirical points mapped to scaling law")
axB.legend(frameon=False, loc="lower right", fontsize=9)

fig.suptitle(
    "Quantifying TLS fluctuation error from repeated time-sweep measurements",
    fontsize=13, y=1.03,
)
fig.tight_layout()
fig.savefig("/mnt/user-data/outputs/4_loglog_fluctuation_scaling.png",
            dpi=200, bbox_inches="tight")
print("saved")
