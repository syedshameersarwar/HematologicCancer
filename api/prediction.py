#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 19:23:54 2021

@author: kazzastic
"""
import pandas as pd
import pickle
filename = 'logisticReg.sav'


class Predict():
    
    def predictLogistic(self, filePath):
        cancers = ['Control', 'AML', 'CML', 'MDS', 'MDS/MPN', 'MPN', 'ALL', 'HL', 'NHL', 'MM', 'APML']
        model = pickle.load(open(filename, 'rb'))
        
        "Read the data and remove the NULL values by remove that particular row"
        data = pd.read_csv(filePath)
        nan_values = float("NaN")
        data.replace("#NULL!", nan_values, inplace=True)
        data.dropna(subset = ['NE_SFL'], inplace=True)
        dropped_cols = ['Sub_groups1', 'Sub_groups2']
        data.drop(dropped_cols, axis='columns', inplace=True)
        print(data.shape)
        
        
        chi2_features = ['LY_WY', 'MO_WY', 'NE_WY', 'LY_WX', 'NE_WZ', 'MO_WZ', 'LY_WZ', 'NE_WX', 'MO_WX', 'NE_SSC', 'MO_Y', 'MO_X', 'MCV', 'LY_X', 'LY_Y', 'NE_FSC', 'MO_Z', 'LY_Z', 'RDW_SD', 'Lymph', 'NE_SFL', 'PCV', 'Mono','MCHC','MCH','PLT','Neut','RDW_CV','Hb','WBC','LYMPH_abs', 'RBC'] 
        removed_feat = ['Mono','MCHC','MCH','PLT','Neut','RDW_CV','Hb','WBC','LYMPH_abs', 'RBC']
        
        
        new_x = data[chi2_features]
        new_x.shape
        
        y_new = model.predict(new_x)
        return cancers[y_new[0]]