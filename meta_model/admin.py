import models
from django.contrib.admin import site as adminsite

adminsite.register(models.DataModel)
adminsite.register(models.Attribute)
adminsite.register(models.DataModelSet)
adminsite.register(models.Field)
adminsite.register(models.Index)
adminsite.register(models.Sequence)
