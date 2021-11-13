"""
streamlit ihm
"""
import glob
import json
import os
import time
import cv2
import pandas as pd
import streamlit as st
import numpy as np
from streamlit.caching import cache
from model.game import Game
import run
from streamlit import caching
import skimage

st.set_page_config(layout="wide")

dict_color = {
    'red': [255,0,0],
    'orange' : [255,165,0],    
    'green' : [0,255,0],
    'blue' : [0,0,255] ,
    'indigo' : [75,0,130],
    'violet' : [238,130,238],
    'yellow' : [255,255,0],
    }
PAS  = 40
RUN_OK = False
LAP = 0

@cache(allow_output_mutation=True)
def results_load():
    file = "results.csv"
    if os.path.isfile(file) :
        results = pd.read_csv(file)
        #print(results)
        results['id'] = results.index.astype(str) + '_(' + results.nb_lap.astype(str) + ')'
        #print('results shape : ' , results.shape)
        print('results_load')
    else :
        results = []    
    return results

@cache(allow_output_mutation=True)
def open_json(file):
    print ('open_json', file)
    with open(file) as f:
        data = json.load(f)
        return data

def array_(data, lap):
    arr = np.ones((10,10,3))
    for n, robot in enumerate(data['robots']):
        pos = robot[lap]
        color = list(dict_color.values())[n]
        #color.append(255)
        color = (np.array(color)/255)
        #color = np.append(color, 1)
        arr[pos[0],pos[1],:] = color
    #arr = cv2.resize(arr, dsize=(10*PAS, 10*PAS), interpolation=cv2.INTER_NEAREST)
    arr = skimage.transform.resize(arr, (10*PAS, 10*PAS), order =0)
    arr[::PAS,:,:]=0
    arr[:,::PAS,:]=0
    return arr

@cache
def loadimage():
    #img = cv2.imread('victory.png') 
    #img = cv2.resize(img, dsize=(PAS, PAS), interpolation=cv2.INTER_NEAREST)
    #img = cv2.normalize(img, img, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    img = skimage.io.imread("victory.png")
    img = skimage.transform.resize(img, (PAS, PAS), order =0)
    img = img[:,:,:3]
    
    return img

def parse_(arr, pos, img):
    mask = img > 0
    x_pos, y_pos = pos
    arr[x_pos*PAS:(x_pos+1)*PAS,y_pos*PAS:(y_pos+1)*PAS,:][mask]=img[mask]
    return arr

def run_env():
    RUN_OK = True    
    game = Game()
    game.run()    
    caching.clear_cache()
    results = results_load()
    print('run_env', results.iloc[-1].tolist())    
    return results

def delete(results):
    print('delete')
    for result in results.filename.tolist() : 
            os.remove(result) 
    os.remove('results.csv')
    caching.clear_cache()
    results = results_load()
    return results

results = results_load()
goal = loadimage()
left_column, right_column = st.beta_columns((1,3))
#placeholder = st.sidebar.empty()

if st.sidebar.button('RUN') & (not RUN_OK):
    results = run_env()
    st.write("finish", results.iloc[-1].nb_lap, 'laps')

if st.sidebar.button('delete'):
    results = delete(results)
  
if len(results) > 0:
    ID = st.sidebar.radio('list_id', results.id, index = len(results)-1)
    dfx = results[results.id == ID].iloc[0]

    FILE = dfx.filename        
    LAP_MAX = int(dfx.nb_lap+1)

    data = open_json(FILE)
    left_column.write(data['main'])

    slider_ph = right_column.empty()
    LAP = slider_ph.slider("slider", 0, LAP_MAX-1)
    arr  = array_(data, LAP)
    arr  = parse_(arr,data['main']['goal'], goal)
    grid = right_column.image(arr, width = 10*PAS, output_format = 'PNG')

    if right_column.button('animate') & (LAP_MAX-1 > 0):
        print("animate")
        for x in range(LAP_MAX-1):
            LAP = slider_ph.slider("slider", 0, LAP_MAX-1, LAP + 1, 1)
            arr  = array_(data, LAP)
            arr  = parse_(arr,data['main']['goal'], goal)
            grid.image(arr, width = 10*PAS, output_format = 'PNG')
            time.sleep(.1)
