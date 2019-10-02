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
        data = self._X_exp, self._Y_exp, self._C_exp.real
        img1 = ax.pcolormesh(*data, rasterized=True)
        cbaxes1 = clb.make_axes(ax, location="top", shrink=0.8, aspect=50, pad=0.075, anchor=(0,0))[0]
        cb1 = plt.colorbar(img1, ax=ax, cax=cbaxes1, orientation="horizontal")
        ax.set_xlabel('Current [$10^{-4}$ A]');
        ax.set_ylabel('Frequency [GHz]');
        cb1.ax.set_title(r"$\mathfrak{Re} [S_{21}]$", position=(1.1,-1.5))

        plt.text(-0.2, 1.05, "(a)", fontdict={"name": "STIX"}, fontsize=22,
                 transform=ax.transAxes)

        self._zoom(ax, data)

    def plot_theory(self, ax):

        try:
            C = self._cache[self.nstate]
        except KeyError:
            C = np.zeros(self._C_th.shape)
            for i in range(C.shape[0]):
                for j in range(C.shape[1]):
                    C[i,j] = self._C_th[i][j][self.nstate][0][self.nstate].real
            self._cache[self.nstate] = C

        data = self._X_th, self._Y_th, C
        img1 = ax.pcolormesh(*data, rasterized=True)
        cbaxes1 = clb.make_axes(ax, location="top", shrink=0.8, aspect=50, pad=0.075, anchor=(1,0))[0]
        cb1 = plt.colorbar(img1, ax=ax, cax=cbaxes1, orientation="horizontal")
        ax.set_xlabel('Current [$10^{-4}$ A]');
        # ax.set_ylabel('Frequency [GHz]');
        cb1.ax.set_title(r"$P(\left|00\right\rangle)$", position=(-0.1,-1.5))
        plt.text(-0.1, 1.05, "(b)", fontdict={"name": "STIX"}, fontsize=22,
                 transform=ax.transAxes)

        self._zoom(ax, data)


    def _zoom(self, ax, data):
        axins = zoomed_inset_axes(ax, 2.5, loc=4)  # zoom-factor: 2.5, location: upper-left
        axins1 = zoomed_inset_axes(ax, 2.5, loc=3)
        axinss1 = zoomed_inset_axes(ax, 2.5, loc=2)
        # ax1.broken_barh([(3.1,0.4)],(5.31,0.02),edgecolors = 'r', facecolors = 'none',linewidth= 1, linestyle = '--')
        for axis in ['top', 'bottom', 'left', 'right']:
            axins.spines[axis].set_color('C1')
        axins.pcolormesh(*data, rasterized=True)
        for axis in ['top', 'bottom', 'left', 'right']:
            axins1.spines[axis].set_color('C1')
        axins1.pcolormesh(*data, rasterized=True)
        for axis in ['top', 'bottom', 'left', 'right']:
            axinss1.spines[axis].set_color('C1')
        axinss1.pcolormesh(*data, rasterized=True)
        x1, x2, y1, y2 = 3.5, 3.8, 5.25, 5.29  # specify the limits
        axins.set_xlim(x1, x2)  # apply the x-limits
        axins.set_ylim(y1, y2)  # apply the y-limits
        axins.set_yticklabels([])
        axins.set_xticklabels([])
        x1, x2, y1, y2 = 2.925, 3.225, 5.225, 5.265
        axins1.set_xlim(x1, x2)  # apply the x-limits
        axins1.set_ylim(y1, y2)  # apply the y-limits
        axins1.set_yticklabels([])
        axins1.set_xticklabels([])
        x1, x2, y1, y2 = 3.16, 3.46, 5.30, 5.34
        axinss1.set_xlim(x1, x2)  # apply the x-limits
        axinss1.set_ylim(y1, y2)  # apply the y-limits
        axinss1.set_yticklabels([])
        axinss1.set_xticklabels([])
        from mpl_toolkits.axes_grid1.inset_locator import mark_inset
        mark_inset(ax, axins, loc1=3, loc2=1, fc="none", ec='C1', linestyle='--')
        mark_inset(ax, axins1, loc1=4, loc2=2, fc="none", ec='C1', linestyle='--')
        mark_inset(ax, axinss1, loc1=3, loc2=1, fc="none", ec='C1', linestyle='--')


    def _load_data(self):
        # import of data
        with open('spectrum_exp.pkl', 'rb') as f:
            self._data_exp = pickle.load(f)
        self._X_exp = self._data_exp['Current [A]'] * (10 ** 4)  # in mA
        self._Y_exp = self._data_exp['Frequency [Hz]'] * (10 ** -9)  # in GHz
        self._C_exp = self._data_exp['data'].T

        if self.nstate not in self._cache:
            with open('two-tone-0.1-0.05.pkl', 'rb') as f:
                self._data_th = pickle.load(f)
            self._C_th = np.array(self._data_th).T
        else:
            self._C_th = self._cache[self.nstate]

        self._X_th = np.linspace(self._X_exp[0], self._X_exp[-1], self._C_th.shape[1])
        self._Y_th = np.linspace(self._Y_exp[0], self._Y_exp[-1], self._C_th.shape[0])


p = MainPicturePlot()
p.plot()