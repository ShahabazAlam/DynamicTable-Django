import os,shutil,datetime,traceback,glob
from django.db import models 

def getLastFile(path):
    list_of_files = glob.glob(path+'/*') # * means all if need specific format then *.csv
    if len(list_of_files) > 0:
        latest_file = list_of_files[-1]
        return latest_file
    return False

def removeFilesFromFolder(folder):
    checked = True
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            checked = False
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    return checked


def moveFilesToAnotherFolder(source_dir,target_dir):
    checked = True
    if os.path.isdir(source_dir):
        try:
            d_date = datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
            shutil.copytree(source_dir, target_dir+"/"+d_date+"/")
        except BaseException as error:
            print('An exception occurred Move files: {}'.format(error)) 
            checked = False     
    return checked



def copyFilesToAnotherFolder(source_dir,target_dir,backup=True):
    if os.path.isfile(source_dir):
        try:
            if backup:
                d_date = datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
                shutil.copyfile(source_dir, target_dir+"/"+d_date+'.py')
                checked = True  
            else:
                shutil.copyfile(source_dir, target_dir)
                checked = True  
        except BaseException as error:
            print('An exception occurred Copy files: {}'.format(error)) 
            checked = False   
    else:
        checked = True    
    return checked

def validateFile(temp_model_path):
    with open(temp_model_path) as f:
        source = f.read()
    valid = True
    try:
        exec(source)
        f.close()
    except Exception as e:
        if str(e)[:11] != 'Conflicting':
            valid = False
            traceback.print_exc()  
    return valid