from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth.decorators import login_required

from ...meta_model.models import DataModel
from ...meta_model.utils import db_connect
try:
    import json
except:
    import simplejson as json 

@login_required
def get(request, dataspace, datamodel):
    user = request.user
    #verify user can access datamodel
    try:
        if DataModel.objects.get(name=datamodel, space__name=dataspace).users.filter(pk = user.pk).count()==0:
            return HttpResponseForbidden('You do not have access to the requested datamodel')
    except:
        return HttpResponseNotFound('Datamodel or dataspace not existing')                
    
    sample = request.REQUEST.get('object', None)
    if sample is None:
        return HttpResponseBadRequest('a sample object should be defined')
    sample = json.loads(sample)
    
    #validate_sample    
    
    dm = DataModel.objects.get(name=datamodel, space__name=dataspace)
    be = dm.backend  
    
    return db_connect(be).get(sample)
    
@login_required
def modify(request, dataspace, datamodel):
    user = request.user
    #verify user can access datamodel
    try:
        if DataModel.objects.get(name=datamodel, space__name=dataspace).users.filter(pk = user.pk).count()==0:
            return HttpResponseForbidden('You do not have access to the requested datamodel')
    except:
        return HttpResponseNotFound('Datamodel or dataspace not existing')                
    
    ul = request.REQUEST.get('update_list', "[]")
    dl = request.REQUEST.get('delete_list', "[]")
    
    try:
        ul = json.loads(ul)
    except ValueError:
        return HttpResponseBadRequest('Wrong format for the update_list. It should be JSON.')
    
    try:
        dl = json.loads(dl)
    except ValueError:
        return HttpResponseBadRequest('Wrong format for the delete_list. It should be JSON.')
    
    dm = DataModel.objects.get(name=datamodel, space__name=dataspace)
    be = dm.backend
    
    return db_connect(be).modify(ul, dl)
    
    