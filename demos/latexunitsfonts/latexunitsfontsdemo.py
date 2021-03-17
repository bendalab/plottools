import os
from collections import OrderedDict

# see https://tex.stackexchange.com/questions/209302/possible-side-effect-of-siunitx-tgheroes-familydefault-combination

units = OrderedDict()
units['siunitx'] = ['siunitx', '\\usepackage[free-standing-units]{siunitx}']  # detect-all results in enlarged micros
#units['siunits'] = ['SIunits', '\\usepackage[mediumspace,mediumqspace,Gray,amssymb]{SIunits}']

# latex font, additional settings for siunitx, matplotlib rcParams
fonts = OrderedDict()
"""
fonts['default'] = ['', '', {'font.family': 'serif', 'mathtext.fontset': 'stix'}]
"""
fonts['pslatex'] = ['\\usepackage{pslatex}', '',
                    {'font.family': 'serif', 'mathtext.fontset': 'stix'}]
fonts['lmodern'] = ['\\usepackage{lmodern}', '',
                    {'font.family': 'serif', 'mathtext.fontset': 'stix'}]
"""
fonts['dejavu'] = ['\\usepackage{dejavu}', '',
                   {'font.family': 'serif', 'mathtext.fontset': 'stix'}]
fonts['bera'] = ['\\usepackage{bera}', '',
                 {'font.family': 'serif', 'mathtext.fontset': 'stix'}]
fonts['stix'] = ['\\usepackage{stix}', '',
                 {'font.family': 'serif', 'mathtext.fontset': 'stix'}]
fonts['libertine'] = ['\\usepackage{libertine}\n\\usepackage[libertine]{newtxmath}', '',
                      {'font.family': 'serif', 'mathtext.fontset': 'stix'}]
fonts['kpfonts'] = ['\\usepackage{kpfonts}', '',
                    {'font.family': 'serif', 'mathtext.fontset': 'stix'}]
fonts['mathpazo'] = ['\\usepackage{mathpazo}', '',
                     {'font.family': 'serif', 'mathtext.fontset': 'stix'}]  # Palatino
fonts['mathptmx'] = ['\\usepackage{mathptmx}', '',
                     {'font.family': 'serif', 'mathtext.fontset': 'stix'}]  # Times
fonts['newpx'] = ['\\usepackage{newpxtext}\n\\usepackage{newpxmath}', '',
                  {'font.family': 'serif', 'mathtext.fontset': 'stix'}]
#fonts['newtx'] = ['\\usepackage{newtxtext}\n\\usepackage{newtxmath}', '',
#                  {'font.family': 'serif', 'mathtext.fontset': 'stix'}]
fonts['default-sf'] = ['\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sfmath}', '',
                       {'font.family': 'sans-serif', 'mathtext.fontset': 'stixsans'}]
fonts['pslatex-sf'] = ['\\usepackage{pslatex}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sfmath}', '',
                       {'font.family': 'sans-serif', 'mathtext.fontset': 'stixsans'}]
fonts['helvet-sansmath'] = ['\\usepackage{sansmathfonts}\n\\usepackage[scaled=.92]{helvet}\n\\renewcommand{\\familydefault}{\\sfdefault}', '',
                            {'font.family': 'sans-serif', 'mathtext.fontset': 'stixsans'}]  # Helvetica
#fonts['dejavu-sf'] = ['\\usepackage{DejaVuSans-TLF}', '',
#                      {'font.family': 'sans-serif', 'mathtext.fontset': 'stixsans'}]
fonts['bera-sf'] = ['\\usepackage{berasans}\n\\renewcommand{\\familydefault}{\\sfdefault}',
                    '\\sisetup{text-ohm=\\text{\\ensuremath{\\mathsf{\\Omega}}}, math-ohm=\\mathsf{\\Omega}}',
                    {'font.family': 'sans-serif', 'mathtext.fontset': 'stixsans'}]
fonts['stix-sf'] = ['\\usepackage{stix}\n\\renewcommand{\\familydefault}{\\sfdefault}',
                    '\\sisetup{text-ohm=\\text{\\ensuremath{\\mathsf{\\Omega}}}, math-ohm=\\mathsf{\\Omega}}',
                    {'font.family': 'sans-serif', 'mathtext.fontset': 'stixsans'}]
"""                  
fonts['iwona'] = ['\\usepackage[math]{iwona}', '',
                  {'font.family': 'sans-serif', 'mathtext.fontset': 'stixsans'}]
fonts['tgheros-sf'] = ['\\usepackage{tgheros}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sfmath}', '\\sisetup{text-ohm=\\text{\\ensuremath{\\mathsf{\\Omega}}}, math-ohm=\\mathsf{\\Omega}}',
                       {'font.family': 'sans-serif', 'mathtext.fontset': 'stixsans'}]
"""                  
fonts['arev'] = ['\\usepackage{arev}', '\\sisetup{text-micro=\\text{\\ensuremath{\mu}}, math-micro=\\mu, text-ohm=\\text{\\ensuremath{\\Omega}}, math-ohm=\\mathsf{\\Omega}}',
                 {'font.family': 'sans-serif', 'mathtext.fontset': 'stixsans'}]
"""                  
fonts['avant'] = ['\\usepackage{avant}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sfmath}', '',
                  {'font.family': 'sans-serif', 'mathtext.fontset': 'stixsans'}]
