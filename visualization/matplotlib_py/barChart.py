from create_customize import ages_x, dev_y, py_dev_y, js_dev_y

import numpy as np
from matplotlib import pyplot as plt

x_indexes = np.arange(len(ages_x))


def show_BarChart_from_previous():
    plt.bar(ages_x, dev_y, color='#444444', label='All Devs')
    plt.bar(ages_x, py_dev_y, color='#008fd5', label='Python')
    plt.bar(ages_x, js_dev_y, color='#e5ae38', label='JavaScript')

def show_BarChart_with_numpy():
    pltTicks = True # my own stuff
    width = 0.25
    plt.bar(x_indexes - width, dev_y,
            width=width, color='#444444', label='All Devs')
    plt.bar(x_indexes, py_dev_y,
            width=width, color='#008fd5', label='Python')
    plt.bar(x_indexes + width, js_dev_y,
            width=width, color='#e5ae38', label='JavaScript')

def main():
    plt.xlabel('Ages')
    plt.ylabel('Median Salary (USD)')
    plt.title('Median Salary (USD) by Age')

    # plt.savefig('plot.png')
    if pltTicks:
        plt.xticks(ticks=x_indexes, labels=ages_x)

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    plt.show()


if __name__ == '__main__':
    pltTicks = False
    # show_BarChart_from_previous()
    show_BarChart_with_numpy()
    main()
