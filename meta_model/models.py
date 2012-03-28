from django.db import models
from django.contrib.auth.models import User

class BackendType(models.Model):
    name = models.CharField(max_length = 200)
    version = models.CharField(max_length = 200)
    module = models.CharField(max_length = 500)
    
    
    is_column_db = models.BooleanField(default = False)
    is_relational_db = models.BooleanField(default = False)
    is_document_db = models.BooleanField(default = False)
    is_object_db = models.BooleanField(default = False)
    is_graph_db = models.BooleanField(default = False)
    
    geo_support = models.BooleanField(default = False)

    def __unicode__(self):
        return "%s %s" % (self.name, self.version,)
    
    class Meta:
        unique_together = ['name','version']
        
    def dump(self):
        return {
                'name':self.name,
                'version':self.version,
                'module':self.module,
                
                'is_column_db':self.is_column_db,
                'is_relational_db':self.is_relational_db,
                'is_document_db':self.is_document_db,
                'is_object_db':self.is_object_db,
                'is_graph_db':self.is_graph_db,
                'geo_support':self.geo_support
               }

class Backend(models.Model):
    name        = models.CharField(max_length=200,unique=True)
    backend_type= models.ForeignKey(BackendType)
    contact     = models.ForeignKey(User)
    db_name     = models.CharField(max_length=200)
    username    = models.CharField(max_length=200)
    password    = models.CharField(max_length=200)
    host        = models.CharField(max_length=200)
    port        = models.IntegerField()
    options     = models.TextField()
    max_pool    = models.IntegerField()
    
    def __unicode__(self):
        return self.name
    
    def dump(self):
        return {
                'name':self.name,
                'backend':self.backend_type.dump(),
                'contact':self.contact.username,
                'db_name':self.db_name,
                'username':self.username,
                'password':self.password,
                'host':self.host,
                'port':self.port,
                'options':self.options,
                'max_pool':self.max_pool,
                
                }

class DataSpace(models.Model):
    name = models.CharField(max_length=200, unique=True)
    creator = models.ForeignKey(User)
    default_backend = models.ForeignKey(Backend)
    
    def __unicode__(self):
        return "%s@v%s" % (self.name, self.version, )
    
class DataSpaceVersion(models.Model):
    space = models.ForeignKey(DataSpace)
    version = models.IntegerField(default=1)
    following = models.ForeignKey('DataSpace', related_name="preceding", null=True, blank=True)
    
class DataModel(models.Model):
    space = models.ForeignKey(DataSpace, related_name="models")
    name = models.CharField(max_length=200, unique=True)
    extends = models.ForeignKey('DataModel', null=True, blank=True)
    abstract = models.BooleanField(default=False)
    lastupdate = models.DateTimeField()
    
    class Meta:
        unique_together=('space', 'name')
    
    def __unicode__(self):
        return self.name

class DataModelVersion(models.Model):
    datamodel = models.ForeignKey(DataModel)
    dataspaceversion = models.ForeignKey(DataSpaceVersion)


class DataBackend(models.Model):
    datamodel = models.ForeignKey(DataModel)
    backend = models.ForeignKey(Backend)
    

class Attribute(models.Model):
    name = models.CharField(max_length=200)
    attribute_type = models.ForeignKey(DataModel)
    owner = models.ForeignKey(DataModelVersion, related_name="attributes")
    required = models.BooleanField(default=True)
    on_delete_cascade = models.BooleanField(default=False)
    lastupdate = models.DateTimeField()
    min_multiplicity = models.IntegerField(default = 0)
    max_multiplicity = models.IntegerField(default = 0)
    
    class Meta:
        unique_together=('owner', 'name')
    
    def __unicode__(self):
        return "%s.%s" % (self.owner,self.name,)
    
class Field(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey('DataModel', related_name="fields")
    supplier = models.CharField(max_length=200)
    
    class Meta:
        unique_together=('owner', 'name')
        
    def __unicode__(self):
        return "%s.%s" % (self.owner,self.name,)
    
class Sequence(models.Model):
    dataspace = models.ForeignKey(DataSpace)
    attribute = models.ForeignKey(Attribute)
    last_value = models.BigIntegerField()
    lastupdate = models.DateTimeField()
    
    def __unicode__(self):
        return "%s: %s" % (self.attribute, self.last_value, )
    
class PrivilegeType(models.Model):
    name = models.CharField(max_length = 50, primary = True)
    
    def __unicode__(self):
        return self.name
    
class Privilege(models.Model):
    
    user = models.ForeignKey(User,related_name="can")
    grant = models.ForeignKey(PrivilegeType)
    data_model = models.ForeignKey(DataModel, related_name = "users")
    
    def __unicode__(self):
        return "%s: %s on %s" % (self.user, self.grant, self.data_model, )
    
class Index(models.Model):
    '''single table indexes'''
    attributes = models.ManyToManyField(Attribute, related_name = "indexes")
    
    def __unicode__(self):
        return "index on cols %s" % [a for a in self.attributes.all()],
    
    def save(self, *args, **kwargs):
        if self.attributes.all().distinct('owner').count() == 1:
            super(Index, self).save(args, kwargs)    
              
    