'''
Created on 16/mar/2012

@author: mmo
'''
class StorageBackend(object):
    def __init__(self, adapter):
        self.adapter = adapter # we'll cover dynamic loading below

    def get(self, obj, depth=0):
        return self.adapter.get(obj, depth)

    def modify(self, upsert_list, delete_list):
        return self.adapter.set(upsert_list, delete_list)
        
    def create_dataspace(self, model):
        self.adapter.create_database(model)
        
    def create_index(self, attributes):
        self.adapter.create_index(attributes)
    
class BaseAdapter(object):
    def __init__(self):    
        self.backend = self.get_backend()

    def get(self, obj, depth=0):
        '''
        This is the implementation of a query. the "obj" is the sample object. The possible interactions
        '''
        return self.backend.get(obj, depth)

    def modify(self, upsert_list, delete_list):
        return self.backend.modify(upsert_list, delete_list)
    
    def create_dataspace(self, structure):
        pass
    
    def create_index(self, model):
        pass
    
    
