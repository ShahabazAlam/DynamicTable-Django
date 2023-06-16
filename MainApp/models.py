from django.db import models
# Create your models here.

class TableName(models.Model):
    table_name = models.CharField('Field Name', max_length=100, null=True, blank=True)
    def __str__(self):
        return self.table_name


class DataType(models.Model):
    param = models.CharField('Date Type', max_length=100, null=True, blank=True)
    def __str__(self):
        return self.param

class DefaultValue(models.Model):
    param = models.CharField('Default Value', max_length=100, null=True, blank=True)
    def __str__(self):
        return self.param

class OnDelete(models.Model):
    param = models.CharField('Default Value', max_length=100, null=True, blank=True)
    def __str__(self):
        return self.param

class RelationshipType(models.Model):
    param = models.CharField('Default Value', max_length=100, null=True, blank=True)
    def __str__(self):
        return self.param

class TableField(models.Model):
    table = models.ForeignKey(TableName, on_delete=models.CASCADE, blank=True, null=True,related_name='table_table')
    field_name = models.CharField('Field Name', max_length=100, null=True, blank=True)
    is_relation = models.BooleanField(null=True, blank=True, default=False)
    relation_type = models.ForeignKey(RelationshipType, on_delete=models.CASCADE, blank=True, null=True,related_name='relation_table')
    related_table_name = models.CharField('Related Table Name', max_length=100, null=True, blank=True)
    field_name = models.CharField('Field Name', max_length=100, null=True, blank=True)
    data_type = models.ForeignKey(DataType, on_delete=models.CASCADE, blank=True, null=True,related_name='data_type_table')
    on_delete = models.ForeignKey(OnDelete, on_delete=models.CASCADE, blank=True, null=True,related_name='on_delete_table')
    default_value = models.ForeignKey(DefaultValue, on_delete=models.CASCADE, blank=True, null=True,related_name='default_value_table')
    verbose_name = models.CharField('Verbose Name', max_length=100, null=True, blank=True)
    field_length = models.CharField('Field Length', max_length=100, null=True, blank=True)
    nullable = models.BooleanField(null=True, blank=True)
    blankable = models.BooleanField(null=True, blank=True)
  
    def __str__(self):
        return self.field_name



