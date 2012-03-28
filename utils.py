import os
from django.utils.datastructures import SortedDict
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
        
class Choices(object):
    """
    Easy declarative "choices" tool::
    
        >>> STATUSES = Choices("Live", "Draft")
        
        # Acts like a choices list:
        >>> list(STATUSES)
        [(1, 'Live'), (2, 'Draft')]
        
        # Easily convert from code to verbose:
        >>> STATUSES.verbose(1)
        'Live'
        
        # ... and vice versa:
        >>> STATUSES.code("Draft")
        2
        
    """
    def __init__(self, *args, **kwargs):
        self.code_map = SortedDict()
        self.verbose_map = {}
        for code, verbose in enumerate(args):
            # Enumerate starts from 0, but for convention's sake we'd prefer to
            # start choices from 1.
            self.code_map[code+1] = verbose
            self.verbose_map[verbose] = code+1
            
        for code, verbose in kwargs.items():
            self.code_map[code] = verbose
            self.verbose_map[verbose] = code
            
    def __iter__(self):
        return self.code_map.iteritems()
                
    def __len__(self):
        return len(self.code_map)
        
    def code(self, verbose):
        """
        Return the code version of the verbose name.
        """
        return self.verbose_map[verbose]
        
    def verbose(self, code):
        """
        Return the verbose name given the code.
        """
        return self.code_map[code]
    
    
def load_backend(backend_name):
    try:
        module = import_module('.base', 'django.db.backends.%s' % backend_name)
        import warnings
        warnings.warn(
            "Short names for DATABASE_ENGINE are deprecated; prepend with 'django.db.backends.'",
            DeprecationWarning
        )
        return module
    except ImportError, e:
        # Look for a fully qualified database backend name
        try:
            return import_module('.base', backend_name)
        except ImportError, e_user:
            # The database backend wasn't found. Display a helpful error message
            # listing all possible (built-in) database backends.
            backend_dir = os.path.join(os.path.dirname(__file__), 'backends')
            try:
                available_backends = [f for f in os.listdir(backend_dir)
                        if os.path.isdir(os.path.join(backend_dir, f))
                        and not f.startswith('.')]
            except EnvironmentError:
                available_backends = []
            if backend_name.startswith('django.db.backends.'):
                backend_name = backend_name[19:] # See #15621.
            if backend_name not in available_backends:
                error_msg = ("%r isn't an available database backend. \n" +
                    "Try using django.db.backends.XXX, where XXX is one of:\n    %s\n" +
                    "Error was: %s") % \
                    (backend_name, ", ".join(map(repr, sorted(available_backends))), e_user)
                raise ImproperlyConfigured(error_msg)
            else:
                raise # If there's some other error, this must be an error in Django itself.
