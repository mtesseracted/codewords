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

    def create_solution_fig(self, fig, labels=None):
        rowsizes = [1,] + [2,]*8 + [1,]
        nrows = 10 #sum(rowsizes)
        ncols = 10
        if not isinstance(self.puzzle, list):
            raise ValueError("Cannot create solution without a list of puzzles")

        if labels is not None and len(labels) != len(self.puzzle):
            raise ValueError("Lenght of labels is not the same as num puzzles")

        puzz_list = self.puzzle
        for ip, puzz in enumerate(puzz_list):
            self.puzzle = puzz
            ilo = (ip+1) * ncols + 1
            ihi = ilo + ncols - 1

            ax = fig.add_subplot(nrows, 10, ilo)
            ax.axis('off')
            bg_rgb = np.array(mcols.to_rgb('w')) * 255
            bg_shape = np.array([10 * 2 / 20, 8]) * fig.dpi
            bg_shape = [*bg_shape.astype(int), 3]
            bg_img = np.zeros(bg_shape, dtype=np.uint8)
            bg_img[:, :, :] = bg_rgb[None, None, :]
            ax.imshow(bg_img)

            spacer = round(bg_shape[1] / 27.5)
            ii = 24
            ximg = spacer * (ii + 1)
            yimg = round(0.5 * bg_shape[0])

            title = ip+1 if labels is None else labels[ip]
            ax.text(ximg, yimg, str(title), fontsize=20,
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax.transData)

            code_ax = fig.add_subplot(nrows, 10, (ilo+1, ihi))
            self.print_code_boxes(code_ax, fig, fill_all=True)

        self.puzzle = puzz_list
        return fig
    #end def create_solution_fig()

    def create_puzzle_fig(self, fig, fill_all=False, title=None, pad=0.6):
        """ create a puzzle figure with title, grid, letter line, then code boxes
        :param fig: pyplot figure, assumed to be 8.5x11"
        :param fill_all: (bool) whether to fill in the solution
        :param title: (str) 
        :param pad: border padding in inches, if 2-tuple it's (w_pad, h_pad)
        """

        fig_size = fig.get_size_inches()

        if hasattr(pad, '__len__'):
            wpad = pad[0] / fig_size[0]
            hpad = pad[1] / fig_size[1]
        else:
            wpad = pad / fig_size[0]
            hpad = pad / fig_size[1]

        grid_size = fig_size[0] - 2*pad
        leftover = fig_size[1] - 2*pad - grid_size
        letters_size = leftover / 4
        title_size = leftover / 4
        code_boxes_size = 2 * leftover / 4

        ax_widths = [wpad, 1 - 2*wpad, wpad]
        ax_heights = [hpad, title_size/fig_size[1],
                      grid_size/fig_size[1], letters_size/fig_size[1], 
                      code_boxes_size/fig_size[1], hpad,]

        fig_spec = fig.add_gridspec(ncols=len(ax_widths), nrows=len(ax_heights),
                                    width_ratios=ax_widths, height_ratios=ax_heights)


        title_ax = fig.add_subplot(fig_spec[1, 1])
        self.print_puzzle_title(title_ax, fig, title=title)

        grid_ax = fig.add_subplot(fig_spec[2, 1])
        self.print_puzzle_grid(grid_ax, fig, fill_all=fill_all)

        lett_ax = fig.add_subplot(fig_spec[3, 1])
        self.print_all_letters(lett_ax, fig, fill_all=fill_all)

        code_ax = fig.add_subplot(fig_spec[4, 1])
        self.print_code_boxes(code_ax, fig, fill_all=fill_all)

        return fig

    def print_puzzle_title(self, ax, fig, title=None):
        """ print the puzzle number at the top """
        ax.axis('off')
        bg_rgb = np.array(mcols.to_rgb('w')) * 255
        # bg_rgb = np.array([100, 100, 100])  # gray
        bg_shape = np.array([10 * 2 / 20, 8]) * fig.dpi
        bg_shape = [*bg_shape.astype(int), 3]
        bg_img = np.zeros(bg_shape, dtype=np.uint8)
        bg_img[:, :, :] = bg_rgb[None, None, :]
        ax.imshow(bg_img)

        if title is not None:
            spacer = round(bg_shape[1] / 27.5)
            ii = int(26 / 2)
            ximg = spacer * (ii + 1)
            yimg = round(0.5 * bg_shape[0])
            ax.text(ximg, yimg, str(title), fontsize=20,
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax.transData)

        return ax

    def print_puzzle_grid(self, ax, fig, fill_all=False, bg_col='w'):
        ax.axis('off')
        bg_rgb = np.array(mcols.to_rgb(bg_col)) * 255
        # bg_rgb = np.array([100, 200, 100])  # lime green
        bg_shape = np.array([8, 8]) * fig.dpi
        bg_shape = [*bg_shape.astype(int), 3]
        bg_img = np.zeros(bg_shape, dtype=np.uint8)
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
        # bg_rgb = np.array([220, 100, 120])  # light red
        bg_shape = np.array([10 * 1 / 20, 8]) * fig.dpi
        bg_shape = [*bg_shape.astype(int), 3]
        bg_img = np.zeros(bg_shape, dtype=np.uint8)
        bg_img[:, :, :] = bg_rgb[None, None, :]
        ax.imshow(bg_img)
        # spacer = round(bg_shape[1] / 27.5)
        spacer = round(bg_shape[1] / 32)
        for ii in range(26):
            ximg = spacer * (ii + 3.25)
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
        # bg_rgb = np.array([240, 80, 220])  # pink
        bg_shape = np.array([10 * 3 / 20, 8]) * fig.dpi
        bg_shape = [*bg_shape.astype(int), 3]
        bg_img = np.zeros(bg_shape, dtype=np.uint8)
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

       



