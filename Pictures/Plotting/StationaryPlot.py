import pickle
from numpy import *
import matplotlib
from matplotlib import ticker, colorbar as clb, patches

matplotlib.use('Qt5Agg')

from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes


class StationaryPlot:

    def __init__(self):
        with open("stationary.pkl", "rb") as f:
            currs, freqs, population10, energies = pickle.load(f)

        fig, axes = plt.subplots(1, 2, figsize=(8, 3), sharey=True)
        plt.subplots_adjust(wspace=.1, )

        mappable = axes[0].pcolormesh(currs, freqs, log10(array(population10)), rasterized=True,
                           cmap="Spectral_r")

        for ax in axes:
            rect1 = patches.Rectangle((3.5, 5.25), .3, .04,
                                      linewidth=1, edgecolor='black',
                                      facecolor='none', linestyle=":")
            ax.add_patch(rect1)
            rect2 = patches.Rectangle((2.925, 5.2275),
                                      3.225-2.925,
                                      5.2675-5.2275,
                                      linewidth=1, edgecolor='black',
                                      facecolor='none', linestyle=":")
            ax.add_patch(rect2)
            rect3 = patches.Rectangle((3.16, 5.3), .3, .04,
                                      linewidth=1, edgecolor='black',
                                      facecolor='none', linestyle=":")
            ax.add_patch(rect3)
            ax.annotate("1", xy=(3.48, 5.23), xytext=(3.575, 5.205), ha="center", fontsize=10,
                        arrowprops=dict(facecolor='black', width=.5, headwidth=3, headlength=3.5,
                                        shrink=0.05))

            ax.annotate('2', xy=(5.08, 5.21), xytext=(5.08, 5.18), ha="center", fontsize=10,
                        arrowprops=dict(facecolor='black', width=.5, headwidth=3, headlength=3.5,
                                        shrink=0.05))

            ax.annotate('3', xy=(3.31, 5.25), xytext=(3.31, 5.26), ha="center", fontsize=10,
                        arrowprops=dict(facecolor='black', width=.5, headwidth=3, headlength=3.5,
                                        shrink=0.05))

            ax.annotate('4', xy=(4.9, 5.195), xytext=(4.75, 5.195), ha="center", va="top", fontsize=10,
                        arrowprops=dict(facecolor='black', width=.5, headwidth=3, headlength=3.5,
                                        shrink=0.05))

            ax.annotate("5", xy=(3.5, 5.175), xytext=(3.65, 5.18), ha="center", va="center",
                        fontsize=10,
                        arrowprops=dict(facecolor='black', width=.5, headwidth=3, headlength=3.5,
                                        shrink=0.05))

        axes[1].pcolormesh(currs, freqs, log10(array(population10)), rasterized=True,
                           cmap="Spectral_r")

        m = 1
        t = .5
        typ1 = (0, (5, 0))
        typ2 = (0, (1, 2))
        secondary_colour = (0.5, 0.5, 0.2)

        plt.plot(currs, ((energies[:, 5].T - energies[:, 2]).T), linewidth=t, linestyle=typ2,
                 color=secondary_colour);  # 01->11
        plt.plot(currs, ((energies[:, 5].T - energies[:, 1]).T), linewidth=t, linestyle=typ2,
                 color=secondary_colour);  # 10-> 11

        plt.plot(currs, ((energies[:, 6].T - energies[:, 1]).T / 2), linestyle=typ2, linewidth=t,
                 color=secondary_colour);  # 01->21
        plt.plot(currs, ((energies[:, 6].T - energies[:, 2]).T / 2), linestyle=typ2, linewidth=t,
                 color=secondary_colour);  # 01->21
        plt.plot(currs, ((energies[:, 6].T - energies[:, 3]).T), linestyle=typ2, linewidth=t,
                 color=secondary_colour);  # 20->21
        plt.plot(currs, ((energies[:, 6].T - energies[:, 4]).T), linestyle=typ2, linewidth=t,
                 color=secondary_colour);  # 02->21

        plt.plot(currs, ((energies[:, 7].T - energies[:, 1]).T / 2), linestyle=typ2, linewidth=t,
                 color=secondary_colour, label='others');  # 10->12
        plt.plot(currs, ((energies[:, 7].T - energies[:, 2]).T / 2), linestyle=typ2, linewidth=t,
                 color=secondary_colour);  # 01->12
        plt.plot(currs, ((energies[:, 7].T - energies[:, 3]).T), linestyle=typ2, linewidth=t,
                 color=secondary_colour);  # 20->12
        plt.plot(currs, ((energies[:, 7].T - energies[:, 4]).T), linestyle=typ2, linewidth=t,
                 color=secondary_colour);  # 02->12
        plt.plot(currs, ((energies[:, 7].T - energies[:, 5]).T), linestyle=typ2, linewidth=t,
                 color=secondary_colour)  # 11->12

        plt.plot(currs, ((energies[:, 8].T - energies[:, 1]).T / 3), linestyle=typ2, linewidth=t,
                 color=secondary_colour);  # 10->22
        plt.plot(currs, ((energies[:, 8].T - energies[:, 2]).T / 3), linestyle=typ2, linewidth=t,
                 color=secondary_colour);  # 01->22
        plt.plot(currs, ((energies[:, 8].T - energies[:, 3]).T / 2), linestyle=typ2, linewidth=t,
                 color=secondary_colour);  # 20->22
        plt.plot(currs, ((energies[:, 8].T - energies[:, 4]).T / 2), linestyle=typ2, linewidth=t,
                 color=secondary_colour);  # 02->22

        plt.plot(currs, ((energies[:, 8].T - energies[:, 6]).T), linestyle=typ2, linewidth=t,
                 color=secondary_colour);  # 21->22

        plt.plot(currs, ((energies[:, 8].T - energies[:, 0]).T / 4), linestyle=typ2, linewidth=t,
                 color=secondary_colour);  # 00->22

        plt.plot(currs, ((energies[:, 1].T - energies[:, 0]).T), label=r"$\left|10\right\rangle$",
                 linewidth=m,
                 linestyle=typ1);  # 00->10

        plt.plot(currs, ((energies[:, 2].T - energies[:, 0]).T), label=r"$\left|01\right\rangle$",
                 linewidth=m,
                 linestyle=typ1);  # 00->01

        plt.plot(currs, ((energies[:, 3].T - energies[:, 0]).T / 2),
                 label=r"$\left|20/2\right\rangle$",
                 linewidth=m, linestyle=typ1);  # 00->20

        plt.plot(currs, ((energies[:, 4].T - energies[:, 0]).T / 2),
                 label=r"$\left|02/2\right\rangle$",
                 linewidth=m, linestyle=typ1);  # 00->02

        plt.plot(currs, ((energies[:, 4].T - energies[:, 1]).T),
                 label=r"$\left|10\right\rangle\rightarrow\left|02\right\rangle$", linewidth=m,
                 linestyle=typ1);  # 10->02

        plt.plot(currs, ((energies[:, 5].T - energies[:, 0]).T / 2), label=r"$\left|11/2\right\rangle$",
                 linewidth=m, linestyle=typ1)  # , color='black');  # 00->11

        plt.plot(currs, ((energies[:, 6].T - energies[:, 0]).T / 3), label=r"$\left|21/3\right\rangle$",
                 linestyle=typ1, linewidth=m , color='C7');  # 00->21/3

        plt.plot(currs, ((energies[:, 7].T - energies[:, 0]).T / 3), label=r"$\left|12/3\right\rangle$",
                 linestyle=typ1, linewidth=m, color="C9");  # 00->12

        plt.ylim(5.1, 5.5)
        plt.xlim(2,6)
        axes[0].set_ylabel("Frequency [GHz]")

        for ax in axes:
            ax.set_xlabel("Current [$10^{-4}$ A]")
        plt.legend(ncol=3, fontsize=5)

        cbaxes1 = fig.add_axes([.925, 0.11, 0.01, .7])
        cb = plt.colorbar(mappable, ax=axes[0], cax=cbaxes1, orientation="vertical")
        cb.ax.set_title(r"$\lg\, P_{\left|10\right\rangle}$", position=(3, 1))
        # print([val.get_text() for val in cb.ax.get_xticklabels()])
        # cbaxes1.set_xticklabels(["$10^{%s}$"%val.get_text() for val in  cb.ax.get_xticklabels()])
        plt.savefig("../stationary.pdf", bbox_inches="tight", dpi=600)


StationaryPlot()
