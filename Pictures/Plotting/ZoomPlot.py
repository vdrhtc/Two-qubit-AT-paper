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

        fig, axes = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(4.5, 4.5))
        plt.subplots_adjust(wspace=.2, hspace=.2)

        for idx, ax in enumerate(axes.ravel()):
            m = ax.pcolormesh(self._X, self._Y, real(array(self._plots[idx]).T),
                              vmax=1, vmin=0, rasterized=True, cmap="Spectral")
            if idx % 2 == 0:
                ax.set_ylabel('$\omega_d^{(1,2)}/2\pi$ (GHz)');
            if idx > 1:
                ax.set_xlabel('Current ($10^{-4}$ A)');


        self._Omega_2s = array([6e-3, 15e-3, 30e-3, 60e-3])*0.75
        self._plot_theory(axes)

        plt.text(.28, .9, r"$20/2$", fontdict={"name": "STIX"}, fontsize=12,
                 transform=axes[0, 0].transAxes, ha='center', color="black", rotation=-70)

        plt.text(.52, .9, r"$01-20$", fontdict={"name": "STIX"}, fontsize=12,
                 transform=axes[0, 0].transAxes, ha='center', color="black", rotation=-85)

        plt.text(.85, .32, r"$21/3$", fontdict={"name": "STIX"}, fontsize=12,
                 transform=axes[0, 0].transAxes, ha='center', color="black", rotation=-27.5)

        plt.text(.7, .9, r"$01$", fontdict={"name": "STIX"}, fontsize=12,
                 transform=axes[0, 0].transAxes, ha='center', color="black", rotation=70)

        plt.text(.12, .025, r"$\Omega_{1,2} / 2\pi  = $4.5 MHz ", fontdict={"name": "STIX"}, fontsize=12,
                 transform=axes[0,0].transAxes, ha='left', color="black")


        plt.text(.52, .025, r"11.25 MHz", fontdict={"name": "STIX"}, fontsize=12,
                 transform=axes[0,1].transAxes, ha='left', color="black")

        plt.text(.55, .025, r"22.5 MHz", fontdict={"name": "STIX"}, fontsize=12,
                 transform=axes[1,0].transAxes, ha='left', color="black")

        plt.text(.65, .025, r"45 MHz", fontdict={"name": "STIX"}, fontsize=12,
                 transform=axes[1,1].transAxes, ha='left', color="black")


        cbaxes1 = fig.add_axes([0.125,.95,0.65,.015])
        # clb.make_axes(axes[0, 0], location="top", shrink=0.8,
        #                         aspect=50, pad=0.075, anchor=(0, 1))[0]
        cb = plt.colorbar(m, ax=axes[0, 0], cax=cbaxes1, orientation="horizontal")
        cb.ax.set_title(r"$P_{\left|00\right\rangle}$", position=(1.125,-2), fontsize=13)

        plt.text(-0.35, 1.15, "(b)", fontdict={"name": "STIX"}, fontsize=20,
                 transform=axes[0,0].transAxes)


        plt.savefig("../zoom2_picture.pdf", bbox_inches="tight", dpi=600)

    def _plot_theory(self, axes):

        X = self._X
        Y = self._Y

        alpha_1 = -.22
        omega_1s = linspace(5.292, 5.197, len(X)) - alpha_1/2
        omega_2s = linspace(5.175, 5.319, len(X))

        for idx, ax in enumerate(axes.ravel()):

            # m = ax.plot(X, omega_2s, "--")
            # m = ax.plot(X, omega_1s + alpha_1/2, "--")

            sol1 = 2 * alpha_1 / 3 + 4 * omega_1s / 3 - omega_2s / 3 + \
                   sqrt(3 * self._Omega_2s[idx] ** 2 + (
                               alpha_1 + 2 * (omega_1s - omega_2s)) ** 2) / 3

            ax.plot(X[:len(X) // 2 + 10], sol1[:len(X) // 2 + 10], "--", color="black")
            ax.plot(X[len(X) // 2 + 10:], sol1[len(X) // 2 + 10:], ":", color="black")

            sol2 = 2 * alpha_1 / 3 + 4 * omega_1s / 3 - omega_2s / 3 - \
                   sqrt(3 * self._Omega_2s[idx] ** 2 + (
                               alpha_1 + 2 * (omega_1s - omega_2s)) ** 2) / 3

            ax.plot(X, sol2, "--", color="black")

            ax.set_xlim(min(X), max(X))
            ax.set_ylim(min(Y), max(Y))


p = ZoomPlot()
