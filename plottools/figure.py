"""
Size and file names of a figure.


Patches matplotlib to provide the following features:


## Figure size in centimeters

You can specify the figure size in centimeters:
```
fig = plt.figure(cmsize=(20.0, 16.0))         # in cm!
fig, ax = plt.subplots(cmsize=(16.0, 10.0))   # in cm!
```


## Default file names for figures

If no file name or only a file extension is specified in `fig.savefig()`,
then the file name of the main script is used. So you can call
```py
fig.savefig()
```
and get a 'figure.pdf' file (if the python script was called 'figure.py').
If the file name just specifies a path that ends with '/', then the name
of the main script is appended:
```py
fig.savefig('plots/')
```
writes the file `plots/figure.pdf'.

If the file name specified in `fig.savefig()` starts with a '+',
then this string without the plus is added to the name of the main script.
This is usefull for saving several figures for a (LaTeX beamer) talk.
For example, a python script named 'example.py'
```py
fig1.savefig('+-one')
fig2.savefig('+-two')
```
generates the files 'example-one.pdf' and 'example-two.pdf' (or whatever file type
was specified in `rcParams['savefig.format']`).

A '@' character in the file name is replaced by 'A', 'B', 'C', ...
according to how often `fig.savefig()` is called from within the same
figure. If the '@' is the first character of the file name,
it is added to the name of the main script. So in 'example.py' we can write
```py
fig.savefig('@')
fig.savefig('@')
latex_include_figures()
```
This prints to the console
```txt
\\includegraphics<1>{exampleA}
\\includegraphics<2>{exampleB}
```
and generates the respective files.
By setting `rcParams['savefig.counter']` (`counter` argument in `figure_params()`)
to 'A', 'a', or '1', '@' in file names is replaced 'A', 'B', 'C', ...,
'a', 'b', 'c', ... or '1', '2', '3', ..., respectively.


## Strip embedded fonts from pdf file

By setting `stripfonts=True` in `savefig()` or via
`rcParams['pdf.stripfonts']`, figures saved as pdf files
are run through `ps2pdf` in order to remove embedded fonts.
This significantly reduces the file size of the generated
figure files, and is in particular useful when using LaTeX mode
and including the figures in a LaTeX document.


## Functions

- `cm_size()`: convert dimensions from cm to inch.
- `latex_include_figures()`: print LaTeX `\\includegraphics<>{}` commands for all saved files.


## Figure member functions

- `set_size_cm()`: set the figure size in centimeters.
- `get_savefig_count()`: number of `savefig()` calls on the figure.


## Settings

- `figure_params()`: set savefig options via matplotlib's rc settings.

`mpl.rcParams` defined by the figures module:
```py
savefig.counter: 'A'
pdf.stripfonts: False
```


## Install/uninstall figure functions

You usually do not need to call these functions. Upon loading the figure
module, `install_figure()` is called automatically.

- `install_figure()`: install functions of the figure module in matplotlib.
- `uninstall_figure()`: uninstall all code of the figure module from matplotlib.
"""

import __main__
import os
import subprocess
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.rcsetup as mrc


def cm_size(*args):
    """ Convert dimensions from cm to inch.

    Use this function to set the size of a figure in centimeter:
    ```
    fig = plt.figure(figsize=cm_size(16.0, 10.0))
    ```

    Parameters
    ----------
    args: one or many float
        Size in centimeter.

    Returns
    -------
    inches: float or list of floats
        Input arguments converted to inch.
    """
    cm_per_inch = 2.54
    if len(args) == 1:
        return args[0]/cm_per_inch
    else:
        return [v/cm_per_inch for v in args]


def set_size_cm(fig, w, h=None, forward=True):
    """ Set the figure size in centimeters.

    Parameters
    ----------
    fig: matplotlib figure
        The figure of which to set the size.
    w: float or (float, float)
        If `h` is not specified, width and height of the figure in centimeters,
        otherwise the width of the figure.
    h: float or None
        Height of the figure in centimeters.
    forward : bool
        If ``True``, the canvas size is automatically updated, e.g.,
        you can resize the figure window from the shell.
    """
    if h is None:
        w, h = w
    winch, hinch = cm_size(w, h)
    fig.set_size_inches(winch, hinch, forward=forward)

    
