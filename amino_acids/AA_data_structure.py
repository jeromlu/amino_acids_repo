# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 15:45:49 2019

@author: jeromlu2
"""

import bisect, io
import pandas as pd

from PyQt5.QtGui import QImage
from PyQt5.QtCore import QFile, QIODevice
import qrc_resources

DATA_LOCATION = './resources/'
PKL_FILE_NAME = 'AA_data.pkl'
FIGURES_LOCATION = './resources/amino_acid_pictures/'

class AminoAcid(object):
    
    def __init__(self, name, short_label, one_letter_label, MW, pI,
                 pKa1, pKa2, pKa, skeletal_formula = None):
    
        self.name = name
        self.short_label = short_label
        self.one_letter_label = one_letter_label
        self.MW = MW
        self.pI = pI
        self.pKa1 = pKa1
        self.pKa2 = pKa2
        self.pKa = pKa
        self.skeletal_formula = skeletal_formula
    


class AminoAcids(object):
    
    def __init__(self):
    
        self.__amino_acids = []
        self.__AA_from_ID = {}
        
    def load_data(self):
        
        #data frame containing the information about the amino acids
        #be careful about the structure of excel file        
        
        file = QFile(':/AA_data.pkl')
        if file.open(QIODevice.ReadOnly):
            f = io.BytesIO(file.readAll().data())
            #AA_df = pd.read_excel(f, header = 1, index_col = 1, num_rows = 21)
            AA_df = pd.read_pickle(f, compression = None)
        #AA_df = pd.read_pickle(DATA_LOCATION + PKL_FILE_NAME)

        for name, row in AA_df.iterrows():
            
            #prepare data about AA
            name = name
            short_label = row.AA_short_label
            one_letter_label = row.AA_one_letter_label
            MW = row.MW
            pI = row.pI
            pKa1 = row.pKa1
            pKa2 = row.pKa2
            pKa = row.pKa
            
            #fname = FIGURES_LOCATION + name.lower() + '.png'
            fname = ':/' + name.lower() + '.png'
            skeletal_formula = QImage(fname)
            #print(skeletal_formula.isNull())
            
            #instantiate amino acid
            AA = AminoAcid(name, short_label, one_letter_label, MW, pI,
                 pKa1, pKa2, pKa, skeletal_formula)
            
            self.add_AA(AA)
            #print(name, AA.short_label)
            
    def __len__(self):
        return len(self.__amino_acids)
    
    def __iter__(self):
        for aa in self.__amino_acids:
            yield self.__amino_acids

    def add_AA(self, amino_acid):
        '''Add AminoAcid object to AminoAcids container.
        We add it to appropriate place with bisect method.'''
        
        if id(amino_acid) in self.__AA_from_ID:
            return False
        key = amino_acid.name
        bisect.insort_left(self.__amino_acids, [key, amino_acid])
        self.__AA_from_ID[id(amino_acid)] = amino_acid
        return True
    
    def get_AA_names(self):
        return [AA[0] for AA in self.__amino_acids]
    
    def get_AA(self, name):
        AA_names = self.get_AA_names()
        if name not in self.get_AA_names():
            return None
        idx = bisect.bisect_left(AA_names, name)
        amino_acid = self.__amino_acids[idx]
        return amino_acid[-1]
        
            
            
if __name__ == '__main__':
    
    AA = AminoAcids()
    AA.load_data()

        
        
