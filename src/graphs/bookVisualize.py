import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

fig, ax = plt.subplots(2, 2)


def animate(i):
    ax[0][0].clear()
    ax[0][0].plot(list(range(5)), random.sample(range(0, 10), 5))

anim = FuncAnimation(fig, animate, interval=1)

plt.show()