import os, sys
import re

def thin_numbered_files(path, stub='', keep_history=7, keep_recent=3, delete=False):
  # First, figure out which files we're interested in thinning
  stems=dict()
  for f in os.listdir(path):
    if not f.startswith(stub): continue
    stemmed = re.match(r'^(\D*)', f)
    if stemmed is None: continue
    #print(stemmed.group(1), f)
    stem=stemmed.group(1)
    if stem not in stems:  stems[stem]=[]
    stems[stem].append(f)

  stems_by_length = sorted( stems.keys(), key=lambda k: len(stems[k]))
  
  if len(stems_by_length)==0:
    return dict(keep=None, comment='No files found')
    
  # So, we now have a candidate for the longest list of files 
  #   that start with the same non-numeric stem

  full = sorted( stems[ stems_by_length[-1] ] )
  history = full[:-keep_recent]
  
  if len(history)<keep_history:
    return dict(keep=None, comment='Not enough files to thin out')

  # Need to figure out which of these historical ones to keep
  #   Work out a 'score' for each one, based on how 'nice' the number is
  #   Then simply order them and pick the first keep_history

  bonus={'1':10, '2':8, '5':9, '8':5, '25':7, '75':7, '15':6, '12':5, '35':6 }

  scores=dict()
  for f in history:
    #stemmed = re.match(r'^([^0-9]*)([0]*)([1-9][0-9]*?)([0]*)', f)
    stemmed_n = re.match(r'^(\D*)([0]*)(\d*)', f)
    if stemmed_n is None: continue
    num = stemmed_n.group(3)
    stemmed_z = re.match(r'^(.*?)([0]*)$', num)
    if stemmed_z is None: continue
    num, zeros = stemmed_z.group(1),stemmed_z.group(2)

    b=bonus[num]/1. if num in bonus else 0 
    
    # We like lots of zeros, dislike required digits of precision, and have a bonus for preferences
    s = len(zeros)*10 - len(num)*2 + b
    # print(s, num, zeros, f)

    scores[f]=s

  scores_desc = sorted([f for f in scores.keys()], key=lambda f:scores[f], reverse=True)

  #for i,f in enumerate( scores_desc ):
  #  print(f"{i:2d}) {scores[f]:6.2f} :: {f}")
  
  delete_me = scores_desc[keep_history:]
  keep_me = sorted( scores_desc[:keep_history]+full[-keep_recent:] )

  if delete:
    for f in delete_me:
      os.remove( os.path.join(path, f) )
      
  return dict(keep=keep_me, delete=delete_me)
