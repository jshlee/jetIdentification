import numpy as np
import cPickle

def merge(red_arr, green_arr, blue_arr):
    return np.array( map(None, red_arr, green_arr, blue_arr))

def get_data(path):
    data = np.loadtxt(path, delimiter=',', unpack=False, dtype=None)
    size = 33*33
    labels = data[:, 0:1]
    # color channels
    cpt   = data[:, 1:1+size]
    npt   = data[:, 1+size: 1+2*size]
    cmul  = data[:, 1+2*size:]
    # merge
    flats = np.array( map(merge, cpt, npt, cmul) )
    # reshape
    images = np.array( map(lambda x: x.reshape((33,33,3)), flats) )
    return images, labels

if __name__ == "__main__":
    path_to_load = '../data/csv/jet.csv'
    data = get_data(path_to_load)
    # save data using cPickle
    path_to_save = '../data/pickle/jet.p'
    f = open(path_to_save, 'w')
    cPickle.dump(data, f)
    f.close()
