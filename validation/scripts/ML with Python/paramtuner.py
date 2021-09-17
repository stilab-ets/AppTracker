import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
import xgboost as XGB
#pip install xgboost
from xgboost import XGBClassifier
from sklearn.naive_bayes import GaussianNB,BernoulliNB
import os
criter =  ['gini', 'entropy']
max_depth = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None]
max_features = ['sqrt', 'log2',  None]
param_choice_ML = {
              'XGB':  
                  {
                          'classifier':XGBClassifier(),
                          'class':XGBClassifier
                         ,'params':{
                                    'max_depth':     max_depth,
                                    'eta':[0.01,0.1,0.3,0.5,0.7],
                                    'num_class':[3],
                                    'objective':['multi:softmax','binary:logistic'],
                                    'eval_metric':['merror'],
                                    'min_child_weight': [1, 5, 10],
                                    'gamma': [0.5, 1, 1.5, 2, 5],
                                    'subsample': [0.6, 0.8, 1.0],
                                    'colsample_bytree': [0.6, 0.8, 1.0],
                                    'n_estimators':[50,100,200,300,600],
                                    'learning_rate':[0.01,0.02,0.05,0.1,0.3],
                                    
                            }
                    },
              'LR':
                  {
                  'classifier':LogisticRegression()
                  ,'class':LogisticRegression
                  ,'params':{
                           'max_iter':   [200, 400, 600, 800, 1000,2000,5000,10000,20000,50000]  ,
                            'penalty': ['l1','l2','none'],
                            'solver':['newton-cg', 'lbfgs', 'sag','saga','liblinear']
                            }
                  },
              
               'DT': 
                   {
                        'classifier':DecisionTreeClassifier()
                        ,'class':DecisionTreeClassifier,
                        'params':{
            			 'criterion':   criter  ,
                          'max_depth': max_depth,
                          'min_samples_split': [2, 10],
                          'min_samples_leaf':[1,2,3,4,5,None], 
                          'max_features':max_features
                        }
                      },
                'RF': 
                    {
                        'classifier':RandomForestClassifier(),
                        'class':RandomForestClassifier,
                        'params':{
                            'n_estimators':    [50,100,200, 400, 600] ,
                            'max_depth': max_depth,
            				'criterion':    criter ,
                            'min_samples_split': [2, 10,50,100],
                            'min_samples_leaf':[1,2,3,4,5], 
                            'max_features':max_features
                            }
                      },
                'SVC':
                    { 'classifier':SVC(),
                     'class':SVC,
                       'params':{
                           'C': [1, 2],
                            'kernel': ['linear','rbf'],
                            'max_iter':     [200, 400, 600, 800, 1000,2000,5000,10000,50000]
                            }
                     },
                'KNN':
                    { 'classifier':KNeighborsClassifier(),
                      'class':KNeighborsClassifier,
                       'params':{
                           'n_neighbors': [2,5,10,20],
                            'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
                            'leaf_size':     [1,2,3,4,5,50],
                            'weights':['uniform','distance']
                            
                            }
                     },
                'BNB':{
                'classifier':BernoulliNB(),
                'class':BernoulliNB,
                   'params':{
                       'alpha': [0.0,1.0],
                        'binarize': [0.0,0.5,1.0,None],
                        'fit_prior':     [True,False]
                        }
                 }
             
             }
def getBestParams(algo,X_train,y_train):
    param_elem = param_choice_ML[algo]
    tuner = GridSearchCV(estimator = param_elem["classifier"],
                                       param_grid =  param_elem["params"],
                                        scoring = 'accuracy',
                                       cv = 5)
     
    tuner = tuner.fit(X_train, y_train)
    best_params = tuner.best_params_
    print("DONE", algo,best_params)
    return best_params,param_elem["class"] 
    
    return {},param_elem["class"]