#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 15:04:21 2020

@author: mulugetasemework
"""
import numpy as np
import pandas as pd
import os

#%% get data
 
data_path = '/Users/mulugetasemework/Dropbox/Python/presbyterian/patient_data.csv' 
results_path = '/Users/mulugetasemework/Dropbox/Python/presbyterian//Results/'

All_data = pd.read_csv(data_path,low_memory=False, error_bad_lines=False)
#%% some parameters
corr_thresh = 0.95 # drop one correlated column
sparsity_thresh = .5 # any column with more than this percentage of redundancy is discarded
# i.e. it has too many redundant values
NaN_thresh = 0.95 # any column with  this percentage of Nans is discarded 
# intentionally kept high for this exercise since the few rows 
# with data in sparse columns are still important
# %% clean up data, for instance, drop highly correlated columns 
def clean_up_data(All_data, sparsity_thresh, NaN_thresh, corr_thresh):
    # cleanup: NANs and zero standard deviation columns and sparse rows
    All_data = All_data.dropna(axis=1, how='all')
    All_data = All_data.dropna(axis=0, how='all')
    All_data = All_data.loc[:, (All_data != All_data.iloc[0]).any()]
    All_data = All_data.reset_index(drop=True)
    
    # first  clean up data with sparsity analysis
    # remove columns which are very sparsely populated as they might cause false results
    # such as becoming very important in predictions despite having few real data points
    # column 1 for this data is ID, so it can be repeated
    sparse_cols = [(len(np.unique(All_data.iloc[:,i]))/len(All_data))*100  < 
                   int((1-sparsity_thresh)*len(All_data)) for i in range(0, All_data.shape[1])]
    
    #remove sparse columns (i.e. with too many redundant values)
    All_data = All_data.iloc[:,sparse_cols]
    
    #remove too-many NaN columns
    non_NaN_cols = [All_data.iloc[:,i].isna().sum() < int(NaN_thresh*len(All_data)) for i in range(All_data.shape[1])]
    All_data = All_data.iloc[:, non_NaN_cols]
    
    # drop the pesky "Unnamed: 0" column, if exists
    # this happens sometimes depending on which packages are used or the quality of the .CSV file
    
    unNamedCols =   All_data.filter(regex='Unnamed').columns
    
    if not unNamedCols.empty:
        All_data = All_data.drop(unNamedCols, axis=1, inplace=True)
    
    # drop highly correlated columns
    
    # To do so, first reate correlation matrix
    corr_matrix = All_data.corr().abs()

    # Select upper triangle of correlation matrix
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
    
    # Find index of feature columns with correlation greater than 0.95
    to_drop = [column  for column in upper.columns if any(upper[column] > corr_thresh)]
    
    # Drop Marked Features
    All_data.drop(All_data[to_drop], axis=1)
    
    return All_data

#%%
    #%% shuffle and clean up data
All_data = All_data.sample(frac=1)     
All_data = clean_up_data(All_data, sparsity_thresh, NaN_thresh, corr_thresh)
#%% now save cleaned up data

All_data.to_csv(os.path.join(results_path, str('clean_data.csv')))