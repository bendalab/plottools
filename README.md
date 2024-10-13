# plottools

Simplify production of publication-quality figures based on [matplotlib].

[matplotlib] is a powerful package for plotting in [python]. It allows
detailed control over every possible aspect of a plot. However, a lot
of the provided functionality is cumbersome to use and impossible to
remember. For specific use cases, however, a lot of this can be hidden
in dedicated functions. The `plottools` package does this for
scientific publications by adding a number of functions to
[matplotlib] [Axes] and [Figure] classes.

The second design goal of the `plottools` package is separation of
content and design. We know this from LaTeX documents. A good LaTeX
document contains only the text and the logical structure. The actual
layout (fonts, format of the sections, etc.) can then be entirely
controlled by the header without touching the text. Equivalently,
[python] scripts generating various figures should only provide the
data and necessary annotation like axes labels. The design should be
controllable by a single central function or module that is used by
all the scripts generating the figures. [matplotlib]'s [rcParams] are
a big step in this direction but do not completely reach this
goal. The `plottools` package expands on this, by providing additional
[rcParams], and by introducing the concept of [plot
styles](https://bendalab.github.io/plottools/api/styles.html).


## Modules

The following modules are provided by the `plottools` package.

See [API documentation](https://bendalab.github.io/plottools/api) of the
modules for more infos.


### Enhanced [matplotlib] functionality

Most modules patch the [matplotlib] [Figure] and [Axes] classes to provide
new functionality or some specialized interface:

- [`align`](https://bendalab.github.io/plottools/api/align.html):
  align axes labels.
- [`arrows`](https://bendalab.github.io/plottools/api/arrows.html):
  arrows.
- [`aspect`](https://bendalab.github.io/plottools/api/aspect.html):
  adapting plots to aspect ratio of axes.
- [`axes`](https://bendalab.github.io/plottools/api/axes.html):
  setting appearance of axes.
- [`circuits`](https://bendalab.github.io/plottools/api/circuits.html):
  electrical circuits.
- [`common`](https://bendalab.github.io/plottools/api/common.html):
  reduce common axis labels.
- [`figure`](https://bendalab.github.io/plottools/api/figure.html):
  size and file names of a [figure].
- [`insets`](https://bendalab.github.io/plottools/api/insets.html):
  insets made easy. [More...](docs/insets.md)
- [`labels`](https://bendalab.github.io/plottools/api/labels.html):
  annotate axis with label and unit.
- [`legend`](https://bendalab.github.io/plottools/api/legend/html):
  enhance legend text.
- [`neurons`](https://bendalab.github.io/plottools/api/neurons.html):
  draw sketches of neurons.
- [`scalebars`](https://bendalab.github.io/plottools/api/scalebars.html):
  labeled scale bars. [More...](docs/scalebars.md)
- [`significance`](https://bendalab.github.io/plottools/api/significance.html):
  indicating statsitical significance.
- [`spines`](https://bendalab.github.io/plottools/api/spines.html):
  modify the appearance of spines. [More...](docs/spines.md)
- [`subplots`](https://bendalab.github.io/plottools/api/subplots.html):
  enhanced subplots with margins. [More...](docs/subplots.md)
- [`tag`](https://bendalab.github.io/plottools/api/tag.html):
  tag axes with a label.
- [`text`](https://bendalab.github.io/plottools/api/text.html):
  enhance textual annotations.
- [`ticks`](https://bendalab.github.io/plottools/api/ticks.html):
  setting tick locations and formats. [More...](docs/ticks.md)
- [`title`](https://bendalab.github.io/plottools/api/title/html):
  enhance title text.

The patching is done by each module's `install_<module>()`
function. This function is called automatically upon importing the
module. While some modules simply add a few new member functions
(e.g. [`insets`](https://bendalab.github.io/plottools/api/insets.html))
others modify existing functions
(e.g. [`figure`](https://bendalab.github.io/plottools/api/figure.html)).
An `uninstall_<module>()` function is provided to undo the patching.

You usually do not need to care about the install/uninstall
functions. Simply import the module of interest and you are all set.


### Colors and styles

These two modules do not patch [matplotlib], but provide functions
aiding the separation of content and design:

- [`colors`](https://bendalab.github.io/plottools/api/colors.html):
  color palettes and tools for manipulating colors. [More...](docs/colors.md)
- [`styles`](https://bendalab.github.io/plottools/api/styles.html):
  plotting styles.


### Helper modules

These modules are used internally by other modules of the plottools
package:

- [`latex`](https://bendalab.github.io/plottools/api/latex.html):
  translate LaTeX texts.
- [`rcsetup`](https://bendalab.github.io/plottools/api/rcsetup.html):
  additional validators for `matplotlib.rcsetup`. 
- [`version`](https://bendalab.github.io/plottools/api/version.html):
  version of plottools and other packages.


## Importing plottools modules

Each module can be imported separately. No other functionality of the
`plottools` is then installed or executed. The only exception are the
[`plottools`](https://bendalab.github.io/plottools/api/plottools.html)
and [`params`](https://bendalab.github.io/plottools/api/params.html)
modules that import all the other modules. For example, if you are
only interested in the functions the
[`ticks`](https://bendalab.github.io/plottools/api/ticks.html) module
provides, then you can do

```py
import matplotlib.pyplot as plt
import plottools.ticks
# installs set_xticks_delta() (and other functions) on matplotlib Axes class

fig, ax = plt.subplots()
ax.set_xticks_delta(1.0)
```

For importing all `plottools` modules, simply import the module

- [`plottools`](https://bendalab.github.io/plottools/api/plottools.html):
  import all plottool modules and install their functions in [matplotlib].

i.e.

```py
import plottools.plottools as pt 
```

This also imports all the functions of the modules such they can be used
directly in the `pt` namespace. For example:

```py
light_blue = pt.lighter(pt.color_palettes['muted']['blue'], 0.4)
```

A special module is

- [`params`](https://bendalab.github.io/plottools/api/params.html):
  functions setting default [rcParams] settings for all modules.

which also imports and installs all other modules via the
[`plottools`](https://bendalab.github.io/plottools/api/plottools.html)
module. This module provides a few functions
(e.g. [`paper_style()`](https://bendalab.github.io/plottools/api/params.html#plottools.params.paper_style))
that set some default [rcParams] and add a number of plotting styles
to a namespace.

These functions can be used like this:

```py
from plottools.params import paper_style

class s: pass   # namespace for plotting styles
paper_style(s)  # install all plottool functions in matplotlib and populate s with plotting styles
fig, ax = plt.subplots(cmsize=(12, 8))  # new subplots() argument `cmsize`
ax.plot(x, y, **s.lsB1)                 # plotting style
ax.set_xticks_delta(0.5)      # new function for setting spacing of tick marks
fig.savefig()                 # use name of script as name for figure file
```

Usually you will not import the
[`params`](https://bendalab.github.io/plottools/api/params.html)
module, but rahter copy one of its functions and adapt them to your
own needs.


## Setting [rcParams]

Most modules have a `<module>_params()` function for setting rc
parameters to default values. In many cases these functions are just
an alternative way to set [matplotlib]'s [rcParams].  Many `plottools`
modules define additional [rcParams], that also can be set by these
functions.

The following modules just provide such a function as an alternative
interface for setting [matplotlib]'s [rcParams]:

- [`grid`](https://bendalab.github.io/plottools/api/git.html):
  setting grid appearance.

Usually, the `<module>_params()` have many arguments that by default
are set to `None`. Only the arguments that you provide and differ from
`None` are actually set, the other ones stay untouched. For example:

```py
from plottools.text import text_params

# set the default font size and family:
text_params(font_size=12.0, font_family='sans-serif')
# turn on LaTex mode:
text_params(latex=True)
```
This is equivalent to

```py
import matplotlib as mpl

mpl.rcParams['font.size'] = 12
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['text.usetex'] = True
```


## Demos

For a demonstration of the functionality of all modules run

```py
python demos.py
```

For demos of the individual modules in `plottools/`, 
run, for example,

```py
python -m src.plottools.spines
```

## Howtos

- A quick introduction to [matplotlib]: [Getting started with
  matplotlib](docs/starter.md).
- A general guidline for preparing figures for your next manuscript or
  presentation: [Figure guidelines](docs/guide.md).
- From spaghetti code to a structured code generating a figure:
  [Coding a figure](docs/code.md).
- A suggestion for structuring code that generates plot figures:
  [How to structure your code](docs/structure.md).


## Bug reporting

The `plottools` are still in a conceptual phase, interfaces might
change without notice and tests on various [python] and [matplotlib]
versions are not done yet. So getting an error is not unlikely.

Providing a pull request that fixes the error or provides new
functionality is, of course, most appreciated.

You can also open an issue, describing the error. Before doing so,
check whether you get the error when you run the demo of the
respective module. E.g.

```py
python -m src.plottools.figures
```

Mention the outcome in the issue.

In any case, run

```py
python -m src.plottools.version
```

and paste the output ([python], [numpy], [pandas], [matplotlib] and
`plottools` versions) into the issue.


## Documentation

The full [documentation](https://bendalab.github.io/plottools) is provided on 
[github.io](https://bendalab.github.io/plottools).


[matplotlib]: https://matplotlib.org/
[axes]: https://matplotlib.org/stable/api/axes_api.html
[figure]: https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure
[rcParams]: https://matplotlib.org/stable/tutorials/introductory/customizing.html
[python]: https://docs.python.org/3/
[numpy]: https://numpy.org/
[pandas]: https://pandas.pydata.org/