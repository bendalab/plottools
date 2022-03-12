# Coding a figure

There are many different ways how to organize your code. This is also
true for code generating figures. But there are some aspects that
require our attention, in particular towards separating design from
content.

Here we start from some spaghetti code and improve it step-by-step, in
order to develop some techniques that make your figure code better
maintainable.


## Quick-and-dirty spagheti code

Let's create a figure with two panels side-by-side, showing two sine
waves and two exponential function. Of course, the two plots should be
properly labeled. So just hacking this down results in something like this:

```py
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 200)
y = np.sin(2*np.pi*3*x)
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
fig.savefig('plot.pdf')
```


## Customize your plot

Well, you do not like the standard appearance of the plots. You want
larger fonts, and you would like to change the color and width of the
plotted lines. You check the documentation of the matplotlib functions
and come up with something like this:

```py
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 200)
y = np.sin(2*np.pi*3*x)
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(x, y, color='tab:red', lw=2)
ax1.plot(x, 2*y, color='tab:orange', lw=2)
ax1.set_xlabel('x', fontsize=14)
ax1.set_ylabel('y', fontsize=14)
x = np.linspace(-5, 5, 200)
y = np.exp(x)
ax2.plot(x, y, color='tab:red', lw=2)
ax2.plot(x, 2*y, color='tab:orange', lw=2)
ax2.set_xlabel('x', fontsize=14)
ax2.set_ylabel('y', fontsize=14)
fig.savefig('plot.pdf')
```

## Modularize your code

Well, this manual and direct way in modifying the plot appearance has
one severe disadvantage: if you want to change the design of your
figures, you need to change colors and font sizes and whatever on
every line you use them. The classical solution to this problem is to
put your code into functions and pull out these parameters as function
parameters:

```py
import numpy as np
import matplotlib.pyplot as plt

def sine_plot(ax, color1, color2, lw, fs):
    """Plots two sine waves with different amplitudes."""
    x = np.linspace(0, 10, 200)
    y = np.sin(2*np.pi*3*x)
    ax.plot(x, y, color=color1, lw=lw)
    ax.plot(x, 2*y, color=color2, lw=lw)
    ax.set_xlabel('x', fontsize=fs)
    ax.set_ylabel('y', fontsize=fs)

def exp_plot(ax, color1, color2, lw, fs):
    """Plots two differently scaled exponential functions."""
    x = np.linspace(-5, 5, 200)
    y = np.exp(x)
    ax.plot(x, y, color=color1, lw=lw)
    ax.plot(x, 2*y, color=color2, lw=lw)
    ax.set_xlabel('x', fontsize=fs)
    ax.set_ylabel('y', fontsize=fs)

# global parameters defining plot appearance:
fs = 14
color1 = 'tab:red'
color2 = 'tab:orange'
lw = 2
# the figure:
fig, (ax1, ax2) = plt.subplots(2, 1)
sine_plot(ax1, color1, color2, lw, fs)
exp_plot(ax2, color1, color2, lw, fs)
fig.savefig('plot.pdf')
```

Much better! There are several advantages of this code:

- each panel is made by a single function and the second part of the
  short main code takes care of their arrangement. This way, the
  panels can be easily rearranged, or even moved to another figure.
- the appearance of the plots can be controlled entirely from the
  initial part of the short main script.  No need to change anything
  within the functions.

There is, however, one problem. Usually plots are a bit more
complex. Some more lines are plotted, for example, and each would need
its own color and line style parameter. So the number of parameters
tend to explode. And this then makes the functions cumbersome to use,
because in the end one has to follow each parameter into the function
to figure out which color or text it will change. This parameter
following gets even worse in case of nested functions.

