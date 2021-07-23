import json
import os
import shutil
from multiprocessing import Pool

with open('test.txt','w') as f:
    for i in range(1500,1732):
        # print(i)
        f.write(str(i)+'\n')
