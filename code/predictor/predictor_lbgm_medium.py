# -*- coding: utf-8 -*-
# @Time    : 2018/4/29 20:12
# @Author  : LeonHardt
# @File    : predictor_lbgm_medium.py

import os
import lightgbm as lgb
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import Imputer
from scoring_test import evalerror
from sklearn.ensemble import RandomForestRegressor

# load or create your dataset
print('Load data...')
path = os.getcwd() + '/data_app/'
save_path = os.getcwd() + '/predict/'
if os.path.exists(save_path) is False:
    os.makedirs(save_path)

print('pre training...')
x_train = np.loadtxt(path+'x_train_nan_error3_change.txt', delimiter=',', dtype='float')
y_train = np.loadtxt(path+'y_train_nan_error3_change.txt', delimiter=',', dtype='float')
x_test = np.loadtxt(path+'x_test_nan_error3_change.txt', delimiter=',', dtype='float')

x_train_2 = np.loadtxt(path+'x_train_nan_error3_change_pred21.txt', delimiter=',', dtype='float')
y_train_2 = np.loadtxt(path+'y_train_nan_error3_change_pred21.txt', delimiter=',', dtype='float')

imp1 = Imputer(missing_values='NaN', strategy='median', axis=1)
imp1.fit(x_train)
x_train1 = imp1.transform(x_train)
x_test1 = imp1.transform(x_test)

imp2 = Imputer(missing_values='NaN', strategy='median', axis=1)
imp2.fit(x_train_2)
x_train_pred2 = imp2.transform(x_train_2)
x_test1_pred2 = imp2.transform(x_test)

print('Start training...')
# train
gbm0 = lgb.LGBMRegressor(objective='regression', num_leaves=57, learning_rate=0.05, n_estimators=195,
                         min_child_weight=1, colsample_bytree=0.7, reg_lambda=3, reg_alpha=2)
gbm0.fit(x_train, y_train[:, 0], eval_metric=evalerror)
pred0 = gbm0.predict(x_test)
prediction = pred0

gbm1 = lgb.LGBMRegressor(objective='regression', num_leaves=45, learning_rate=0.05, n_estimators=156,
                         min_child_weight=1, colsample_bytree=0.7, reg_lambda=3, reg_alpha=2)
gbm1.fit(x_train, y_train[:, 1], eval_metric=evalerror)
pred1 = gbm1.predict(x_test)
prediction = np.vstack((prediction, pred1))

# gbm2 = lgb.LGBMRegressor(objective='regression', num_leaves=85, learning_rate=0.03, n_estimators=239,
#                          min_child_weight=1, colsample_bytree=0.7, reg_lambda=3, reg_alpha=2)
# gbm2.fit(x_train_2, y_train_2, eval_metric=evalerror)   # train 2
# pred2 = gbm2.predict(x_test)
# prediction = np.vstack((prediction, pred2))

rf2 = RandomForestRegressor(n_estimators=400, n_jobs=-1)
rf2.fit(x_train_pred2, y_train_2)   # train 2
pred2 = rf2.predict(x_test1_pred2)
prediction = np.vstack((prediction, pred2))

gbm3 = lgb.LGBMRegressor(objective='regression', num_leaves=59, learning_rate=0.05, n_estimators=515,
                         min_child_weight=1, colsample_bytree=0.7, reg_lambda=3, reg_alpha=2)
gbm3.fit(x_train, y_train[:, 3], eval_metric=evalerror)
pred3 = gbm3.predict(x_test)
prediction = np.vstack((prediction, pred3))

gbm4 = lgb.LGBMRegressor(objective='regression', num_leaves=73, learning_rate=0.04, n_estimators=305,
                         min_child_weight=1, colsample_bytree=0.7, reg_lambda=3, reg_alpha=2)
gbm4.fit(x_train, y_train[:, 4], eval_metric=evalerror)
pred4 = gbm4.predict(x_test)
prediction = np.vstack((prediction, pred4))

prediction = prediction.T
np.savetxt(save_path+'prediction_gbm_nan_change_error3_pred21.txt', prediction, fmt='%.3e',  delimiter=',')
