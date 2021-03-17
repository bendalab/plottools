import os
from collections import OrderedDict

# https://tug.org/FontCatalogue
# https://mirror.informatik.hs-fulda.de/tex-archive/macros/latex/required/psnfss/psnfss2e.pdf
# https://tex.stackexchange.com/questions/59702/suggest-a-nice-font-family-for-my-basic-latex-template-text-and-math/59706

fonts = OrderedDict()
fonts['default'] = ''
fonts['pslatex'] = '\\usepackage{pslatex}'
fonts['lmodern'] = '\\usepackage{lmodern}'
#fonts['dejavu'] = '\\usepackage{dejavu}'
fonts['bera'] = '\\usepackage{bera}'
fonts['stix'] = '\\usepackage{stix}'
fonts['libertine'] = '\\usepackage{libertine}\n\\usepackage[libertine]{newtxmath}'
fonts['kpfonts'] = '\\usepackage{kpfonts}'
fonts['mathpazo'] = '\\usepackage{mathpazo}'
fonts['mathptmx'] = '\\usepackage{mathptmx}'  # Times
fonts['newpx'] = '\\usepackage{newpxtext}\n\\usepackage{newpxmath}'
fonts['newtx'] = '\\usepackage{newtxtext}\n\\usepackage{newtxmath}'
fonts['default-sf'] = '\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sfmath}'
fonts['default-sf-sansmath'] = '\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sansmathfonts}'
fonts['pslatex-sf'] = '\\usepackage{pslatex}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sfmath}'
fonts['helvet-sansmath'] = '\\usepackage{sansmathfonts}\n\\usepackage[scaled=.92]{helvet}\n\\renewcommand{\\familydefault}{\\sfdefault}'  # Helvetica, sansmathfonts needs to be included first, sfmath is not so good
#fonts['dejavu-sf'] = '\\usepackage{DejaVuSans-TLF}'
fonts['bera-sf'] = '\\usepackage{bera}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sfmath}'
#fonts['bera-sf-lucbmath'] = '\\usepackage{bera}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage[expert]{lucbmath}\n\\def\\DeclareLucidaFontShape#1#2#3#4#5#6{\\DeclareFontShape{#1}{#2}{#3}{#4}{<->s*[0.90]#5}{#6}}'  # https://rcweb.dartmouth.edu/doc/texmf-dist/doc/fonts/bera/bera.txt
fonts['iwona'] = '\\usepackage[math]{iwona}'
fonts['kurier'] = '\\usepackage[math]{kurier}'
fonts['tgheros-sf'] = '\\usepackage{tgheros}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sfmath}'    
fonts['arev'] = '\\usepackage{arev}'
fonts['avant'] = '\\usepackage{avant}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sansmathfonts}'
fonts['cmbright'] = '\\usepackage{cmbright}\n\\SetSymbolFont{largesymbols}{normal}{OMX}{iwona}{m}{n}'
fonts['lmodern-sf'] = '\\usepackage{lmodern}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sfmath}'
fonts['kpfonts-sf'] = '\\usepackage[sfmath]{kpfonts}\n\\renewcommand{\\familydefault}{\\sfdefault}'
fonts['newtx-sf'] = '\\usepackage{newtxtext}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{newtxmath}\n\\usepackage{sfmath}'


def make_latex(secnum, fonts_key):
    fonts_str = fonts[fonts_key]
    base_name = fonts_key
    with open(base_name + '.tex', 'w') as df:
        df.write('\\documentclass[a4paper,11pt]{article}\n')
        df.write('\\usepackage[left=30mm, right=30mm, top=20mm]{geometry}\n')
        df.write('\\pagestyle{empty}\n')
        df.write('\\usepackage{graphicx}\n')
        df.write('\n')
        df.write('\\usepackage[T1]{fontenc}\n')
        df.write('\n')
        df.write(fonts_str)
        df.write('\n')
        df.write('\\begin{document}\n')
        df.write('\\setcounter{section}{%d}\n' % secnum)
        df.write('\\section{%s}\n' % base_name)
        df.write('\\begin{verbatim}\n')
        df.write(fonts_str)
        df.write('\n')
        df.write('\\end{verbatim}\n')
        with open('latexfonts-text.tex') as sf:
            for line in sf:
                df.write(line)
        df.write('\\end{document}\n')
        
    os.system('pdflatex %s' % base_name)
    os.remove(base_name + '.tex')
    os.remove(base_name + '.aux')
    os.remove(base_name + '.log')
    return base_name


if __name__ == "__main__":
    pdf_files = []
    for k, fonts_key in enumerate(fonts):
        pdf_file = make_latex(k, fonts_key)
        pdf_files.append(pdf_file + '.pdf')
    os.system('pdftk ' + ' '.join(pdf_files) + ' cat output latexfontsdemo.pdf')
    # pdfjam does not work properly!
    #os.system('pdfjam --a4paper -o latexfontsdemo.pdf ' + ' '.join(pdf_files))
    for pf in pdf_files:
        os.remove(pf)
