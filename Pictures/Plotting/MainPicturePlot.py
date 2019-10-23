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

        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5), sharey=True)
        plt.subplots_adjust(wspace=.1)

        ax1, ax2 = axes

        self.plot_experiment(ax1)
        self.plot_theory(ax2)

        plt.savefig("../main_picture.pdf", bbox_inches="tight", dpi=600)

        with open(self._cache_file, "wb") as f:
            pickle.dump(self._cache, f)


    def plot_experiment(self, ax):
        data = self._X_exp, self._Y_exp, np.real(self._C_exp)
        img1 = ax.pcolormesh(*data, rasterized=True, vmin=-0.005, vmax=0.022)
        cbaxes1 = clb.make_axes(ax, location="top", shrink=0.8, aspect=50, pad=0.075, anchor=(0,0))[0]
        cb = plt.colorbar(img1, ax=ax, cax=cbaxes1, orientation="horizontal")
        ax.set_xlabel('Current [$10^{-4}$ A]');
        ax.set_ylabel('Frequency [GHz]');
        cb.ax.set_title(r"$\mathfrak{Re} [S^{exp}_{21}]$", position=(1.125,-1.5))
        loc = ticker.MultipleLocator(base=0.01)  # this locator puts ticks at regular intervals
        cb.locator = loc
        cb.update_ticks()
        plt.text(-0.15, 1.1, "(a)", fontdict={"name": "STIX"}, fontsize=22,
                 transform=ax.transAxes)

        self._zoom(ax, data, vmin=-0.005, vmax = 0.022)

    def plot_theory(self, ax):

        # try:
        #     C = self._cache[self.nstate]
        # except KeyError:
        #     C = np.zeros(self._C_th.shape)
        #     for i in range(C.shape[0]):
        #         for j in range(C.shape[1]):
        #             C[i,j] = self._C_th[i][j][self.nstate][0][self.nstate].real
        #     self._cache[self.nstate] = C

        C = np.real(self._C_th.T)
        C = (C-np.min(C)-np.ptp(C)/2)/np.ptp(C)*0.027+(0.027/2-0.005)# + np.random.normal(scale=0.001,
                                                           #                    size=C.shape)
        C = C
        data = self._X_th, self._Y_th, C
        img1 = ax.pcolormesh(*data, rasterized=True, vmax = 1.025*np.max(C))
        cbaxes1 = clb.make_axes(ax, location="top", shrink=0.8, aspect=50, pad=0.075, anchor=(1,0))[0]
        cb = plt.colorbar(img1, ax=ax, cax=cbaxes1, orientation="horizontal")
        ax.set_xlabel('Current [$10^{-4}$ A]');
        # ax.set_ylabel('Frequency [GHz]');
        cb.ax.set_title(r"$\mathfrak{Re} [S^{sim}_{21}]$", position=(-0.125,-1.5))
        loc = ticker.MultipleLocator(base=0.01)  # this locator puts ticks at regular intervals
        cb.locator = loc
        cb.update_ticks()
        plt.text(-0.075, 1.1, "(b)", fontdict={"name": "STIX"}, fontsize=22,
                 transform=ax.transAxes)

        self._zoom(ax, data, vmin=np.min(C), vmax = np.max(C))


    def _zoom(self, ax, data, vmin, vmax):

        color = "black"
        axins = zoomed_inset_axes(ax, 2.5, loc=4)  # zoom-factor: 2.5, location: upper-left
        axins1 = zoomed_inset_axes(ax, 2.5, loc=3)
        axinss1 = zoomed_inset_axes(ax, 2.5, loc=2)
        # ax1.broken_barh([(3.1,0.4)],(5.31,0.02),edgecolors = 'r', facecolors = 'none',linewidth= 1, linestyle = '--')
        for axis in ['top', 'bottom', 'left', 'right']:
            axins.spines[axis].set_color(color)
        axins.pcolormesh(*data, rasterized=True, vmax = vmax, vmin=vmin)
        for axis in ['top', 'bottom', 'left', 'right']:
            axins1.spines[axis].set_color(color)
        axins1.pcolormesh(*data, rasterized=True, vmax = vmax, vmin=vmin)
        for axis in ['top', 'bottom', 'left', 'right']:
            axinss1.spines[axis].set_color(color)
        axinss1.pcolormesh(*data, rasterized=True, vmax = vmax, vmin=vmin)
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
        with open('two-tone-0.1-0.05_color_only.pkl', 'rb') as f:
            self._data_th = pickle.load(f)
            self._C_th = np.array(self._data_th)
        # else:
        #     self._C_th = self._cache[self.nstate]

        self._X_th = np.linspace(self._X_exp[0], self._X_exp[-1], self._C_th.shape[1])
        self._Y_th = np.linspace(self._Y_exp[0], self._Y_exp[-1], self._C_th.shape[0])


p = MainPicturePlot()
p.plot()