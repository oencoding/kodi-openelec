import time
import os
import tarfile
import shutil

OUTPUT_DIR = "OUTPUT"
STORAGE = "storage"
#FOLDERS = [".kodi", ".config", ".cache"]
FOLDERS = [".config", ".cache"]

if os.path.isdir(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)

current_time = time.strftime("%Y%m%d%H%M")
path = os.path.join(OUTPUT_DIR,current_time,STORAGE)
os.makedirs(path)

arc_name = current_time + ".tar"
arc_path = os.path.join(OUTPUT_DIR, arc_name)
tar = tarfile.open(arc_path,"w")

print "Creating tar..."
for folder in FOLDERS:
    my_path = os.path.join(STORAGE,folder)
    tar.add(folder,my_path,True)
tar.close()
print "Finished."
print "Tar location: %s" %(arc_path)