def __plt_figure(num=None, cmsize=None, **kwargs):
    """ plt.figure() with `cmsize` argument to specify figure size in centimeters.
    """
    if cmsize:
        kwargs.update(figsize=cm_size(*cmsize))
    fig = plt.__figure_orig_figure(num, **kwargs)
    return fig


def __plt_subplots(*args, cmsize=None, **kwargs):
    """ plt.subplots() with figure size in cm.
    """
    if cmsize:
        kwargs.update(figsize=cm_size(*cmsize))
    fig, axs = plt.__subplots_orig_figure(*args, **kwargs)
    return fig, axs


plot_saved_files = []


def get_savefig_count(fig):
    """ Number of `savefig()` calls on the figure.

    Parameters
    ----------
    fig: matplotlib.figure
        The figure.    

    Returns
    -------
    counter: int
        The number of calls to `fig.savefig()` on this figure.
    """
    if hasattr(fig, '__saved_files_counter'):
        return fig.__saved_files_counter
    else:
        return 0


def __savefig_filename(fig, fname):
    """ Set default file name to name of main python script. """
    # increment figure counter:
    if not hasattr(fig, '__saved_files_counter'):
        fig.__saved_files_counter = 0
    fig.__saved_files_counter += 1
    # set file name:
    basename = os.path.splitext(os.path.basename(__main__.__file__))[0]
    if len(fname) == 0:
        fname = '.' + mpl.rcParams['savefig.format']
    if fname[0] in '.@' and '/' not in fname and os.path.sep not in fname:
        fname = basename + fname
    elif fname[0] == '+':
        fname = basename + fname[1:]
    if fname[-1] == '/' or fname[-1] == os.path.sep:
        fname += basename
    if '@' in fname:
        cs = chr(ord('A')+fig.__saved_files_counter-1)
        if mpl.rcParams['savefig.counter'] == 'a':
            cs = chr(ord('a')+fig.__saved_files_counter-1)
        elif mpl.rcParams['savefig.counter'] == '1':
            cs = '%d' % fig.__saved_files_counter
        fname = fname.replace('@', cs)
    if len(os.path.splitext(fname)[1]) <= 1:
        fname = os.path.splitext(fname)[0] + '.' + mpl.rcParams['savefig.format']
    # store file name and fiure counter:
    global plot_saved_files
    plot_saved_files.append([fname, fig.__saved_files_counter])
    return fname

        
def __savefig_stripfonts(fname, stripfonts):
    """ Postprocess pdf files. """
    if stripfonts is None:
        stripfonts = mpl.rcParams['pdf.stripfonts']
    if os.path.splitext(fname)[1] == '.pdf' and stripfonts:
        subprocess.call(['ps2pdf', '-dAutoRotatePages=/None', fname, 'tmp-'+fname])
        os.rename('tmp-'+fname, fname)

            
def __fig_savefig(fig, fname='', *args, stripfonts=None, **kwargs):
    """ Set default file name to the one of the main script.
    
    If no fileextension is given, then rcParams['savefig.format'] is used.
    """
    if hasattr(fname, '__len__'):
        fname = __savefig_filename(fig, fname)
        fig.__savefig_orig_figure(fname, *args, **kwargs)
        __savefig_stripfonts(fname, stripfonts)
    else:
        fig.__savefig_orig_figure(fname, *args, **kwargs)


def __plt_savefig(fname='', *args, stripfonts=None, **kwargs):
    """ Set default file name to the one of the main script.
    
    If no fileextension is given, then rcParams['savefig.format'] is used.
    """
    if hasattr(fname, '__len__'):
        fname = __savefig_filename(plt.gcf(), fname)
        plt.__savefig_orig_figure(fname, *args, **kwargs)
        __savefig_stripfonts(fname, stripfonts)
    else:
        fig.__savefig_orig_figure(fname, *args, **kwargs)


