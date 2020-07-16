# Spines module

Control spine visibility, bounds (extend of spine), and position
(moving it outward or inward).

To be able to use the show_spines(), set_spines_bounds() and
set_spines_outward() functions they need to be installed first by
means of the install_spines() function. For setting default spine
appearance import and call spines_params(). This function implicitely
installs all necessary functions, so no further call to installing
functions is needed.

```
import matplotlib.pyplot as plt
from plottools.spines import spines_params

spines_params('lb')
fig, (ax0, ax1, ax2) = plt.subplots(1, 3)
```

## Spine visibility

The `ax.show_spines()` functions controls visibility of spines and
modifies tick and label positions accordingly.

![show](figures/spines-show.png)

```
ax0.show_spines('lb')
ax1.show_spines('bt')
ax2.show_spines('tr')
```

## Spine bounds

The length of the spine can span
- the full length of the axis as set by the axis's limits ('full'),
- the extend of the data or the closest tick locations ('data'),
- the range between the minimum and maximum tick location ('ticks').

![bounds](figures/spines-bounds.png)

```
ax0.set_spines_bounds('lb', 'full')
ax1.set_spines_bounds('lb', 'data')
ax2.set_spines_bounds('lb', 'ticks')
```

## Spine position

Spines can be moved outward (positive offset in points)
or inward (negative offset).

![outward](figures/spines-outward.png)

```
ax0.set_spines_outward('lb', 0)
ax1.set_spines_outward('lb', 10)
ax2.set_spines_outward('lb', -10)
```

## Default spine appearance

The `spines_params()` controls the default appearance of spines.

