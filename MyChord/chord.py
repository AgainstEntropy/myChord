from typing import Union

import numpy as np
from numpy import ndarray
import matplotlib.pyplot  as plt
import matplotlib.patches as mpatches
from matplotlib.collections import LineCollection, PathCollection
from matplotlib.colors import Colormap, LinearSegmentedColormap

CmapLike = Union[LinearSegmentedColormap, Colormap]

class Chord:
    def __init__(self, r: float = 1, linewidth: float = 2, 
                 use_outer_circle: bool = True, divisions: int = 100):
        self.r = r
        self.lw = linewidth
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        if use_outer_circle:
            self.draw_circle()
        self._prepare_t(divisions)

        self.ax.set_axis_off()
        lim = np.array((-1.1, 1.1)) * r
        self.ax.set_xlim(*lim)
        self.ax.set_ylim(*lim)

    def _prepare_t(self, divisions: int):
        self.divsions = divisions
        t = np.linspace(0, 1, divisions)
        self.T2 = np.stack((1-t, t), axis=1) ** 2

    def get_cmap(self, colors: list[Union[str, tuple[float]]]):
        return LinearSegmentedColormap.from_list('my_cmap', colors, N=self.divsions)

    def add_curve(self, start_end: Union[tuple[float], ndarray[float]], 
                  cmap: CmapLike):
        # polar to cartesian
        x = np.cos((start_end))
        y = np.sin((start_end))
        xy = self.r * np.stack((x, y), axis=1)

        # compute the quadratic Bezier curve
        XY = self.T2 @ xy  # (T, 2) @ (2, 2) -> (T, 2)

        # split the curve into segments
        segments = np.stack([XY[:-1], XY[1:]], axis=1)
        idxs = np.array(range(XY.shape[0]))  # (0, 1, 2, ..., T-1)
        norm = plt.Normalize(idxs[0], idxs[-1])
        
        lc = LineCollection(segments, linewidths=self.lw, cmap=cmap, norm=norm, antialiaseds=True)
        lc.set_array(idxs)
        self.ax.add_collection(lc)

        # draw two ends
        self.ax.scatter(*xy.T, s=15, c=cmap([0, 1.]))
    
    def draw_circle(self):
        # draw the outer circle
        circle = mpatches.Circle((0, 0), self.r, color='black', fill=False)
        self.ax.add_artist(circle)

    def remove_curves(self):
        for c in self.ax.collections:
            if type(c) in [LineCollection, PathCollection]:
                c.remove()

    def show(self):
        self.fig.show()
        plt.show()
    
    def get_fig(self):
        return self.fig


if __name__ == '__main__':
    graph = Chord()
    graph.remove_curves()

    cmap1 = graph.get_cmap(['red', 'blue'])
    graph.add_curve(start_end=np.array((0, 30)) / 180 * np.pi, cmap=cmap1)

    cmap2 = graph.get_cmap(['green', 'gold'])
    graph.add_curve(start_end=np.array((-45, 210)) / 180 * np.pi, cmap=cmap2)

    graph.show()