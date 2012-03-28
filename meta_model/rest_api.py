from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.api import Api
from models import *

auth = Authorization

class AttributeResource(ModelResource):
    class Meta:
        queryset = Attribute.objects.all()
        resource_name = 'attribute'
        authorization= auth()


    def get_object_list(self, request):
        return super(Attribute, self).get_object_list(request)
    
    def get_detail(self, request, **kwargs):
        return super(Attribute, self).get_detail(self, request, **kwargs) 
    
class BackendResource(ModelResource):
    '''represents the info on backends. Can only be read through GET.'''
    class Meta:
        queryset = Backend.objects.all()
        resource_name = 'backend'
        authorization= auth()
        excludes = ['password', 'username']
        allowed_methods = ['get']

    def get_object_list(self, request):
        return super(Backend, self).get_object_list(request)
    
    def get_detail(self, request, **kwargs):
        return super(Backend, self).get_detail(self, request, **kwargs) 
    

class DataSpaceResource(ModelResource):
    class Meta:
        queryset = DataSpace.objects.all()
        resource_name = 'dataspace'
        authorization= auth()


    def get_object_list(self, request):
        return super(DataSpace, self).get_object_list(request)
    
    def get_detail(self, request, **kwargs):
        return super(DataSpace, self).get_detail(self, request, **kwargs) 
    
    
class DataModelResource(ModelResource):
    class Meta:
        queryset = DataModel.objects.all()
        resource_name = 'datamodel'
        authorization= auth()


    def get_object_list(self, request):
        return super(DataModel, self).get_object_list(request)
    
    def get_detail(self, request, **kwargs):
        return super(DataModel, self).get_detail(self, request, **kwargs) 
    
    
class FieldResource(ModelResource):
    class Meta:
        queryset = Field.objects.all()
        resource_name = 'field'
        authorization= auth()


    def get_object_list(self, request):
        return super(Field, self).get_object_list(request)
    
    def get_detail(self, request, **kwargs):
        return super(Field, self).get_detail(self, request, **kwargs) 
    
       
class PrivilegeResource(ModelResource):
    class Meta:
        queryset = Privilege.objects.all()
        resource_name = 'attribute'
        authorization= auth()


    def get_object_list(self, request):
        return super(Privilege, self).get_object_list(request)
    
    def get_detail(self, request, **kwargs):
        return super(Privilege, self).get_detail(self, request, **kwargs) 
    
    
class IndexResource(ModelResource):
    class Meta:
        queryset = Attribute.objects.all()
        resource_name = 'attribute'
        authorization= auth()


    def get_object_list(self, request):
        return super(Attribute, self).get_object_list(request)
    
    def get_detail(self, request, **kwargs):
        return super(Attribute, self).get_detail(self, request, **kwargs) 
    



'''
Prepare urls for API
''' 

v1_api = Api(api_name='v1')
v1_api.register(AttributeResource())
v1_api.register(BackendResource())
v1_api.register(DataSpaceResource())
v1_api.register(DataModelResource())
v1_api.register(FieldResource())
v1_api.register(PrivilegeResource())
v1_api.register(IndexResource())