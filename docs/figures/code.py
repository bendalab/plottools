import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.constrained_layout.use'] = True

x = np.linspace(0, 10, 200)
y = np.sin(2*np.pi*0.5*x)
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(x, y)
ax1.plot(x, 2*y)
ax1.set_xlabel('x')
ax1.set_ylabel('y')
x = np.linspace(-5, 5, 200)
y = np.exp(x)
ax2.plot(x, y)
ax2.plot(x, 2*y)
ax2.set_xlabel('x')
ax2.set_ylabel('y')
fig.savefig('code-plain.png')

x = np.linspace(0, 10, 200)
y = np.sin(2*np.pi*0.5*x)
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(x, y, color='tab:red', lw=2)
ax1.plot(x, 2*y, color='tab:orange', lw=2)
ax1.set_xlabel('x', fontsize=18)
ax1.set_ylabel('y', fontsize=18)
x = np.linspace(-5, 5, 200)
y = np.exp(x)
ax2.plot(x, y, color='tab:red', lw=2)
ax2.plot(x, 2*y, color='tab:orange', lw=2)
ax2.set_xlabel('x', fontsize=18)
ax2.set_ylabel('y', fontsize=18)
fig.savefig('code-params.png')


def plot_style():
    class s: pass
    s.lsSmall = dict(color='tab:red', lw=2)
    s.lsLarge = dict(color='tab:orange', lw=2)
    plt.rcParams['font.size'] = 18
    return s

def sine_plot(ax, s):
    x = np.linspace(0, 10, 200)
    y = np.sin(2*np.pi*0.5*x)
    ax.plot(x, y, **s.lsSmall)
    ax.plot(x, 2*y, **s.lsLarge)
    ax.set_xlabel('x')
    ax.set_ylabel('y')

def exp_plot(ax, s):
    x = np.linspace(-5, 5, 200)
    y = np.exp(x)
    ax.plot(x, y, **s.lsSmall)
    ax.plot(x, 2*y, **s.lsLarge)
    ax.set_xlabel('x')
    ax.set_ylabel('y')

s = plot_style()
# the figure:
fig, (ax1, ax2) = plt.subplots(2, 1)
sine_plot(ax1, s)
exp_plot(ax2, s)
fig.savefig('code-plotstyle.png')
