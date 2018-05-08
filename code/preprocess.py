"""
map the class ID to the image ID and resize the images to corresponding files automatically
It divides into training and testing dataset
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
    cls = []
    for i in range(cls_num):
        cls.append(cls_name[i])
    return cls

# make directory at the root path according to the class
def make_dir(root_path, cls):
    directories = []
    for folder in cls:
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

if __name__ == "__main__":
    # define the variables here
    csv_file_path = '/Users/jiahuiwu/Desktop/DL_project/Pictures.csv'
    headers = ['UID', 'ID1', 'Cls1', 'ID2', 'Cls2', 'ID3', 'Cls3']
    column_ID = 'Cls1'
    image_id = 'UID'
    cls_num = 10
    file_num_per_class_training = 1000
    file_num_per_class_testing = 200
    root_path = '/Users/jiahuiwu/Desktop/DL_project'
    data_path = ['training_data', 'testing_data']
    testing_file_phase = False
    w = 100
    h = 80

    # get the top ten class list according to column 2 of the csv file
    df = pd.read_csv(csv_file_path, names=headers)
    cls = get_class(df, column_ID, cls_num)

    cls_training = cls
    # deep copy the cls list into cls_testing for conditional check
    cls_testing = []
    for i in range(len(cls)):
        cls_testing.append(cls[i])

    file_num_per_class = file_num_per_class_training
    # make directory according to the class in training and testing directory
    training_path, testing_path = make_dir(root_path, data_path)

    # populate the class folders in training path and testing path
    make_dir(training_path, cls_training)
    make_dir(testing_path, cls_testing)

    # get the source directory
    source_list = []
    for i in range(1, 10):
        directory = os.path.join(root_path, 'picture{}'.format(i))
        source_list.append(os.listdir(directory))

    # process the image and save the image into new directory
    for i in range(1, 10):
        source_path = os.path.join(root_path, 'picture{}'.format(i))
        for file_name in source_list[i - 1]:
            name, extension = os.path.splitext(file_name)
            curr_class = get_class_by_image_name(df, image_id, column_ID, name)
            if len(cls_training) == 0:
                cls = cls_testing
                testing_file_phase = True
            # break the loop if the testing class are all satisfied
            if len(cls_testing) == 0:
                break
            if curr_class in cls and extension == '.jpg':
                source = os.path.join(source_path, str(file_name))
            # save the images to the training folder
                if not testing_file_phase:
                    destination = os.path.join(training_path, str(curr_class))
                else:
                    file_num_per_class = file_num_per_class_testing
                    destination = os.path.join(testing_path, str(curr_class))
                file_count = len(os.listdir(destination))
                if file_count < file_num_per_class:
                    imageResize(destination, source, file_name, w, h)
            # if each class has enough files, stop copy, remove the class
                else:
                    cls.remove(curr_class)



            