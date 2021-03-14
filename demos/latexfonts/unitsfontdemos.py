import os
from collections import OrderedDict

units = OrderedDict()
units['siunitx'] = ['siunitx', '\\usepackage[free-standing-units]{siunitx}']  # detect-all results in enlarged micros
units['siunits'] = ['SIunits', '\\usepackage[mediumspace,mediumqspace,Gray,amssymb]{SIunits}']

fonts = OrderedDict()
fonts['default'] = ['', '', '']
fonts['pslatex'] = ['\\usepackage{pslatex}', '', '']
fonts['lmodern'] = ['\\usepackage{lmodern}', '', '']
fonts['libertine'] = ['\\usepackage{libertine}\n\\usepackage[libertine]{newtxmath}', '', '']
fonts['kpfonts'] = ['\\usepackage{kpfonts}', '', '']
fonts['mathpazo'] = ['\\usepackage{mathpazo}', '', '']  # Palatino
fonts['mathptmx'] = ['\\usepackage{mathptmx}', '', '']  # Tinmes
fonts['newpx'] = ['\\usepackage{newpxtext}\n\\usepackage{newpxmath}', '', '']
fonts['newtx'] = ['\\usepackage{newtxtext}\n\\usepackage{newtxmath}', '', '']
fonts['default-sf'] = ['\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sfmath}', '', '']
fonts['pslatex-sf'] = ['\\usepackage{pslatex}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sfmath}', '', '']
#fonts['helvet'] = ['\\usepackage[scaled]{helvet}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sfmath}', '', '']
fonts['helvet-sansmath'] = ['\\usepackage{sansmathfonts}\n\\usepackage[scaled=.92]{helvet}\n\\renewcommand{\\familydefault}{\\sfdefault}', '', '']  # Helvetica
fonts['iwona'] = ['\\usepackage[math]{iwona}', '', '']
fonts['tgheros-sf'] = ['\\usepackage{tgheros}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sfmath}', '\\sisetup{text-ohm=\\text{\\ensuremath{\\mathsf{\\Omega}}}, math-ohm=\\mathsf{\\Omega}}', '']
fonts['arev'] = ['\\usepackage{arev}', '\\sisetup{text-micro=\\text{\\ensuremath{\mu}}, math-micro=\\mu, text-ohm=\\text{\\ensuremath{\\Omega}}, math-ohm=\\mathsf{\\Omega}}', '']
fonts['avant'] = ['\\usepackage{avant}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sfmath}', '', '']
fonts['cmbright'] = ['\\usepackage{cmbright}\n\\SetSymbolFont{largesymbols}{normal}{OMX}{iwona}{m}{n}', '\\sisetup{math-ohm=\\mathsf{\\Omega}}', '']
#fonts['cabin'] = ['\\usepackage[sfdefault]{cabin}\n\\usepackage{sfmath}', '\\sisetup{text-ohm=\\text{\\ensuremath{\\mathsf{\\Omega}}}, math-ohm=\\mathsf{\\Omega}}', '']
fonts['lmodern-sf'] = ['\\usepackage{lmodern}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{sfmath}', '', '']
fonts['kpfonts-sf'] = ['\\usepackage[sfmath]{kpfonts}\n\\renewcommand{\\familydefault}{\\sfdefault}', '', '']
fonts['newtx-sf'] = ['\\usepackage{newtxtext}\n\\renewcommand{\\familydefault}{\\sfdefault}\n\\usepackage{newtxmath}\n\\usepackage{sfmath}', '\\sisetup{text-ohm=\\text{\\ensuremath{\\mathsf{\\Omega}}}, math-ohm=\\mathsf{\\Omega}}', '']

# see https://tug.org/FontCatalogue
# and https://tex.stackexchange.com/questions/59702/suggest-a-nice-font-family-for-my-basic-latex-template-text-and-math/59706


def make_latex(units_key, fonts_key, units_fonts):
    units_file = units_key
    units_str = units[units_key][1]
    fonts_str = fonts[fonts_key][0]
    base_name = '%s-%s' % (units[units_key][0], fonts_key)
    with open(base_name + '.tex', 'w') as df:
        #df.write('\\documentclass[varwidth=16cm, border=10mm, 12pt]{standalone}\n')
        df.write('\\documentclass[a4paper,12pt]{article}\n')
        df.write('\\usepackage[left=30mm, right=30mm, top=20mm]{geometry}\n')
        df.write('\\pagestyle{empty}\n')
        df.write('\n')
        df.write('\\usepackage[T1]{fontenc}')
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
        df.write('\\input{%s-text}\n' % units_file)
        df.write('\\end{document}\n')
        
    os.system('pdflatex %s' % base_name)
    os.remove(base_name + '.tex')
    os.remove(base_name + '.aux')
    os.remove(base_name + '.log')
    return base_name


if __name__ == "__main__":
    pdf_files = []
    for k, units_key in enumerate(units):
        for fonts_key in fonts:
            pdf_file = make_latex(units_key, fonts_key, fonts[fonts_key][k+1])
            pdf_files.append(pdf_file + '.pdf')
    os.system('pdfjam --a4paper -o unitsfontdemos.pdf ' + ' '.join(pdf_files))
    for pf in pdf_files:
        os.remove(pf)
