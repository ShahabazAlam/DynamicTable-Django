from MainApp.models import *
from MainApp.models import *
from .views import *
import os
from .make_backup import *

# Python3 code to remove whitespace
def remove(string):
    return string.replace(" ", "")


# Write normal fields lines which we have to write in model 
def writeLines(data_type,data): 
    text = ''
    option_text = ''
    if data['verbose_name'] is not None:
        option_text += 'verbose_name ='+ '"' + data['verbose_name'] + '"'
        option_text += ', '
    
    if data['field_length'] is not None:
        option_text += 'max_length ='+ str(data['field_length'])
        option_text += ', '

    if (data['default_value'] is not None):
        default_value = DefaultValue.objects.get(id=data['default_value'])
        if default_value.param == False:
            option_text += 'default = False, '
        if default_value.param == True:
            option_text += 'default = True, '
        if default_value.param == 'DateTime':
            option_text += 'auto_now = True, '
            
    if data_type not in ['DateTimeField','DateField']:
        if data['nullable'] is not None:
            option_text += 'null = ' + str(data['nullable']) + ', ' 
        if data['blankable'] is not None:
            option_text += 'blank = ' + str(data['blankable']) + ', ' 


    text += str(data['field_name']) + '= models.'+data_type+'('+ option_text +')'
    return text



# Write lines for relation fields which we have to write in model 
def writeLinesForRelation(data):
    text = ''
    option_text = ''
    if data['on_delete'] is not None:
        field_name = OnDelete.objects.get(id=data['on_delete'])
        option_text += 'on_delete = models.'+ field_name.param +', '

    if data['nullable'] is not None:
        option_text += 'null = ' + str(data['nullable']) + ', ' 
    if data['blankable'] is not None:
        option_text += 'blank = ' + str(data['blankable']) + ', ' 
    
    realetion_name = RelationshipType.objects.get(id=data['relation_type'])
    text += str(data['field_name']) + '= models.'+realetion_name.param+'('+data['related_table_name']+ 'Model, '+ option_text +')'
    return text


# Create whole models.py file
def writeModelFile(model_path, backup=False):
    checked = True
    try:
        fields = [f.name for f in TableField._meta.get_fields()]
        fields.remove('id')
        fields.remove('table')
        fp = open(os.path.join(model_path),mode='w')
        fp.truncate()
        text = 'from django.db import models \n\n'
        fp.write(text)

        tables = TableName.objects.all().order_by('-id')
        for table in tables:
            model_text = '\n'
            model_text += f"class {remove(table.table_name)}Model(models.Model):"
            model_text += '\n\t'
            table = TableField.objects.filter(table_id=table.id).values(*fields)
            if table:
                i = 0
                return_text = ''
                for c in table:
                    if c['is_relation'] == False:
                        if i == 0:
                            return_text += c['field_name']
                        data_type = DataType.objects.get(id=c['data_type'])
                        model_text += writeLines(data_type.param, c)
                        model_text += '\n\t'
                        i += 1
                    if c['is_relation'] == True:
                        if i == 0:
                            return_text += c['field_name']
                        if writeLinesForRelation(c) is not None:
                            model_text += writeLinesForRelation(c)
                            model_text += '\n\t'
                            i += 1
                model_text += '\n\t'
                model_text += 'def __str__(self):'
                model_text += '\n\t\t'
                model_text += f'return str(self.{return_text})'
                model_text += '\n\n'
                fp.write(model_text)
                # fp.close()
    except BaseException as error:
        revert_back_model()
        print('An exception occurred write model file: {}'.format(error)) 
        checked = False 
    return checked






