#!/system/bin/sh
#/system/bin/ps aux
export ANDROID_ROOT=/system/sdcard
export PYTHONHOME=/system/data/data/org.acestream.engine/files/python
export PYTHONPATH=/system/data/data/org.acestream.engine/files/python/lib/python2.7/lib-dynload:/system/data/data/org.acestream.engine/files/python/lib/python2.7
export PATH=$PYTHONHOME/bin:$PATH
export LD_LIBRARY_PATH=/system/data/data/org.acestream.engine/files/python/lib:/system/data/data/org.acestream.engine/files/python/lib/python2.7/lib-dynload
/system/data/data/org.acestream.engine/files/python/bin/python