def latex_include_figures():
    """ Print LaTeX `\\includegraphics<>{}` commands for all saved files.

    This can then be copied directly into you LaTeX document to include
    the generated figures.  For multiple files from the same figure,
    beamer overlay specification are printed as well.

    Examples
    --------
    A python script named 'intro.py'
    ```py
    from plottools.figure import latex_include_figures
    ...
    fig1.savefig('@')
    fig1.savefig('@')
    fig2.savefig('data')
    latex_include_figures()
    ```
    writes to console
    ```txt
    \\includegraphics<1>{introA}
    \\includegraphics<2>{introB}
    \\includegraphics{data}
    ```
    """
    global plot_saved_files
    for k in range(len(plot_saved_files)):
        if plot_saved_files[k][1] <= 1 and \
           (k+1 >= len(plot_saved_files) or plot_saved_files[k+1][1] <= 1):
            plot_saved_files[k][1] = None
    for fname, counter in plot_saved_files:
        fname = os.path.splitext(fname)[0]
        if counter is not None:
            print(r'\includegraphics<%d>{%s}' % (counter, fname))
        else:
            print(r'\includegraphics{%s}' % fname)
    plot_saved_files = []
    

def figure_params(color=None, format=None, counter=None, dpi=None,
                  compression=None, fonttype=None, stripfonts=None,
                  cmsize=None):
    """Set figure parameter.
                  
    Only parameters that are not `None` are updated.

    Parameters
    ----------
    color: matplotlib color specification or 'none'
        Background color for the whole figure. Sets rcParam `figure.facecolor`.
    format: 'png', 'ps', 'pdf', 'svg'
        File format of the saved figure. Sets rcParam `savefig.format`.
    counter: 'A', 'a', or '1'
        Specifies how a '@' character in the file name passed to `fig.savefig()`
        is translated into a string. Sets rcParam `savefig.counter`.
    dpi: int
        For pixel graphics the number of dots per inch.
    compression: int
        Compression level of pdf file from 0 to 9.
        Sets rcParam `pdf.compression`.
    fonttype: 3 or 42
        Type 3 (Type3) or Type 42 (TrueType) fonts.
        Sets rcParams `pdf.fonttype` and `ps.fonttype`.
        Type3 use less disk space but are less well editable,
        Type42 use more disk space but are better editable in vector
        graphics software (says the internet).
    stripfonts: boolean
        If output file format is pdf, then run ps2pdf on the generated
        pdf file to strip it from embedded fonts. This might then look
        ugly as a standalone figure, but results in nice plots within
        a latex documents at a fraction of the file size.  Sets
        rcParam `pdf.stripfonts`.
    cmsize: tuple of floats
        Default width and height of a figure in centimeters.
    """
    if counter is not None and 'savefig.counter' in mrc._validators:
        mpl.rcParams['savefig.counter'] = counter
    if stripfonts is not None and 'pdf.stripfonts' in mrc._validators:
        mpl.rcParams['pdf.stripfonts'] = stripfonts
    if color is not None:
        mpl.rcParams['figure.facecolor'] = color
    if format is not None:
        mpl.rcParams['savefig.format'] = format
    if dpi is not None:
        mpl.rcParams['figure.dpi'] = dpi
    # these all have only minor effects on file size:
    if compression is not None:
        mpl.rcParams['pdf.compression'] = compression
    if fonttype is not None:
        mpl.rcParams['pdf.fonttype'] = fonttype
        mpl.rcParams['ps.fonttype'] = fonttype
    mpl.rcParams['pdf.use14corefonts'] = False
    mpl.rcParams['pdf.inheritcolor'] = False
    if cmsize is not None:
        mpl.rcParams['figure.figsize'] = cm_size(cmsize)


