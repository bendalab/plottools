# plottools

Simplify production of publication-quality figures based on matplotlib.

[matplotlib](https://matplotlib.org/) is a powerful package for
plotting in python. It allows detailed control over every possible
aspect of a plot. However, a lot of the provided functionality is
combersome to use and impossible to remember. For specific use cases,
however, a lot of this can be hidden in dedicated functions. The
*plottools* package does this for scientific publications by adding a
number of functions to matplotlib axes and figure classes.

The second design goal of the plottools package is separation of
content and design. We know this from LaTeX documents. A good LaTeX
document contains only the text and the logical structure. The actual
layout (fonts, format of the sections, etc.) can then be entirely
controlled by the header without touching the text. Equivalently,
python scripts generating various figures should only provide the data
and necessary annotation like axes labels. The design should be
controllable by a single central function or module that is used by
all the scripts generating the figures. matplotlib's rcParams are a
big step in this direction but do not completely reach this goal. The
plottools package expands on this. See the styles module for details.


## Modules

The following modules are provided by the plottools package:

- `styles`: layout settings and plot styles.
- `colors`: color palettes and tools for manipulating colors. [More...](docs/colors.md)
- `figure`: size, margins and file names of a figure.
- `spines`: modify the appearance of spines. [More...](docs/spines.md)
- `ticks`: setting tick locations and formats. [More...](docs/ticks.md)
- `labels`: annotate axis with label and unit and align axes labels.
- `text`: enhance textual annotations.
- `legend`: enhance legend text.
- `arrows`: arrows.
- `aspect`: adapting plots to aspect ratio of axes.
- `tag`: tag axes with a label.
- `axes`: simplify common axis labels.
- `insets`: insets made easy. [More...](docs/insets.md)
- `scalebars`: labeled scale bars. [More...](docs/scalebars.md)
- `significance`: indicating statsitical significance.
- `neurons`: draw sketches of neurons.

See [documentation](https://bendalab.github.io/plottools/api) in the
modules for more infos.

Most modules patch the matplotlib Figure and Axes classes. The
patching is done by each module's `install_<module>()` function. This
function is called automatically upon importing the module. A
`uninstall_<module>()` function is provided to undo the patching.  So
you usually do not need to care about the install/uninstall
functions. Simply import the module of interest and you are all set.

Each module can be imported separately. No other functionality of the
plottools is then installed or executed. The only exception is the
`styles` module that imports all the other modules. For example, if
you are only interested in the functions the `ticks` module provides,
then you can do
```py
import matplotlib.pyplot as plt
import plottools.ticks   # installs set_xticks_delta() (an others) on matplotlib Axes class

fig, ax = plt.subplots()
ax.set_xticks_delta(1.0)
```

Each module also has a `<module>_params()` function for setting
parameters to default values. In many cases these functions are just
an alternative way to set matplotlib's
[rcParams](https://matplotlib.org/stable/tutorials/introductory/customizing.html).
Many plottools define additional rcParams (right now in a separate
ptParams dictionary), that also can be set by this function.

Usually, the `<module>_params()` have many arguments that by default
are set to `None`. Only the arguments that you provide and differ from
`None` are actually set, the other ones stay untouched. For example:
```py
from plottools.text import text_params

# set the default fon size and family:
text_params(font_size=10.0, font_family='sans-serif')
# turn on LaTex mode:
text_params(latex=True)
```


## Demos

For a demonstration of the functionality of all modfules run
```py
python demos.py
```
For demos of the individual modules in `plottools/`, 
run, for example,
```py
python -m plottools.spines
```

## Howtos

- A quick introduction to matplotlib: [Getting started with
  matplotlib](docs/starter.md).
- A general guidline for preparing figures for your next manuscript or
  presentation: [How to prepare figures](docs/guide.md).


## Bug reporting

The plottools are still in a conceptual phase, interfaces might change
without notice and tests on various python and matplotlib versions
are not done yet. So getting an error is not unlikely.

Providing a pull request that fixes the error is, of course, most
appreciated.

You can also open an issue, describing the error. Before doing so,
check whether you get the error when you run the demo of the
respective module:
```py
python -m plottools.figures
```
Mention the outcome in the issue.

In any case, run
```py
python -m plottools.version
```
and paste the output (python, numpy, matplotlib and plottools
versions) into the issue.


## Documentation

[Documentation](https://bendalab.github.io/plottools)
