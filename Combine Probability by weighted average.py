# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 13:26:20 2016

@author: chod1
"""

import pandas as pd
import os 
import numpy as np
import math
CWD =r"S:\GSTS Integrity\PRIM Implementation\Daniel Cho\Risk Validation"
os.chdir(CWD)

def read_file():
    PIM_filepath = r".\test1.xls"
    IRIS_filepath = r".\EGDI Stress Corrosion Cracking Run 2548 by Segment - oshawa.xls"
    #IRIS = pd.read_excel(IRIS_filepath, skip_rows=3, header=3)
    IRIS = pd.read_excel(IRIS_filepath)
    PIM = pd.read_excel ( PIM_filepath,sheetname='test1',index_col=0 )
    #IRIS["index combined"] = IRIS["Index"].str.cat(IRIS["Index.1"])
    return PIM, IRIS
    
def merge_file(PIM,IRIS):
    df= IRIS.merge(PIM,on="idSegment",how='left', suffixes=('_IRIS','_PIM')) 
    # working
    #within_IRIS_bucket =  (IRIS['Start Chainage (m)_IRIS'] <= IRIS['Start Chainage (m)_PIM'] ) & (IRIS['Start Chainage (m)_PIM'] <= IRIS['End Chainage (m)_IRIS'] )
    within_IRIS_bucket =  df['Start Chainage (m)_PIM'].between(df['Start Chainage (m)_IRIS'],df['End Chainage (m)_IRIS'] ) & df['End Chainage (m)_PIM'].between(df['Start Chainage (m)_IRIS'],df['End Chainage (m)_IRIS'] )  
    
    PIM_start_sticking_out =  df['Start Chainage (m)_IRIS'].between(df['Start Chainage (m)_PIM'], df['End Chainage (m)_PIM']   )
    PIM_end_sticking_out =  df['End Chainage (m)_IRIS'].between(df['Start Chainage (m)_PIM'],  df['End Chainage (m)_PIM'] )
    # Cutting the line by adjusting PIM start to match IRIS start for start sticking out and recalculate length
    df.loc[PIM_start_sticking_out,'Start Chainage (m)_PIM'] = df.loc[PIM_start_sticking_out,'Start Chainage (m)_IRIS']
    df.loc[PIM_start_sticking_out,'Length (m)_PIM'] = df.loc[PIM_start_sticking_out,'End Chainage (m)_PIM'] - df.loc[PIM_start_sticking_out,'Start Chainage (m)_PIM']
    # Cutting the line by adjusting PIM End to match IRIS End for End sticking out and recalculate length
    df.loc[PIM_end_sticking_out,'End Chainage (m)_PIM'] = df.loc[PIM_end_sticking_out,'End Chainage (m)_IRIS']
    df.loc[PIM_end_sticking_out,'Length (m)_PIM'] = df.loc[PIM_end_sticking_out,'End Chainage (m)_PIM'] - df.loc[PIM_end_sticking_out,'Start Chainage (m)_PIM']
    
    
    merged = df [ within_IRIS_bucket | PIM_start_sticking_out | PIM_end_sticking_out  ]
    
    #IRIS.groupby('Segment_IRIS').apply(lambda x: np.average(IRIS['Probability of Ignition, Rupture'], weights=IRIS['Length (m)_PIM'] )).unique()
    return merged
    
def export_file(merged):

    #PIM.to_excel(r".\PIM.xlsx")
    merged.to_excel(r".\merged.xlsx")
    return

def main():
    PIM, IRIS =  read_file()
    merged = merge_file(PIM,IRIS)
    export_file(merged)
    return 
    
main()    