import pickle
from numpy import *
import matplotlib
from matplotlib import ticker, colorbar as clb

matplotlib.use('Qt5Agg')

from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from matplotlib.pyplot import MultipleLocator


class Powerscan1D:

    def __init__(self):

        self._load_data()

        fig, axes = plt.subplots(4, 3, sharex=False, sharey=False, figsize=(8, 6))
        plt.subplots_adjust(wspace=.3, hspace=.3)

        for idx, ax in enumerate(axes.ravel()[:-1]):

            X, Y, data = self._data[idx]["Current [A]"] * 1e4, \
                         self._data[idx]["Frequency [Hz]"] / 1e9, \
                         real(self._data[idx]["data"] * exp(1j * pi / 2)).T * 1e3

            # if idx in [0]:
            #     data = data - median(data, axis=0)

            m = ax.pcolormesh(X, Y, data, rasterized=True, cmap="Spectral_r")
            if idx % 3 == 0:
                ax.set_ylabel('Frequency (GHz)');
                ax.yaxis.set_major_locator(MultipleLocator(0.01))
                ax.set_xlabel("")
                ax.set_xticklabels([])
            if idx > 8:
                ax.set_xlabel('Current ($10^{-4}$ A)');

        self._Omega_2s = array([6e-3, 7.55e-3, 9.5e-3, 11.9e-3, 15e-3, 19e-3,
                                23e-3, 30e-3, 37.8e-3, 47.65e-3, 60e-3]) * 0.75
        self._plot_theory(axes)
        print(self._Omega_2s)

        cbaxes1 = fig.add_axes([0.125, .95, 0.5, .015])
        # clb.make_axes(axes[0, 0], location="top", shrink=0.8,
        #                         aspect=50, pad=0.075, anchor=(0, 1))[0]
        cb = plt.colorbar(m, ax=axes[0, 0], cax=cbaxes1, orientation="horizontal")
        cb.ax.set_title(r"$\mathfrak{Re}\ S^{exp}_{21}$", position=(1.3, -2))

        plt.text(-0.35, 1.15, "(a)", fontdict={"name": "STIX"}, fontsize=22,
                 transform=axes[0, 0].transAxes)

        # plt.savefig("powerscan_1d.png", dpi=400)

        plt.figure(figsize=(7, 2))
        mvolts = sqrt(10 ** (linspace(-20, 0, 11) / 10) * 1e-3 * 50) * 1e3
        plt.plot(mvolts, 1 / sqrt(3) * 2 * mvolts / 5, "black", label="Fit, " + \
                                                                      r"$\frac{2 \sqrt{3}}{3} V_{rms} \cdot %.2f$ MHz/mV" % (
                                                                              sqrt(
                                                                                  3) / 3 * 2 / 5)
                 )
        plt.plot(mvolts, self._Omega_2s * sqrt(3) / 3 * 2 * 1e3, "o", markersize=5, color="C0", label="Data")
        # plt.text(.1, .7, r"$\Omega_2 = \frac{2}{\sqrt{3}} V_{rms} \cdot %.2f$ MHz/mV" % (
        #         sqrt(3) / 3 * 2 / 5),
        #          fontdict={"name": "STIX"}, fontsize=12,
        #          transform=plt.gca().transAxes)
        plt.xlabel("$V_{rms}$ (mV)")
        plt.ylabel("Splitting (MHz)")
        plt.legend()
        plt.grid(color='black', linestyle=':', linewidth=1)

        plt.text(-0.1, 1.05, "(c)", fontdict={"name": "STIX"}, fontsize=20,
                 transform=plt.gca().transAxes)

        plt.savefig("../powerscan_1d.pdf", dpi=400, bbox_inches="tight")

        # plt.savefig("../powerscan.pdf", bbox_inches="tight", dpi=600)
        #

    def _plot_theory(self, axes):

        for idx, ax in enumerate(axes.ravel()[:-1]):
            X = self._data[idx]["Current [A]"] * 1e4
            Y = self._data[idx]["Frequency [Hz]"] / 1e9

            alpha_1 = - .22
            if idx in [0, 4, 7, 10]:
                omega_1s = linspace(5.3365, 5.2505, len(X)) - alpha_1 / 2
                omega_2s = linspace(5.2275, 5.3575, len(X))
            else:
                omega_1s = linspace(5.3315, 5.2525, len(X)) - alpha_1 / 2
                omega_2s = linspace(5.22, 5.3375, len(X))

            m = ax.plot(X, omega_2s, "--")
            m = ax.plot(X, omega_1s + alpha_1 / 2, "--")

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

    def _load_data(self):

        paths = ["powerscan/19-15-21 - II-TTS-01-20--20dbm/II-TTS-01-20--20dbm_raw_data.pkl",
                 "powerscan/09-17-58 - II-TTS-01-20--18dbm/II-TTS-01-20--18dbm_raw_data.pkl",
                 "powerscan/09-37-48 - II-TTS-01-20--16dbm/II-TTS-01-20--16dbm_raw_data.pkl",
                 "powerscan/09-57-37 - II-TTS-01-20--14dbm/II-TTS-01-20--14dbm_raw_data.pkl",
                 "powerscan/19-46-21 - II-TTS-01-20--12dbm/II-TTS-01-20--12dbm_raw_data.pkl",
                 "powerscan/10-17-31 - II-TTS-01-20--10dbm/II-TTS-01-20--10dbm_raw_data.pkl",
                 "powerscan/10-37-20 - II-TTS-01-20--8dbm/II-TTS-01-20--8dbm_raw_data.pkl",
                 "powerscan/20-17-17 - II-TTS-01-20--6dbm/II-TTS-01-20--6dbm_raw_data.pkl",
                 "powerscan/10-57-13 - II-TTS-01-20--4dbm/II-TTS-01-20--4dbm_raw_data.pkl",
                 "powerscan/11-17-35 - II-TTS-01-20--2dbm/II-TTS-01-20--2dbm_raw_data.pkl",
                 "powerscan/21-56-58 - II-TTS-01-20-0dbm/II-TTS-01-20-0dbm_raw_data.pkl"]
        self._data = []
        for path in paths:
            with open(path, "rb") as f:
                self._data.append(pickle.load(f))


p = Powerscan1D()
