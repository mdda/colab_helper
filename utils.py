import os, sys
import subprocess

#import urllib, shutil
import requests, shutil

def status():
  print("Doing fine")
  
def gdrive_mount(point='gdrive', link='my_drive'):
  from google.colab import drive
  drive.mount(point)
  if link is not None:
    # ! ln -s "gdrive/My Drive" my_drive 
    subprocess.run(["ln", "-s", point+"/My Drive", link,])
    print("'%s' mounted as '%s'" % (point+"/My Drive", link,))

def download(url, base_path='.', unwrap=True, dest_path=None):
  if not os.path.exists(base_path):
    os.makedirs(base_path)

  # What type of file are we expecting
  url_path = requests.utils.urlparse( url ).path
  url_file = os.path.basename(url_path)
  urlfilepath = os.path.join(base_path, url_file)
  url_file_l = url_file.lower()
  
  is_zip, is_tar, is_tgz = url_file_l.endswith('.zip'), False, False
  if url_file_l.endswith('.tar'): 
    is_tar=True
  if url_file_l.endswith('.tar.gz') or url_file_l.endswith('.tgz'):
    is_tar, is_tgz=True, True

  fetch_url=True
  if os.path.isfile(urlfilepath):
    fetch_url=False  # No need to fetch
  
  dest_path_full=base_path  # default - but can't check for unwrapping
  if dest_path is not None:
    dest_path_full = os.path.join(base_path, dest_path) 
    
    if is_zip or is_tar: # Unwrappable
      # Does the dest_path have stuff in it?
      if os.path.isdir( dest_path_full ) and len(os.listdir( dest_path_full ))>=2:
        print("'%s' already has files in it" % (dest_path_full,))
        return
        
  if not fetch_url:
    print("'%s' already present" % (urlfilepath,))
    pass
    
  else:
    # Download the missing file
    #urllib.request.urlretrieve(url, urlfilepath)
    response = requests.get(url, stream=True)
    if response.status_code == requests.codes.ok:
      print("Downloading %s" % (url,))
      with open(urlfilepath, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    else:
      print("FAILED TO DOWNLOAD %s" % (url,))
      return
  
  if unwrap and (is_zip or is_tar):
    if is_zip:
      print("Uncompressing .zip : '%s'" % (urlfilepath,))
      import zipfile
      zipfile.ZipFile(urlfilepath, 'r').extractall(dest_path_full)
    
    if is_tar:
      if is_tgz: 
        tar_flags='r:gz'
        print("Uncompressing .tar.gz : '%s'" % (urlfilepath,))
      else:
        tar_flags='r:'
        print("Unwrapping .tar : '%s'" % (urlfilepath,))
      import tarfile
      tarfile.open(urlfilepath, tar_flags).extractall(dest_path_full)
      #shutil.move(os.path.join(models_dir, models_orig_dir), os.path.join(models_dir, models_here_dir))

    if dest_path is not None and len(os.listdir( dest_path_full ))>2:
      # Something appeared in dest_path : no need for unwrapped file
      print("Deleting '%s'" % (urlfilepath,))
      os.unlink(urlfilepath)

  if len(os.listdir( dest_path_full ))>2:
    print("'%s' now contains data" % (dest_path_full,))  

"""
if not os.path.isfile( os.path.join(tf_zoo_models_dir, 'models', 'README.md') ):
    print("Cloning tensorflow model zoo under %s" % (tf_zoo_models_dir, ))
    !cd {tf_zoo_models_dir}; git clone https://github.com/tensorflow/models.git

sys.path.append(tf_zoo_models_dir + "/models/research/slim")
"""
