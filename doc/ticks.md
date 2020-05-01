# ticks module

```
fig, ax = plt.subplots()
```

## Increments

```
ax.set_xticks_delta(0.5)
```
![delta](figures/ticks-delta.png)


## Custom format

```
ax.set_xticks_format('%04.1f')
```
![format](figures/ticks-format.png)


## SU unit prefixes

```
ax.set_xscale('log')
ax.set_xlim(1e-6, 1e0)
ax.set_xticks_prefix()
```
![prefix](figures/ticks-prefix.png)


## Fractions

```
ax.set_xlim(-1, 1)
ax.set_xticks_fracs(4)
```
![fracs](figures/ticks-fracs.png)


## Multiples of Pi

```
ax.set_xlim(-np.pi, 2*np.pi)
ax.set_xticks_pifracs(2)
```
![pifracs](figures/ticks-pifracs.png)


## Pi in the denominator

```
ax.set_xlim(0, 4*np.pi/3)
ax.set_xticks_pifracs(3, True)
```
![pifracstop](figures/ticks-pifracstop.png)


## Fixed locations

```
ax.set_xticks_fixed((0, 0.3, 1))
```
![fixed](figures/ticks-fixed.png)


## Fixed locations and labels

```
ax.set_xticks_fixed((0, 0.5, 1), ('a', 'b', 'c'))
```
![fixedlabels](figures/ticks-fixedlabels.png)


## No tick labels

```
ax.set_xticks_blank()
```
![blank](figures/ticks-blank.png)


## No ticks at all

```
ax.set_xticks_off()
```
![off](figures/ticks-off.png)
