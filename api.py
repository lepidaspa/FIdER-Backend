class StorageBackend(object):
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
    def _get(self, sample, depth=0):
        pass
    def _modify(self, upsert_list, delete_list):
        pass

class StorageManager(StorageBackend):    
    def get(self, sample, depth=0):
        return super(StorageManager, self)._get(sample, depth)
    def modify(self, upsert_list, delete_list):
        return super(StorageManager, self)._modify(upsert_list, delete_list)
    def put(self, upsert_list):
        return super(StorageManager, self)._modify(upsert_list, [])
    def delete(self, delete_list):
        return super(StorageManager, self)._modify([], delete_list)
    
class ModelManager(StorageBackend):
    def put(self, model):
        return super(ModelManager, self)._modify([model], [])
    def get(self, version):
        return super(ModelManager, self)._get(version, 0)
    
class CacheManager(StorageBackend):
    def create_cache(self, name):
        pass
    def put(self, name, key, value):
        pass
    def get(self, name, key):
        pass

        
        