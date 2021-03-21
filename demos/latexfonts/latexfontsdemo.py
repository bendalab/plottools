import os
import sys
from collections import OrderedDict

# https://tug.org/FontCatalogue
# https://mirror.informatik.hs-fulda.de/tex-archive/macros/latex/required/psnfss/psnfss2e.pdf
# https://tex.stackexchange.com/questions/59702/suggest-a-nice-font-family-for-my-basic-latex-template-text-and-math/59706

fonts_serif = [
    'fontsdefault',
    'fontsams',
    'fontsmathabx',
    'fontspslatex',
    'fontslmodern',
    'fontsbera',
    'fontsstix',
    'fontsfourier',
    'fontsfouriernc',
    'fontslibertine',
    'fontstgtermes',
    'fontstgtermesqtxmath',
    'fontstgtermesmathptmx',
    'fontskerkis',
    'fontskerkismathdesign',
    'fontskpfonts',
    'fontsmathdesigncharter',
    'fontsmathdesignutopia',
    'fontsmathpazo',
    'fontsmathpazoeuler',
    'fontsmathpazomnsymbol',
    'fontspagella',
    'fontsmathptmx',
    'fontsnewpx',
    'fontsnewtx',
    'fontsanttor',
    ]

fonts_sans = [
    'fontsdefaultsf',
    'fontsdefaultsansmath',
    'fontspslatexsf',
    'fontshelvetsansmath',
    'fontsberasf',
    'fontsbeton',
    'fontsbetoneuler',
    'fontsbiolinum',
    'fontscomfortaa',
    'fontsiwona',
    'fontskurier',
    'fontsgfsneohellenic',
    'fontsgfsneohelleniciwona',
    'fontsgfsneohelleniclxfonts',
    'fontstgheros',
    'fontstgherosarev',
    'fontstgheroscmbright',
    'fontstgadventorsf',
    'fontstgadventorlxfonts',
    'fontsarev',
    'fontsarevisomath',
    'fontsavant',
    'fontscmbright',
    'fontslmodernsf',
    'fontslxfonts',
    'fontskpfontssf',
    'fontsnewtxsf',
]

fonts = fonts_serif + fonts_sans


def make_latex(secnum, font_package, text_fragment, remove=True):
    print()
    print('LATEX %s.tex' % font_package)
    font_name = font_package[5:]
    font_descr = []
    font_procon = []
    with open('%s.sty' % font_package) as sf:
        for line in sf:
            if len(line) > 0 and line[0] == '%':
                line = line.lstrip('%').strip()
                if len(line)>0 and not '---' in line:
                    if line[0] in '+-':
                        font_procon.append(line)
                    else:
                        font_descr.append(line)
            else:
                break
        if len(font_descr) > 0:
            font_name = font_descr.pop(0)
    with open(font_package + '.tex', 'w') as df:
        df.write('\\documentclass[a4paper,11pt]{article}\n')
        df.write('\\usepackage[left=30mm, right=30mm, top=20mm]{geometry}\n')
        df.write('\\usepackage{ifthen}\n')
        df.write('\\usepackage{graphicx}\n')
        df.write('\\pagestyle{empty}\n')
        df.write('\n')
        df.write('\\usepackage{%s}\n' % font_package)
        df.write('\n')
        df.write('\\newcommand\\hmmax{0} % fix "too many math alphabets" error introduced by bm package\n')
        df.write('\\newcommand\\bmmax{0} % fix "too many math alphabets" error introduced by bm package\n')
        df.write('\\usepackage{bm}\n')
        df.write('\\newcommand*{\\try}[2]{\\ifthenelse{\\isundefined{#1}}%\n')
        df.write('{\\textrm{undefined}}{#1{#2}}}\n')
        df.write('\\newcommand{\\abc}{abcdefghijklmnopqrstuvwxyz}\n')
        df.write('\\newcommand{\\ABC}{ABCDEFGHIJKLMNOPQRSTUVWXYZ}\n')
        df.write('\\newcommand{\\textdemo}{The quick brown fox jumps over the sleazy dog}\n')
        df.write('\\newcommand{\\mathdemo}{\\sqrt{2\\pi} \\int \\alpha_k \\sin(2\\pi f_k t) \, dt}\n')
        df.write('\n')
        df.write('\\begin{document}\n')
        df.write('\n')
        df.write('\\setcounter{section}{%d}\n' % secnum)
        df.write('\\section{%s}\n' % font_name)
        df.write('\n')
        for descr in font_descr:
            df.write('%s\n' % descr)
        if len(font_procon) > 0:
            df.write('\\begin{itemize}\n')
            df.write('\\setlength{\\itemsep}{0pt}\n')
            for procon in font_procon:
                df.write('\\item[$%s$] %s\n' % (procon[0], procon[2:]))
            df.write('\\end{itemize}\n')
        df.write('\n')
        if len(font_descr) + len(font_procon) > 0:
            df.write('\\bigskip\n')
            df.write('\\noindent\n')
        with open(text_fragment) as sf:
            for line in sf:
                df.write(line.replace('IMAGEFILE', '%s-plot' % font_package))
        df.write('\n')
        df.write('\\subsection{Usage}\n')
        df.write('\\texttt{%s.sty}:\n' % font_package)
        df.write('\\begin{verbatim}\n')
        with open('%s.sty' % font_package) as sf:
            for line in sf:
                if len(line.strip()) > 0 and line[0] != '%':
                    df.write(line)
        df.write('\\end{verbatim}\n')
        df.write('\\end{document}\n')
        
    os.system('pdflatex %s' % font_package)
    if remove:
        os.remove(font_package + '.tex')
    os.remove(font_package + '.aux')
    os.remove(font_package + '.log')


if __name__ == "__main__":
    # set up font list:
    font_list = fonts
    merge_pdfs = True
    if len(sys.argv) > 1:
        font_args = [font.replace('.sty', '') for font in sys.argv[1:]]
        font_list = []
        for font in font_args:
            if font not in fonts:
                font = 'fonts' + font
                if font not in fonts:
                    continue
            font_list.append(font)
        merge_pdfs = False
    # make demo pages:
    pdf_files = []
    for k, font_package in enumerate(font_list):
        make_latex(k, font_package, 'latexfonts-text.tex', merge_pdfs)
        pdf_files.append(font_package + '.pdf')
    # combine pages:
    print()
    if merge_pdfs:
        print('GENERATE latexfontsdemo.pdf')
        os.system('pdftk ' + ' '.join(pdf_files) + ' cat output latexfontsdemo.pdf')
        for pf in pdf_files:
            os.remove(pf)
