# Subplots module

Enhanced subplots with margins.

Importing the subplots module modifies the matplotlib functions
`plt.subplots()`, `fig.add_gridspec()`, `gridspec.update()`. 

 ```
import matplotlib.pyplot as plt 
import plottools.subplots
```

Then the following features are available:


## Figure margins

In matplotlib margins, i.e. the space between the axes and the figure
edges, are controlled via `left`, `right`, `top`, and `bottom`
arguments to the `fig.subplots_adjust()` and related functions. These
arguments are given in fractions of the figure size as values ranging
between 0 and 1. This is often quite cumbersome, because the margins
get bigger if the figure size is enlarged, although the size of the
tick and axis labels stay the same.

The subplots module introduces `leftm`, `rightm`, `topm`, and
`bottomm` as additional arguments to the `plt.subplots()`,
`fig.subplots_adjust()`, `fig.add_gridspec()` and `gridspec.update()`
functions. These arguments specify the margins in units of the current
font size, because the font size is what sets the size of the tick and
axis labels. And they are measured from the respective figure edge,
not from the figure's origin. I.e. specifying `topm=0` is the same as
`top=1`, and results in no margin at the top of the upper axes. In
addition, a resize event handler is installed, that ensures that the
margins stay the same (when specified by the new arguments) when you
resize the figure on the screen.

TODO: image illustrating figure margins.


## Grid specs

`plt.subplots()` can be called with `width_ratios` and `height_ratios`.

Further, `figure.add_gridspec()` is made available for older
matplotlib versions that do not have this function yet.

To merge several subplots into a single axes, call `fig.merge()`.

