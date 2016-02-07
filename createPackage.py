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

my_file = open(path+ "/test.txt", "w")
my_file.write("Hello")
my_file.close()

arc_name = current_time + ".tar"
arc_path = os.path.join(OUTPUT_DIR, arc_name)
tar = tarfile.open(arc_path,"w")

for folder in FOLDERS:
    my_path = os.path.join(STORAGE,folder)
    tar.add(folder,my_path,True)
tar.close()

