import glob
import os


def delfile(path):
    # read all the files under the folder
    file_names = glob.glob(path + r'\*')
    for fileName in file_names:
        try:
            # delete file
            os.remove(fileName)
        except:
            try:
                # delete empty folders
                os.rmdir(fileName)
            except:
                # Not empty, delete files under folders
                delfile(fileName)
                # now, folders are empty, delete it
                os.rmdir(fileName)


def create_file(path):
    if os.path.exists(path):
        delfile(path)
    else:
        os.makedirs(path)
