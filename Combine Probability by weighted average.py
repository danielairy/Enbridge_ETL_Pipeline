# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 13:26:20 2016

@author: chod1
"""

import pandas as pd
import os 
import numpy as np
import math
import collections
CWD =r"S:\GSTS Integrity\PRIM Implementation\Daniel Cho\Risk Validation"
os.chdir(CWD)
action = pd.read_excel(r".\action.xlsx",index_col= 0, squeeze=True)
def weighed_average(grp):
    return grp._get_numeric_data().multiply(grp['Length (m)_PIM'], axis=0).sum()/grp['Length (m)_PIM'].sum()
    #return  np.average(grp, axis=0, weights=grp['Length (m)_PIM'])

actiondict = {
        'Segment_IRIS':  lambda x:x.value_counts().index[0] if x.notnull().all() else None,    
        'Segment_PIM':lambda x:str(np.min(x)) +'-' + str( np.max(x)),
        'Pipeline Index' : lambda x:x.value_counts().index[0] if x.notnull().all() else None,
        'Pipeline Name' : lambda x:x.value_counts().index[0] if x.notnull().all() else None,
        'Segment ID' : lambda x:x.value_counts().index[0] if x.notnull().all() else None,
        'Start Chainage (m)_PIM':np.min ,
        'End Chainage (m)_PIM':np.max ,
        'Length (m)_PIM':'sum',
        'HCA Name_PIM':lambda x:x.value_counts().index[0] if x.notnull().all() else None,
        'HCA Start Chainage (m)_PIM':np.min ,
        'HCA End Chainage (m)_PIM':np.max,
        'Rupture Ignition - Health & Safety':'sum',
        'Rupture Ignition - Physical Damage & Econ Loss':'sum',
        'Rupture Ignition - Evironmental Damage':'sum',
        'Rupture Ignition - Regulatory Impact':'sum',
        'Rupture Ignition - Customer Satisfaction':'sum',
        'Rupture Ignition - Corporate Image':'sum',
        'Rupture No Ignition - Health & Safety':'sum',
        'Rupture No Ignition - Physical Damage & Econ Loss':'sum',
        'Rupture No Ignition - Evironmental Damage':'sum',
        'Rupture No Ignition - Regulatory Impact':'sum',
        'Rupture No Ignition - Customer Satisfaction':'sum',
        'Rupture No Ignition - Corporate Image':'sum',
        'Leak Pinhole No Ignition - Health & Safety':'sum',
        'Leak Pinhole No Ignition - Physical Damage & Econ Loss':'sum',
        'Leak Pinhole No Ignition - Evironmental Damage':'sum',
        'Leak Pinhole No Ignition - Regulatory Impact':'sum',
        'Leak Pinhole No Ignition - Customer Satisfaction':'sum',
        'Leak Pinhole No Ignition - Corporate Image':'sum',
        'Leak 10mm Ignition - Health & Safety':'sum',
        'Leak 10mm Ignition - Physical Damage & Econ Loss':'sum',
        'Leak 10mm Ignition - Evironmental Damage':'sum',
        'Leak 10mm Ignition - Regulatory Impact':'sum',
        'Leak 10mm Ignition - Customer Satisfaction':'sum',
        'Leak 10mm Ignition - Corporate Image':'sum',
        'Leak 10mm No Ignition - Health & Safety':'sum',
        'Leak 10mm No Ignition - Physical Damage & Econ Loss':'sum',
        'Leak 10mm No Ignition - Evironmental Damage':'sum',
        'Leak 10mm No Ignition - Regulatory Impact':'sum',
        'Leak 10mm No Ignition - Customer Satisfaction':'sum',
        'Leak 10mm No Ignition - Corporate Image':'sum',
        'Leak  2580mm Ignited - Health & Safety':'sum',
        'Leak  2580mm Ignited - Physical Damage & Econ Loss':'sum',
        'Leak  2580mm Ignited - Evironmental Damage':'sum',
        'Leak  2580mm Ignited - Regulatory Impact':'sum',
        'Leak  2580mm Ignited - Customer Satisfaction':'sum',
        'Leak  2580mm Ignited - Corporate Image':'sum',
        'Leak  2580mm No Ignition - Health & Safety':'sum',
        'Leak  2580mm No Ignition - Physical Damage & Econ Loss':'sum',
        'Leak  2580mm No Ignition - Evironmental Damage':'sum',
        'Leak  2580mm No Ignition - Regulatory Impact':'sum',
        'Leak  2580mm No Ignition - Customer Satisfaction':'sum',
        'Leak  2580mm No Ignition - Corporate Image':'sum',
        'Total Consequence ($)_PIM':'sum',
        'Risk/m ($/m.yr)':'sum',
        'Total Risk ($/yr)':'sum',
        'Risk ($/m.yr) - Health & Safety':'sum',
        'Risk ($/m.yr) - Physical Damage & Econ Loss':'sum',
        'Risk ($/m.yr) - Evironmental Damage':'sum',
        'Risk ($/m.yr) - Regulatory Impact':'sum',
        'Risk ($/m.yr) - Customer Satisfaction':'sum',
        'Risk ($/m.yr) - Corporate Image':'sum',
        'nmStartMeter':np.min ,
        'nmEndMeter':np.max}

def f(grp):
    return pd.DataFrame({'Stress Corrosion Cracking (SCC) (/m.yr)':np.sum(grp['Stress Corrosion Cracking (SCC) (/m.yr)']),
        'Manufacturing-Related Defects (/m.yr)':np.sum(grp['Manufacturing-Related Defects (/m.yr)']),
        'Welding / Fabrication Related Defects (/m.yr)':np.sum(grp['Welding / Fabrication Related Defects (/m.yr)'])})

def read_file():
    PIM_filepath = r".\PiMSlider Risk_Dec13.xls"
    #PIM_filepath = r".\test1.xls"
    #IRIS_filepath = r".\EGDI Stress Corrosion Cracking Run 2548 by Segment - oshawa.xls"
    IRIS_filepath =r"Combined with idSegments.xlsx"
    IRIS = pd.read_excel(IRIS_filepath, skip_rows=3, header=3)
    #IRIS = pd.read_excel(IRIS_filepath)
    PIM = pd.read_excel ( PIM_filepath,sheetname=0,index_col=0 )
    #IRIS["index combined"] = IRIS["Index"].str.cat(IRIS["Index.1"])
    PIM = PIM.apply(lambda x: x.astype('float32') if x.dtypes == np.dtype('float64') else x)
    IRIS = IRIS.apply(lambda x: x.astype('float32') if x.dtypes == np.dtype('float64') else x)
    return PIM, IRIS

def cond_merge(g):
    g = IRIS.merge(PIM,on="idSegment",how='left', suffixes=('_IRIS','_PIM')) 
    within_IRIS_bucket =  df['Start Chainage (m)_PIM'].between(df['Start Chainage (m)_IRIS'],df['End Chainage (m)_IRIS'] ) & df['End Chainage (m)_PIM'].between(df['Start Chainage (m)_IRIS'],df['End Chainage (m)_IRIS'] )  
    PIM_start_sticking_out =  df['Start Chainage (m)_IRIS'].between(df['Start Chainage (m)_PIM'], df['End Chainage (m)_PIM']   )
    PIM_end_sticking_out =  df['End Chainage (m)_IRIS'].between(df['Start Chainage (m)_PIM'],  df['End Chainage (m)_PIM'] )
    df.loc[PIM_start_sticking_out,'Start Chainage (m)_PIM'] = df.loc[PIM_start_sticking_out,'Start Chainage (m)_IRIS']
    df.loc[PIM_start_sticking_out,'Length (m)_PIM'] = df.loc[PIM_start_sticking_out,'End Chainage (m)_PIM'] - df.loc[PIM_start_sticking_out,'Start Chainage (m)_PIM']
    # Cutting the line by adjusting PIM End to match IRIS End for End sticking out and recalculate length
    df.loc[PIM_end_sticking_out,'End Chainage (m)_PIM'] = df.loc[PIM_end_sticking_out,'End Chainage (m)_IRIS']
    df.loc[PIM_end_sticking_out,'Length (m)_PIM'] = df.loc[PIM_end_sticking_out,'End Chainage (m)_PIM'] - df.loc[PIM_end_sticking_out,'Start Chainage (m)_PIM']
    g = df [ within_IRIS_bucket | PIM_start_sticking_out | PIM_end_sticking_out  ]
    return g
    
def merge_file(PIM,IRIS):
    df= IRIS.merge(PIM,on="idSegment",how='left', suffixes=('_IRIS','_PIM')) 
    # working
    #within_IRIS_bucket =  (IRIS['Start Chainage (m)_IRIS'] <= IRIS['Start Chainage (m)_PIM'] ) & (IRIS['Start Chainage (m)_PIM'] <= IRIS['End Chainage (m)_IRIS'] )
    
    # Cutting the line by adjusting PIM start to match IRIS start for start sticking out and recalculate length
    df.loc[PIM_start_sticking_out,'Start Chainage (m)_PIM'] = df.loc[PIM_start_sticking_out,'Start Chainage (m)_IRIS']
    df.loc[PIM_start_sticking_out,'Length (m)_PIM'] = df.loc[PIM_start_sticking_out,'End Chainage (m)_PIM'] - df.loc[PIM_start_sticking_out,'Start Chainage (m)_PIM']
    # Cutting the line by adjusting PIM End to match IRIS End for End sticking out and recalculate length
    df.loc[PIM_end_sticking_out,'End Chainage (m)_PIM'] = df.loc[PIM_end_sticking_out,'End Chainage (m)_IRIS']
    df.loc[PIM_end_sticking_out,'Length (m)_PIM'] = df.loc[PIM_end_sticking_out,'End Chainage (m)_PIM'] - df.loc[PIM_end_sticking_out,'Start Chainage (m)_PIM']

    df = df [ within_IRIS_bucket | PIM_start_sticking_out | PIM_end_sticking_out  ]
    
    column_to_wavg = ['Segment_IRIS'] +['Length (m)_PIM'] + list( df.loc[:,'External Corrosion (/m.yr) - Rupture, Ignition':'Total Probability (/m.yr)']  )
    columns_to_agg = ['Segment_IRIS'] + list( df.loc[:,'Segment_PIM':'HCA End Chainage (m)_PIM']  ) + list( df.loc[:,'Rupture Ignition - Health & Safety':'nmEndMeter']  ) 
    
    wa = df[column_to_wavg].groupby('Segment_IRIS').apply(weighed_average)
    agg = df[columns_to_agg].groupby('Segment_IRIS').agg(actiondict)
    #df.groupby('Segment_IRIS').apply(f)
    #df.groupby('Segment_IRIS').apply(lambda x: np.average(x['Equipment Failure (/m.yr)'], weights=x['Length (m)_PIM']))
    wa = wa.drop(['Segment_IRIS','Length (m)_PIM'],1)
    wa = wa.reset_index(drop=False)
    #agg = agg.reset_index(drop=True)
    #IRIS = IRIS.set_index('Segment')
    #mergedx = pd.concat([IRIS,agg,wa])
    merged = pd.merge(IRIS,agg,left_on='Segment',right_on='Segment_IRIS', how='left', suffixes=('_IRAS','_PIM'))
    merged = pd.merge(merged,wa,left_on='Segment_IRIS',right_on='Segment_IRIS', how='left', suffixes=('_left','_PIM'))
    #df.groupby('Segment_IRIS').agg(OrderedDict([("Manufacturing-Related Defects (/m.yr) - Leak, Pinhole, No Ignition",np.mean), ("Leak  2580mm No Ignition - Regulatory Impact",weighed_average  )]     ))
    #IRIS.groupby('Segment_IRIS').apply(lambda x: np.average(IRIS['Probability of Ignition, Rupture'], weights=IRIS['Length (m)_PIM'] )).unique()
    
    return merged
exportcolumns =['Matrix', 'Segment', 'Corporation', 'Index', 'idSegment', 'Start Chainage (m)', 'Begin Series', 'Start Station (m)', 'End Chainage (m)', 'End Station (m)', 'Length (m)', 'HCA Name_PIM', 'HCA Start Section', 'HCA Start Chainage (m)_PIM', 'HCA End Section', 'HCA End Chainage (m)_PIM', 'HCA Start Station', 'HCA Start Engg. Station (m)', 'HCA End Series', 'HCA End Engg. Station (m)', 'Regulator', 'Wall Thickness (mm)', 'Outside Diameter (mm)', 'MOP (kPa )', 'Pipe Grade (MPa)', '% SMYS', 'SCC RF Factor A', 'SCC RF Factor B', 'SCC RF Factor C', 'SCC  Rupture Frequency', 'Line Coating', 'SCC FR Factor A', 'SCC FR Factor B', 'SCC Failure Rate', 'SCC Failure Rupture Frequency (/km.yr)', 'SCC Failure  Leak Frequency (/km.yr)', 'Probability of Ignition, Rupture', 'SCC Rupture - Ignition (/km.yr)', 'SCC Rupture -  No Ignition', 'SCC Leak (pinhole) -  No Ignition (/km.yr)', 'Stress Corrosion Cracking (SCC) (/km.yr)', 'Consequence ($)', 'Total Consequence ($)_PIM','Segment_PIM','Pipeline Index','Pipeline Name','Segment ID','Start Chainage (m)_PIM','End Chainage (m)_PIM','Length (m)_PIM','HCA Name','HCA Start Chainage (m)','HCA End Chainage (m)','External Corrosion (/m.yr) - Rupture, Ignition','External Corrosion (/m.yr) - Rupture, No Ignition','External Corrosion (/m.yr) - Leak, 10mm, Ignition','External Corrosion (/m.yr) - Leak, 10mm, No Ignition','Internal Corrosion (/m.yr) - Rupture, Ignition','Internal Corrosion (/m.yr) - Rupture, No Ignition','Internal Corrosion (/m.yr) - Leak, 10mm, Ignition','Internal Corrosion (/m.yr) - Leak, 10mm, No Ignition','Internal Erosion (/m.yr) - Rupture, Ignition','Internal Erosion (/m.yr) - Rupture, No Ignition','Internal Erosion (/m.yr) - Leak, 10mm, Ignition','Internal Erosion (/m.yr) - Leak, 10mm, No Ignition','Stress Corrosion Cracking (SCC) (/m.yr) - Rupture, Ignition','Stress Corrosion Cracking (SCC) (/m.yr) - Rupture, No Ignition','Stress Corrosion Cracking (SCC) (/m.yr) - Leak, Pinhole, No Ignition','Manufacturing-Related Defects (/m.yr) - Rupture, Ignition','Manufacturing-Related Defects (/m.yr) - Rupture, No Ignition','Manufacturing-Related Defects (/m.yr) - Leak, Pinhole, No Ignition','Welding / Fabrication Related Defects (/m.yr) - Rupture, Ignition','Welding / Fabrication Related Defects (/m.yr) - Rupture, No Ignition','Welding / Fabrication Related Defects (/m.yr) - Leak, Pinhole, No Ignition','Equipment Failure (/m.yr) - Leak, Pinhole, No Ignition','Weather-Related (/m.yr) - Leak , 2580mm, Ignited','Third Party / Mechanical Damage (/m.yr) - Rupture, Ignition','Third Party / Mechanical Damage (/m.yr) - Rupture, No Ignition','Third Party / Mechanical Damage (/m.yr) - Leak , 2580mm, Ignited','Third Party / Mechanical Damage (/m.yr) - Leak , 2580mm, No Ignition','Outside Forces (/m.yr) - Rupture, Ignition','Outside Forces (/m.yr) - Rupture, No Ignition','Incorrect Operation Procedures (/m.yr) - Rupture, Ignition','Incorrect Operation Procedures (/m.yr) - Rupture, No Ignition','Incorrect Operation Procedures (/m.yr) - Leak , 2580mm, Ignited','Incorrect Operation Procedures (/m.yr) - Leak , 2580mm, No Ignition','External Corrosion (/m.yr)','Internal Corrosion (/m.yr)','Internal Erosion (/m.yr)','Stress Corrosion Cracking (SCC) (/m.yr)','Manufacturing-Related Defects (/m.yr)','Welding / Fabrication Related Defects (/m.yr)','Equipment Failure (/m.yr)','Weather-Related (/m.yr)','Third Party / Mechanical Damage (/m.yr)','Outside Forces (/m.yr)','Incorrect Operation Procedures (/m.yr)','Rupture, Ignition (/m.yr)','Rupture, No Ignition (/m.yr)','Leak, Pinhole, No Ignition (/m.yr)','Leak, 10mm, Ignited (/m.yr)','Leak, 10mm, No Ignition (/m.yr)','Leak , 2580mm, Ignited (/m.yr)','Leak , 2580mm, No Ignition (/m.yr)','Total Probability (/m.yr)','Rupture Ignition - Health & Safety','Rupture Ignition - Physical Damage & Econ Loss','Rupture Ignition - Evironmental Damage','Rupture Ignition - Regulatory Impact','Rupture Ignition - Customer Satisfaction','Rupture Ignition - Corporate Image','Rupture No Ignition - Health & Safety','Rupture No Ignition - Physical Damage & Econ Loss','Rupture No Ignition - Evironmental Damage','Rupture No Ignition - Regulatory Impact','Rupture No Ignition - Customer Satisfaction','Rupture No Ignition - Corporate Image','Leak Pinhole No Ignition - Health & Safety','Leak Pinhole No Ignition - Physical Damage & Econ Loss','Leak Pinhole No Ignition - Evironmental Damage','Leak Pinhole No Ignition - Regulatory Impact','Leak Pinhole No Ignition - Customer Satisfaction','Leak Pinhole No Ignition - Corporate Image','Leak 10mm Ignition - Health & Safety','Leak 10mm Ignition - Physical Damage & Econ Loss','Leak 10mm Ignition - Evironmental Damage','Leak 10mm Ignition - Regulatory Impact','Leak 10mm Ignition - Customer Satisfaction','Leak 10mm Ignition - Corporate Image','Leak 10mm No Ignition - Health & Safety','Leak 10mm No Ignition - Physical Damage & Econ Loss','Leak 10mm No Ignition - Evironmental Damage','Leak 10mm No Ignition - Regulatory Impact','Leak 10mm No Ignition - Customer Satisfaction','Leak 10mm No Ignition - Corporate Image','Leak  2580mm Ignited - Health & Safety','Leak  2580mm Ignited - Physical Damage & Econ Loss','Leak  2580mm Ignited - Evironmental Damage','Leak  2580mm Ignited - Regulatory Impact','Leak  2580mm Ignited - Customer Satisfaction','Leak  2580mm Ignited - Corporate Image','Leak  2580mm No Ignition - Health & Safety','Leak  2580mm No Ignition - Physical Damage & Econ Loss','Leak  2580mm No Ignition - Evironmental Damage','Leak  2580mm No Ignition - Regulatory Impact','Leak  2580mm No Ignition - Customer Satisfaction','Leak  2580mm No Ignition - Corporate Image','Total Consequence ($)','Risk/m ($/m.yr)','Total Risk ($/yr)','Risk ($/m.yr) - Health & Safety','Risk ($/m.yr) - Physical Damage & Econ Loss','Risk ($/m.yr) - Evironmental Damage','Risk ($/m.yr) - Regulatory Impact','Risk ($/m.yr) - Customer Satisfaction','Risk ($/m.yr) - Corporate Image','nmStartMeter','nmEndMeter']    
def export_file(merged):

    #PIM.to_excel(r".\PIM.xlsx")
    merged[exportcolumns].to_csv(r".\merged.csv",mode='w',  index = False, encoding = 'cp1252')
    agg.to_csv(r".\agg.csv",mode='w',  index = False, encoding = 'cp1252')
    wa.to_csv(r".\wa.csv",mode='w',  index = False, encoding = 'cp1252')
    return

def main(bigmerged):
    
    PIM, IRIS =  read_file()
    groupedPIM = PIM.groupby('idSegment')
    groupedIRIS = IRIS.groupby('idSegment')
    for name, group in groupedPIM:
        merged = merge_file(groupedPIM.get_group(name),groupedIRIS.get_group(name))
        bigmerged = bigmerged.append(merged)
    export_file(merged)
    return 
    
main()    