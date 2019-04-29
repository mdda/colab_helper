# colab-helper
Utility files to help set up colab for experimentation + development

The idea is to let you :

```
! git clone https://github.com/mdda/colab_helper
from colab_helper import utils as chu
```

at the top of a notebook, and have a bunch of useful stuff ready-to-go 
(you can choose the name under which to import it, 
so as to avoid collisions with your existing code).


### Google Drive helper

This mounts your Google Drive at (per convention) `~/gdrive` but also optionally
adds a link, so that you can use a path that doesn't need the awkard space character
introduced by 'My Drive' :

```
chu.gdrive_mount(point='gdrive', link='my_drive')
! ls -l my_drive/*
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

Then you can access the Kaggle CLI (see also [the Kaggle API docs](https://github.com/Kaggle/kaggle-api)):

```
# Description page : https://www.kaggle.com/ronitf/heart-disease-uci
! kaggle datasets download ronitf/heart-disease-uci
```


### SSH Reverse Proxy

>   This is for *expert use* only.  If you don't know what this is doing, 
>   or how to get it to run, then this isn't something you should be messing with.

>   Note also that this is far more security conscientious than other scripts you might find on the web : 
>   It doesn't allow logins via passwords, for instance, nor execute arbitrary scripts downloaded from a url.

Example use (it will print out the required local `ssh` command) :

```
chu.ssh_reverse_proxy("""
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDEQbFcc8U/XMIUoATs+jGFIPMREgMlsLAnatzcc
OTHERSTUFFOTHERSTUFFOTHERSTUFFOTHERSTUFFOTHERSTUFFOTHERSTUFFOTHERSTUFFOTHERSTUFFOTHERSTUFF
ihku00gbBwSOu2M38GMdGV9qU9XrEkLSjD/1WtzYJZL7buzpitlGlTvhnqQT+t andrewsm@square.herald
""")
```

The `pub_key` field cleans out any line-breaks pasted in from `~/.ssh/id_rsa.pub` for your convenience.  
And, as an aside, there's no problem leaving your public key(s) in the colab file itself, 
since that's not the private key bit (obviously).

Using the `rsync` command given in the output, one can then do a auto-sync-to-colab for
locally edited files (use the `%autoreload 2` [magic](https://ipython.readthedocs.io/en/stable/config/extensions/autoreload.html?highlight=autoreload) to 
transparently have the updated code reloaded as you run the notebook cells) : 

```
while rsync-command-from-colab_helper; do inotifywait -qqre close_write,move,create,delete code/; done
```

