import os
import shutil
import argparse
import sys
import math
import datetime
# find the current directory using below logic
"""
/*
current_directory = os.getcwd()
print(current_directory)
*/
"""

current_directory = r"C:\Users\vthapan\1afile"


def organizeByExtension(path):
    all_files = os.listdir(path)
    all_fext = []
#split all file extensions from the dir
    for f in all_files:
        _, fext = os.path.splitext(f)
        if fext not in all_fext:
            all_fext.append(fext)
#create all dirs to organise files
    for ext in all_fext:
        if ext:
            os.mkdir(os.path.join(path, ext))
#move all files to their respective dirs
    for f in all_files:
        _, ext = os.path.splitext(f)
        old_path = os.path.join(path, f)
        new_path = os.path.join(path, ext, f)
        os.rename(old_path, new_path)
    


#organize_by_extention(directory)



def organizeBySize(path):
    files = os.listdir(path)
    file_size1 = {}
    for i in files:
        file_size1[i] = os.stat(os.path.join(path, i)).st_size
    sorted_file = sorted(file_size1.items(), key=lambda x: x[1])
    file_size0 = []
    size_types = []
    for i in sorted_file:
        f1 = (os.stat(os.path.join(path, i[0])).st_size)
        f2 = convert_size(f1)
        f3 = str(f2).split("_")
        if f3 == [] or f3 == ["0B"]:
            pass
        else:
            file_size0.append(f3)
    types = []
    sub = "."
    for i in sorted_file:
        if sub in i[0]:
            a1 = i[0][::-1].find(".")
            a2 = i[0][-a1:]
            if a2 not in types:
                types.append(a2)

    # folder creation according to size
    for i in file_size0:
        if i[1] not in size_types:
            size_types.append(i[1])
    for i in size_types:
        for k in file_size0:
            if k[1] == i and int(k[0]) < 50:
                if not os.path.exists(os.path.join(path, "FilesLessThan50"+k[1])):
                    os.mkdir(os.path.join(path, "FilesLessThan50"+k[1]))
            elif k[1] == i and int(k[0]) > 50:
                if not os.path.exists(os.path.join(path, "FilesMoreThan100"+k[1])):
                    os.mkdir(os.path.join(path, "FilesMoreThan100"+k[1]))

    # move files to their respective folders
    new_files = [file for file in os.listdir(
        path) if os.path.isfile(os.path.join(path, file))]
    f = [f for f in new_files if checkFile(f)==False]
    for i in f:
        size_new = convert_size(os.stat(os.path.join(path, i)).st_size)
        size_new = size_new.split("_")
        if int(size_new[0]) < 50:
            shutil.move(os.path.join(path, i),
                        os.path.join(path, "FilesLessThan50"+size_new[1]))
        else:
            shutil.move(os.path.join(path, i),
                    os.path.join(path, "FilesMoreThan100"+size_new[1]))
    print("File segrigation is Completed based on Size")

# below function converts bytes to their readable size (ex: 1024b=1kb)
def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s_%s" % (round(s), size_name[i])

# this function protects current script from being moved with other files
def checkFile(filename):
        d = os.path.basename(__file__)
        if filename==d:
            return True
        return False


#organizeBySize(directory)

def organizeByDate(path):
    files = [file for file in os.listdir(
        path) if os.path.isfile(os.path.join(path, file))]
    f = [f for f in files if checkFile(f)==False]
    for i in f:
        mtime = (os.stat(os.path.join(path, i)).st_atime)
        timestamp = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
        cur_date = datetime.datetime.now().strftime('%Y-%m-%d')
        d1 = datetime.date(int(timestamp[:4]), int(
            timestamp[5:7]), int(timestamp[8:]))
        d2 = datetime.date(int(cur_date[:4]), int(
            cur_date[5:7]), int(cur_date[8:]))
        d3 = str(d2-d1)
        d4 = d3.split(",")[0]
        if d4[-4:]=="days":
            if int(d3[:-14]) < 10:
                if not os.path.exists(os.path.join(path, "Files Less than 2 Days")):
                    os.mkdir(os.path.join(path, "Files Less than 2 Days"))
                shutil.move(os.path.join(path, i), os.path.join(
                    path, "Files Less than 2 Days"))
            elif int(d3[:-14]) < 20:
                if not os.path.exists(os.path.join(path, "Files Less than 5 Days")):
                    os.mkdir(os.path.join(path, "Files Less than 5 Days"))
                shutil.move(os.path.join(path, i), os.path.join(
                    path, "Files Less than 5 Days"))
            else:
                if not os.path.exists(os.path.join(path, "Files More than 10 Days")):
                    os.mkdir(os.path.join(path, "Files More than 10 Days"))
                shutil.move(os.path.join(path, i), os.path.join(
                    path, "Files More than 10 Days"))
        else:
            if not os.path.exists(os.path.join(path, "Files Less than 2 Days")):
                os.mkdir(os.path.join(path, "Files Less than 2 Days"))
            shutil.move(os.path.join(path, i), os.path.join(
                path, "Files Less than 2 Days"))
    print("File segrigation is Completed based on Date")

#organizeByDate(directory)


def main():
    
    parser = argparse.ArgumentParser()
    #asking for the path of the directory if not provided by user then it will take current directory as default
    parser.add_argument('--path', default = '.', help = 'Which directory to organize?')

    #asking for the oranize depends like ext or size or date
    parser.add_argument('--o', default = 'extension', help = 'Which Criteria to Organize?', 
                        choices = ['extension', 'size', 'date'])

    args = parser.parse_args()
    path = args.path
    organizeBy = args.o

    if organizeBy =="extension":
        organizeByExtension(path)
    elif organizeBy =="size":
        organizeBySize(path)
    elif organizeBy =="date":
        organizeByDate(path)
    else :
        print(" Input must be either \'extension' or \'size' or \'date' only Please Check ")
    


if __name__ == "__main__":
    main()
