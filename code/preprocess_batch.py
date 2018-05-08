"""
map the class ID to the image ID and resize the images to corresponding files automatically
process in batches, easy for the following steps
"""
import pandas as pd
import os
from PIL import Image

# df as dataframe
# get the classes we wanted to classify
def get_class(df, column_ID, cls_num):
    # get the top #cls_num class names and save them into cls list 
    freq = df.groupby(column_ID).size().sort_values(ascending=False)
    cls_name = freq.head(cls_num).keys()
    cls_list = []
    for i in range(cls_num):
        cls_list.append(cls_name[i])
    return cls_list

# make directory at the root path according to the class
def make_dir(root_path, cls_list):
    directories = []
    for folder in cls_list:
        directory = os.path.join(root_path, str(folder))
        directories.append(directory)
        if not os.path.exists(directory):
            os.mkdir(directory)
    return directories

# retrieve the class according to the column_ID
# image_id is the column name of the image, column_ID is the column name of the class of the image
def get_class_by_image_name(df, image_id, column_ID, file_name):
    # locate the row of the image_id
    row = df.loc[df[image_id] == int(file_name)]
    # retrieve the value of the row in column column_ID
    class_name = row.iloc[0][column_ID]    
    # return class
    return class_name

# resize the image and save it to destination
# w is width, h is for height, and resize it according to algorizm Image.ANTIALIAS
def imageResize(destination, source, file_name, w, h):  
    img = Image.open(source)  
    new_img= img.resize((w, h),Image.ANTIALIAS) 
    new_img.save(destination+'/'+file_name, quality=100)

# main
if __name__ == "__main__":
    # define the variables here
    csv_file_path = '/Users/jiahuiwu/Desktop/DL_project/Pictures.csv'
    headers = ['UID', 'ID1', 'Cls1', 'ID2', 'Cls2', 'ID3', 'Cls3']
    column_ID = 'Cls1'
    image_id = 'UID'
    cls_num = 10
    file_num_per_class = 100
    root_path = '/Users/jiahuiwu/Desktop/DL_project'
    data_path = []
    cls_batches = []
    batch_size = 2
    w = 100
    h = 80
    stop = False

    # create data_path according to batch_size
    for i in range(batch_size):
        data_path.append('batch{}'.format(i + 1))

    # get the top ten class list according to column 2 of the csv file
    df = pd.read_csv(csv_file_path, names=headers)
    cls_list = get_class(df, column_ID, cls_num)

    # deep copy the cls_list into cls_batches for conditional check
    for i in range(batch_size):
        curr_cls = []
        for j in range(len(cls_list)):
            curr_cls.append(cls_list[j])
        cls_batches.append(curr_cls)

    # make directory according to the class in batches
    batch_paths = make_dir(root_path, data_path)

    # populate the class folders in batches
    for i in range(batch_size):  
        make_dir(batch_paths[i], cls_list)        

    # get the source directory
    source_list = []
    for i in range(1, 10):
        directory = os.path.join(root_path, 'picture{}'.format(i))
        source_list.append(os.listdir(directory))

    # process the image and save the image into new directory
    for i in range(1, 10):
        if not stop:
            source_path = os.path.join(root_path, 'picture{}'.format(i))
            for file_name in source_list[i - 1]:
                if not stop:
                    name, extension = os.path.splitext(file_name)
                    curr_class = get_class_by_image_name(df, image_id, column_ID, name)
                    for j in range(batch_size):
                    # break the loop if all batches are processed 
                        if len(cls_batches[batch_size - 1]) == 0:
                            stop = True
                            break
                    # if we current image belongs to the class that needs to be resized
                        if curr_class in cls_batches[j] and extension == '.jpg':
                            source = os.path.join(source_path, str(file_name))
                            destination = os.path.join(batch_paths[j], str(curr_class))
                            file_count = len(os.listdir(destination))
                            if file_count < file_num_per_class:
                                imageResize(destination, source, file_name, w, h)
                        # if each class has enough files, stop copy, remove the class
                            else:
                                cls_batches[j].remove(curr_class)
                        



