"""
Translate LaTeX texts.


Used by the text module.


## Functions

- `translate_latex_text()`: translate text to fit both normal and LaTeX mode.
"""

import matplotlib as mpl


def translate_latex_text(s, **kwargs):
    """ Translate text to fit both normal and LaTeX mode.

    Attempts to modify the string such that inpedent of whether
    matplotlib is in LaTeX mode (`text.usetex = True`) or not, a useful
    result is produced. Best results are achieved, if strings are
    entirely written as LaTeX code.
    
    This is, in LaTeX mode (`text.usetex = True`) `fontstyle` and
    `fontweight` arguments are translated to corresponding LaTeX
    commands. Some unicode characters like thin space and
    micro are replaced by appropriate LaTeX commands.

    In non-LaTeX mode, '\\,' is translated to thin space, '\\micro' to
    upright unicode micro character. Escaped '&', '%', '$', '#', '_',
    '{', and '}' characters are unescaped.

    Parameters
    ----------
    s: string
        The text.
    kwargs: dict
        Key-word arguments for the text.
    fontstyle: string
        In LaTeX mode, if set to `italic` put text into '\\textit{}' command.
    fontweight: string
        In LaTeX mode, if set to `bold` put text into '\\textbf{}' command.

    Returns
    -------
    s: string
        Translated text.
    kwargs: dict
        Updated and adapted key-word arguments.
    """
    # italics and bold LaTeX font:
    if mpl.rcParams['text.usetex']:
        s = s.replace(u'\u2009', r'\,')
        s = s.replace(u'\u00B5', r'\micro{}')
        if 'fontstyle' in kwargs and kwargs['fontstyle'] == 'italic':
            del kwargs['fontstyle']
            s = r'\textit{' + s + r'}'
        if 'fontweight' in kwargs and kwargs['fontweight'] == 'bold':
            del kwargs['fontweight']
            s = r'\textbf{' + s + r'}'
    else:
        s = s.replace(r'\&', '&')
        s = s.replace(r'\%', '%')
        s = s.replace(r'\$', '$')
        s = s.replace(r'\#', '#')
        s = s.replace(r'\_', '_')
        s = s.replace(r'\{', '{')
        s = s.replace(r'\}', '}')
        s = s.replace(r'\,', u'\u2009')
        s = s.replace(r'\micro{}', u'\u00B5')
        s = s.replace(r'\micro ', u'\u00B5')
        s = s.replace(r'\micro', u'\u00B5')
    return s, kwargs

