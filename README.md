# plottools

Simplify creation of publication-quality figures based on matplotlib.

matplotlib is a powerful package for plotting in python. It allows
very detailed control over every possible aspect of a plot. However, a
lot of the provided functionality is combersome to use and impossible
to remember. For specific use cases, however, a lot of this can be
hidden in dedicated functions. The plottools package does this for
scientific publications and adds a number of functions to matplotlib
axes and figure classes.

The second design goal of the plottol package is separation of content
and design. We know this from LaTeX documents. A good LaTeX document
contains only the text and the logical structure. The actual layout
(fonts, format of the sections, etc.) can then be entirely controlled
by the header without touching the text. Equivalently, python scripts
generating various figures should only provide the data and necessary
annotation like axes labels. It's design should be controllable by a
single central function or module that is used by all the scripts
generating the figures. matplotlib's rc settings are a big step in
this direction but do not completely reach this goal. The plottools
package expands on this. See the styles module for details.

The following modules are provided by the plottools package:
- `styles`: layout settings and plot styles.
- `colors`: color palettes and tools for manipulating colors.
- `figure`: size and margins of a figure.
- `spines`: modify the appearance of spines.
- `ticks`: setting tick locations and formats.
- `labels`: annotate axis with label and unit and align axes labels.
- `arrows`: arrows.
- `labelaxes`: mark panels with a label.
- `insets`: insets made easy.
- `scalebars`: labeled scale bars.
- `significance`: indicating statsitical significance.

See documentation in the modules for more infos.

For all demos simply run
```
python demos.py
```
For demos of the individual modules in `plottools/`, 
run, for example,
```
python -m plottools.spines
```
