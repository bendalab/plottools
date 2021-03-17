import os
from collections import OrderedDict

# https://tug.org/FontCatalogue
# https://mirror.informatik.hs-fulda.de/tex-archive/macros/latex/required/psnfss/psnfss2e.pdf
# https://tex.stackexchange.com/questions/59702/suggest-a-nice-font-family-for-my-basic-latex-template-text-and-math/59706

fonts = [
    'fontsdefault',
    'fontspslatex',
    'fontslmodern',
    'fontsbera',
    'fontsstix',
    'fontslibertine',
    'fontskpfonts',
    'fontsmathpazo',
    'fontsmathptmx',
    'fontsnewpx',
    'fontsnewtx',
    'fontsdefaultsf',
    'fontsdefaultsansmath',
    'fontspslatexsf',
    'fontshelvetsansmath',
    'fontsberasf',
    'fontsbetoneuler',
    'fontsbiolinum',
    'fontscomfortaa',
    'fontsiwona',
    'fontskurier',
    'fontstgheros',
    'fontstgadventor-sf',
    'fontsarev',
    'fontsavant',
    'fontscmbright',
    'fontslmodernsf',
    'fontskpfontssf',
    'fontsnewtxsf',
]


def make_latex(secnum, font_package, text_fragment, remove=True):
    print()
    print('LATEX %s.tex' % font_package)
    with open(font_package + '.tex', 'w') as df:
        df.write('\\documentclass[a4paper,11pt]{article}\n')
        df.write('\\usepackage[left=30mm, right=30mm, top=20mm]{geometry}\n')
        df.write('\\usepackage{graphicx}\n')
        df.write('\\pagestyle{empty}\n')
        df.write('\n')
        df.write('\\usepackage{%s}\n' % font_package)
        df.write('\n')
        df.write('\\begin{document}\n')
        df.write('\n')
        df.write('\\setcounter{section}{%d}\n' % secnum)
        df.write('\\section{%s}\n' % font_package[5:])
        df.write('\n')
        df.write('\\begin{verbatim}\n')
        with open('%s.sty' % font_package) as sf:
            for line in sf:
                if len(line.strip()) > 0:
                    df.write(line)
        df.write('\\end{verbatim}\n')
        df.write('\n')
        with open(text_fragment) as sf:
            for line in sf:
                df.write(line.replace('IMAGEFILE', '%s-plot' % font_package))
        df.write('\n')
        df.write('\\end{document}\n')
        
    os.system('pdflatex %s' % font_package)
    if remove:
        os.remove(font_package + '.tex')
    os.remove(font_package + '.aux')
    os.remove(font_package + '.log')


if __name__ == "__main__":
    pdf_files = []
    for k, font_package in enumerate(fonts):
    #for k, font_package in enumerate(['fontscomfortaa']):
        make_latex(k, font_package, 'latexfonts-text.tex', True)
        pdf_files.append(font_package + '.pdf')
    os.system('pdftk ' + ' '.join(pdf_files) + ' cat output latexfontsdemo.pdf')
    for pf in pdf_files:
        os.remove(pf)
