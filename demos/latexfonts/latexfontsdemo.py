import os
from collections import OrderedDict

fonts = OrderedDict()
"""
fonts['default'] = ''
"""
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
fonts['pslatex-sf'] = '\\usepackage{pslatex}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sfmath}'
fonts['helvet-sansmath'] = '\\usepackage{sansmathfonts}\n\\usepackage[scaled=.92]{helvet}\n\\renewcommand{\\familydefault}{\\sfdefault}'  # Helvetica
#fonts['dejavu-sf'] = '\\usepackage{DejaVuSans-TLF}'
fonts['bera-sf'] = '\\usepackage{berasans}\n\\renewcommand{\\familydefault}{\\sfdefault}'
fonts['stix-sf'] = '\\usepackage{stix}\n\\renewcommand{\\familydefault}{\\sfdefault}'
fonts['iwona'] = '\\usepackage[math]{iwona}'
fonts['tgheros-sf'] = '\\usepackage{tgheros}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sfmath}'    
fonts['arev'] = '\\usepackage{arev}'
fonts['avant'] = '\\usepackage{avant}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sfmath}'
fonts['cmbright'] = '\\usepackage{cmbright}\n\\SetSymbolFont{largesymbols}{normal}{OMX}{iwona}{m}{n}'
fonts['lmodern-sf'] = '\\usepackage{lmodern}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sfmath}'
fonts['kpfonts-sf'] = '\\usepackage[sfmath]{kpfonts}\n\\renewcommand{\\familydefault}{\\sfdefault}'
fonts['newtx-sf'] = '\\usepackage{newtxtext}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{newtxmath}\n\\usepackage{sfmath}'

# https://tug.org/FontCatalogue
# https://mirror.informatik.hs-fulda.de/tex-archive/macros/latex/required/psnfss/psnfss2e.pdf
# https://tex.stackexchange.com/questions/59702/suggest-a-nice-font-family-for-my-basic-latex-template-text-and-math/59706

def make_latex(fonts_key):
    fonts_str = fonts[fonts_key]
    base_name = fonts_key

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
        preamble = r'\usepackage[T1]{fontenc}'
        preamble += fonts_str.replace('\n', '')
        #preamble += r'\usepackage[warn]{textcomp}'
        df.write('plt.rcParams["text.latex.preamble"] = r"%s"\n' % preamble)
        df.write('fig, ax = plt.subplots(figsize=(16.0/2.54, 8.0/2.54))\n')
        df.write('fig.subplots_adjust(bottom=0.15)\n')
        df.write('ax.plot(x, y)\n')
        df.write('ax.set_xlabel(r"Time [ms]")\n')
        df.write('ax.set_ylabel(r"Current [nA]")\n')
        df.write('fig.savefig("%s-plot.pdf")\n' % base_name)
        df.write('plt.close()\n')
    os.system('python3 %s-plot.py' % base_name)
    os.remove(base_name + '-plot.py')

    if not os.path.isfile(base_name + '-plot.pdf'):
        return None
        
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
        df.write('\\section{%s}\n' % base_name)
        df.write('\\begin{verbatim}\n')
        df.write(fonts_str)
        df.write('\n')
        df.write('\\end{verbatim}\n')
        with open('latexfonts-text.tex') as sf:
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
    for fonts_key in fonts:
        pdf_file = make_latex(fonts_key)
        if pdf_file is not None:
            pdf_files.append(pdf_file + '.pdf')
    os.system('pdftk ' + ' '.join(pdf_files) + ' cat output latexfontsdemos.pdf')
    # pdfjam does not work properly!
    #os.system('pdfjam --a4paper -o latexfontsdemos.pdf ' + ' '.join(pdf_files))
    for pf in pdf_files:
        os.remove(pf)
