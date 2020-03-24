# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 13:54:09 2019

@author: jeromlu2
"""
import time
import pandas as pd

DATA_LOCATION = './'
XL_FILE_NAME = 'AA_data.xlsx'

try:
    print('loading file: {0}'.format(XL_FILE_NAME))
    AA_df = pd.read_excel(DATA_LOCATION + XL_FILE_NAME, header = 1, index_col = 1, nrows = 21,
                          sheet_name = 'amino_acids')
    
    pkl_fname = DATA_LOCATION + XL_FILE_NAME.split('.')[0] + '.pkl'
    print('saving file: {0}'.format(XL_FILE_NAME))
    AA_df.to_pickle(pkl_fname)
    time.sleep(5)
    
except Exception as e:
    print(e)
    time.sleep(30)

