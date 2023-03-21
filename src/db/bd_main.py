from bd_insert import *
import os
import glob

if __name__ == '__main__':
    directory = '../../data/output'
    pattern = '*.json'

    files = glob.glob(os.path.join(directory, pattern))

    for file in files:
        all_insert(file)
        print('----------')