def install_figure():
    """ Install functions of the figure module in matplotlib.

    Patches a few matplotlib functions (`plt.figure()`,
    `plt.subplots()`, `fig.savefig()`, `plt.savefig()`).
    
    See also
    --------
    uninstall_figure()
    """
    if not hasattr(mpl.figure.Figure, 'set_size_cm'):
        mpl.figure.Figure.set_size_cm = set_size_cm
    if not hasattr(mpl.figure.Figure, 'get_savefig_count'):
        mpl.figure.Figure.get_savefig_count = get_savefig_count
    if not hasattr(plt, '__figure_orig_figure'):
        plt.__figure_orig_figure = plt.figure
        plt.figure = __plt_figure
    if not hasattr(mpl.figure.Figure, '__savefig_orig_figure'):
        mpl.figure.Figure.__savefig_orig_figure = mpl.figure.Figure.savefig
        mpl.figure.Figure.savefig = __fig_savefig
    if not hasattr(plt, '__savefig_orig_figure'):
        plt.__savefig_orig_figure = plt.savefig
        plt.savefig = __plt_savefig
    if not hasattr(plt, '__subplots_orig_figure'):
        plt.__subplots_orig_figure = plt.subplots
        plt.subplots = __plt_subplots
    # add figure parameter to rc configuration:
    if 'savefig.counter' not in mpl.rcParams:
        mrc._validators['savefig.counter'] = mrc.ValidateInStrings('savefig.counter', ['A', 'a', '1'])
        mrc._validators['pdf.stripfonts'] = mrc.validate_bool
        mpl.rcParams['savefig.counter'] = 'A'
        mpl.rcParams['pdf.stripfonts'] = False


def uninstall_figure():
    """ Uninstall all code of the figure module from matplotlib.

    See also
    --------
    install_figure()
    """
    if hasattr(mpl.figure.Figure, 'set_size_cm'):
        delattr(mpl.figure.Figure, 'set_size_cm')
    if hasattr(mpl.figure.Figure, 'get_savefig_count'):
         delattr(mpl.figure.Figure, 'get_savefig_count')
    if hasattr(plt, '__figure_orig_figure'):
        plt.figure = plt.__figure_orig_figure
        delattr(plt, '__figure_orig_figure')
    if hasattr(mpl.figure.Figure, '__savefig_orig_figure'):
        mpl.figure.Figure.savefig = mpl.figure.Figure.__savefig_orig_figure
        delattr(mpl.figure.Figure, '__savefig_orig_figure')
    if hasattr(plt, '__savefig_orig_figure'):
        plt.savefig = plt.__savefig_orig_figure
        delattr(plt, '__savefig_orig_figure')
    if hasattr(plt, '__subplots_orig_figure'):
        plt.subplots = plt.__subplots_orig_figure
        delattr(plt, '__subplots_orig_figure')
    # remove figure parameter from mpl.rcParams:
    mrc._validators.pop('savefig.counter', None)
    mrc._validators.pop('pdf.stripfonts', None)
    #del mpl.rcParams['savefig.counter']
    #del mpl.rcParams['pdf.stripfonts']


install_figure()

        
def demo():
    """ Run a demonstration of the figure module.
    """
    figure_params(counter='A')
    fig, axs = plt.subplots(2, 1, cmsize=(18.0, 10.0))  # figsize in cm!
    fig.suptitle('plottools.figure')
    [ax.set_visible(False) for ax in axs.ravel()]
    axs[0].set_visible(True)
    axs[0].text(0.1, 1.6, 'fig, ax = plt.subplots(2, 1, cmsize=(18.0, 10.0))')
    axs[0].text(0.1, 1.2, "fig.savefig('@')")
    x = np.linspace(0.0, 2.0, 200)
    axs[0].plot(x, np.sin(2.0*np.pi*x))
    axs[0].set_ylim(-1.0, 2.0)
    fig.savefig('@', stripfonts=True)
    axs[1].set_visible(True)
    axs[1].text(0.1, 1.6, "fig.savefig('@')")
    axs[1].plot(x, np.sin(4.0*np.pi*x))
    axs[1].set_ylim(-1.0, 2.0)
    fig.savefig('@', stripfonts=True)
    latex_include_figures()
    plt.show()


if __name__ == "__main__":
    demo()
