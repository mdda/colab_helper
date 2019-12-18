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


def get_experiments_and_series(base):
  return


def load_events(base, experiment, series):
  p_series = os.path.join(base, experiment, series)
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
        agg.append( {'ts':ts,'step':step, summary_value[0].tag:summary_value[0].simple_value,} )
    
  df = pd.DataFrame(agg)  # , columns=['ts', 'step', 'value']
  # https://www.science-emergence.com/Articles/How-to-add-metadata-to-a-data-frame-with-pandas-in-python-/
  df.base=base
  df.experiment=experiment
  df.series=series
  return df
  
def ranges(df_orig, x='step', y='value', buckets=1000, min_max=False):
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
  
  df['mid']   = df['mean']
  if min_max:
    df['upper'] = cats.max()[y]
    df['lower'] = cats.min()[y]
  else:
    df['upper'] = df['mean']+df['std']
    df['lower'] = df['mean']-df['std']

  # Store the inputs as metadata on the thinned set
  df.x         = x
  df.y         = y
  df.min_max   = min_max
  df.base      = getattr(df_orig, 'base', '')
  df.experiment= getattr(df_orig, 'experiment', '')
  df.series    = getattr(df_orig, 'series', '')
  return df

"""
# https://towardsdatascience.com/its-2019-make-your-data-visualizations-interactive-with-plotly-b361e7d45dc6
! pip install plotly_express
"""
init_plotly_done=False
def init_plotly():
  global init_plotly_done
  if init_plotly_done: return
  
  try:
    import plotly_express as pltx
  except e:
    import subprocess
    subprocess.call("pip install plotly_express".split())
    
  import plotly_express as pltx
  
  import plotly.offline as plotly_offline
  plotly_offline.init_notebook_mode(connected=False)
  
  print("Plotly running offline")
  init_plotly_done=True


def series_fig(
    df_arr,    # Array of dataframes (will be thinned if required)
    min_max=False,                    # If passed non-thinned dataframe 
    x='step',  # What the x axis is called in dataframes (might be 'ts', for instance) - now retrieved from thinned df metadata
    y='value', # What the y axis is called in the dataframes
    xrange=None, yrange=None,         # User defined axis range ([low, high])
    ylog=False,                       # Do log plot
    point_format='(%{x:s},%{y:s})',   # Can include python formatting information
    fig=None,  # Can pass in a fig to add on to it
  ):
  if not init_plotly_done: init_plotly()
  
  import plotly_express as pltx
  import plotly.graph_objects as pltgo
  
  if fig is None:
    fig = pltgo.Figure()

  #matplotlib.colors.to_rgb('yellow')  -> (1.0, 1.0, 0.0)
  
  # Choosing a good sequence of different colours isn't going to be so easy...
  # http://colorbrewer2.org/#type=qualitative&scheme=Dark2&n=5
  
  # https://www.chronicle.com/blogs/profhacker/color-blind-accessible-figures/59189 :: Okabe and Ito :
  cmap=[ (0,0,0), (230,159,0), (86,180,224), (0,158,115), (240,228,66), (0,114,178), (213,94,0), (204,121,167) ]
  def rbga(c,alpha=1.0):
    ret=f'rgba({c[0]},{c[1]},{c[2]},{alpha})'
    #print(ret)
    return ret
  
  for i, df in enumerate(df_arr):
    if getattr(df, 'x', None) is None:
      df = ranges(df, y=y, min_max=min_max, )
    
    x=getattr(df, 'x', 'step')
    c=cmap[i % len(cmap)]
    
    hovertemplate=(
      point_format+"<br>"
      #+"2019-12-13_01-slim-decoder-from0<br>"
      +getattr(df, 'experiment', '')+"<br>"
      #+"ferts-fert-loss"
      +getattr(df, 'series', '')+"<br>"
      +"<extra></extra>"
    )
    
    # https://plot.ly/python-api-reference/generated/plotly.express.line.html#plotly.express.line
    # https://plot.ly/python/hover-text-and-formatting/
    
    #fig = pltx.line(df, x='step', y='mean', range_y=[0.8,1.6])
    fig.add_trace(pltgo.Scatter(x=df[x], y=df['mid'],  # +0.2
                  fill=None, mode='lines', 
                  #line_color='blue',
                  line_color=rbga(c),
                  #name="2019-12-13_01-slim-decoder-from0.ferts-fert-loss", 
                  name= getattr(df, 'experiment', '')+" "+getattr(df, 'series', ''),
                  hovertemplate=hovertemplate,
                  ))
    #fig.add_scatter(x=df['step'], y=df['mean_plus'], mode='lines')

    # https://plot.ly/python/line-charts/#filled-lines
    # https://plot.ly/python/filled-area-plots/
    fig.add_trace(pltgo.Scatter(x=df[x], y=df['upper'],
                  mode='lines', fill=None, 
                  fillcolor=rbga(c, alpha=0.2),
                  #line_color='rgba(255,255,255,0)',  # transparent
                  line_color=rbga(c, alpha=0.2),
                  #hovertemplate=point_format+"<br><extra></extra>",
                  hovertemplate=hovertemplate,
                  showlegend=False,  )) 
    fig.add_trace(pltgo.Scatter(x=df[x], y=df['lower'],
                  mode='lines', fill='tonexty', # fill area between trace0 and trace1
                  #opacity=0.50,
                  fillcolor=rbga(c, alpha=0.2),
                  #line_color='rgba(255,255,255,0)',  # transparent
                  line_color=rbga(c, alpha=0.2),
                  #hovertemplate=point_format+"<br><extra></extra>",
                  hovertemplate=hovertemplate,
                  showlegend=False,  
                  ))  

  #fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
  
  if xrange is not None:
    fig.update_xaxes(range=xrange)
  if yrange is not None:
    fig.update_yaxes(range=yrange)

  if ylog:
    # https://plot.ly/python/log-plot/
    fig.update_layout(yaxis_type="log")

  #https://plot.ly/python/reference/#layout-legend  
  fig.update_layout(legend= dict(x=-0.1, y=1.02, yanchor='bottom', ))
  
  return fig
