# Spines module

Control spine visibility, bounds (extend of spine), and position
(moving it outward or inward).

```
import matplotlib.pyplot as plt
import plottools.spines

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

The `set_default_spines()` controls the default appearance of spines.

