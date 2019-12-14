import os

import numpy as np
import pandas as pd 

#print("Hello from tb_lite")

# https://github.com/tensorflow/tensorboard/
#    blob/master/tensorboard/backend/event_processing/event_file_loader.py
import tensorboard.backend.event_processing.event_file_loader as event_file_loader



def pytorch_summary(model):
  size_tot=0
  for name, param in model.named_parameters():
    dims=list(param.size())
    size=np.prod(dims)
    print(f"{size:10,d} : {name:50s} = {dims}")
    size_tot+=size
  print(f"{size_tot:10,d} : TOTAL")

def load_events(base_path, series, as_list=False):
  p_series = os.path.join(base_path, series)
  agg=[]
  for f in os.listdir(p_series):
    #print(f)
    efl = event_file_loader.EventFileLoader(os.path.join(p_series, f))
    
    for i, e in enumerate(efl.Load()):
      #if i>=5:break
      #print(i, e)
      ts=e.wall_time
      step=e.step
      summary_value = e.summary.value
      if len(summary_value)>0:
        # https://developers.google.com/protocol-buffers/docs/pythontutorial
        #print(f"Found {type(v)}")
        #print(f"Found {summary_value[0].simple_value}")
        sv = summary_value[0].simple_value
        #print(ts,step,sv)
        agg.append( (ts,step,sv) )
  if as_list: 
    return agg
  return pd.DataFrame(agg, columns=['ts', 'step', 'value'])
  
def thinned_out(df_orig, x='step', y='value', buckets=1000, min_max=False):
  df = pd.DataFrame()
  # https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.qcut.html
  # https://stackoverflow.com/questions/10373660/converting-a-pandas-groupby-output-from-series-to-dataframe
  cats = df_orig.groupby( pd.qcut(df_orig[x], buckets), 
                         as_index=False ) # otherwise 'step' is a new column itself
  
  # These are the new 'x' values
  df[x] = cats.max()[x]
  
  # These are the new 'y' values
  df['mean']  = cats.mean()[y]
  df['std']   = cats.std()[y]
  if min_max:
    df['upper'] = cats.max()[y]
    df['lower'] = cats.min()[y]
  else:
    df['upper'] = df['mean']+df['std']
    df['lower'] = df['mean']-df['std']
  return df

"""
# https://towardsdatascience.com/its-2019-make-your-data-visualizations-interactive-with-plotly-b361e7d45dc6
! pip install plotly_express
"""
def init_plotly():
  try:
    import plotly_express as pltx
  except e:
    import subprocess
    subprocess.call("pip install plotly_express".split())
    
  import plotly_express as pltx
  
  import plotly.offline as plotly_offline
  plotly_offline.init_notebook_mode(connected=False)
  
  print("Plotly running offline")
