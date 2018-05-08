"""
Purppose: to get the extensions and dimensions of the dataset
"""

import cv2
import glob
import os

arr = []
for i in range(1, 10):
    arr.append(os.listdir('/Users/jiahuiwu/Desktop/DL_project/picture{}'.format(i)))
extensions = {}
dimensions = {}
for i in range(9):
    for img in glob.glob("/Users/jiahuiwu/Desktop/DL_project/picture{}/*.jpg".format(i + 1)):
        n = cv2.imread(img)
        dimension = n.shape[:2] 
        if dimension not in dimensions.keys():
            dimensions[dimension] = 1
        else:
            dimensions[dimension] += 1

    for file in arr[i]:
        name, extension = os.path.splitext(file)
        if extension not in extensions.keys():
            extensions[extension] = 1
        else:
            extensions[extension] += 1

print(extensions)
print(dimensions)