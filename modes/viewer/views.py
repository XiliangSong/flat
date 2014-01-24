from __future__ import print_function, unicode_literals, division, absolute_import
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
import flat.settings as settings
import flat.comm
import flat.users
import json

def getcontext(request,namespace,docid, doc):
    return {
            'namespace': namespace,
            'docid': docid,
            'mode': 'viewer',
            'modes': settings.EDITOR_MODES,
            'modes_json': json.dumps([x[0] for x in settings.EDITOR_MODES]),
            'dochtml': doc['html'],
            'docannotations': json.dumps(doc['annotations']),
            'docdeclarations': json.dumps(doc['declarations']),
            'setdefinitions': json.dumps(doc['setdefinitions']),
            'loggedin': request.user.is_authenticated(),
            'username': request.user.username
    }


@login_required
def view(request, namespace, docid):
    if flat.users.models.hasreadpermission(request.user.username, namespace):
        doc = flat.comm.get(request, '/getdoc/' + namespace + '/' + docid + '/')
        d = getcontext(request,namespace,docid, doc)
        return render(request, 'viewer.html', d)
    else:
        return HttpResponseForbidden("Permission denied")




@login_required
def subview(request, namespace, docid, elementid):
    if flat.users.models.hasreadpermission(request.user.username, namespace):
        e = flat.comm.get(request, '/getelement/' + namespace + '/' + docid + '/' + elementid + '/')
        d = {
                'elementid': elementid,
                'html': e['html'],
                'annotations': json.dumps(e['annotations']),
        }
        return HttpResponse(json.dumps(d), mimetype='application/json')
    else:
        return HttpResponseForbidden("Permission denied")

@login_required
def poll(request, namespace, docid):
    if flat.users.models.hasreadpermission(request.user.username, namespace):
        r = flat.comm.get(request, '/poll/' + namespace + '/' + docid + '/')
        d = []
        if len(r) > 0:
            for elementid in r:
                e = flat.comm.get(request, '/getelement/' + namespace + '/' + docid + '/' + elementid + '/')
                d.append({
                        'elementid': elementid,
                        'html': e['html'],
                        'annotations': json.dumps(e['annotations']),
                })
        return HttpResponse(json.dumps(d), mimetype='application/json')
    else:
        return HttpResponseForbidden("Permission denied")

