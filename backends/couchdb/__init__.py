from .. import BaseAdapter

class Adapter(BaseAdapter):
	
	def get_backend(self):
		self.client = {}
		return self
	
	def modify(self, upsert_list, delete_list):
		
		return self.client
	
	def get(self, obj, depth=0):
		return self.client.get(self, obj, depth=depth)
	
	def create_database(self, structure):
		return self.client
	
	def create_index(self, attributes):
		return self.client
	