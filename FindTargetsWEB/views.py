# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.shortcuts import render

from FindTargetsWEB.forms import SBMLFileForm, Passo1Form
from FindTargetsWEB.pipelineFindTargets import FindTargets, MyThread
from django.http.response import HttpResponseRedirect
from django.core.cache import cache
from django.http import HttpResponse

#@cache_control(must_revalidate=True)
#@never_cache
# Create your views here.
def index(request):
    if request.method == 'POST':

        form = SBMLFileForm(request.POST, request.FILES)
        
        sbmlfile_in = request.FILES["file"]
        organism_in = form.data["organism"]
        email_in = form.data["email"]
        name_in = form.data["name"]
        
        request.session['organism'] = organism_in
        request.session['email'] = email_in
        request.session['name'] = name_in
        #request.session['file'] = sbmlfile_in

        dict_return_full = {}
        dict_return_form = {
                                'name': name_in,
                                'email': email_in,
                                'organism': organism_in,
                                'file': sbmlfile_in,
                            }
        
   
        if form.is_valid():
            model = FindTargets().readModel(sbmlfile_in)
            dict_return_validate = FindTargets().validateModel(model)
           
            cache.set('model', model)
            
            if dict_return_validate['ehParaFazer']:
                request.session['ehParaFazer'] = True
            else:
                request.session['ehParaFazer'] = False
            
            dict_return_full.update(dict_return_form)
            dict_return_full.update(dict_return_validate)
            del dict_return_full['file']
            cache.set('dict_return_full', dict_return_full)
            
            #return HttpResponseRedirect('/passo1/')
            return HttpResponseRedirect('FindTargetsWEB/passo1/') #servidor
        
    else:
        request.session.flush()
        cache.clear()
        #cache.close()
        form = SBMLFileForm()
        
    return render(request, 'FindTargetsWEB/index.html', {'form': form})


def passo1(request):
    if request.method == 'POST': # Aqui está clicando no submit
        form = Passo1Form(request.POST, request.FILES)
        organism_in2 = request.session["organism"]
        email_in2 = request.session["email"]
        name_in2 = request.session["name"]
        method = form.data['method']
        #sbmlfile_in2 = request.session['file']
        modelPOG = cache.get('model')
        #modelPOG = FindTargets().readModel(sbmlfile_in2)

        dict_return_full = {}
        dict_return_form = {
                                'name': name_in2,
                                'email': email_in2,
                                'organism': organism_in2,
                                'method': method
                            }
        
        if form.is_valid():
            
            if request.session['ehParaFazer']:
                t = MyThread(name_in2, organism_in2, email_in2, modelPOG, method)
                t.start()
            
            dict_return_full.update(dict_return_form)
            #return HttpResponseRedirect('/passo2/')
            return HttpResponseRedirect('FindTargetsWEB/passo2/') #servidor
        
    else: # Aqui está entrando na pagina passo1.html
        dict_return_full = cache.get('dict_return_full')
        organism_in2 = request.session["organism"]
        email_in2 = request.session["email"]
        name_in2 = request.session["name"]
        valInitialSolutionFmt = dict_return_full['valInitialSolutionFmt']
        message = dict_return_full['message']
        
        form = Passo1Form()
        
        dict_form = {
                        'name': name_in2,
                        'email': email_in2,
                        'organism': organism_in2,
                        'valInitialSolutionFmt': valInitialSolutionFmt,
                        'message': message,
                        'form': form
                    }
        
    return render(request, 'FindTargetsWEB/passo1.html', dict_form)


def passo2(request):
    request.session.flush()
    cache.clear()
    cache.close()
    return render(request, 'FindTargetsWEB/passo2.html')


def download(request):
    dir_path = os.path.dirname(os.path.realpath(__file__)) # identifica o local real onde esse arquivo esta
    response = HttpResponse(open(dir_path+"/static/FindTargetsWEB/User_Manual_FindTargetsWeb_v1.1.pdf", 'rb').read())
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = 'attachment; filename=User_Manual_FindTargetsWeb_v1.1.pdf'
    return response