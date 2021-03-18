import os
import sys
from latexfontsdemo import fonts, fonts_serif, fonts_sans, make_latex


def make_plot(font_package, family, remove=True):
    print()
    print('PLOT %s-plot.pdf' % font_package)
    with open(font_package + '-plot.py', 'w') as df:
        df.write('import numpy as np\n')
        df.write('import matplotlib as mpl\n')
        df.write('import matplotlib.pyplot as plt\n')
        df.write('\n')
        df.write('x = np.linspace(0.0, 10.0, 200)\n')
        df.write('y = np.sin(2.0*np.pi*0.5*x)\n')
        df.write('mpl.rcdefaults()\n')
        df.write('plt.rcParams["font.size"] = 11\n')
        df.write('plt.rcParams["font.family"] = "%s"\n' % family)
        df.write('plt.rcParams["text.usetex"] = True\n')
        preamble = ''
        with open('%s.sty' % font_package) as sf:
            for line in sf:
                preamble += line.strip()
        #preamble += r'\usepackage[warn]{textcomp}'
        df.write('plt.rcParams["text.latex.preamble"] = r"%s"\n' % preamble)
        df.write('fig, ax = plt.subplots(figsize=(16.0/2.54, 8.0/2.54))\n')
        df.write('fig.subplots_adjust(bottom=0.15)\n')
        df.write('ax.plot(x, y)\n')
        df.write('ax.set_xlabel(r"Time [ms]")\n')
        df.write('ax.set_ylabel(r"Current [nA]")\n')
        df.write('fig.savefig("%s-plot.pdf")\n' % font_package)
        df.write('plt.close()\n')
    ret_val = os.system('python3 %s-plot.py' % font_package)
    if remove:
        os.remove(font_package + '-plot.py')
    if ret_val == 0:
        return True
    else:
        if os.path.isfile(font_package + '-plot.pdf'):
            os.remove(font_package + '-plot.pdf')
        return False


if __name__ == "__main__":
    # set up font list:
    font_list = fonts
    save_failed = True
    merge_pdfs = True
    if len(sys.argv) > 1:
        font_list = sys.argv[1:]
        save_failed = False
        merge_pdfs = False
    # make demo pages:
    pdf_files = []
    failed_fonts = []
    for k, font_package in enumerate(font_list):
    #for k, font_package in enumerate(['fontscomfortaa']):
    #for k, font_package in enumerate(['fontskpfonts']):
        family = 'sans_serif' if font_package in fonts_sans else 'serif'
        if make_plot(font_package, family, merge_pdfs):
            make_latex(k, font_package, 'latexplotfonts-text.tex', True)
            os.remove(font_package + '-plot.pdf')
            pdf_files.append(font_package + '.pdf')
        else:
            failed_fonts.append(font_package)
    # combine pages:
    print()
    if merge_pdfs:
        print('GENERATE latexplotfontsdemo.pdf')
        os.system('pdftk ' + ' '.join(pdf_files) + ' cat output latexplotfontsdemo.pdf')
        for pf in pdf_files:
            os.remove(pf)
    # report and save failed fonts:
    if len(failed_fonts) > 0:
        print()
        print('Failed to generate plots for')
        for font in failed_fonts:
            print('  ' + font)
        print('see failedfonts.txt for the list of failed font packages.')
        if save_failed:
            with open('failedfonts.txt', 'w') as df:
                for font in failed_fonts:
                    df.write(font + '\n')
    print()
