from django.shortcuts import render

from django.shortcuts import render, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView
import pickle
import pandas as pd

def homePageView(request):
    return render(request, 'home.html')


def homePost(request):

    try:
        genHlth = int(request.POST['genHlth'])
        age = int(request.POST['age'])
        diffWalking = int(request.POST['diffWalking'])
        highBP = int(request.POST['highBP'])
        stroke = int(request.POST['stroke'])
        highChol = int(request.POST['highChol'])

        if genHlth > 5 or genHlth < 1:
            raise ValueError('GenHlth out of range')
        if age > 80 or age < 1:
            raise ValueError('Age out of range')

    except Exception as e:
        print(e)
        return render(request, 'home.html', {
            'errorMessage': '*** Your submission was invalid, please try again'})
    else:
        return HttpResponseRedirect(reverse('results', args=(genHlth, age, diffWalking, highBP, stroke, highChol)))


def results(request, genHlth, age, diffWalking, highBP, stroke, highChol):
    with open('./a2-model', 'rb') as f:
        loadedModel = pickle.load(f)

    singleSampleDf = pd.DataFrame(columns=['GenHlth', 'Age', 'DiffWalk', 'HighBP', 'Stroke', 'HighChol'])
    singleSampleDf = singleSampleDf.append({'GenHlth': genHlth,
                                            'Age': int(age/5),
                                            'DiffWalk': diffWalking,
                                            'HighBP': highBP,
                                            'Stroke': stroke,
                                            'HighChol': highChol
                                            },
                                           ignore_index=True)

    singlePrediction = loadedModel.predict(singleSampleDf)

    return render(request, 'results.html', {'genHlth': genHlth, 'age': age, 'diffWalking': diffWalking,
                                            'highBP': highBP, 'stroke': stroke, 'highChol': highChol,
                                            'prediction': singlePrediction})
