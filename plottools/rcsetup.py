"""Additional validators for `matplotlib.rcsetup`. 

This module is used by a few other modules to provide validators for
new rcParams they provide.

## Validator functions

- `_validate_dict()`: validates a dictionary for matplotlib.rcsetup.
- `_validate_fontdict()`: validates a dictionary with font properties for matplotlib.rcsetup.


## Install/uninstall rcsetup functions

You usually do not need to call these functions. Upon loading the rcsetup
module, `install_rcsetup()` is called automatically.

- `install_rcsetup()`: install validators of the rcsetup module in matplotlib.rcsetup.
- `uninstall_rcsetup()`: uninstall all validators from matplotlib.rcsetup.
"""

import matplotlib.rcsetup as mrc


def _validate_dict(s):
    """ Validates a dictionary for matplotlib.rcsetup.
    """
    d = {}
    if isinstance(s, dict):
        d = s
    else:
        if len(s) < 2:
            return {}
        if s[0] != '{' or s[-1] != '}':
            raise ValueError('not a valid dictionary string: ' + s)
        for i in s[1:-1].strip().split(','):
            kv = i.split(':')
            if len(kv) != 2:
                raise ValueError('invalid key-value pair for dict in ' + s)
            d[kv[0].strip()] = kv[1].strip()
    return d

            
def _validate_fontdict(s):
    """ Validates a dictionary with font properties for matplotlib.rcsetup.
    """
    d = mrc.validate_dict(s)
    for k in d:
        if k in ('alpha', 'fontstretch', 'stretch'):
            d[k] = mrc.validate_float(d[k])
        elif k in ('fontsize', 'size'):
            d[k] = mrc.validate_fontsize(d[k])
        elif k in ('fontweight', 'weigth'):
            d[k] = mrc.validate_fontweight(d[k])
    return d

    
def install_rcsetup():
    """ Install validators of the rcsetup module in matplotlib.rcsetup.

    See also
    --------
    uninstall_rcsetup()
    """
    if not hasattr(mrc, 'validate_dict'):
        mrc.validate_dict = _validate_dict
    if not hasattr(mrc, 'validate_fontdict'):
        mrc.validate_fontdict = _validate_fontdict


def uninstall_rcsetup():
    """ Uninstall all validators from matplotlib.rcsetup.

    See also
    --------
    install_rcsetup()
    """
    if hasattr(mrc, 'validate_dict'):
        delattr(mrc, 'validate_dict')
    if hasattr(mrc, 'validate_fontdict'):
        delattr(mrc, 'validate_fontdict')


install_rcsetup()


