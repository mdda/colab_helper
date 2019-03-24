import os

def status():
  print("Doing fine")
  
def gdrive_mount(point='gdrive', link='my_drive'):
  from google.colab import drive
  drive.mount(point)
  if link is not None:
    import subprocess
    # ! ln -s "gdrive/My Drive" my_drive 
    subprocess.run(["ln", "-s", point+"/My Drive", link,])
    print("'%s' mounted as '%s'" % (point+"/My Drive", link,))
