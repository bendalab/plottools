# Figure module

Alternative ways to set the size, margins and default filename of a figure.

Calling `install_figure()` from the figure module adds some arguments
to the matplotlib functions `plt.figure()`, `plt.subplots()`,
`fig.add_gridspec()`, `gridspec.update()`, `fig.savefig()`,
`plt.savefig()`.
```
import matplotlib.pyplot as plt
from plottools.figure import install_figure

install_figure()
```

Then the following features are available:


## Figure size

The figure size can be specified in centimeters instead of inches via
the `cmsize` argument to `plt.figure()` and `plt.subplots()`. Like this:
```
fig = plt.figure(cmsize=(12, 8))  # in centimeters
```
or
```
fig = plt.subplots(3, 2, cmsize=(12, 8))  # in centimeters
```
Alternatively, a `set_size_cm()` function is provided:
```
fig = plt.figure()
fig.set_size_cm(12, 8)  # in centimeters
```


## Figure margins

In matplotlib margins, i.e. the space between the axes and the figure
edges, are controlled via `left`, `right`, `top`, and `bottom`
arguments to the `fig.subplots_adjust()` and related functions. These
arguments are given in fractions of the figure size as values ranging
between 0 and 1. This is often quite cumbersome, because the margins
get bigger if the figure size is enlarged, although the size of the
tick and axis labels stays the same.

The figure module introduces `leftm`, `rightm`, `topm`, and `bottomm`
as additional arguments to the `plt.subplots()`,
`fig.subplots_adjust()`, `fig.add_gridspec()` and `gridspec.update()`
functions. These arguments specify the margins in units of the current
font size, because the font size is what sets the size of the tick and
axis labels. And they are measured from the respective figure edge,
not from the figure's origin. I.e. specifying `topm=0` is the same as
`top=1`, and results in no margin to the top of the upper axes. In
addition, a resize event handler is installed, that ensures that the
margins stay the same (when specified by the new arguments) when you
resize the figure on the screen.

TODO: image illustrating figure margins.


## Default file name

It is good practice to have a python script save a figure under the
same name as the script (see our [plotting guidline](guide.md)). That
way it is easy to figure out, which script generated that figure,
whithout the need to use cool command line tools like `grep`. To
simplify this, the figure module patches the `fig.savefig()` function
to use the name of the script as the name of the outpt file, when
called without argument.

If you have a python script `myplot.py` producing a figure and saving it like this:
```
import matplotlib.pyplot as plt
from plottools.figure import install_figure

install_figure()

fig, ax = plt.subplots(2, 3)
# some fancy plots ...
fig.savefig()
```
The the plot is saved in a file named `myplot.pdf`.


## Strip fonts from a pdf figure

When using full LaTeX based typesetting in your figures, the resulting
files are quite large, because the LaTeX fonts are stored in the
files. When you then include these files in a LaTeX document, then the
resulting document can be really large, because for each included
figure the fonts are stored again and again in the pdf of the
document. The best solution I figured out to remove the excessive font
descriptions is to run the pdfs of the figures through the `ps2ps`
shell command (from Ghostscript). Then the standalone figure file may
look not that nice, but included into the LaTeX docuement it looks the
same as before and the resulting pdf is *much* smaller. To simplify
this post-processing step the figure module adds a `stripfont`
argument to `fig.savefig()`. When set `True`, then after the figure
has been saved to a pdf file it is run through `ps2ps` in order to
remove the fonts.

```
fig.savefig(stripfonts=True)
```

## Default settings

TODO: describe default file type.

