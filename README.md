# plottools

Simplify production of publication-quality figures based on matplotlib.

matplotlib is a powerful package for plotting in python. It allows
detailed control over every possible aspect of a plot. However, a lot
of the provided functionality is combersome to use and impossible to
remember. For specific use cases, however, a lot of this can be hidden
in dedicated functions. The plottools package does this for scientific
publications by adding a number of functions to matplotlib axes and
figure classes.

The second design goal of the plottools package is separation of
content and design. We know this from LaTeX documents. A good LaTeX
document contains only the text and the logical structure. The actual
layout (fonts, format of the sections, etc.) can then be entirely
controlled by the header without touching the text. Equivalently,
python scripts generating various figures should only provide the data
and necessary annotation like axes labels. The design should be
controllable by a single central function or module that is used by
all the scripts generating the figures. matplotlib's rc settings are a
big step in this direction but do not completely reach this goal. The
plottools package expands on this. See the styles module for details.

The following modules are provided by the plottools package:

- `styles`: layout settings and plot styles.
- `colors`: color palettes and tools for manipulating colors. [More...](docs/colors.md)
- `figure`: size and margins of a figure.
- `spines`: modify the appearance of spines. [More...](docs/spines.md)
- `ticks`: setting tick locations and formats. [More...](docs/ticks.md)
- `labels`: annotate axis with label and unit and align axes labels.
- `text`: enhance textual annotations.
- `arrows`: arrows.
- `axes`: tag axes with a label and simplify common axis labels.
- `insets`: insets made easy. [More...](docs/insets.md)
- `scalebars`: labeled scale bars. [More...](docs/scalebars.md)
- `significance`: indicating statsitical significance.

See documentation in the modules for more infos.

For a demonstration of the functionality of all modfules run
```
python demos.py
```
For demos of the individual modules in `plottools/`, 
run, for example,
```
python -m plottools.spines
```

## How to prepare figures

Read our [guidline](docs/guide.md) for preparing figures for your next paper manuscript or thesis.


## Documentation

[Documentation](https://bendalab.github.io/plottools)
