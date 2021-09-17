#imblearn
import pandas as pd

import statistics 
from sklearn.metrics import matthews_corrcoef,precision_score,f1_score,recall_score
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler

import os
import warnings
warnings.filterwarnings('ignore') 

import paramtuner

global results

results = pd.DataFrame(columns = 
                                   ["proj"]+["algo"]+["exp"]
                                  +["F1_1"]+["pre_1"] +["rec_1"]
                                  +["F1_2"]+["pre_2"] +["rec_2"]
                                  +["F1_3"]+["pre_3"] +["rec_3"]
                                  +["F1_weight"]+["pre_weight"] +["rec_weight"]
                                  +["F1_macro"]+["pre_macro"] +["rec_macro"]
                                  +["MCC"]
                                  +["AUC_1"]+["AUC_2"] +["AUC_3"]+["AUC_macro"]+["AUC_weight"]
                                 +["params"]
                                  +["cat"]
                                  )

def prep(data,sc):
    X = data.iloc[:, 1:].values
    y = data.iloc[:, 0].values
    Feature Scaling
    col_idx = np.array([18,20,22,24,26,28,30,32,34,36])
    X[:, 0:17] = sc.fit_transform(X[:, 0:17])
    X[:, col_idx] = sc.fit_transform(X[:, col_idx])
    X[:, 37:52] = sc.fit_transform(X[:, 37:52])   
    X = sc.fit_transform(X)
    return X,y

def getsamples(reel,clsx):
    n=0
    for x in reel:
        if (x==clsx):
            n+=1
    return n
    
def preprocessing(train_dataset,test_dataset,algo):
    sc = StandardScaler()
    X_train, y_train =  prep(train_dataset,sc)
    X_test,y_test    =  prep(test_dataset,sc)
    if "XGB" not in algo:
        try:
            X_train, y_train = SMOTE().fit_resample(X_train, y_train)
        except Exception as ex:
            print("error in sampling ",ex)
    return X_train, y_train,X_test,y_test

def getExp(proj_name):
    exp=""    
    for s in proj_name[proj_name.index("_"):]:
      if s.isdigit():
        exp=exp+s
    return exp

def getBinary_AUC(classs,reel,predict):
    df_predict= getLabel(classs,predict,"predict")
    df_reel= getLabel(classs,reel,"reel")
    
    
def lunchML(X_train, y_train,X_test,y_test,proj_name,model_name, cat="within"):
    results=[]
    scores=[]
    entries = []
    median_ent={}
    best_params, model = paramtuner.getBestParams(model_name,X_train,y_train)
    model = model(**best_params)
    
    for i in range(1,32):
        model.fit(X_train,y_train)
        y_test_pred = model.predict(X_test)
        
        entry = {}
        entry["cat"] =  cat
        #entry["params"] = best_params
        entry["proj"] = proj_name[ 0:proj_name.index("_")]
        entry["algo"] = model_name       
        f1 =    f1_score(y_test,y_test_pred, average=None)
        preci = precision_score(y_test,y_test_pred, average=None)
        recal = recall_score(y_test,y_test_pred, average=None)
        for i in range(1,(f1.shape[0]+1)):
          entry[str("F1_"+str(i))] =  f1[i-1]
          entry[str("pre_"+str(i))] =  preci[i-1]
          entry[str("rec_"+str(i))] =  recal[i-1]
          entry[str("AUC_"+str(i))] =  getBinary_AUC(i,y_test_pred,y_test)
    
        entry["exp"] =  getExp(proj_name)
        entry["F1_weight"] =  f1_score(y_test,y_test_pred, average='weighted')
        entry["pre_weight"] =  precision_score(y_test,y_test_pred, average='weighted')
        entry["rec_weight"] =  recall_score(y_test,y_test_pred, average='weighted')
        
        entry["F1_macro"] =  f1_score(y_test,y_test_pred, average='macro')
        entry["pre_macro"] =  precision_score(y_test,y_test_pred, average='macro')
        entry["rec_macro"] =  recall_score(y_test,y_test_pred, average='macro')
        
        n = getMCC.getsamples(y_test,1)
        m = getMCC.getsamples(y_test,2)
        p = getMCC.getsamples(y_test,3)
    
        entry["MCC"] =  matthews_corrcoef(y_test,y_test_pred)
        entry["AUC_weight"] = (entry["AUC_1"] * n + entry["AUC_2"] * m + entry["AUC_3"] *p)/(n+m+p)
        entry["AUC_macro"]  = (entry["AUC_1"]  + entry["AUC_2"] + entry["AUC_3"])/3
        
        print(entry["F1_macro"])
        scores.append(entry["F1_macro"])
        entries.append(entry)    
        
    bestScore=statistics.median(scores)
    for entry in entries:
        if entry["F1_macro"]==bestScore:
            median_ent=entry
            
    print(cat,"****",proj_name,"****",model_name,"***",median_ent["F1_macro"])
    results.append(median_ent)
    return results






def launchScript_Cross(algo):
    global results   
    path='path to cross data'#
    for cat in os.listdir(path):
        for file_name in os.listdir(path+"/"+cat):
            if("_train" in file_name):
                print("---------------",file_name)
                train = pd.read_csv(path+"/"+cat+'/'+file_name)
                test= pd.read_csv(path+"/"+cat+'/'+(file_name.replace("_train","_test")))
                X_train, y_train,X_test,y_test=preprocessing(train,test,algo)
                try:
                    results = results.append(lunchML(X_train, y_train,X_test,y_test,file_name,algo,cat))
                except Exception as ex:
                    print("prob in "+file_name)
                    print(ex)
    
    results.to_excel("res_cross"+algo+".xlsx")
    
#launchScript_Cross("XGB")
def launchScript_within(algo):
    global results   
    path='path to within data'
    for file_name in os.listdir(path):
        if("_train" in file_name):
            print("---------------",file_name)
            train = pd.read_csv(path+"/"+'/'+file_name)
            test= pd.read_csv(path+"/"+'/'+(file_name.replace("_train","_test")))
            X_train, y_train,X_test,y_test=preprocessing(train,test,algo)
            try:
                results = results.append(lunchML(X_train, y_train,X_test,y_test,file_name,algo))
            except Exception as ex:
                print("error in "+file_name)
                print(ex)
    
    results.to_excel("res_cross"+algo+".xlsx")
    
def runAllAlgo():        
    for algo in ['KNN','SVC',"BNB",'RF',"XGB","LR",'DT','BNB']:
        launchScript_within(algo)
    results.to_excel("res_k.xlsx")
    
    ##############################

    
    
    
    