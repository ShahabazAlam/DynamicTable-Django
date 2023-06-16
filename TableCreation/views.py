from django.db import models
from django.contrib import admin
from django.core.management import call_command
from django.shortcuts import render, redirect
from TableCreation import revertBackProcess
from MainApp.models import *
from django.conf import settings
import os,shutil,datetime


from .create_table import *
from .make_backup import *
from .migrate_action import *
from .file_handle import *
from .revertBackProcess import *

def WriteModel(request):
    try:
        if not os.path.isdir(str(settings.BASE_DIR)+"/ModelsBackup/"):
            os.makedirs(str(settings.BASE_DIR)+"/ModelsBackup/")
    except BaseException as error:
        print('An exception occurred write model ignorable: {}'.format(error))

    createDBBackup()
    key = "Success"
    temp_model_path = os.path.join(settings.BASE_DIR, 'TableCreation/temp_models.py')
    if writeModelFile(temp_model_path):
        if(validateFile(temp_model_path)):
            model_path = os.path.join(settings.BASE_DIR, 'TableCreation/models.py')
            source_path = str(settings.BASE_DIR)+"/TableCreation/models.py"
            target_path = str(settings.BASE_DIR)+'/ModelsBackup'
            if copyFilesToAnotherFolder(source_path,target_path):
                try:
                    writeModelFile(model_path)
                except BaseException as e:
                    print(',,,,,',e)
            else:
                key = 'Failed'
        else:
            key = 'Failed'
    else:
        key = 'Failed'
    if key== "Failed":
        revert_back_model()
    return render(request,'home.html',{'key':key})


def Migrate(request):
    try:
        if not os.path.isdir(str(settings.BASE_DIR)+"/MigrationsBackup/"):
            os.makedirs(str(settings.BASE_DIR)+"/MigrationsBackup/")
    except BaseException as error:
        print('An exception occurred migrate ignorable: {}'.format(error))

    copied = moveFilesToAnotherFolder(str(settings.BASE_DIR)+"/TableCreation/migrations",str(settings.BASE_DIR)+"/MigrationsBackup/")
    if copied:
        writted = False
        try:
            dir_path = str(settings.BASE_DIR)+"/TableCreation/migrations"
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path) 
            if not os.path.isfile(str(settings.BASE_DIR)+"/TableCreation/migrations/__init__.py"):
                with open(str(settings.BASE_DIR)+"/TableCreation/migrations/__init__.py", 'w') as fp:
                    fp.close
            writted = True
        except BaseException as error:
            print('An exception occurred Migrate: {}'.format(error))
        if writted:
            runMigration()  
            key = 'Success'  
        else:  
            key = 'Failed'
    else:
        key = 'Failed'
        
    return render(request,'home.html',{'key':key})


def revert_back_model():
    last_model = getLastFile(str(settings.BASE_DIR) + '/ModelsBackup')
    last_migration = getLastFile(str(settings.BASE_DIR) + '/MigrationsBackup')
    last_db = getLastFile(str(settings.BASE_DIR) + '/DBBackup')
    model_path = str(settings.BASE_DIR) + "/TableCreation/models.py"
    migration_folder = str(settings.BASE_DIR) + "/TableCreation/migrations/"
    fp = open(os.path.join(model_path), mode='w')
    fp.truncate()
    fp.close()
    shutil.copyfile(last_model, model_path)
    return True
def RevertBackToLastStage(request):
    revert_back_model()
    return render(request,'home.html',{'key':'Success'})
