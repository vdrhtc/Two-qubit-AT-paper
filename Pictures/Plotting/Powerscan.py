import pickle
from numpy import *
import matplotlib
from matplotlib import ticker, colorbar as clb

matplotlib.use('Qt5Agg')

from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes


class ZoomPlot:

    def __init__(self):

        self._load_data()

        fig, axes = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(5, 5))
        plt.subplots_adjust(wspace=.2, hspace=.2)

        for idx, ax in enumerate(axes.ravel()):

            X, Y, data = self._data[idx]["Current [A]"]*1e4,\
                         self._data[idx]["Frequency [Hz]"]/1e9, \
                         real(self._data[idx]["data"]*exp(1j*pi/2)).T*1e3

            if idx in [0]:
                data = data - median(data, axis=0)

            m = ax.pcolormesh(X, Y, data, rasterized=True, cmap="Spectral_r")
            if idx % 2 == 0:
                ax.set_ylabel('Frequency [GHz]');
            if idx > 1:
                ax.set_xlabel('Current [$10^{-4}$ A]');

        plt.text(.15, .8, r"$\left|20/2\right\rangle$", fontdict={"name": "STIX"}, fontsize=12,
                 transform=axes[0,0].transAxes, ha='center', color="black")
        plt.text(.8, .9, r"$\left|01\right\rangle$", fontdict={"name": "STIX"}, fontsize=12,
                 transform=axes[0,0].transAxes, ha='center', color="black")

        plt.text(.375, .025, r"$P_{exc} =$-20 dBm", fontdict={"name": "STIX"}, fontsize=12,
                 transform=axes[0,0].transAxes, ha='left', color="black")


        plt.text(.66, .025, r"-12 dBm", fontdict={"name": "STIX"}, fontsize=12,
                 transform=axes[0,1].transAxes, ha='left', color="black")

        plt.text(.7, .025, r"-6 dBm", fontdict={"name": "STIX"}, fontsize=12,
                 transform=axes[1,0].transAxes, ha='left', color="black")

        plt.text(.7, .025, r"0 dBm", fontdict={"name": "STIX"}, fontsize=12,
                 transform=axes[1,1].transAxes, ha='left', color="black")


        cbaxes1 = fig.add_axes([0.125,.95,0.5,.015])
        # clb.make_axes(axes[0, 0], location="top", shrink=0.8,
        #                         aspect=50, pad=0.075, anchor=(0, 1))[0]
        cb = plt.colorbar(m, ax=axes[0, 0], cax=cbaxes1, orientation="horizontal")
        cb.ax.set_title(r"$\mathfrak{Re} [S^{exp}_{21}]$ [mU]", position=(1.3,-2))

        plt.text(-0.35, 1.15, "(a)", fontdict={"name": "STIX"}, fontsize=22,
                 transform=axes[0,0].transAxes)

        plt.savefig("../powerscan.pdf", bbox_inches="tight", dpi=600)


    def _load_data(self):

        paths = ["powerscan/19-15-21 - II-TTS-01-20--20dbm/II-TTS-01-20--20dbm_raw_data.pkl",
                 "powerscan/19-46-21 - II-TTS-01-20--12dbm/II-TTS-01-20--12dbm_raw_data.pkl",
                 "powerscan/20-17-17 - II-TTS-01-20--6dbm/II-TTS-01-20--6dbm_raw_data.pkl",
                 "powerscan/21-56-58 - II-TTS-01-20-0dbm/II-TTS-01-20-0dbm_raw_data.pkl"]
        self._data = []
        for path in paths:
            with open(path, "rb") as f:
                self._data.append(pickle.load(f))


p = ZoomPlot()
