#!/usr/bin/python3

import collections
import matplotlib.pyplot as plt
import numpy as np
import re
import sys
from operator import itemgetter
from pylab import rcParams


def plotbars(counter, xlabel, ylabel='Ocorrências', label_rotation=0, h=False):
    o = counter.items()
    o = sorted(list(o), key=itemgetter(1))
    labels, values = zip(*o)
    indexes = np.arange(len(labels))
    width = 1
    if not h:
        plt.bar(indexes, values, width)
        plt.xticks(indexes + width * 0.5, labels)
    else:
        plt.barh(indexes, values, width)
        plt.yticks(indexes + width * 0.5, labels)
    locs, xlabels = plt.xticks()
    plt.setp(xlabels, rotation=label_rotation)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

FLAWFINDER_RE = r'(.*:[0-9]*):\s*\[([0-9]+)\]\s*\((\w+)\)\s*(\w+):'

if __name__ == "__main__":
    rcParams['figure.figsize'] = 9, 7
    f = sys.stdin.read()
    print(f)

    flaws_list = re.findall(FLAWFINDER_RE, f)

    count_by_type = collections.Counter()
    for f in flaws_list:
        count_by_type[f[2]] += 1

    count_by_type_danger = collections.Counter()
    for f in flaws_list:
        count_by_type_danger[f[2] + "/" + f[1]] += 1

    count_by_danger = collections.Counter()
    for f in flaws_list:
        count_by_danger[f[1]] += 1

    count_by_func = collections.Counter()
    for f in flaws_list:
        count_by_func[f[-1]+"/"+f[2]+"/"+f[1]] += 1

    plotbars(count_by_type, 'Tipo da falha')
    plotbars(count_by_type_danger, 'Tipo de falha/periculosidade')
    plotbars(count_by_danger, 'Periculosidade')
    plotbars(count_by_func, 'Ocorrências', 'Função', h=True)
