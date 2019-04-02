import os
import glob
import inspect
import tarfile
from gmicpy  import  gmic_call as gmic
from gmicpy  import  reset
from gmicpy  import  _init_gmic_instance
from gmicpy  import add_commands,path_rc,gmic_version
_init_gmic_instance()
del _init_gmic_instance
#"%supdate%u.gmic"
modulepath=os.path.abspath(inspect.getfile(inspect.currentframe()))
moduledir=os.path.join(os.path.dirname(modulepath))
with tarfile.open(os.path.join(moduledir,"include.tar.bz2"), "r") as tar:
    for tarinfo in tar:
        if tarinfo.name.endwith(".gmic"):
            print("parsing:",tarinfo.name)
            with tar.extractfile(tarinfo) as f:
                add_commands(f.read)


del tarinfo
del tar



name = "gmic"
