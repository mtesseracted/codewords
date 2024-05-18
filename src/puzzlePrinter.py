import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcols
# from matplotlib.patches import Rectangle
from puzzles import PuzzleGrid

class PuzzlePrinter():
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def grid2coordinates(self):
        grid = self.puzzle.make_grid()
        mask = grid != self.puzzle.blank
        x, y = np.where(mask)
        letters = grid[mask]
        return x, y, letters


    def create_puzzle_fig(self, fig, fill_all=False):

        grid_ax = fig.add_subplot(20, 1, (1, 16))
        self.print_puzzle_grid(grid_ax, fig, fill_all=fill_all)

        lett_ax = fig.add_subplot(20, 1, 17)
        self.print_all_letters(lett_ax, fig, fill_all=fill_all)

        code_ax = fig.add_subplot(20, 1, (18, 20))
        self.print_code_boxes(code_ax, fig, fill_all=fill_all)

        fig.tight_layout(pad=0)
        return fig

    def print_puzzle_grid(self, ax, fig, fill_all=False, bg_col='w'):
        ax.axis('off')
        bg_rgb = np.array(mcols.to_rgb(bg_col)) * 255
        bg_shape = np.array([8, 8]) * fig.dpi
        bg_shape = [*bg_shape.astype(int), 3]
        bg_img = np.zeros(bg_shape, dtype=np.uint8)
        # bg_col = np.array([100, 200, 100])  # lime green
        bg_img[:, :, :] = bg_rgb[None, None, :]
        ax.imshow(bg_img)

        grid = self.puzzle.make_grid()
        mask = grid != self.puzzle.blank
        x, y = np.where(mask)
        letters = grid[mask]

        grid_max = max(x.max(), y.max(), 16)
        box_size = round(bg_shape[0] / (grid_max + 3))

        for xc, yc, ll in zip(x, y, letters):
            ximg = box_size * (xc + 1)
            yimg = box_size * (yc + 1)
            ilett = ord(ll.lower()) - ord('a')
            p = plt.Rectangle((ximg, yimg), box_size, box_size, fill=False, lw=1.2)
            p.set_transform(ax.transData)
            ax.add_patch(p)

            coded = self.puzzle.code[ilett]
            ax.text(ximg + 1, yimg + 3, f'{coded + 1}', fontsize=8,
                    horizontalalignment='left', verticalalignment='top', transform=ax.transData)

            if ilett in self.puzzle.knowns or fill_all:
                ax.text(ximg + 0.5 * box_size, yimg + 0.6 * box_size, f'{ll.upper()}', fontsize=12,
                        horizontalalignment='center', verticalalignment='center', transform=ax.transData)

        return ax


    def print_all_letters(self, ax, fig, fill_all=False):
        # print all letter for the puzzle solver to cross out found letters
        ax.axis('off')
        bg_rgb = np.array(mcols.to_rgb('w')) * 255
        bg_shape = np.array([10 * 1 / 20, 8]) * fig.dpi
        bg_shape = [*bg_shape.astype(int), 3]
        bg_img = np.zeros(bg_shape, dtype=np.uint8)
        # bg_col = np.array([220, 100, 120])  # light red
        bg_img[:, :, :] = bg_rgb[None, None, :]
        ax.imshow(bg_img)
        spacer = round(bg_shape[1] / 27.5)
        for ii in range(26):
            ximg = spacer * (ii + 1)
            yimg = round(0.5 * bg_shape[0])
            ax.text(ximg, yimg, f'{chr(ii + ord("A"))}', fontsize=8,
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax.transData)
            if ii in self.puzzle.knowns:
                ax.text(ximg + 1, yimg, '/', fontsize=12, fontweight='bold',
                        horizontalalignment='center',
                        verticalalignment='center', transform=ax.transData)
                # ax.text(ximg, yimg, '\\', fontsize=10, horizontalalignment='center',
                #         verticalalignment='center', transform=ax.transData)
                # ax.text(ximg, yimg, '-', fontsize=10, horizontalalignment='center',
                #         verticalalignment='center', transform=ax.transData)

        return ax


    def print_code_boxes(self, ax, fig, fill_all=False):
        # @TODO: make order of boxes in code order, not lexigraphical
        # print out empty numbered boxes for the puzzle solver to fill in
        ax.axis('off')
        bg_rgb = np.array(mcols.to_rgb('w')) * 255
        bg_shape = np.array([10 * 3 / 20, 8]) * fig.dpi
        bg_shape = [*bg_shape.astype(int), 3]
        bg_img = np.zeros(bg_shape, dtype=np.uint8)
        # bg_col = np.array([240, 80, 220])  # pink
        bg_img[:, :, :] = bg_rgb[None, None, :]
        ax.imshow(bg_img)

        wspacer = round(bg_shape[1] / 15)
        hspacer = round(bg_shape[0] / 3)
        for jj in range(2):
            for ii in range(13):
                ximg = wspacer * (ii + 1)
                yimg = hspacer * (jj + 0.5)
                coded = ii + jj * 13
                ilett = self.puzzle.code_inv[coded]
                p = plt.Rectangle((ximg, yimg), wspacer, hspacer, fill=False, lw=1.2)
                ax.text(ximg + 1, yimg + 3, f'{coded + 1}', fontsize=8,
                        horizontalalignment='left', verticalalignment='top', transform=ax.transData)
                p.set_transform(ax.transData)
                ax.add_patch(p)

                if ilett in self.puzzle.knowns or fill_all:
                    ax.text(ximg + 0.5 * wspacer, yimg + 0.6 * hspacer, f'{chr(ilett+ord("A"))}',
                            fontsize=16, horizontalalignment='center',
                            verticalalignment='center', transform=ax.transData)

        return ax

