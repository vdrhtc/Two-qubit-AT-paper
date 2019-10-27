import pickle
from numpy import *
import matplotlib
from matplotlib import ticker, colorbar as clb

matplotlib.use('Qt5Agg')

from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes


class StationaryPlot:

    def __init__(self):

        with open("stationary.pkl", "rb") as f:
            currs, freqs, population10, energies = pickle.load(f)

        plt.pcolormesh(currs, freqs, log10(array(population10)), rasterized=True, cmap="Spectral_r")

        plt.savefig("../stationary.pdf", bbox_inches="tight", dpi=600)


StationaryPlot()