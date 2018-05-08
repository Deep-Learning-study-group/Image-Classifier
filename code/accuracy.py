import os
from tabulate import tabulate

path = "/Users/jiahuiwu/desktop/classifier/scanned/"

# get the path of the directory
table = []
for directory in os.listdir(path):
    if not directory.startswith('.'):
        class_name = directory.lower()
        len_class_name = len(class_name)
        # absolute directory
        directory = os.path.join(path, directory)
        total = len(os.listdir(directory))
        mis_classified = 0
        for file_name in os.listdir(directory):
            name, _ = os.path.splitext(file_name)
            name = name[:len_class_name]
            print(name)
            print(class_name)
            if name != class_name:
                mis_classified += 1
        accuracy = round((total - mis_classified) / total, 2)
        table.append([class_name, accuracy])

print(tabulate(table, headers=['class', 'accuracy']))