fonts['cmbright'] = ['\\usepackage{cmbright}\n\\SetSymbolFont{largesymbols}{normal}{OMX}{iwona}{m}{n}', '\\sisetup{math-ohm=\\mathsf{\\Omega}}',
                     {'font.family': 'sans-serif', 'mathtext.fontset': 'stixsans'}]
"""
fonts['lmodern-sf'] = ['\\usepackage{lmodern}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sfmath}', '',
                       {'font.family': 'sans-serif', 'mathtext.fontset': 'stixsans'}]
fonts['kpfonts-sf'] = ['\\usepackage[sfmath]{kpfonts}\n\\renewcommand{\\familydefault}{\\sfdefault}', '',
                       {'font.family': 'sans-serif', 'mathtext.fontset': 'stixsans'}]
fonts['newtx-sf'] = ['\\usepackage{newtxtext}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{newtxmath}\n\\usepackage{sfmath}', '\\sisetup{text-ohm=\\text{\\ensuremath{\\mathsf{\\Omega}}}, math-ohm=\\mathsf{\\Omega}}',
                     {'font.family': 'sans-serif', 'mathtext.fontset': 'stixsans'}]
"""                     

# https://tug.org/FontCatalogue
# https://mirror.informatik.hs-fulda.de/tex-archive/macros/latex/required/psnfss/psnfss2e.pdf
# https://tex.stackexchange.com/questions/59702/suggest-a-nice-font-family-for-my-basic-latex-template-text-and-math/59706

def make_latex(units_key, fonts_key, units_fonts):
    units_file = units_key
    units_str = units[units_key][1]
    fonts_str = fonts[fonts_key][0]
    matplotlib_dict = fonts[fonts_key][2]
    base_name = '%s-%s' % (units[units_key][0], fonts_key)

    print()
    print('PLOT %s-plot.pdf' % base_name)

    with open(base_name + '-plot.py', 'w') as df:
        df.write('import numpy as np\n')
        df.write('import matplotlib as mpl\n')
        df.write('import matplotlib.pyplot as plt\n')
        df.write('\n')
        df.write('x = np.linspace(0.0, 10.0, 200)\n')
        df.write('y = np.sin(2.0*np.pi*0.5*x)\n')
        df.write('mpl.rcdefaults()\n')
        df.write('plt.rcParams["font.size"] = 11\n')
        #df.write('plt.rcParams["font.family"] = "sans-serif"\n')
        df.write('plt.rcParams["text.usetex"] = True\n')
        preamble = '\\usepackage[T1]{fontenc}'
        preamble += fonts_str.replace('\n', '')
        preamble += '\\usepackage[warn]{textcomp}'
        preamble += units_str.replace('\n', '')
        if len(units_fonts) > 0:
            preamble += units_fonts.replace('\n', '')
        df.write('plt.rcParams["text.latex.preamble"] = r"%s"\n' % preamble)
        df.write('fig, ax = plt.subplots(figsize=(16.0/2.54, 8.0/2.54))\n')
        df.write('fig.subplots_adjust(bottom=0.15)\n')
        df.write('ax.plot(x, y)\n')
        df.write('ax.set_xlabel(r"Time [\\si{\\micro\\second}]")\n')
        df.write('ax.set_ylabel(r"Resistance [\\si{\\mega\\ohm}]")\n')
        df.write('fig.savefig("%s-plot.pdf")\n' % base_name)
        df.write('plt.close()\n')
    os.system('python3 %s-plot.py' % base_name)
    os.remove(base_name + '-plot.py')
        
    with open(base_name + '.tex', 'w') as df:
        df.write('\\documentclass[a4paper,11pt]{article}\n')
        df.write('\\usepackage[left=30mm, right=30mm, top=20mm]{geometry}\n')
        df.write('\\pagestyle{empty}\n')
        df.write('\\usepackage{graphicx}\n')
        df.write('\n')
        df.write('\\usepackage[T1]{fontenc}\n')
        df.write('\n')
        df.write(units_str)
        df.write('\n')
        df.write(fonts_str)
        df.write('\n')
        if len(units_fonts) > 0:
            df.write(units_fonts)
            df.write('\n')
        df.write('\n')
        df.write('\\begin{document}\n')
        df.write('\\section{%s}\n' % base_name)
        df.write('\\begin{verbatim}\n')
        df.write(fonts_str)
        df.write('\n')
        df.write(units_str)
        df.write('\n')
        if len(units_fonts) > 0:
            df.write(units_fonts)
            df.write('\n')
        df.write('\\end{verbatim}\n')
        with open('%s-text.tex' % units_file) as sf:
            for line in sf:
                df.write(line.replace('IMAGEFILE', '%s-plot' % base_name))
        df.write('\\end{document}\n')
        
    os.system('pdflatex %s' % base_name)
    os.remove(base_name + '.tex')
    os.remove(base_name + '.aux')
    os.remove(base_name + '.log')
    os.remove(base_name + '-plot.pdf')
    return base_name


if __name__ == "__main__":
    pdf_files = []
    for k, units_key in enumerate(units):
        for fonts_key in fonts:
            unit_font = fonts[fonts_key][k+1] if k < 1 else ''
            pdf_file = make_latex(units_key, fonts_key, unit_font)
            pdf_files.append(pdf_file + '.pdf')
    os.system('pdftk ' + ' '.join(pdf_files) + ' cat output latexunitsfontsdemo.pdf')
    # pdfjam does not work properly!
    #os.system('pdfjam --a4paper -o latexunitsfontsdemo.pdf ' + ' '.join(pdf_files))
    for pf in pdf_files:
        os.remove(pf)
