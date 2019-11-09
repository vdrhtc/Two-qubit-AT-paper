import pickle
from numpy import *
import matplotlib
from matplotlib import ticker, colorbar as clb

matplotlib.use('Qt5Agg')

from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes


class ZoomPlot:

    def __init__(self):
        with open('zoom2.pkl', 'rb') as f:
            self._X, self._Y, self._plots = pickle.load(f)

        fig, axes = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(5, 5))
        plt.subplots_adjust(wspace=.2, hspace=.2)

        for idx, ax in enumerate(axes.ravel()):
            m = ax.pcolormesh(self._X, self._Y, real(array(self._plots[idx]).T),
                              vmax=1, vmin=0, rasterized=True, cmap="Spectral")
            if idx % 2 == 0:
                ax.set_ylabel('Frequency [GHz]');
            if idx > 1:
                ax.set_xlabel('Current [$10^{-4}$ A]');

        plt.text(.15, .8, r"$\left|20/2\right\rangle$", fontdict={"name": "STIX"}, fontsize=12,
                 transform=axes[0,0].transAxes, ha='center', color="black")
        plt.text(.8, .9, r"$\left|01\right\rangle$", fontdict={"name": "STIX"}, fontsize=12,
                 transform=axes[0,0].transAxes, ha='center', color="black")


        plt.text(.25, .025, r"$\Omega_{1,2}/2\pi =$8 MHz", fontdict={"name": "STIX"}, fontsize=12,
                 transform=axes[0,0].transAxes, ha='left', color="black")


        plt.text(.66, .025, r"15 MHz", fontdict={"name": "STIX"}, fontsize=12,
                 transform=axes[0,1].transAxes, ha='left', color="black")

        plt.text(.6, .025, r"30 MHz", fontdict={"name": "STIX"}, fontsize=12,
                 transform=axes[1,0].transAxes, ha='left', color="black")

        plt.text(.6, .025, r"60 MHz", fontdict={"name": "STIX"}, fontsize=12,
                 transform=axes[1,1].transAxes, ha='left', color="black")


        cbaxes1 = fig.add_axes([0.125,.95,0.65,.015])
        # clb.make_axes(axes[0, 0], location="top", shrink=0.8,
        #                         aspect=50, pad=0.075, anchor=(0, 1))[0]
        cb = plt.colorbar(m, ax=axes[0, 0], cax=cbaxes1, orientation="horizontal")
        cb.ax.set_title(r"$P_{\left|00\right\rangle}$", position=(1.125,-2))

        plt.text(-0.35, 1.15, "(b)", fontdict={"name": "STIX"}, fontsize=22,
                 transform=axes[0,0].transAxes)

        plt.savefig("../zoom2_picture.pdf", bbox_inches="tight", dpi=600)


p = ZoomPlot()
