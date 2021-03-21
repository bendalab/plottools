# LaTeX font survey for science

In science we need various fonts for

- journal papers: spacious serif font
- project proposal: a potentially narrower serif font
- presentations: a nicely flowing sans serif font
- poster: sans serif font

The default computern modern LaTeX fonts look pretty nice but have
several drawbacks that have been overcome in recent years. You
definitely want to load a different font in your LaTeX
preamble. Choosing a different font, however, requires to find
matching fonts for

- main text, inclusively italics and bold text for emphasis and section titles
- math typesetting (greek symbols, brackets, integrals)
- units (via `siunitsx` or `SIunits` packages) both in text and math context
- plots via python matplotlib

With the demos provided in this directory we explore LaTeX fonts for
these specific requirements. In this directory a number of python
scripts `latex*demo.py` are provided that generate pdf examples for a
range of fonts covering the different use cases.

For each font setting, a little style file is provided (`fonts*.sty`)
that contains all the necessary commands to put into the preamble of a
LaTeX document. Alternatively, just copy the style file into the
directory of your document and include it into your preample like this:
```
\documentclass{article}
\usepackage{fontslibertine}
\begin{document}
...
\end{document}
```

First, a survey on various fonts for the different demands is
presented. In the final section, some recommendations for the
different use cases are given.


## Font survey

In the following we test various fonts.


### Fonts for the main text

Only changing the default font for your main text is simple. Look at
the [TUG font catalogue](https://tug.org/FontCatalogue), choose a font
you want, and add the necessay packages to your preamble.

Run
```
python3 latexfontsdemo.py
```
to generate `latexfontsdemo.pdf` showing how a number of fonts look
like and how to use them.


### Math fonts

For many serif fonts, a matching math font set is provided. For sans
serif fonts, finding matching math fonts is often more demanding.

A nice survey of free math fonts is provided at
http://milde.users.sourceforge.net/Matheschriften/matheschriften.html
(in german).

Again, run
```
python3 latexfontsdemo.py
```
to generate `latexfontsdemo.pdf` showing how a number of fonts look
like, both in normal text and in math mode, and how to use them.


### Units

...


### Plot fonts

Good typesetting style also uses fonts matching the main text font in
generated figures. matplotlib supports this by allowing to use LaTeX
directly for typesetting all text elements in a plot. Here the
question is not so much what exactly is the right font - this was
adressed above. Rather one needs to figure out how to convince
`matplotlib` do actually use the font you want.

...


### Units in plots

...


## Recommendations

From the considerations and results presented above, the following
fonts can be recommended for the different use cases in science.


### Journal papers

You definitely want to set your manuscript in a serif font for better
readability. The commonly used `Arial` font from clueless Word users
is a no go. Serifs are there for a good reason. They guide your eye
along the lines of a text.

Just use Latin Modern fonts. These are close to the original Computer
Modern fonts and are not too narrow, but also do not take up too much
space. Mathematical typesetting is also well supported.
```
\usepackage{lmodern}
\usepackage[T1]{fontenc}
```


### Project proposals

The Latin Modern font is good, but if you need a tighter font, because
you are running out of space, then `stix` is a good option:
```
\usepackage{stix}
\usepackage[T1]{fontenc}
```
Alternatives are `pslatex`, `libertine`, `mathptmx`, `newtx`.


### Presentations

For presentations you need a clear, good looking sans serif font. Tis
in itself is not a problem. Getting a matching math font, however, is
in many cases more difficult.

`Iwona` is nice and complete, but is on the more narrow side.

`Arev` is a nice sans serif font, somewhat on the heavy side.

`Computer Modern Bright` is a lighter sans serif font with good math support.


### Poster

Similar fonts as for presentations.


## Resources

- [TUG font catalogue](https://tug.org/FontCatalogue)
- [LaTeX2e font selection](https://www.latex-project.org/help/documentation/fntguide.pdf)
- [A Survey of Free Math Fonts for TeX and LaTeX](https://ctan.net/info/Free_Math_Font_Survey/survey.html)
- [Freie Mathematikschriften für LaTeX](http://milde.users.sourceforge.net/Matheschriften/matheschriften.html)
- [Filenames for TeX fonts](http://tug.org/fontname/fontname.html)
- [Fonts and TeX](http://tug.org/fonts/)
- [TeX user group](http://tug.org/)
- [The LaTeX project](https://www.latex-project.org/)
