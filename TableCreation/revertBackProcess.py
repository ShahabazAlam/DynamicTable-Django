import os, glob, shutil
from django.conf import settings
from .file_handle import *
from .views import *
from .migrate_action import *
from django.core.cache import cache
from .make_backup import *

def revertBackProcessFunction():
    cache.clear()
    last_model = getLastFile(str(settings.BASE_DIR)+'/ModelsBackup') 
    last_migration = getLastFile(str(settings.BASE_DIR)+'/MigrationsBackup') 
    last_db = getLastFile(str(settings.BASE_DIR)+'/DBBackup') 
    model_path = str(settings.BASE_DIR)+"/TableCreation/models.py"
    migration_folder = str(settings.BASE_DIR)+"/TableCreation/migrations/"
    fp = open(os.path.join(model_path),mode='w')
    fp.truncate()
    fp.close()
    createDBBackup()
    copyFilesToAnotherFolder(last_model,model_path,False)
    return True
