from django.core.management import call_command
from django.db.migrations.executor import MigrationExecutor
from django.db import connections, DEFAULT_DB_ALIAS
import os
from django.conf import settings
import subprocess


def is_database_synchronized(database):
    connection = connections[database]
    connection.prepare_database()
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    return not executor.migration_plan(targets)

def makeMigrationsFolder():
    dir_path = str(settings.BASE_DIR)+"/TableCreation/migrations"
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path) 
    if not os.path.isfile(str(settings.BASE_DIR)+"/TableCreation/migrations/__init__.py"):
        with open(str(settings.BASE_DIR)+"/TableCreation/migrations/__init__.py", 'w') as fp:
            fp.close
    return True

# Run migrations functions
def migrateFunction():
    if is_database_synchronized(DEFAULT_DB_ALIAS):
        migrated = True
        print('Migration not required')
    else:
        # Unapplied migrations found.
        try:
            call_command('migrate')
            migrated = True
        except BaseException as e:
            migrated = False
    return migrated


def runMigration():
    makemigrations = False
    if makeMigrationsFolder():
        try:
            s = subprocess.getstatusoutput('python3 manage.py makemigrations')
            makemigrations = True
        except BaseException as error:
            print('An exception occurred run Migrations: {}'.format(error))
        if makemigrations:
            migrateFunction()
    return makemigrations