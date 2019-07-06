#!/usr/bin/env python3

# Cumulative distribution function (CDF) plotter. Extracted from the post below,
# all credits goes to daeumerj:
# https://gist.github.com/daeumerj/d67b44c2c87d34b15ad0082ba16b17b1
#
# What to look for at the plot?
# -----------------------------
# If the CDF plot is highly straight, the file might be compressed and/or encrypted.
# If it is not, most probably it is neither compressed nor encrypted. See the
# gist above for detailed examples; or analyze /dev/urandom or a compressed file
# yourself to get an understanding.

import seaborn as sns
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [15, 5]
sns.set()


def plot_relative_frequency_distribution(data, filename):
    # unvariate
    ax = sns.distplot(np.array(list(data)),
                      bins=256,
                      kde=False,
                      hist_kws={'alpha': 0.8},
                      norm_hist=True,
                      color='blue')
    ax.set(xlabel='Byte Value (base 10)',
           ylabel='Relative Frequency',
           title='Relative Frequency Histogram of Byte Values')
    # control x axis range
    ax.set_xlim(-10, 260)
    #ax.set_ylim(0, 0.10)
    ax.set_title(filename)


def plot_cdf(data, filename):
    ax = sns.distplot(np.array(list(data)),
                      bins=256,
                      kde=False,
                      hist_kws={'histtype': 'step', 'cumulative': True,
                                'linewidth': 1, 'alpha': 1},
                      kde_kws={'cumulative': True},
                      norm_hist=True,
                      color='red')

    ax.set(xlabel='Byte Value (base 10)',
           ylabel='Probability',
           title='CDF of Byte Values')
    # control x axis range
    ax.set_xlim(-10, 260)
    #ax.set_ylim(0, 0.10)


def create_plots(file, fsize):
    if fsize > 0:
        with open(file, 'rb') as f:
            data = f.read(fsize)
    else:
        with open(file, 'rb') as f:
            data = f.read()

    # control layout
    grid = plt.GridSpec(1, 3, wspace=0.3, hspace=0.1)

    # first plot
    plt.subplot(grid[0, :2])
    plot_relative_frequency_distribution(data, f.name)

    # second plot
    plt.subplot(grid[0, 2:])
    plot_cdf(data, f.name)

    plt.show()


def main(argv):
    fsize = 0
    if len(sys.argv) == 3:
        fsize = int(sys.argv[2])

    create_plots(argv[1], fsize)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(
            'Usage: %s <FILE> [SIZE]\nExamples:\n\t%s fw.bin\n\t%s /dev/urandom 50000' %
            (sys.argv[0], sys.argv[0], sys.argv[0]))

    if not os.path.exists(sys.argv[1]):
        sys.exit('ERROR: %s was not found!' % sys.argv[1])

    main(sys.argv)
