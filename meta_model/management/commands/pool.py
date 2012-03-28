from django.core.management.base import BaseCommand, CommandError
from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing import Pool
from daemon import Daemon
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

import socket
import threading
try:
    import json
except:
    import simplejson as json

class Command(BaseCommand):
    args = ''
    help = 'Starts the connection-pooler'

    def handle(self, *args, **options):
        b = BackEndPool("be.pid")
        b.start()            
            
            
class BackEndPool(Daemon):
    def __init__(self):
        self.backends = {}
        
    def run(self):
        self.server = SimpleJSONRPCServer(('localhost', 8473))
        
        self.server.register_function(self.spawn_backends, "spawn")
        self.server.register_function(self.kill_backends, "kill")
        self.server.serve_forever()
    
    def spawn_backends(self, backend):
        space = backend['space'] 
        model = backend['model']
        if space not in self.backends:
            self.backends[space] = {}
        if model not in self.backends[space]:
            self.backends[space][model] = []
        self.backends[space][model].append(BackEndProcess(backend))
        for be in self.backends[backend['space']][backend['model']]:
            be.start()
        
    def kill_backends(self, backend):
        for be in self.backends[backend['space']][backend['model']]:
            be.join()    

class BackEndProcess(Process):
    def __init__(self, backend):
        
        