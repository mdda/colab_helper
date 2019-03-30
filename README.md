# colab-helper
Utility files to help set up colab for experimentation + development

The idea is to let you :

```
! rm -rf colab_helper
! git clone https://github.com/mdda/colab_helper
from colab_helper import utils as chu
```

at the top of a notebook, and have a bunch of useful stuff ready-to-go 
(optionally without flooding your namespace with stuff).


### Google Drive helper

This mounts your Google Drive at (per convention) `~/gdrive` but also optionally
adds a link, so that you can use a path that doesn't need the awkard space character
introduced by 'My Drive' :

```
chu.gdrive_mount(point='gd', link='mgd')
! ls -l mgd/*
```

### Downloader/Unwrapper

This just cleanly downloads data (unwrapping by default), without downloading
(or unwrapping) when the required files are already present.

Single file (no unwrap required): 
```
chu.download('http://redcatlabs.com/'
             +'downloads/deep-learning-workshop/notebooks/data/RNN/'
             +'glove.first-100k.6B.50d.txt')
```

More complex `.tar.gz` example (the `dest_path` parameter allows it to check on whether the 
unwrapped files have appeared in a particular directory) :
```
chu.download('http://www.openslr.org/'
             +'resources/1/waves_yesno.tar.gz', 
             dest_path='waves_yesno')
```

### Kaggle Credentials helper

Generate the `kaggle.json` file and upload it to Colab, 
or just use your `username` and `key` in-line :

```
! pip install kaggle
chu.kaggle_credentials(file='./kaggle.json')
```

Then you can access the Kaggle CLI :

```
# Description page : https://www.kaggle.com/ronitf/heart-disease-uci
! kaggle datasets download ronitf/heart-disease-uci
```