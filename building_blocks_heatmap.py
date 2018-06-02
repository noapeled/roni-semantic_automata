import matplotlib
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


def differences(global_min, global_max):
    def encoding_length_all():
        return 5

    def encoding_length_exactly(n1, n2):
        return 12 + n1 + n2

    return {(n1, n2): (encoding_length_exactly(n1, n2) - encoding_length_all())
            for n1 in range(global_min, global_max + 1)
            for n2 in range(n1, global_max + 1)}


def plot_heatmap(global_min, global_max, title, image_file_name, max_n, matrix_as_dict):
    base_fontsize = 15
    font = {'weight': 'bold', 'size': base_fontsize}
    matplotlib.rc('font', **font)
    mask = np.zeros((max_n + 1, max_n + 1))
    mask[:, 0] = True
    mask[0, :] = True
    matrix_as_array = np.zeros((max_n + 1, max_n + 1))
    for k, v in matrix_as_dict.items():
        matrix_as_array[k[1], k[0]] = v
        if k[0] != k[1]:
            mask[k[0], k[1]] = True
    with sns.axes_style("white"):
        fig, ax = plt.subplots(figsize=(20, 20))
        cbar_ax = fig.add_axes([0.94, 0.1, 0.01, 0.79])
        ax = sns.heatmap(matrix_as_array,
                         # vmin=global_min, vmax=global_max,
                         ax=ax,
                         mask=mask, square=True,
                         cmap='bwr',
                         cbar_ax=cbar_ax, cbar=True,
                         annot=True, fmt='.0f')
        ax.invert_yaxis()
        ax.set_xlim(xmin=1)
        ax.set_ylim(ymin=1)
        ax.set_title(title, fontsize=base_fontsize * 2.5)
        ax.set_xlabel('$n_2$', fontsize=base_fontsize * 2.5)
        ax.set_ylabel('$n_1$', fontsize=base_fontsize * 2.5)
        plt.savefig(image_file_name)


if __name__ == '__main__':
    minimum_n, maximum_n = 1, 20
    plot_heatmap(minimum_n, maximum_n,
                 "$\\left|T^{EX}\\left(n_1, n_2 \\right)\\right| - \\left|T^{ALL}\\right|$",
                 "bb_len_diff.png", maximum_n,
                 differences(minimum_n, maximum_n))
