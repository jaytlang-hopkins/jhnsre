# JHNSRE: The JHU Near-Space Radiation Experiment

A balloon-borne Geiger counter that set out to measure the Pfotzer maximum,
failed in an electrically interesting way, and accidentally measured a
Paschen-like breakdown minimum at 25.2 ± 0.5 km altitude instead.

**Authors:** Jay Lang, Samvedh Cheruvu, Shreyas Krishnan, Leo Elkins

## What happened

We launched a Raspberry Pi + MightyOhm Geiger counter to 35.6 km on a weather
balloon. The high-voltage bias supply for the SBM-20 tube - a 555-driven
flyback converter - was unshielded against pressure changes. As the payload
ascended into the stratosphere, the air gap at the package shoulder of the
flyback transistor (Q1, FJN3303F, TO-92) entered the Paschen-active regime
and began breaking down on every switching cycle, radiating EMI directly
into the AC-coupled pulse-detection front end. The recorded count rates
peaked at ~430,000 CPM at 25 km - well above the SBM-20's physical maximum
of ~316,000 CPM, and ~5 orders of magnitude above any cosmic-ray secondary
flux.

Post-flight inspection of Q1 revealed carbonization on the package epoxy
between the leads, thermal bronzing of the leads themselves, and damage
asymmetric between the C-E and C-B paths consistent with the boost
converter's source-impedance asymmetry. An identical TO-92 package on the
same board (Q3, 2N3904) operating at low-voltage drive levels showed no
damage, serving as a clean negative control.

The count rate vs altitude curve traces out a parabolic feature on both
ascent and descent legs. Plotted as seconds-per-count vs atmospheric
pressure, the curve fits the Paschen functional form on the low-pressure
flank with sub-percent residuals, and recovers an effective gap of
~0.5 mm - independently consistent with the gap implied by the location
of the minimum alone.

## Result

(pd) at observed breakdown minimum: **2.5 ± 0.8 Pa·m**
Theoretical air Paschen minimum:    **1.12 ± 0.19 Pa·m**

Agreement within 2σ; residual attributable to non-ideal cylindrical-electrode
geometry and surface tracking.

## Repository layout


```
album/              Photos from launch day. TODO: add photos from the school!
analysis.ipynb      Main analysis notebook (data prep, fits, plots)
analysis.pdf        The above, but instructor readable
common.py           Utility functions I wrote for all our physics labs
data/               Minute-binned flight data. The full JSON is 2.6GB. You don't want it.
figures/            Plots used on the poster
LICENSE             GPL-3.0
Makefile
memes/              Work in progress.
poster.mplstyle     Matplotlib style for poster figures
poster.pdf          The poster itself
requirements.txt    Python dependencies
stratosphere/       Onboard data-collection daemon (TODO, rescue from ffs SD card)
text.mplstyle       Matplotlib style for PDF compilation
```

## Reproducing the analysis

```sh
pip install -r requirements.txt
jupyter notebook analysis.ipynb
```

The notebook loads `data/binned.csv` and produces every figure in
`figures/`. Set `FOR_POSTER` depending on what you want those figures
to look like.

## Acknowledgments

Our DEEPEST thanks to Fiore Family Hardware for helping us supply a truly
astonishing amount of helium during a national shortage.

In addition, we extend our sincerest gratitude to the elementary school
students of Bishop Guilfoyle academy. Dr. Mumford said he worried this project
might be over-ambitious, but as the kids taught us on Friday, anything is
possible - and any failed experiment is worthwhile.

## License

GPL-3.0. See LICENSE.

## A note on units

The Paschen calculations in this repository use SI units throughout
(p in Pa, d in m, pd in Pa·m). The Wikipedia constants A = 112.5 (kPa·cm)⁻¹
and B = 2737.5 V/(kPa·cm) are converted once at the top of the relevant
cell to A = 11.25 (Pa·m)⁻¹ and B = 273.75 V/(Pa·m). This avoids in-line
unit conversions that are easy to get wrong. We got them wrong at least
once.
