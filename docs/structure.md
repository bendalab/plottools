# How to structure your code

With our insights from [coding a figure](code.md) and from the [guide
lines](docs/guide.md) we arrive on some best-practice tips on how to
structure code for figures, such that:

- Others, including your future self, are able to modify your figures.
- Plot appearance can be changed quickly from a central module.
- Design and content are separated.
- It makes fun to improve your plots.


## File organization

Let's assume we need three figures that we call `basicdata`,
`methods`, and `coolresult`.  Then for each of the figures we will
have a separate python script ([guide line 1](docs/guide.md)) with the
respective name ([guide line 2](docs/guide.md)).  That way everybody
(or a Makefile for that matter) easily finds the script generating
that figure.

In addition, we will have a script defining the appearance of the
figures ([guide line 4](docs/guide.md)) that will be imported by all
of the scripts generating the actual figures. Let's call that script
`plotstyle.py`. This file is central for the separation of content
from layout.

We keep the file hierarchy flat and simply have four files in our
working directory:
``` txt
plotstyle.py
basicdata.py
methods.py
coolresult.py
```

Data files can also go along with the python scripts, or in a separate
sub-direcotry, for example `data/`.


## Object-oriented matplotlib interface

You should exclusively use the object-oriented interface of
matplotlib. That way it is always clear on which axes plot commands
are applied. And matplotlib recommends using the object-oriented
interface anyways (check out the [object-oriented
API](https://matplotlib.org/stable/api/index.html#the-object-oriented-api)
and [the lifecycle of a
plot](https://matplotlib.org/stable/tutorials/introductory/lifecycle.html#a-note-on-the-object-oriented-api-vs-pyplot)).


## The plotstyle module

The `plotstyle.py` module provides a function that we name here
`plot_style()`. This function contains code defining the overall
design of your plots. It sets some
[rcParams](https://matplotlib.org/stable/tutorials/introductory/customizing.html) and defines some [`plotting styles`](https://bendalab.github.io/plottools/api/styles.html). For now we just define two line styles and set the ticks
to point outwards:

```py
import matplotlib.pyplot as plt

def plot_style():
    # namespace for plotting styles:
    class s: pass
    s.lsSmall = dict(color='tab:red', lw=2)
    s.lsLarge = dict(color='tab:orange', lw=2)
    
    # global settings:
    plt.rcParam['xtick.direction'] = 'out'
    plt.rcParam['ytick.direction'] = 'out'
    
    return s
```

Of course, this function will be much larger as you keep working on
your plots. Step by step you improve and expand on the
[rcParams](https://matplotlib.org/stable/tutorials/introductory/customizing.html)
and the more data you plot the more [`plotting
styles`](https://bendalab.github.io/plottools/api/styles.html) you
need to add.

Working on the `plotstyle` module requires some effort in the very
beginning. Over time, however, the module converges to a state where
you only occasionally add another [`plotting
styles`](https://bendalab.github.io/plottools/api/styles.html). Choose
the names of the [`plotting
styles`](https://bendalab.github.io/plottools/api/styles.html), then
they are easy to use. And of course you can use it for all your aother
manuscripts, posters, or presentations. Just copy it over and adapt it
if necessary.


## Plotting scripts

So how to write a script generating a specific figure?

Let's start simple with the script `basicdata.py` generating a figure
with just a single panel (subplot).


### Package imports

First of all we need the usual imports of `numpy`, `scipy`, and
`pandas` as required, of course of `matplotlib.pyplot` and also of the
`plot_style()` function from our central `plotstyle.py` module:
```py
import numpy as np
import matplotlib.pyplot as plt
from plotstyle import plot_style
```

In contrast to your analysis scripts, try to keep the number of
imported packages as low as possible. This reduces dependencies to a
minimum and makes it easier to reuse the code for generating the
figures. A low number of imports should be no problem, because the
plotting scripts do only the plotting and are not supposed to do any
complex data analysis.  The results of complex computation are stored
in files. The plotting scripts just need to read these files and plot
their content - not much overhead is needed.

In particular this implies that we do not need to import `numba` for
plotting! And `embed()` from the `IPython` package should not be
needed - this is for more complicated issues than plotting.

A well readable import list is necessary so that one can easily trace
back the origin of some functions. To support this

- import only what is needed by your script
- import every package/symbol only once
- sort the imports according to package - common packages first, your
  own modules last.


### Main code

We start out at the bottom of the script with the
following two lines:
```py
if __name__ == "__main__":
    s = plot_style()
```
The call of the `plot_style()` function sets up the plot appearance
and returns a namespace containing various plotting styles as dicussed
above.

The following lines of code should set up the figure, call functions
generating the actual plots, and save the figure to a file. In case of
our simple example this looks like this:
```py
    fig, ax = plt.subplots(figsize=(6, 4))
    fig.subplots_adjust(top=0.95, bottom=0.1, left=0.1, right=0.95)
    plot_data(ax, s)
    fig.savefig('basicdata.pdf')
```

The call to `plt.subplots()` returns a new figure `fig` of the
specified size and a single axes `ax`.

Most certainly you need to adjust the figure margins via
[`fig.subplots_adjust()`](https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.subplots_adjust). A
good plot does not have excessive white space on the borders. In
particular if you include your figure in a LaTeX document it is much
simpler to handle when it tightly fills the figure
canvas. [`fig.tight_layout()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.tight_layout.html)
usually does not work, but you may give a try to the
`constrained_layout` argument to
[`plt.subplots()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html).
A problem with
[`fig.subplots_adjust()`](https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.subplots_adjust)
is, that the figure margins are specified relative to the figure
size. Whenever changing the figure size you need to readjust the
figure margins.

The following function call to `plot_data(ax)` does the actual
plotting. We discuss this in the next section.

Finally, the figure needs to be saved. The filename should be the same
as the name of the script to allow others to find the script given the
figure file. You may omit the file extension if you have set the
[rcParam](https://matplotlib.org/stable/tutorials/introductory/customizing.html)
`savefig.format` to your preferred format. In the context of
scientific publications this should be a vector graphic format like
`pdf` or `svg`.

Of course, you may stuff all this figure code into a function.


### Plot code

The basic unit of any figure is a plot, a single matplotlib axes.  You
may rearrange the position of an axes within a figure or even move an
axes to another figure. To allow for this flexibility, collecting all
code needed to draw the content of an axes into a single dedicated
function is central. This function takes as the first argument the
axes into which it should draw. As a second argument it takes the
namespace with the plotting styles.

*For every axes make a function that does the plotting and that takes
 this axes as an argument.*

In our example this is the `plot_data()` function that might look
like this:
```py
def plot_data(ax, s):
    x, y = load_data()
    ax.plot(x, y, **lsSmall)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
```
The first part of the function loads or generates the data to be
plotted - symbolized by the `load_data()` function call.  The second
part does the actual plotting. If you manage to separate content from
design well, then the functions for the actual plotting are usually
simple and sweet. Everybody can comprehend what is going on. The
function - the plot - can be easily reused in a different context.

Alternatively we could have called `load_data()` outside the
`plot_data()` function and pass the loaded data as arguments to the
plot function:
```py
    x, y = load_data()
    plot_data(ax, s, x, y)
```
Then `plot_data()` would only contain plot commands. This is in
particular useful for a multi-panel plot, where many panels use the
same data for their plotting.  On the other hand, in many cases the
data are loaded or generated in no time. So from a performance point
of view it does not hurt to load/generate them for any plot within
each plot function. But with the load function inside you need less
function arguments and the plot function can be more easily moved
somewhere else.


### Complexity/simplicity of the plot function

Most of the desing of the plots is handled by the central
`plot_style()` function as described above. Then the plot function
anly needs to provide content and usually gets quite simple. What is
left to specify simply is:

- what to plot, e.g. [`ax.plot(x,
  y)`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html). Of
  course, this might require several [plot
  commands](https://matplotlib.org/stable/plot_types/index.html), but
  if you provide the data such that they can be more or less directly
  passed to the plot commands, this stays simple.
- how to annotate,
  e.g. [`ax.text()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.text.html),
  [`ax.annotate()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.annotate.html)
  and/or some arrows.
- axis limits, e.g. [`ax.set_xlim()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_xlim.html).
- tick marks (actually that often is a matter of design and should not be here...).
- axis scaling,
  e.g. [`ax.set_xscale('log')`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_xscale.html).
- axis labels, e.g. [`ax.set_xlabel()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_xlabel.html).

That's it. No hiding of spines, no fixing of tick positions, etc. All
these design issues should at least be bundled in some helper
functions that would go into the central `plotstyle.py` module. Having
code for the design directly in the plot function makes it very
tedious to change the design later on, because this then needs to be
changed in every plot function. Anyways, repeating the same commands
over and over in all the different plot functions is not considered
good coding style! Why should it be different for coding your figures?

How to provide the data for the plotting function is the only other
issue. You should make sure by means of other scripts that the data
are available in appropriate formats. The data should be stored in a
way that makes it simple to plot them. Then it is simply a matter of
loading a file and selecting, for example, the relevant rows and
columns. No rearranging, fixing, or whatever annoying stuff should be
needed to make the data plotable. All this should go into scripts that
output the files on which the plotting is based.

The big advantages of keeping the plotting- as well as the
data-handling code simple are

- less arguments need to be passed to the plot function, which makes
  the code less cluttered, and
- dependencies of the plot function are reduced, which makes it
  simpler to copy (or import) the plot function to another script and
  use it there.


### Multipanel figures

Scripts for multipanel figures follow the same structure as the
single-panel script discussed so far. We have the same minimal
imports. The main code setting up the figure is more complex, of
course. For example, the main code in a `coolresult.py` script might
look like this:
```py
if __name__ == "__main__":
    plot_style()
    fig, axs = plt.subplots(2, 2, figsize=(6, 4))
    fig.subplots_adjust(top=0.95, bottom=0.1, left=0.1, right=0.95, hspace=0.6, wspace=0.6)
    plot_waveform(axs[0,0])
    plot_temperature(axs[0,1])
    plot_signal_n_power(axs[1,0], axs[1,1])
    fig.savefig('coolresult.pdf')
```
With the `plt.subplots()` we generate an array of axes.

We pass `hspace` and `wspace` arguments to
[`fig.subplots_adjust()`](https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.subplots_adjust). Try
large values! You will be surprised how much better your plot looks
with lot's of white space between the panels, althought the panels get
smaller.
