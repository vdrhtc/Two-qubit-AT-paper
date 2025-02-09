import pickle
import numpy as np
import matplotlib
from matplotlib import ticker, colorbar as clb, patches

matplotlib.use('Qt5Agg')

from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes


class MainPictureSlices:

    def __init__(self):
        self._cmap = "Spectral"
        self.nstate = 0


    def plot(self):
        self._load_data()
        indices = [98, 124, 158]
        indices_th  = (np.array(indices)/len(self._C_exp[0,:])*len(self._C_th[0,:])).astype(int)
        print(indices, indices_th)
        titles = ["Feature I", "Feature III", "Sweet spot"]
        fig, axes = plt.subplots(1, 3, figsize=(5*0.9,3*0.9), sharey=True)

        for counter, ax, index in zip(range(3), axes, indices):
            C_exp = np.abs(self._C_exp - self._C_exp[3, 0])
        # plt.pcolormesh(*data, rasterized=True, vmin=-0.005, vmax=0.022, cmap=self._cmap)
        #     ax.pcolormesh(*data, rasterized=True, vmin=-0.005, vmax=0.022, cmap=self._cmap)

            # ax.plot([self._X_exp[index]]*2, [self._Y_exp[0], self._Y_exp[-1]], 'black', lw=0.1)
            ax.plot(np.real(C_exp[:,index]), self._Y_exp, zorder=1, color="gray",
                    label="Exp.")
            th_slice = np.real(self._C_th[:,indices_th[counter]])*1.3
            ax.plot(th_slice, np.linspace(self._Y_exp[0], self._Y_exp[-1], len(th_slice)), zorder=3,
                    color="black", lw=.5, label ="Sim.")

            rect = patches.Rectangle((np.min((C_exp[:,index]))-.001, 5.3575),
                                     np.ptp((C_exp[:,index]))+0.002, .02, linewidth=1, edgecolor='none',
                                     facecolor='white', zorder=2, alpha=0.66)
            ax.add_patch(rect)
            # ax.set_title("I=%.2f mA"%(self._X_exp[index]/10), fontsize=9)
            ax.set_title(titles[counter], fontsize=10)

            print(self._X_exp[index])

            if counter==2:
                ax.annotate('', xy=(.0035, 5.4525), xytext=(.0035, 5.4075), ha="center", va="top",
                            fontsize=10,
                            arrowprops=dict(facecolor='#1f77b4', edgecolor="#1f77b4",
                                            arrowstyle="<|-|>, head_length=.3, head_width=.1"))

                ax.annotate('$\Omega_2$', xy=(.003, 5.425), color = "#1f77b4", ha="right")

                ax.annotate('', xy=(.0035, 5.27), xytext=(.0035, 5.215), ha="center", va="top",
                            fontsize=10,
                            arrowprops=dict(facecolor='#ff7e67', edgecolor="#ff7e67",
                                            arrowstyle="<|-|>, head_length=.3, head_width=.1"))

                ax.annotate('$\Omega_1$', xy=(.003, 5.235), color = "#ff7e67", ha="right")

                ax.annotate('01', xy=(.011, 5.43), color="#1f77b4", fontsize=9, ha="right")
                ax.annotate('10', xy=(.011, 5.23), color="#ff7e67", fontsize=9, ha="right")
                ax.annotate('02/2', xy=(.01, 5.31), color="#1f77b4", fontsize=9)
                ax.annotate('20/2', xy=(.0075, 5.13), color="#ff7e67", fontsize=9)
                ax.annotate('11/2', xy=(.003, 5.345), fontsize=9)
                ax.annotate('12/3', xy=(.011, 5.275), fontsize=9, ha="right")
                # ax.set_xlim(-0.002, np.max(np.real(self._C_exp[:,index])))


            elif counter==1:

                ax.annotate('01', xy=(.01, 5.39), color="#1f77b4", fontsize=9)

                ax.annotate('10', xy=(.016, 5.275), color="#ff7e67", fontsize=9)
                ax.annotate('02/2', xy=(.016, 5.245), color="#1f77b4", fontsize=9)
                ax.annotate('12/3', xy=(.016, 5.215), color="black", fontsize=9)

                ax.annotate('20/2', xy=(.0075, 5.155), color="#ff7e67", fontsize=9)
                ax.annotate('11/2', xy=(.005, 5.34), fontsize=9)
                ax.set_xlim(-0.002, np.max(np.real(self._C_exp[:,index])))

            elif counter==0:

                ax.annotate('01', xy=(.022, 5.35-0.005), color="#1f77b4", fontsize=9, ha="right")
                ax.annotate('10', xy=(0.022, 5.32-0.005), color="#ff7e67", fontsize=9, ha="right")
                ax.annotate('11/2', xy=(.022, 5.29-0.005), fontsize=9, ha="right")

                ax.annotate('02/2', xy=(.015, 5.16), color="#1f77b4", fontsize=9)
                ax.annotate('20/2', xy=(.015, 5.13), color="#ff7e67", fontsize=9)
                ax.annotate('12/3', xy=(.007, 5.255), color="black", fontsize=9)
                ax.annotate('21/3', xy=(.007, 5.225), color="black", fontsize=9)
                # ax.set_xlim(-0.005, np.max(np.real(self._C_exp[:,index])))
                ax.legend(fontsize=9, loc="upper right")




        axes[0].set_ylabel("$\omega_d}/2\pi$ (GHz)")
        axes[1].set_xlabel(r"$|\Delta S^{exp}_{21}|, 1.3 \, |\Delta S^{exp}_{21}|$")


        plt.text(-0.53, 1.1, "(c)", fontdict={"name": "STIX"}, fontsize=17,
                 transform=axes[0].transAxes)

        plt.savefig("../main_picture_slices.pdf", bbox_inches="tight", dpi=600)



    def _load_data(self):
        # import of data
        with open('spectrum_exp.pkl', 'rb') as f:
            self._data_exp = pickle.load(f)
        self._X_exp = self._data_exp['Current [A]'] * (10 ** 4)  # in mA
        self._Y_exp = self._data_exp['Frequency [Hz]'] * (10 ** -9)  # in GHz
        self._C_exp = self._data_exp['data'].T


        # with open('two-tone-0.1-0.05_color_only.pkl', 'rb') as f:
        with open('two-tone-0.12-0.06_color_only_3.pkl', 'rb') as f:
            self._data_th = pickle.load(f)
            C = np.array(self._data_th).T
            self._C_th = C #(C-np.min(C)-np.ptp(C)/2)/np.ptp(C)*0.02+(0.02/2+0.002)

p = MainPictureSlices()
p.plot()