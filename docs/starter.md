# Getting started with matplotlib

This is a quick introduction into generating figures with
[`python`](https://www.python.org/) and the
[`matplotlib`](https://matplotlib.org/) package.  Use it for hints on
the most important commands. Check then their documentation for
further details.

Let's generate some time series data for plotting:
```py
import numpy as np
t = np.arange(0.0, 1.0, 0.01) # one second with time step 0.01
x = np.sin(2.0*np.pi*10.0*t)  # 10Hz sine wave
```

Import the [`matplotlib`](https://matplotlib.org/) package:
```py
import matplotlib.pyplot as plt
```

Then a quick way to plot this is
```py
plt.plot(t, x)
plt.show()
```
Do not forget the `show()` - this command displays the plot in a new
window and let you interact with it (zooming and panning). By the way,
these features have short keys: press `o` for zooming or `p` for
panning. `backspace` brings you back.

This is great for quickly checking data in your code. For properly
annotating a plot and for producing nice figures we use the
object-oriented interface of matplotlib. This is described in the
following:


## Single plot in a figure

Generate a figure and an axes using the `plt.subplots()` function:
```py
fig, ax = plt.subplots()
```

Then `ax` is a single matplotlib axes. This is a plot, a coordinate
system in which you can draw and annotate your data:
```py
ax.plot(t, x)
ax.set_xlim(0, 0.2)
ax.set_xlabel('Time [s]')
ax.set_ylabel('Voltage [mV]')
```


### Plot commands

See the [matplotlib.axes
API](https://matplotlib.org/stable/api/axes_api.html) for a (long)
list of member functions, including various types of plots and
annotations.

Here is a selection of often used plot commands:

- [`plot()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html): plot y versus x with markers and connected by lines. 
- [`errorbar()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.errorbar.html): plot errorbars (both vertical and horizontal ones)
- [`scatter()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.scatter.html): plot y versus x with varying marker size and color.
- [`fill_between()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.fill_between.html): fill area between a curve and an axis (or another curve).
- [`hist()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.hist.html): histogram (see also `np.histogram()` and `ax.bar()`).
- [`boxplot()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.boxplot.html): box-whisker plot.
- [`contour()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.contour.html): contour lines.
- [`pcolormesh()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.pcolormesh.html): pseudocolor plot of a mtrix with specified x- and y-axis ranges.
- [`imshow()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.imshow.html): plot an image - (almost) *never* use it for pseudocolor plots of matrices, use [`pcolormesh()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.pcolormesh.html) instead.


### Setting colors, lines, and markers

Further key-word arguments to the plot commands allow to change
colors, lines, and markers. In the following some of the more commonly
used ones are listed.

Lines:

- `color` or `c`: color specification, e.g. `'red'`, or `'#DD0000'`
- `linewidth` or `lw`: width of connecting lines
- `linestyle` or `ls`: solid, dashed, or dotted: '-', '--', '-.', ':', ''

Markers:

- `marker`: the marker symbol, e.g. '.', 'o', 'v', 's', 'D', 'p', 'h', 'x', '+', '*', etc.
  see [matplotlib.markers](https://matplotlib.org/stable/api/markers_api.html) for a table.
- `markersize` or `ms`: size of the marker symbol.
- `markerfacecolor` or `mfc`: fill color of the marker, e.g. `'green'` or `'#00CC00'`
- `markeredgecolor` or `mec`: color of the outline of the marker, e.g. `'blue'` or `'#0000DD'`
- `markeredgewidth` or `mew`: width of the marker outline. 

Other:

- `label`: a label for the legend (see below).
- `clip_on`: set to `False` if you do not want, for example, marker symbols to be clipped.
- `zorder`: some number specifying the order in which elements are drawn into the plot. Higher numbers are drawn on top of lower numbers.


### Logarithmic axis

For a logarithmic x-axis use
```py
ax.set_xlim(0.01, 1.0)
ax.set_xscale('log')
```
Likewise for the y-axis.

Make sure the data range starts at positive (non-zero) values using
`ax.set_xlim()`.


### Legend

When you plot several data sets into an axes, you might want to add a
legend to your plot. Pass a `label` to the plot commands and then call
`legend()`:
```py
ax.plot(t, x, label='one')
ax.plot(t, 1.5*x, label='two')
ax.plot(t, 2.2*x, label='three')
ax.legend(loc='upper right')
```


### Annotation

You can place some text somewhere in (or outside) your plot:
```py
ax.text(0.1, 0.9, 'a note')
```
The first two arguments are the x- and y-coordinate of the text in data coordinates.

Very useful is to specify the position of the text in relative axes coordinates:
```py
ax.text(0.9, 0.9, 'another note', ha='right', transform=ax.transAxes)
```
This text is placed right aligned (`ha='right'`) in the top right corner.


### Save figure to a file

`fig` is a matplotlib figure. In this example it holds just one axes,
but it can have many more (see next section). Each window you get with
`plt.show()` contains a matplotlib figure. And you can save a
matplotlib figure to a file like this:
```py
fig.savefig('myplot.pdf')
```
You can save the figure into `pdf`, `svg`, `png`, `jpg` and `tex`
files. Just supply the right file extension.

If you also want to display your figure on screen, then call
`plt.show()` *after* `fig.savefig()`, because on exit (closing the
window), `plt.show()` destroys the figure.


## Multiple plots in a figure

The simplest scenario is having a grid of subplots. The following
example generates two rows and three columns of axes (=subplots):
```py
fig, axs = plt.subplots(2, 3)
```
Now, `axs` is a 2-dimensional numpy array holding the six axes that we
use like this:
```py
axs[0,0].plot(t, x)    # top left plot
axs[1,2].plot(t, 2*x)  # bottom right plot
```

A single row or column of subplots can also be initialized like this:
```py
fig, (ax1, ax2) = plt.subplots(1, 2)
```

A very useful and less well known feature is that the relative widths
and heights of the columns and rows of a grid of subplots can be
specified like this:
```py
fig, axs = plt.subplots(2, 3, gridspec_kw=dict(width_ratios=[3, 1, 1], height_ratios=[4, 1]))
```
The `width_ratios` and `height_ratios` give for each column/row a
relative width/height.

For more details on how to layout subplots you definitely want to read
the [GridSpec
tutorial](https://matplotlib.org/stable/tutorials/intermediate/gridspec.html).
Also check out the note on [Figure and Axes
creation/management](https://matplotlib.org/stable/users/whats_new.html#figure-and-axes-creation-management).


## Customizing figure layout

First of all, you want to specify the size of your figure. Make each
figure as large as you want it to be in your manuscript or
presentation to ensure that the plot labels of all your figures have
the same font size (*no* scaling of the figures in the manuscript or
presentation).
```py
fig, axs = plt.subplots(2, 3, figsize=(8, 5))  # in inch!
```
Unfortunately, the `figsize` argument takes the width and the height
of the figure measured in inches. Hey - we are doing science here and
want SI units! To specify your figure size in centimeters you need to
divide by 2.54 cm/inch:
```py
fig, axs = plt.subplots(2, 3, figsize=(12/2.54, 8/2.54))  # in cm
```

Second, you want your plots to nicely fill the figure (no extra
whitespace at the borders). For this use
```py
fig.subplots_adjust(left=0.2, right=0.95, top=0.95, bottom=0.1)
```
These are fractions of the full figure size. `right` and `top` are
absolute coordinates, not the width and the height of the
subplots. Adapt them as needed. After a while you get a feeling for
good values and adjusting them gets easy.

Third, adjust the whitespace between the subplots. Don't let your urge
to give each subplot as much space as possible win. Figures usually
look much better with quite a lot of whitespace between them:
```py
fig.subplots_adjust(wspace=0.5, hspace=0.4)
```
Both `wspace` and `hspace` specify the amount of whitespace relative
to the average width/height of the subplots. `hspace` stands for
"height" not "horizontal" ...


## Customizing figure design

Label fonts, default colors, etc. can be customized globally for all
your plots via
[rcParams](https://matplotlib.org/stable/tutorials/introductory/customizing.html). This
is a must-read!

For example, to set the standard font size to 11pt and have somewhat
smaller tick labels you may call
```py
plt.rcParams['font.size'] = 11
plt.rcParams['xtick.labelsize'] = 'small'
plt.rcParams['ytick.labelsize'] = 'small'
```
before you create any figures and axes.


## Cheat sheets

matplotlib provides some nice cheat sheets:
https://github.com/matplotlib/cheatsheets/blob/master/cheatsheets.pdf


## How to prepare figures

Continue reading with suggestions on [how to prepare figures](guide.md). 