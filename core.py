import numpy as np
import matplotlib as mpl
import cv2
import scipy
fit = scipy.optimize.curve_fit
from win_precise_time import time
from uncertainties import unumpy
vals = unumpy.nominal_values
errs = unumpy.std_devs
from uncertainties import ufloat
#mpl.rc('text', usetex=False)
#mpl.rc('mathtext', fontset='cm')
#mpl.rc('font',family = 'serif', serif = 'cmr10', size=16)
import matplotlib.pyplot as plt
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)