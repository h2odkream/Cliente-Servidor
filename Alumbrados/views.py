# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import plotly.offline as opy
import plotly.graph_objs as go
import twitter
import json
import pandas
import pandas as pd
import numpy as np
from sodapy import Socrata

# Create your views here.
@login_required
def home(request):
	user = request.user
	print user
	context = locals()
	template = 'consultas/index.html'
	return render(request, template, context)

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return render_to_response('index.html', {}, RequestContext(request))

def get_data(request):
    template = 'consultas/data.html'
    client = Socrata("www.datos.gov.co", None)

    results = client.get("hsfc-j4sh", limit=2000)
    results_df = pd.DataFrame.from_records(results)


    context = {
        'results_df': client.get("hsfc-j4sh", limit=2000),

    }
    return render (request, template, context)

# CONSULTA DE DATOS

def result_data(request):
    value = request.POST.get('codigo')
    value2 = request.POST.get('codigo2')
    client = Socrata("www.datos.gov.co", None)

    results = client.get("hsfc-j4sh", limit=2000)
    #print results
    results_df = pd.DataFrame.from_records(results)

    xresult=[]
    yresult=[]

    #SACA CADA UNO DE LOS DATOS PARA LAS GRAFICAS
    for t in range (len(results_df)):
        if (True != pd.isnull (results_df.comuna[t])):
			x=(results_df.comuna[t])
			xresult.append(pd.to_numeric(x))
        if (True != pd.isnull(results_df.a_o[t])):
			y=(results_df.a_o[t])
			yresult.append(y)

    xresults=sorted(xresult)
    yresults=yresult


    context = {
        'codigo': value,
        'codigo2': value2,
        'results_df': client.get("hsfc-j4sh", limit=2000),
        'graph': pd.DataFrame.from_records(results),
        'x': xresults,
        'y': yresults
    }
    template = 'consultas/resultado_consultas.html'
    return render(request, template, context)
