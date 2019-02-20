import numpy as np
from gmicpy  import  gmic_call


def test_gmic_base():
    res=gmic_call("testimage2d 512",[],[])
    assert res[0].shape== (512, 512, 1, 3)
   


def test_gmic_alloc_small():
    img=[np.random.normal(size=(10,10,1,3))]
    gmic_call("srand 100 360,240,900,3",img,[])
    
    
def test_gmic_alloc_medium():
    img=[np.random.normal(size=(320,320,1,3))]
    gmic_call("srand 100 360,240,900,3",img,[])    

def test_gmic_alloc_large():
    img=[np.random.normal(size=(4096,4096,1,3))]
    gmic_call("",img,[])   
    
def test_gmic_alloc_large_direct():
    res=gmic_call(" 4096,4096,1,3  ",[],[])
    assert res[0].shape== (4096,4096,1,3)

    
    
    
    
