import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def plotFilter(filter, filter_size):

    height, width = filter_size, filter_size
    spines = 'left', 'right', 'top', 'bottom'

    labels = ['label' + spine for spine in spines]

    tick_params = {spine : False for spine in spines}
    tick_params.update({label : False for label in labels})

    desired_width = 8 #in inches
    scale = desired_width / float(width)

    fig, ax = plt.subplots(1, 1, figsize=(desired_width, height*scale))
    img = ax.imshow(filter, cmap=cm.Greys_r, interpolation='none')

    #remove spines
    for spine in spines:
        ax.spines[spine].set_visible(False)

    #hide ticks and labels
    ax.tick_params(**tick_params)

    #preview
    plt.show()


def getNormConvFilters(param_vals):
    filter_1 = param_vals[0]
    num_filters = filter_1.shape[0]
    for i in range(num_filters):
        sub_filter = filter_1[i, 0, :, :]
        filter_norm = (sub_filter - np.min(sub_filter)) \
                      / (np.max(sub_filter) - np.min(sub_filter))
        yield filter_norm
