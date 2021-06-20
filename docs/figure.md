# Figure module

Size and file names of a figure.

Importing the figure module modifies the matplotlib functions
`plt.figure()`, `plt.subplots()`, `fig.savefig()`, and `plt.savefig()`.

```
import matplotlib.pyplot as plt
import plottools.figure
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
A `set_size_cm()` function is also provided:
```
fig = plt.figure()
fig.set_size_cm(12, 8)  # in centimeters
```


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
fig, ax = plt.subplots(2, 3)
# some fancy plots ...
fig.savefig()
```
The plot is saved in a file named `myplot.pdf`.

When only providing a path, the name of the script is appended:
```
fig.savefig('../')    # -> ../myplot.pdf
```

A string to be added to the name of the script is indicated by a initial '+':
```
fig.savefig('+-example')    # -> myplot-example.pdf
```

When saving a figure multiple times (for example when needed for a
LaTeX beamer talk), then you may want to use the '@' character in the
file name. This character in the file name is replaced by 'A', 'B',
'C', ...  according to how often `fig.savefig()` is called from within
the same figure.  If the '@' is the first character of the file name,
it is added to the name of the main script. So in 'example.py' we can
write

```py
fig.savefig('@')
fig.savefig('@')
latex_include_figures()
```
This prints to the console
```txt
\includegraphics<1>{myplotA}
\includegraphics<2>{myplotB}
```
and generates the respective files.


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
