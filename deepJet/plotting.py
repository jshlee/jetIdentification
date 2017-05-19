from __future__ import absolute_import 
from __future__ import division
from __future__ import print_function

import numpy as np
#from scipy.interpolate import splrep, splev
from statsmodels.nonparametric.smoothers_lowess import lowess
import matplotlib.pyplot as plt
# import seaborn as sns

def tb_scalar_paser(path):
    raw = ''.join(open(path).readline())[1:-2]
    raw = raw.split('],')
    data = []
    for i in xrange(len(raw)):
        data.append( raw[i].split(',')[1:] )
    return np.array( data )

def load_train_log(acc_path, loss_path):
    acc = tb_scalar_paser(acc_path)
    loss = tb_scalar_paser(loss_path)
    
    if False in ( acc[:, 0] == loss[:, 0]):
        print('Something wrong! Xp')
        pass
    
    log = {'step': acc[:, 0],
           'accuracy': acc[:, 1],
           'loss': loss[:, 1]}
    return log

def load_test_log(path):
    log = np.loadtxt(fname=path, delimiter=',', dtype=np.float64)
    return {'step': log[:, 0],
            'loss': log[:, 1],
            'accuracy': log[:, 2]}

def plot_maker(train_log, test_log, y, title, path, smooth=True, show=False):
    fig, ax = plt.subplots()
    # train
    if smooth:
        filtered = lowess(train_log[y], train_log['step'], is_sorted=True, frac=0.075, it=0)
        plt.plot(train_log['step'], train_log[y], color='lightblue', label='train')
        plt.plot(filtered[:,0], filtered[:, 1], color='navy', label='train-smooth')
    else:
        plt.plot(train_log['step'], train_log[y], color='navy', label='train')
    # test plot
    plt.plot(test_log['step'], test_log[y], color='darkorange', label='test')
    plt.title(title + ' / ' + y)
    # set legend
    if y == 'accuracy':
        plt.legend(loc='lower right')
    elif y=='loss':
        plt.legend(loc='upper right')
    else:
        print('Something wrong!')
    ax.set_xlabel('step')
    ax.set_ylabel(y)
    ax.grid(True, zorder=5)
    plt.savefig(path)
    if show:
        plt.show()

def draw_graphs(tr_acc_path, tr_loss_path, test_path, plot_path, title=':D', smooth=True, show=False):
    train_log = load_train_log(tr_acc_path, tr_loss_path)
    test_log = load_test_log(test_path)
    #
    acc_path = plot_path + '/' + title + '_accuracy.png'
    loss_path = plot_path + '/' + title + '_loss.png' 
    plot_maker(train_log, test_log, 'accuracy', title=title, path=acc_path, smooth=smooth, show=show)
    plot_maker(train_log, test_log, 'loss', title=title, path=loss_path, smooth=smooth, show=show) 
