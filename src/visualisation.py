import matplotlib.pyplot as plt
import numpy as np

x = [0, 1, 2, 3, 0.5, 2.5, 1, 2, 3, 4, 1.5, 3.5]
y = [0, 0, 0, 0, np.sqrt(3)/2, np.sqrt(3)/2, np.sqrt(3), np.sqrt(3), np.sqrt(3), np.sqrt(3), 3*np.sqrt(3)/2, 3 *np.sqrt(3)/2]

fig, ax = plt.subplots()
ax.plot(x, y, "o", markersize=14)
plt.show()
