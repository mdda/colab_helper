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

def download(url, base_path='.', uncompress=True, dest_path=''):
  if not os.path.exists(base_path):
    os.makedirs(base_path)

  # Does the dest_path have stuff in it?
  dest_path_full = os.path.join(base_path, dest_path) 
  
  if not os.path.isdir( dest_path_full ) or len(os.listdir( dest_path_full ))<=2:
    # Nothing in dest_path_full - does the tar/zip file exist?
    
    #url_path = urllib.parse.urlparse( url ).path
    url_path = requests.utils.urlparse( url ).path
    url_file = os.path.basename(url_path)

    urlfilepath = os.path.join(base_path, url_file)
    if not os.path.isfile(urlfilepath):
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
    
    if uncompress:
      url_file_l = url_file.lower()
      
      if url_file_l.endswith('.zip'):
        print("Uncompressing .zip : '%s'" % (urlfilepath,))
        import zipfile
        zipfile.ZipFile(urlfilepath, 'r').extractall(dest_path_full)
      
      if url_file_l.endswith('.tar'):
        print("Unwrapping .tar : '%s'" % (urlfilepath,))
        import tarfile
        tarfile.open(urlfilepath, 'r:').extractall(dest_path_full)
        #shutil.move(os.path.join(models_dir, models_orig_dir), os.path.join(models_dir, models_here_dir))
      
      if url_file_l.endswith('.tar.gz') or url_file_l.endswith('.tgz'):
        print("Uncompressing .tar.gz : '%s'" % (urlfilepath,))
        import tarfile
        tarfile.open(urlfilepath, 'r:gz').extractall(dest_path_full)
        #shutil.move(os.path.join(models_dir, models_orig_dir), os.path.join(models_dir, models_here_dir))


      if len(os.listdir( dest_path_full ))>2:
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
