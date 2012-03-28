from LabsBackend.meta_model.models import DataModel, DataSpace
from tastypie.bundle import Bundle
from tastypie.resources import Resource
from tastypie.api import Api
try:
    import json
except:
    #import simplejson as json
    pass
    
from ..meta_model.models import *

########################## meta-methods

def tpy_get_resource_uri(self, bundle_or_obj):
    kwargs = {
        'resource_name': self._meta.resource_name,
    }

    if isinstance(bundle_or_obj, Bundle):
        kwargs['pk'] = bundle_or_obj.obj.uuid
    else:
        kwargs['pk'] = bundle_or_obj.uuid

    if self._meta.api_name is not None:
        kwargs['api_name'] = self._meta.api_name
    return self._build_reverse_url("api_dispatch_detail", kwargs=kwargs)

def tpy_obj_delete_list(self, request=None, **kwargs):
    pass
##############################################################
class LabsMetaObject(type):
    def __new__(cls, clsname, clsbases, clsdict):
        clsdict['_data'] = {}
        clsdict['_meta'] = {}
        clsdict['get_resource_uri'] = tpy_get_resource_uri 
        clsdict['get_object_list'] = tpy_get_resource_uri 
        clsdict['obj_get_list'] = tpy_get_resource_uri 
        clsdict['obj_get'] = tpy_get_resource_uri 
        clsdict['obj_create'] = tpy_get_resource_uri 
        clsdict['obj_update'] = tpy_get_resource_uri 
        clsdict['obj_delete_list'] = tpy_get_resource_uri 
        clsdict['obj_delete'] = tpy_get_resource_uri 
        clsdict['rollback'] = tpy_get_resource_uri 
            
        return type.__new__(cls, clsname, clsbases, clsdict)
    
    

class LabsObject(Resource):
    __metaclass__ = LabsMetaObject
    
    def __init__(self, initial=None):
        if hasattr(initial, 'items'):
            self.__dict__['_data'] = initial

    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value
        
    

   
class Constructor(object):
    def __init__(self):
        self.apis = {}
        pass
    
    def create_models(self):
        for dataspace in DataSpace.objects.all():
            self.create_dataspace(dataspace)
            for model in DataModel.objects.filter(space = dataspace, abstract = False):
                self.create_model(model)
                
    def create_dataspace(self, dataspace):
        self.apis[dataspace.name] = self.create_api(dataspace.name, dataspace.version, dataspace.creator)
        self.apis[dataspace.name]['models'] = {}
            
    def create_model(self, model):
        self.apis[model.space.name]['models'][model.name] = self.create_resource(model.name, model.parent_model, model.attributes.all())
        self.apis[model.space.name].register(self.apis[model.space.name]['models'][model.name])
    
    def create_resource(self, name, parent, attributes):
        att_dict = {}
        for att in attributes:
            att_dict[att.name] = att.attribute_type
         
        clas = type(name, (LabsObject,) , att_dict)
        return clas
    
    def create_api(self, name, version, creator):
        
        pass
    
    @property
    def urls(self):
        pass
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        