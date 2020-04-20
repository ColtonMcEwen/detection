from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
import pandas as pd
import numpy as np
import pickle

from .models import *
from newsbot.strainer import *
from newsbot.util import *

@xframe_options_exempt
def index(request):
    url = request.GET.get('u')
    if((url is not None) and (len(url) > 5)):
        # Load the saved models
        print("Setting up")
        svc_model = pickle.load(open('newsbot/svc_model.sav', 'rb'))
        mlp_model = pickle.load(open('newsbot/MLPC_model.sav', 'rb'))
        log_model = pickle.load(open('newsbot/log_model.sav', 'rb'))
        cDict = loadCanonDict()
        ss = SoupStrainer()
        ss.init()
        print("Setup complete")
        print("Attempting URL: " + url)
        if(ss.loadAddress(url)):
            articleX = buildExampleRow(ss.extractText, cDict)
        else:
            print("Error on URL, exiting")
            return render(request, 'urlFail.html', {'URL', url})

        articleX = articleX.reshape(1, -1)

        # Send the X row to the model to produce a prediction
        svc_prediction = svc_model.predict(articleX)
        svc_probabilities = svc_model.predict_proba(articleX)

        mlp_prediction = mlp_model.predict(articleX)
        mlp_probabilities = mlp_model.predict_proba(articleX)

        log_prediction = log_model.predict(articleX)
        log_probabilities = log_model.predict_proba(articleX)

        # Calculate fake + sketchy and seems legit + true to come up with an is it real or not. Then display the probabiilties.
        svc_prb = (svc_probabilities[0][0]*100, svc_probabilities[0][1]*100, svc_probabilities[0][2]*100, svc_probabilities[0][3]*100)
        svc_totFake = (svc_probabilities[0][0]*100) + (svc_probabilities[0][1]*100)
        svc_totReal = (svc_probabilities[0][2]*100) + (svc_probabilities[0][3]*100)

        mlp_prb = (mlp_probabilities[0][0]*100, mlp_probabilities[0][1]*100, mlp_probabilities[0][2]*100, mlp_probabilities[0][3]*100)
        mlp_totFake = (mlp_probabilities[0][0]*100) + (mlp_probabilities[0][1]*100)
        mlp_totReal = (mlp_probabilities[0][2]*100) + (mlp_probabilities[0][3]*100)

        log_prb = (log_probabilities[0][0]*100, log_probabilities[0][1]*100, log_probabilities[0][2]*100, log_probabilities[0][3]*100)
        log_totFake = (log_probabilities[0][0]*100) + (log_probabilities[0][1]*100)
        log_totReal = (log_probabilities[0][2]*100) + (log_probabilities[0][3]*100)

        fin_prb = ( (((svc_probabilities[0][0]*100)+(mlp_probabilities[0][0]*100)+(log_probabilities[0][0]*100))/3),
                    (((svc_probabilities[0][1]*100)+(mlp_probabilities[0][1]*100)+(log_probabilities[0][1]*100))/3),
                    (((svc_probabilities[0][2]*100)+(mlp_probabilities[0][2]*100)+(log_probabilities[0][2]*100))/3),
                    (((svc_probabilities[0][3]*100)+(mlp_probabilities[0][3]*100)+(log_probabilities[0][3]*100))/3) )

        fin_deg = ( (((svc_probabilities[0][0]*180)+(mlp_probabilities[0][0]*180)+(log_probabilities[0][0]*180))/3),
                    (((svc_probabilities[0][1]*180)+(mlp_probabilities[0][1]*180)+(log_probabilities[0][1]*180))/3),
                    (((svc_probabilities[0][2]*180)+(mlp_probabilities[0][2]*180)+(log_probabilities[0][2]*180))/3),
                    (((svc_probabilities[0][3]*180)+(mlp_probabilities[0][3]*180)+(log_probabilities[0][3]*180))/3) )

        fin_totFake = (svc_totFake + mlp_totFake + log_totFake)/3
        fin_totReal = (svc_totReal + mlp_totReal + log_totReal)/3

        fin_totFakeDeg = fin_totFake/100 * 180
        fin_totRealDeg = fin_totReal/100 * 180

        # Display processed text and the results
        context = {'headline':ss.recHeadline,
                   'words': ss.extractText,
                   'url' : url,
                   'svc_totFake': svc_totFake,
                   'svc_totReal': svc_totReal,
                   'svc_prediction': svc_prediction,
                   'svc_probabilities': svc_prb,
                   'mlp_totFake': mlp_totFake,
                   'mlp_totReal': mlp_totReal,
                   'mlp_prediction': mlp_prediction,
                   'mlp_probabilities': mlp_prb,
                   'log_totFake': log_totFake,
                   'log_totReal': log_totReal,
                   'log_prediction': log_prediction,
                   'log_probabilities': log_prb,
                   'fin_totFake': fin_totFake,
                   'fin_totReal': fin_totReal,
                   'fin_probabilities': fin_prb,
                   'fin_degrees': fin_deg,
                   'fin_totalFakeDeg': fin_totFakeDeg,
                   'fin_totalRealDeg': fin_totRealDeg,
                   }

        return render(request, 'newsbot/fakePatrol.html', context)
    else:
        return render(request, 'newsbot/fakePatrol.html')