One solution to this problem is provided by matplotlib's
[rcParams](https://matplotlib.org/stable/tutorials/introductory/customizing.html). They
allow you to change basic properties of your plots in a global
manner. That way, you do not need to pass these parameters through
function parameters. In our example, we set the font size via
[rcParams](https://matplotlib.org/stable/tutorials/introductory/customizing.html)
*before* we create the figure:

```py
import numpy as np
import matplotlib.pyplot as plt

# no need to pass font size as a parameter:
def sine_plot(ax, color1, color2, lw):
    x = np.linspace(0, 10, 200)
    y = np.sin(2*np.pi*3*x)
    ax.plot(x, y, color=color1, lw=lw)
    ax.plot(x, 2*y, color=color2, lw=lw)
    ax.set_xlabel('x')
    ax.set_ylabel('y')

def exp_plot(ax, color1, color2, lw):
    x = np.linspace(-5, 5, 200)
    y = np.exp(x)
    ax.plot(x, y, color=color1, lw=lw)
    ax.plot(x, 2*y, color=color2, lw=lw)
    ax.set_xlabel('x')
    ax.set_ylabel('y')

# use rcParams to set font size globally:
plt.rcParams['font.size'] = 14
color1 = 'tab:red'
color2 = 'tab:orange'
lw = 2
# the figure:
fig, (ax1, ax2) = plt.subplots(2, 1)
sine_plot(ax1, color1, color2, lw)
exp_plot(ax2, color1, color2, lw)
fig.savefig('plot.pdf')
```

This already removes quite some clutter from your plot functions and
it also improves the main code, because the parameter lists get
shorter.

But there are still too many parameters for defining the appearances
of the plotted lines (and points, and fill styles, ...).


## Plotting styles

Each line you plot has several attributes that you might want to
change. It is not only its color, but also its line width, the line
style (solid or dashed), transparency, etc. If you take it serious,
then all of these should be passed as parameters to the functions make
the plot. This results in very long parameter lists and also many
lines of code setting these parameters in your main script.

This explosion of parameters can be nicely reduced to a single
variable for each specific type of line you want to plot. Since these
parameters are supplied as keyword arguments to the plot functions,
they can be combined into dictionaries.

And you can give them functional names. Not "red line style", but
"line style for small amplitude functions", for example.

```py
import numpy as np
import matplotlib.pyplot as plt

# pass for each line a whole line style dictionary:
def sine_plot(ax, lsSmall, lsLarge):
    x = np.linspace(0, 10, 200)
    y = np.sin(2*np.pi*3*x)
    ax.plot(x, y, **lsSmall)  # key-word arguments provided by line style
    ax.plot(x, 2*y, **lsLarge)
    ax.set_xlabel('x')
    ax.set_ylabel('y')

def exp_plot(ax, lsSmall, lsLarge):
    x = np.linspace(-5, 5, 200)
    y = np.exp(x)
    ax.plot(x, y, **lsSmall)
    ax.plot(x, 2*y, **lsLarge)
    ax.set_xlabel('x')
    ax.set_ylabel('y')

plt.rcParams['font.size'] = 14
# define two line styles:
lsSmall = dict(color='tab:red', lw=2)
lsLarge = dict(color='tab:orange', lw=2)
# the figure:
fig, (ax1, ax2) = plt.subplots(2, 1)
sine_plot(ax1, lsSmall, lsLarge) # just pass line styles to the functions
exp_plot(ax2, lsSmall, lsLarge)
fig.savefig('plot.pdf')
```

This way we significantly reduce the number of parameters to the plot
function. And we achieved another big step towards the separation of
design and content. The plot functions just supply the content. How
the plots appear is entirely defined by the initial lines of the main
script.

We can do better.


## Namespace for plotting styles

The
[rcParams](https://matplotlib.org/stable/tutorials/introductory/customizing.html)
control plotting in a global way. Similarly, we could summarize all
our plotting styles in a namespace that we then provide to the
functions creating the plots:

```py
import numpy as np
import matplotlib.pyplot as plt

# just pass a namespace holding plotting style:
def sine_plot(ax, s):
    x = np.linspace(0, 10, 200)
    y = np.sin(2*np.pi*3*x)
    ax.plot(x, y, **s.lsSmall)  # key-word arguments provided by line style
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

plt.rcParams['font.size'] = 14
# namespace for plotting styles:
class s: pass
# define two line styles in the `s` namespace:
s.lsSmall = dict(color='tab:red', lw=2)
s.lsLarge = dict(color='tab:orange', lw=2)
# the figure:
fig, (ax1, ax2) = plt.subplots(2, 1)
sine_plot(ax1, s)  # just pass the namespace to the functions
exp_plot(ax2, s)
fig.savefig('plot.pdf')
```

Now, we reduced the parameter lists to just two arguments: the axes
and the namespace holding the plotting styles.

Each plot function just gets this namespace. So it is up to the plot
function to select an appropriate plotting style from this
namespace. In all the examples before, the plotting styles were
defined by the caller of the plot functions. By whatever parameters
where passed to the function the design of the plotted lines was
set. By just passing the namespace, we give this control back to the
plot function.

Key is to use functional names for the plotting styles. In this way it
can be easily ensured that similar things get plotted in the very same
way. You can set a few line styles for stimuli, for example, that were
used to probe the function of a neuron (e.g. `lsStimA`,
`lsStimB`). And a few other style, for example, for the resulting
responses (e.g. `lsRespA`, `lsRespB`).


## Central function for controlling the design

As a last step we pull out the initial lines of the main script into a
function that we place into a separate module.

This is our `plotstyle.py` module:

```py
import matplotlib.pyplot as plt

def plot_style():
    # namespace for plotting styles:
    class s: pass
    s.lsSmall = dict(color='tab:red', lw=2)
    s.lsLarge = dict(color='tab:orange', lw=2)
    # global settings:
    plt.rcParams['font.size'] = 14
```

And this is how our script looks like:

```py
import numpy as np
import matplotlib.pyplot as plt
from plotstyle import plot_style

def sine_plot(ax, s):
    x = np.linspace(0, 10, 200)
    y = np.sin(2*np.pi*3*x)
    ax.plot(x, y, **s.lsSmall)  # key-word arguments provided by line style
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
fig.savefig('plot.pdf')
```

A single line of code (the first on of the main script) defines all
the global design of your plot. The remaining main script arranges the
subplots. And the plot functions doing the actual plotting provide and
plot the data and the content (e.g. axes labels, text, arrows),
without influencing the design.


## How to structure your code

Continue reading with suggestions on [how to structure your
code](structure.md).