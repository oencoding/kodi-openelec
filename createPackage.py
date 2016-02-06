import time
import os
import tarfile
import shutil

shutil.rmtree("OUTPUT")
current_time = time.strftime("%Y%m%d%H%M")
path = "OUTPUT/" + current_time + "/storage"
os.makedirs(path)
my_file = open(path+ "/test.txt", "w")
my_file.write("Hello")
my_file.close()
os.chdir("OUTPUT")
tar = tarfile.open(current_time + ".tar","w")
tar.add(current_time, True)
tar.close()

