import matplotlib.pyplot as plt
import numpy as np

a = 1
c = 1/2
a1 = np.array([a, 0])
a2 = np.array([a/2, a*np.sqrt(3)/2])
cs = [
        np.array([0, 0]),
        np.array([c, 0]),
        np.array([c/2, c*np.sqrt(3)/2])
]

fig, ax = plt.subplots()
for i in range(2):
    for j in range(2):
        for n, l in enumerate(cs):
            x = a1[0]*i + a2[0]*j + l[0]
            y = a1[1]*i + a2[1]*j + l[1]
            ax.plot(x, y, "o",
                    color="C0")
            ax.annotate(
                        f"s{3*i+6*j+n}",
                        xy=(x, y), xycoords="data",
                        xytext=(0, 5), textcoords="offset points"
                    )
ax.set_aspect("equal")
ax.set_xlabel(r"$x\ [a]$")
ax.set_ylabel(r"$y\ [a]$")
fig.savefig("figs/reskagome.png")
