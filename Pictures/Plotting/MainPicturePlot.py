import pickle
import numpy as np
import matplotlib
from matplotlib import ticker, colorbar as clb

matplotlib.use('Qt5Agg')

from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes


class MainPicturePlot:

    def __init__(self):
        self._cache_file = "main_pic_cache.pkl"
        self._cmap = "Spectral_r"
        self.nstate = 0
        try:
            with open(self._cache_file, "rb") as f:
                self._cache = pickle.load(f)
        except:
            self._cache = {}
            with open(self._cache_file, "wb") as f:
                pickle.dump(self._cache, f)

    def plot(self):
        self._load_data()

        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 4), sharey=True)
        plt.subplots_adjust(wspace=.1)

        ax1, ax2 = axes

        self.plot_experiment(ax1)
        self.plot_theory(ax2)

        plt.savefig("../main_picture.pdf", bbox_inches="tight", dpi=800)

        with open(self._cache_file, "wb") as f:
            pickle.dump(self._cache, f)


    def plot_experiment(self, ax):

        data = self._X_exp, self._Y_exp, np.abs(self._C_exp - self._C_exp[0,0])
        img1 = ax.pcolormesh(*data, rasterized=True, vmin=0, vmax=.022, cmap = self._cmap)
        cbaxes1 = clb.make_axes(ax, location="top", shrink=0.8, aspect=50, pad=0.09, anchor=(0,0))[0]
        cb = plt.colorbar(img1, ax=ax, cax=cbaxes1, orientation="horizontal")
        ax.set_xlabel('Current ($10^{-4}$ A)');
        ax.set_ylabel('$\omega_d/2\pi$ (GHz)');
        cb.ax.set_title(r"$|\Delta S^{exp}_{21}|$", position=(1.125,-2.5))
        loc = ticker.MultipleLocator(base=0.01)  # this locator puts ticks at regular intervals
        cb.locator = loc
        cb.update_ticks()
        plt.text(-0.15, 1.1, "(a)", fontdict={"name": "STIX"}, fontsize=17,
                 transform=ax.transAxes)

        plt.text(.53, .815, r"$\omega_2(I)/2\pi$", fontdict={"name": "STIX"}, fontsize=7.5,
                 transform=ax.transAxes, ha='center')

        plt.text(.54, .355, r"$\omega_1(I)/2\pi$", fontdict={"name": "STIX"}, fontsize=7.5,
                 transform=ax.transAxes, ha='center')

        ax.annotate('spurious\nresonance', xy=(5, 5.37), xytext=(5.1, 5.45), ha="center", fontsize=10,
                    arrowprops=dict(facecolor='black', width =1, headwidth = 5, headlength = 7, shrink=0.05))


        ax.annotate("1", xy=(3.5, 5.2325), xytext=(3.64, 5.2075), ha="right", fontsize=10,
                    arrowprops=dict(facecolor='black', width =.5, headwidth = 3, headlength = 3.5, shrink=0.05))

        ax.annotate('2', xy=(5.07, 5.21), xytext=(5.07, 5.18), ha="center", fontsize=10,
                    arrowprops=dict(facecolor='black', width=.5, headwidth=3, headlength=3.5,
                                    shrink=0.05))

        ax.annotate('3', xy=(3.31, 5.25), xytext=(3.31, 5.265), ha="center", fontsize=10,
                    arrowprops=dict(facecolor='black', width=.5, headwidth=3, headlength=3.5,
                                    shrink=0.05))

        ax.annotate('4', xy=(4.9, 5.195), xytext=(4.8, 5.195), ha="center", va="top", fontsize=10,
                    arrowprops=dict(facecolor='black', width=.5, headwidth=3, headlength=3.5,
                                    shrink=0.05))

        ax.annotate("5", xy=(3.516, 5.177), xytext=(3.61, 5.1795), ha="center", va="bottom", fontsize=10,
                    arrowprops=dict(facecolor='black', width=.5, headwidth=3, headlength=3.5,
                                    shrink=0.05))

        J_eff = 8e-3*np.sqrt(2)
        lower_branch = 5.283
        x_pos = 5.41
        bar_size = 5e-2
        # ax.plot([x_pos+bar_size]*2, [lower_branch, lower_branch+J_eff], color="black", lw=.5)
        ax.plot([x_pos, x_pos + bar_size], [lower_branch] * 2, color="black", lw=.5)
        ax.plot([x_pos, x_pos + bar_size], [lower_branch+J_eff] * 2, color="black", lw=.5)


        ax.annotate(r"J$\sqrt{2}$", xy=(x_pos+bar_size+.01, lower_branch+J_eff/2), xytext=(x_pos+bar_size+.11, lower_branch+.01),
                    ha="left", va="bottom", fontsize=7,
                    arrowprops=dict(facecolor="black", width=.1, headwidth=3, headlength=3.5,
                                    shrink=0.1))
        self._zoom(ax, data, vmin=0, vmax = .022)

    def plot_theory(self, ax):
        # try:
        #     C = self._cache[self.nstate]
        # except KeyError:
        #     C = np.zeros(self._C_th.shape)
        #     for i in range(C.shape[0]):
        #         for j in range(C.shape[1]):
        #             C[i,j] = self._C_th[i][j][self.nstate][0][self.nstate].real
        #     self._cache[self.nstate] = C

        C = np.real(self._C_th.T)*1.3
        # C = (C-np.min(C)-np.ptp(C)/2)/np.ptp(C)*0.02+(0.02/2+0.0025)# + np.random.normal(scale=0.001,
                                                           #                    size=C.shape)
        data = self._X_th, self._Y_th, C
        img1 = ax.pcolormesh(*data, rasterized=True, vmax = .022, vmin=0, cmap = self._cmap)
        cbaxes1 = clb.make_axes(ax, location="top", shrink=0.7, aspect=50, pad=0.09, anchor=(1,0))[0]
        cb = plt.colorbar(img1, ax=ax, cax=cbaxes1, orientation="horizontal")
        ax.set_xlabel('Current ($10^{-4}$ A)');
        # ax.set_ylabel('Frequency [GHz]');
        cb.ax.set_title(r"$1.3 \, |\Delta S^{sim}_{21}$|", position=(-0.225,-3))
        loc = ticker.MultipleLocator(base=0.01)  # this locator puts ticks at regular intervals
        cb.locator = loc
        cb.update_ticks()

        ax.annotate("1", xy=(3.48, 5.23), xytext=(3.56, 5.205), ha="center", fontsize=10,
                    arrowprops=dict(facecolor='black', width=.5, headwidth=3, headlength=3.5,
                                    shrink=0.05))

        ax.annotate('2', xy=(5.07, 5.21), xytext=(5.07, 5.18), ha="center", fontsize=10,
                    arrowprops=dict(facecolor='black', width=.5, headwidth=3, headlength=3.5,
                                    shrink=0.05))

        ax.annotate('3', xy=(3.31, 5.245), xytext=(3.31, 5.26), ha="center", fontsize=10,
                    arrowprops=dict(facecolor='black', width=.5, headwidth=3, headlength=3.5,
                                    shrink=0.05))

        ax.annotate('4', xy=(4.9, 5.195), xytext=(4.8, 5.195), ha="center", va="top", fontsize=10,
                    arrowprops=dict(facecolor='black', width=.5, headwidth=3, headlength=3.5,
                                    shrink=0.05))

        ax.annotate("5", xy=(3.5, 5.175), xytext=(3.59, 5.1775), ha="center", va="bottom", fontsize=10,
                    arrowprops=dict(facecolor='black', width=.5, headwidth=3, headlength=3.5,
                                    shrink=0.05))

        plt.text(.67, .77, "01", fontsize=10,
                 transform=ax.transAxes, ha='center', rotation=-45)

        plt.text(.8, .77, "10", fontsize=10,
                 transform=ax.transAxes, ha='center', rotation=55)

        plt.text(.42, .6, "11/2", fontsize=10,
                 transform=ax.transAxes, ha='center', rotation=10)

        plt.text(.475, .525, "02/2", fontsize=10,
                 transform=ax.transAxes, ha='center', rotation=20)

        plt.text(.53, .465, "12/3", fontsize=10,
                 transform=ax.transAxes, ha='center')

        plt.text(.53, .07, "20/2", fontsize=10,
                 transform=ax.transAxes, ha='center')

        plt.text(-0.09, 1.1, "(b)", fontdict={"name": "STIX"}, fontsize=17,
                 transform=ax.transAxes)


        self._zoom(ax, data, vmin=0, vmax = .022)


    def _zoom(self, ax, data, vmin, vmax):

        color = "black"
        axins = zoomed_inset_axes(ax, 2.5, loc=4)  # zoom-factor: 2.5, location: upper-left
        axins1 = zoomed_inset_axes(ax, 2.5, loc=3)
        axinss1 = zoomed_inset_axes(ax, 2.5, loc=2)


        plt.text(0.04, 0.8, "I", fontdict={"name": "STIX"}, fontsize=10,
                 transform=axinss1.transAxes)
        plt.text(0.04, 0.8, "II", fontdict={"name": "STIX"}, fontsize=10,
                 transform=axins1.transAxes)
        plt.text(0.04, 0.8, "III", fontdict={"name": "STIX"}, fontsize=10,
                 transform=axins.transAxes)

        # ax1.broken_barh([(3.1,0.4)],(5.31,0.02),edgecolors = 'r', facecolors = 'none',linewidth= 1, linestyle = '--')
        for axis in ['top', 'bottom', 'left', 'right']:
            axins.spines[axis].set_color(color)
        axins.pcolormesh(*data, rasterized=True, vmax = vmax, vmin=vmin, cmap = self._cmap)
        for axis in ['top', 'bottom', 'left', 'right']:
            axins1.spines[axis].set_color(color)
        axins1.pcolormesh(*data, rasterized=True, vmax = vmax, vmin=vmin, cmap = self._cmap)
        for axis in ['top', 'bottom', 'left', 'right']:
            axinss1.spines[axis].set_color(color)
        axinss1.pcolormesh(*data, rasterized=True, vmax = vmax, vmin=vmin, cmap = self._cmap)
        x1, x2, y1, y2 = 3.5, 3.8, 5.25, 5.29  # specify the limits
        axins.set_xlim(x1, x2)  # apply the x-limits
        axins.set_ylim(y1, y2)  # apply the y-limits
        axins.set_yticks([])
        axins.set_xticks([])
        x1, x2, y1, y2 = 2.925, 3.225, 5.2275, 5.2675
        axins1.set_xlim(x1, x2)  # apply the x-limits
        axins1.set_ylim(y1, y2)  # apply the y-limits
        axins1.set_yticks([])
        axins1.set_xticks([])
        x1, x2, y1, y2 = 3.16, 3.46, 5.30, 5.34
        axinss1.set_xlim(x1, x2)  # apply the x-limits
        axinss1.set_ylim(y1, y2)  # apply the y-limits
        axinss1.set_yticks([])
        axinss1.set_xticks([])
        from mpl_toolkits.axes_grid1.inset_locator import mark_inset
        mark_inset(ax, axins, loc1=3, loc2=1, fc="none", ec=color, linestyle=':')
        mark_inset(ax, axins1, loc1=4, loc2=2, fc="none", ec=color, linestyle=':')
        mark_inset(ax, axinss1, loc1=3, loc2=1, fc="none", ec=color, linestyle=':')


    def _load_data(self):
        # import of data
        with open('spectrum_exp.pkl', 'rb') as f:
            self._data_exp = pickle.load(f)
        self._X_exp = self._data_exp['Current [A]'] * (10 ** 4)  # in mA
        self._Y_exp = self._data_exp['Frequency [Hz]'] * (10 ** -9)  # in GHz
        self._C_exp = self._data_exp['data'].T

        # if self.nstate not in self._cache:
        with open('two-tone-0.12-0.06_color_only_3.pkl', 'rb') as f:
            self._data_th = pickle.load(f)
            self._C_th = np.array(self._data_th)
        # else:
        #     self._C_th = self._cache[self.nstate]

        self._X_th = np.linspace(self._X_exp[0], self._X_exp[-1], self._C_th.shape[1])
        self._Y_th = np.linspace(self._Y_exp[0], self._Y_exp[-1], self._C_th.shape[0])


p = MainPicturePlot()
p.plot()