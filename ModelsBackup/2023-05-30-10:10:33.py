from django.db import models 


class FirstTableModel(models.Model):
	name= models.CharField(verbose_name ="Name", max_length =200, null = True, blank = True, )
	age= models.IntegerField(verbose_name ="Age", null = True, blank = True, )
	
	def __str__(self):
		return self.id


class CategoryModel(models.Model):
	project_category= models.ForeignKey(FirstTableModel, on_delete = models.CASCADE, null = True, blank = True, )
	
	def __str__(self):
		return self.id

