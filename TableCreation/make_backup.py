from django.core.management import call_command
from django.conf import settings
import datetime,os,sys


# Create DB Backup while migrations command is running 
def createDBBackup():
    check = True
    if not os.path.isdir(str(settings.BASE_DIR)+"/DBBackup"):
        os.makedirs(str(settings.BASE_DIR)+"/DBBackup")
    try:
        d_date = datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        if not os.path.isfile(str(settings.BASE_DIR)+'/DBBackup/'+str(d_date)+".json"):
            with open(str(settings.BASE_DIR)+'/DBBackup/'+str(d_date)+".json", "w", encoding="utf-8") as fp:
                call_command("dumpdata", format="json",indent=4, stdout=fp)
            fp.close()
    except BaseException as error:
        print('An exception occurred from DB Backup: {}'.format(error))
        check = False
    return check