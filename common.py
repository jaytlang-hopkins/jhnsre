import platform
import math
import numpy as np
import scipy.optimize as opt
        
# MARK: Significant figures

def sf(x, dx, tex=False):
    if dx == 0: return f"{x:g} ± 0"
    dx = abs(dx)

    exponent = math.floor(math.log10(dx))
    first_digit = dx / 10**exponent

    if first_digit < 2: precision = -exponent + 1
    else: precision = -exponent

    rounded_x = round(x, precision)
    rounded_dx = round(dx, precision)

    fmt = f"{{:.{max(0, precision)}f}}"
    s = f"{fmt.format(rounded_x)} ± {fmt.format(rounded_dx)}"

    if tex: return s.replace("±", r"\pm")
    else: return s

# MARK: Linear Fit

class LinearFit:
    def __init__(self, x, y, xerr=None, yerr=None, iterations=2):
        self.x = np.asarray(x); self.y = np.asarray(y)
        self.xerr = np.zeros_like(x) if xerr is None else np.asarray(xerr)
        self.yerr = np.zeros_like(y) if yerr is None else np.asarray(yerr)
        
        self._model = lambda x, m, b: m * x + b
        
        current_yerr = np.copy(self.yerr)
        
        for i in range(iterations):
            (self.m, self.b), pcov = opt.curve_fit(
                self._model, self.x, self.y,
                sigma=current_yerr,
                absolute_sigma=True
            )
            
            self.dm, self.db = np.sqrt(np.diag(pcov))
            current_yerr = np.sqrt(self.yerr**2 + (self.m * self.xerr)**2)

    def evaluate(self, x):
        return self._model(x, self.m, self.b)

    def evaluate_with_uncertainty(self, x, dx):
        result = self.evaluate(x)        
        uncertainty = math.sqrt((self.dm * x)**2 + (dx * self.m)**2 + self.db**2)
        return result, uncertainty

    def tex_label(self, yname="y", xname="x"):
        slope = sf(self.m, self.dm, tex=True)
        intercept = sf(self.b, self.db, tex=True)

        return rf"${yname} = ({slope}) {xname} + ({intercept})$"

    def __str__(self):
        return f"f(x) = ({sf(self.m, self.dm)}) * x + ({sf(self.b, self.db)})"
        
    def __repr__(self):
        return f"LinearFit(m={sf(self.m, self.dm)}, b={sf(self.b, self.db)})"

# MARK: Statistical utilities

def discrepancy(a, da, b, db):
    return round(abs(a - b) / np.sqrt(da**2 + db**2), 2)
    
def weighted_average(x, dx):
    weights = [uncertainty**-2 for uncertainty in dx]
    numerator_list = [x * w for x, w in zip(x, weights)]
    
    wav = sum(numerator_list) / sum(weights)
    uwav = 1 / (sum(weights)**0.5)

    return wav, uwav

# MARK: Measurements with various devicesw

def voltmeter_uncertainty(readout):
    # Per the device manual...
    unscaled_uncertainty = readout * 0.008
    
    if readout < 4: return unscaled_uncertainty + 0.001
    elif readout < 40: return unscaled_uncertainty + 0.01
    elif readout < 400: return unscaled_uncertainty + 0.1
    else: return readout * 0.01 + 3

def ammeter_uncertainty(readout):
    if readout < 400e-6: return readout * 0.01 + 0.2e-6
    elif readout < 4000e-6: return readout * 0.01 + 2e-6
    elif readout < 40e-3: return readout * 0.012 + 0.03e-3
    elif readout < 400e-3: return readout * 0.012 + 0.3e-3
    elif readout < 4: return readout * 0.015 + 0.005
    elif readout < 10: return readout * 0.015 + 0.05

    else: raise NotImplementedError("That's a big current!")
        
def lcm_uncertainty(readout):
    # Per the device manual
    if readout < 0.4: return readout * 0.025 + 0.0002
    elif readout < 4: return readout * 0.007 + 0.0002
    elif readout < 40: return readout * 0.005 + 0.002
    elif readout < 400: return readout * 0.005 + 0.02
    else: raise NotImplementedError("That's a big capacitance!")

