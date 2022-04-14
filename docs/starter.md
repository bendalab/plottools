# Getting started with matplotlib

This is a quick introduction into generating figures with
[`python`](https://www.python.org/) and the
[`matplotlib`](https://matplotlib.org/) package.  Use it for hints
(and links) on the most important commands. Check then their
documentation for further details.

Import the [`matplotlib`](https://matplotlib.org/) package:
```py
import matplotlib.pyplot as plt
```
and generate some time series data for plotting:
```py
import numpy as np
t = np.arange(0.0, 1.0, 0.01) # one second with time step 0.01
x = np.sin(2.0*np.pi*10.0*t)  # 10Hz sine wave
```

Then a quick way to plot this is
```py
plt.plot(t, x)
plt.show()
```
Do not forget the
[`show()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.show.html)
- this command displays the plot in a new window and let you interact
with it (zooming and panning). By the way, these features have short
keys: press `o` for zooming or `p` for panning. `backspace` brings you
back. `f` is fullscreen mode.

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
system, in which you can draw and annotate your data:
```py
ax.plot(t, x)
ax.set_xlim(0, 0.2)
ax.set_xlabel('Time [s]')
ax.set_ylabel('Voltage [mV]')
```


### Plot commands

A nice overview on available plot types is given
[here](https://matplotlib.org/stable/plot_types/index.html).  See the
[matplotlib.axes API](https://matplotlib.org/stable/api/axes_api.html)
for a (long) list of member functions, including various types of
plots and annotations.

Here is a selection of often used plot commands:

- [`plot(x, y)`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html): plot y versus x with markers and connected by lines. 
- [`errorbar(x, y, yerr)`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.errorbar.html): plot errorbars (both vertical and horizontal ones)
- [`scatter(x, y, size, color)`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.scatter.html): plot y versus x with varying marker size and color.
- [`fill_between(x, y1, y2)`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.fill_between.html): fill area between a curve and an axis (or another curve).
- [`hist(x, bins)`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.hist.html): histogram (see also `np.histogram()` and `ax.bar()`).
- [`boxplot(x)`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.boxplot.html): box-whisker plot.
- [`contour(x, y, z)`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.contour.html): contour lines.
- [`pcolormesh(x, y, z)`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.pcolormesh.html): pseudocolor plot of a mtrix with specified x- and y-axis ranges.
- [`imshow(z)`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.imshow.html): plot an image - (almost) *never* use it for pseudocolor plots of matrices, use [`pcolormesh()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.pcolormesh.html) instead.


### Setting colors, lines, and markers

Further key-word arguments to the plot commands allow to change
colors, lines, and markers. In the following some of the more commonly
used ones are listed.

Lines:

- `color` or `c`: color specification, e.g. `'red'`, `'#DD0000'`, or `'C3'` (forth color of color cycle), see [specifying colors](https://matplotlib.org/stable/tutorials/colors/colors.html).
- `linewidth` or `lw`: width of connecting lines.
- `linestyle` or `ls`: solid, dashed, or dotted: '-', '--', '-.', ':', ''.

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
[`ax.set_xscale()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_xscale.html):
```py
ax.set_xlim(0.01, 1.0)
ax.set_xscale('log')
```
Likewise for the y-axis.

Make sure the data range starts at positive (non-zero) values using
[`ax.set_xlim()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_xlim.html) and [`ax.set_ylim()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_ylim.html).


### Legend

When you plot several data sets into an axes, you might want to add a
legend to your plot. Pass a `label` to the plot commands and then call
[`legend()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html):
```py
ax.plot(t, x, label='one')
ax.plot(t, 1.5*x, label='two')
ax.plot(t, 2.2*x, label='three')
ax.legend(loc='upper right')
```


### Annotation

You can place some text somewhere in (or outside) your plot using the
[`text()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.text.html)
function:
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
matplotlib figure to a file using the
[`savefig()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html)
function:
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
example generates two rows and three columns of axes (=subplots) using
the
[`subplots()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html)
function:
```py
fig, axs = plt.subplots(2, 3)
```
Now, `axs` is a 2-dimensional numpy array holding the six axes that we
use like this:
```py
axs[0,0].plot(t, x)    # top left plot
axs[1,2].plot(t, 2*x)  # bottom right plot
```

Alternatively to indexing the axes by both a row and a column index,
you can flatten the axes array:
```py
for k, ax in enumarate(axs.flat):
    ax.plot(x, k*y, label=f'{k}')
```

A single row or column of subplots can also be initialized like this:
```py
fig, (ax1, ax2) = plt.subplots(1, 2)
```

With the `sharex` and `sharey` key words, you can tie the respective
axis of the subplots together, such that is you zoom into one subplot,
the other ones get zoomed as well:
```py
fig, axs = plt.subplots(2, 3, sharex=True, sharey=True)
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
the [Arranging multiple Axes in a
Figure](https://matplotlib.org/stable/tutorials/intermediate/arranging_axes.html)
tutorial and the [GridSpec
tutorial](https://matplotlib.org/stable/tutorials/intermediate/gridspec.html).
Also check out the new
[subplot_mosaic()](https://matplotlib.org/stable/tutorials/provisional/mosaic.html) function.


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
"height" not "horizontal".


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


## Further reading and cheat sheets

- A gallery of various plots with [example](https://matplotlib.org/stable/plot_types/index.html) code.

- matplotlib provides some nice [cheat
  sheets](https://github.com/matplotlib/cheatsheets/blob/master/cheatsheets.pdf)

- and there are a number of
  [tutorials](https://matplotlib.org/stable/tutorials/index.html).


## How to prepare figures

Continue reading with suggestions on [how to prepare figures](guide.md). 