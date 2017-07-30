from __future__ import print_function

import numpy as np
import xgboost as xgb
import argparse

def param_space(max_depth, gamma, eta):
    
    yield param

data_set = np.loadtxt('./data/jet4np.txt', delimiter=',', dtype=np.float32)
train_size = int(data.shape[0] * 0.6)
dtrain = xgb.DMatrix(data = data[:train_size, 1:], label = data[:train_size, 0])
dtest = xgb.DMatrix(data = data[train_size:, 1:], label = data[train_size, 0])
watchlist = [(dtrain, 'train'), (dtest, 'test')]

bst = xgb.train(param, dtrain, num_round, watchlist)

param_space = get_params(

for param in param_space:
    

