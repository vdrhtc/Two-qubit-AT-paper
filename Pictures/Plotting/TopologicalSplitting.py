import pickle
from numpy import *
import matplotlib
from matplotlib import ticker, colorbar as clb

matplotlib.use('Qt5Agg')

from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from matplotlib.pyplot import MultipleLocator


class TopologicalSplitting:

    def __init__(self):
        with open('10-01-11.pkl', 'rb') as f:
            self._X, self._Y, self._plots = pickle.load(f)
        with open('10-01-11-2.pkl', 'rb') as f:
            dummy1, dummy2, plots2 = pickle.load(f)
            self._plots += plots2
        with open("transitions.pkl", "rb") as f:
            self._currs, self._transitions_1, self._transitions_2 = pickle.load(f)

        Omegas = array([(15, 7.5),
                        (30, 7.5),
                        (45, 7.5),
                        (7.5, 15),
                        (7.5, 30),
                        (7.5, 45),
                        (15, 45),
                        (30, 45),
                        (45, 45)])

        fig, axes = plt.subplots(3, 3, sharex=True, sharey=True, figsize=(10, 5))
        plt.subplots_adjust(wspace=.1, hspace=.2)

        for idx, ax in enumerate(axes.ravel()):
            m = ax.pcolormesh(self._X, self._Y, array(self._plots[idx]).T,
                              vmin=0, vmax=1, cmap="Spectral", rasterized=True)
            if idx in [8, 7, 6]:
                ax.set_xlabel("Current ($10^{-4}$ A)")
            if idx in [0, 3, 6]:
                ax.set_ylabel("$\omega_d^{(1,2)}/2\pi$ (GHz)")
            if idx in [0]:
                plt.text(.5, .7, "$\Omega_1: {0}$ MHz\n$\Omega_2: {1}$ MHz".format(Omegas[idx][0],
                                                                                   Omegas[idx][
                                                                                       1]),
                         fontsize=10,
                         transform=ax.transAxes, ha='center', color="black")
            else:
                plt.text(.5, .7, "${0}$ MHz\n${1}$ MHz".format(Omegas[idx][0],
                                                               Omegas[idx][
                                                                   1]),
                         fontsize=10,
                         transform=ax.transAxes, ha='center', color="black")

            # ax.plot(self._currs[len(self._currs) // 2 + 10:],
            #         self._transitions_1[len(self._currs) // 2 + 10:], "--", color="gray",
            #         linewidth=1)
            ax.plot(self._currs[len(self._currs) // 2 + 10:],
                    self._transitions_2[len(self._currs) // 2 + 10:], "--", color="gray",
                    linewidth=1)

            def transmon_spec(Ej, Ec, d, sws, period, offset, currs):
                Ej = Ej * abs(cos(pi * (currs - sws) / period + offset * pi) * \
                              sqrt((1 + d ** 2 * tan(
                                  pi * (currs - sws) / period + offset * pi) ** 2)))
                return sqrt(8 * Ej * Ec) - Ec

            currs = self._currs[len(self._currs) // 2 + 10:]

            f1 = transmon_spec(22.75, 0.22, 0.745, 4.145, 9.5, 1 / 2, currs)
            f2 = transmon_spec(18.15, 0.22, 0.7, 4.12, 6.4, 0, currs)

            # ax.plot(currs, f1, linewidth=1)
            # ax.plot(currs, f2, linewidth=1)

            Omega_1 = Omegas[idx][0]/1e3
            Omega_2 = Omegas[idx][1]/1e3

            # if idx in [3,4,5]:
            sub_currs = currs[f1>f2]
            sub_f1 = f1[f1>f2]
            sub_f2 = f2[f1>f2]
            sol = (sub_f1 ** 2 - sub_f2 ** 2 + Omega_1 ** 2 - Omega_2 ** 2) / 2 / (sub_f1 - sub_f2)
            ax.plot(sub_currs, sol, "--", color="black", linewidth=1)

            sub_currs = currs[f1<f2]
            sub_f1 = f1[f1<f2]
            sub_f2 = f2[f1<f2]
            sol = (sub_f1 ** 2 - sub_f2 ** 2 + Omega_1 ** 2 - Omega_2 ** 2) / 2 / (sub_f1 - sub_f2)
            ax.plot(sub_currs, sol, "--", color="black", linewidth=1)
            # else:
            #     sub_currs = currs[f1>f2]
            #     sub_f1 = f1[f1>f2]
            #     sub_f2 = f2[f1>f2]
            #     sol = (sub_f1 ** 2 - sub_f2 ** 2 + Omega_1 ** 2) / 2 / (sub_f1 - sub_f2)
            #     ax.plot(sub_currs, sol, "--", color="black", linewidth=1)
            #
            #
            #     sub_currs = currs[f1<f2]
            #     sub_f1 = f1[f1<f2]
            #     sub_f2 = f2[f1<f2]
            #     sol = (sub_f1 ** 2 - sub_f2 ** 2 + Omega_1 ** 2) / 2 / (sub_f1 - sub_f2)
            #     ax.plot(sub_currs, sol, "--", color="black", linewidth=1)

            ax.set_xlim(self._X[0], self._X[-1])
            ax.set_ylim(self._Y[0], self._Y[-1])

            ax.yaxis.set_major_locator(MultipleLocator(0.05))
            ax.tick_params(axis='y', rotation=70)

        plt.text(.075, .7, "10", fontsize=10,
                 transform=axes[0, 0].transAxes,
                 ha='center', color="black", rotation=-70)

        plt.text(.135, .15, "01", fontsize=10,
                 transform=axes[0, 0].transAxes,
                 ha='center', color="black", rotation=75)

        plt.text(.42, .45, "11/2", fontsize=10,
                 transform=axes[0, 0].transAxes,
                 ha='center', color="black", rotation=10)

        plt.text(.61, .26, "02/2", fontsize=10,
                 transform=axes[0, 0].transAxes,
                 ha='center', color="black", rotation=-47.5)

        cbaxes1 = fig.add_axes([0.5 - 0.25 + 0.01, .93, 0.5, .015])
        # clb.make_axes(axes[0, 0], location="top", shrink=0.8,
        #                         aspect=50, pad=0.075, anchor=(0, 1))[0]
        cb = plt.colorbar(m, ax=axes[0, 0], cax=cbaxes1, orientation="horizontal")
        cb.ax.set_title(r"$P_{\left|00\right\rangle}$", position=(1.05, -2), fontsize=13)

        plt.savefig("../topological_splittings.pdf", bbox_inches="tight", dpi=600)


TopologicalSplitting()
