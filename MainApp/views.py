from django.db.models import options
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import *
from TableCreation.views import *

# Create your views here.
from pathlib import Path
import os
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

def Home(request):
    return render(request,'home.html')

def populateData(request):
    TYPE_CHOICES = [
        "BooleanField",
        "CharField",
        "DateField",
        "FileField",
        "FloatField",
        "ImageField",
        "IntegerField",
        "SlugField",
        "SmallIntegerField",
        "TextField",
        "TimeField",
        "URLField",
        "UUIDField",
        "DateTimeField",
    ]



    DEFAULT_CHOICES = [
        "Null",
        "False",
        "True",
        "DateTime",
        "None",
        ]



    DELETE_CHOICES = [
        "CASCADE",
        "SET_NULL",
        "SET_DEFAULT",
        "SET",
        "PROTECT",
        "DO_NOTHING",
        ]

    RELATION_CHOICES = [
                        'ForeignKey',
                        'ManyToManyField',
                        'OneToOneField'
                        ]

    for v in DEFAULT_CHOICES:
        if not DefaultValue.objects.filter(param=v).exists():
            DefaultValue.objects.create(param=v)
    for v in DELETE_CHOICES:
        if not OnDelete.objects.filter(param=v).exists():
            OnDelete.objects.create(param=v)
    for v in TYPE_CHOICES:
        if not DataType.objects.filter(param=v).exists():
            DataType.objects.create(param=v)
    for v in RELATION_CHOICES:
        if not RelationshipType.objects.filter(param=v).exists():
            RelationshipType.objects.create(param=v)
    return render(request,'home.html',{'key':'success'})


def createDictForModel(data_type,data):
    options = {} 
    if data['verbose_name'] is not None:
        options.update({'verbose_name':data['verbose_name']})
    
    if data['field_length'] is not None:
        options.update({'max_length':int(data['field_length'])})

    if (data['default_value'] is not None):
        default_value = DefaultValue.objects.get(id=data['default_value'])
        if default_value.param == False:
            options.update({'default':False})
        if default_value.param == True:
            options.update({'default':True})
        if default_value.param == 'DateTime':
            options.update({'auto_now':True})
    if data['nullable'] is not None:
        options.update({'null':True})
    else:
        options.update({'null':False})
    if data['blankable'] is not None:
        options.update({'blank':True})
    else:
        options.update({'blank':False})
  
    if data_type == 'BooleanField':
        return {data['field_name'] : models.BooleanField(**options)}
    
    if data_type == 'CharField':
        return {data['field_name'] : models.CharField(**options)}
    
    if data_type == 'DateField':
        return {data['field_name'] : models.DateField(**options)}
    


def CreateModel(request):
    model_text = '\n\n'
    model_text += "class NewModel(models.Model):"
    model_text += '\n\t'

    fields = [f.name for f in TableField._meta.get_fields()]
    fields.remove('id')
    fields.remove('category')
    category = TableField.objects.filter(category_id=1).values(*fields)
    temp = {}
    for c in category:
        if c['is_relation'] == False:
            data_type = DataType.objects.get(id=c['data_type'])
            if createDictForModel(data_type.param, c) is not None:
                model_text += writeLines(data_type.param, c)
                model_text += '\n\t'
                # temp.update(createDictForModel(data_type.param, c))
    # mo = create_model('Profile', fields=temp, app_label='MainApp', module='', options=None, admin_opts=True)
    model_text += '\n\t'
    # model_text += 'history = HistoricalRecords()'
    # model_text += '\n\t'
    model_text += 'def __str__(self):'
    model_text += '\n\t\t'
    model_text += 'return self.'+category[0]['field_name']
    model_text += '\n\n'
    open(os.path.join(BASE_DIR, 'MainApp/models.py'),mode='a').write(model_text)
    print(model_text)
    return render(request,'home.html',{'key':'success'})




def CreateModelReturn():
    fields = [f.name for f in TableField._meta.get_fields()]
    fields.remove('id')
    fields.remove('category')
    category = TableField.objects.filter(category_id=1).values(*fields)
    temp = {}
    for c in category:
        if c['is_relation'] == False:
            data_type = DataType.objects.get(id=c['data_type'])
            if createDictForModel(data_type.param, c) is not None:
                temp.update(createDictForModel(data_type.param, c))
    return create_model('Profile', fields=temp, app_label='MainApp', module='', options=None, admin_opts=True)
