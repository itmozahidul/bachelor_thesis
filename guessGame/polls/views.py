# Create your views here.
import json
import os
import re
import sys

from django.conf import settings
from django.shortcuts import render
from scipy import spatial
from sent2vec.vectorizer import Vectorizer
from django.core.files.storage import FileSystemStorage
from tkinter import messagebox


class fileInfo:
  def __init__(self, url, name):
    self.name = name
    self.url = url


def index(request):


    fs = FileSystemStorage()
    dist = [0, 0]
    sentences = [
        "This is an awesome book to learn NLP.",
        "How are you doing",
        "This is an good book to learn NLP.",
    ]

    filelist = []
    fileList = os.listdir(settings.MEDIA_ROOT)
    for f in fileList:
        url = fs.url(f)
        filelist .append(fileInfo(url, f))
    context = {'files': filelist }

    return render(request, 'base.html', context)


def add(request):

    if request.FILES:
        uploadedFile = request.FILES['fname']
        fs = FileSystemStorage()
        name = fs.save(uploadedFile.name, uploadedFile)
        f = open(fs.path(name), 'rt')
        sentenceRR = f.read()
        sentenceR = re.sub('@', '', sentenceRR)
        sentencee = re.sub('[uU][Ss][Ee][Rr]', '', sentenceR)
        sentenceee = re.sub('_', ' ', sentencee)
        sentenceeee = re.sub('-', ' ', sentenceee)
        sentenceeeee = re.sub('=', ' ', sentenceeee)
        sentence = re.sub('%', ' ', sentenceeeee)

        sepsent = re.findall('\d,+(.*)\n', sentence)
        print(sepsent)
        i = 1
        centroids = []

        # for each cluster we defined separate distance and vector list
        Dist1 = []
        Dist2 = []
        Dist3 = []
        Dist4 = []
        Cluster1 =[]
        Cluster2 = []
        Cluster3 = []
        Cluster4 = []

        # showing the progress information on the display
        i = 0

        # we take each sentence from the list and calculate its bert representation in vector
        for x in sepsent:
            progress_percent = round(((i*100)/len(sepsent)),2)
            remained_time_h =int(((7*len(sepsent)) - (i*7))/3600)
            remained_time_m = ((7 * len(sepsent)) - (i * 7)) % 3600
            print(' ----------------  progress :'+str(progress_percent)+'% ---------remaining time(hh:mm): '+str(remained_time_h)+':'+str(remained_time_m)+' ------', end='\r')
            i = i+1

            vectorizer = Vectorizer()
            vectorizer.bert(x)
            vectors_bert = vectorizer.vectors
            centroids.append(vectors_bert[0])
            print
        # we took 4 random centers for k means algorithm
        if os.path.isfile('center_json_data.json'):
            pfc = open('center_json_data.json')
            jcenter = json.load(pfc)
            pfc.close()
            centroid1 = jcenter['center1']
            centroid2 = jcenter['center2']
            centroid3 = jcenter['center3']
            centroid4 = jcenter['center4']
        else:
            centroid1v = sum(centroids) / len(centroids)
            centroid2v = sum(centroids) / (len(centroids) / 2)
            centroid3v = sum(centroids) / (len(centroids) / 10)
            centroid4v = sum(centroids) / (len(centroids) / 28)
            centroid1 = centroid1v.tolist()
            centroid2 = centroid2v.tolist()
            centroid3 = centroid3v.tolist()
            centroid4 = centroid4v.tolist()

        print(centroid1)

# creating json format for them to save them later

        lock1 = 0
        lock2 = 0
        lock3 = 0
        lock4 = 0

        loop_no=0

        while True:
            print('---cluster:---')
            print(len(Cluster1))
            print(len(Cluster2))
            print(len(Cluster3))
            print(len(Cluster4))

            print('----------------')

            print('#######################')
            if len(Cluster1) > 0:
                if (centroid1 != (sum(Cluster1) / len(Cluster1))).all():
                    centroidiv1 = sum(Cluster1) / len(Cluster1)
                    centroid1 = centroidiv1.tolist()

                else:
                    lock1 = 1
            else:
                if loop_no >100:
                    lock1 = 1
            if len(Cluster2) > 0:
                if (centroid2 != (sum(Cluster2) / len(Cluster2))).all():
                    centroidiv2 = sum(Cluster2) / len(Cluster2)
                    centroid2 = centroidiv2.tolist()

                else:
                    lock2 = 1
            else:
                if loop_no >100:
                    lock2 = 1
            if len(Cluster3) > 0:
                if (centroid3 != (sum(Cluster3) / len(Cluster3))).all():
                    centroidiv3 = sum(Cluster3) / len(Cluster3)
                    centroid3 = centroidiv3.tolist()

                else:
                    lock3 = 1
            else:
                if loop_no >100:
                    lock3 = 1
            if len(Cluster4) > 0:
                if (centroid4 != (sum(Cluster4) / len(Cluster4))).all():
                    centroidiv4 = sum(Cluster4) / len(Cluster4)
                    centroid4 = centroidiv4.tolist()

                else:
                    lock4 = 1
            else:
                if loop_no >100:
                    lock4 = 1
            Dist1.clear()
            Cluster1.clear()
            Dist2.clear()
            Cluster2.clear()
            Dist3.clear()
            Cluster3.clear()
            Dist4.clear()
            Cluster4.clear()
            for x in centroids:

                Tdist1 = spatial.distance.cosine(centroid1, x)
                Tdist2 = spatial.distance.cosine(centroid2, x)
                Tdist3 = spatial.distance.cosine(centroid3, x)
                Tdist4 = spatial.distance.cosine(centroid4, x)

                if Tdist1 == min([Tdist1, Tdist2, Tdist3, Tdist4]):
                    Dist1.append(Tdist1)
                    Cluster1.append(x)
                elif Tdist2 == min([Tdist1, Tdist2, Tdist3, Tdist4]):
                    Dist2.append(Tdist2)
                    Cluster2.append(x)
                elif Tdist3 == min([Tdist1, Tdist2, Tdist3, Tdist4]):
                    Dist3.append(Tdist3)
                    Cluster3.append(x)
                elif Tdist4 == min([Tdist1, Tdist2, Tdist3, Tdist4]):
                    Dist4.append(Tdist4)
                    Cluster4.append(x)
            print('---lock---')
            print(lock1)
            print(lock2)
            print(lock3)
            print(lock4)
            loop_no = loop_no + 1
            if lock1 == 1 and lock2 == 1 and lock3 == 1 and lock4 == 1:
                print('break')
                break

        json_center = {'center1': centroid1,
                       'center2': centroid2,
                       'center3': centroid3,
                       'center4': centroid4,
                       }

        with open('center_json_data.json', 'w') as fc:
            json.dump(json_center, fc)
        fc.close()


        if os.path.isfile('meanDistance_json_data.json'):
            pfd = open('meanDistance_json_data.json')
            jdist = json.load(pfd)
            previous_dist1 = jdist['dist1']
            previous_dist2 = jdist['dist2']
            previous_dist3 = jdist['dist3']
            previous_dist4 = jdist['dist4']
            if previous_dist1 != 0:
                Dist1.append(previous_dist1)
            if previous_dist2 != 0:
                Dist2.append(previous_dist2)
            if previous_dist3 != 0:
                Dist3.append(previous_dist3)
            if previous_dist4 != 0:
                Dist4.append(previous_dist4)

        if len(Dist1) > 0:
            MeanDist1 = sum(Dist1) / len(Dist1)
        else:
            MeanDist1 = 0
        if len(Dist2) > 0:
            MeanDist2 = sum(Dist2) / len(Dist2)
        else:
            MeanDist2 = 0
        if len(Dist3) > 0:
            MeanDist3 = sum(Dist3) / len(Dist3)
        else:
            MeanDist3 = 0
        if len(Dist4) > 0:
            MeanDist4 = sum(Dist4) / len(Dist4)
        else:
            MeanDist4 = 0

        json_MeanDist={'dist1': MeanDist1,
                       'dist2': MeanDist2,
                       'dist3': MeanDist3,
                       'dist4': MeanDist4,
                       }
        with open('meanDistance_json_data.json', 'w') as fd:
            json.dump(json_MeanDist, fd)
        fd.close()

        f.close()
        fs.delete(name)
        context = {
            'center': 'centroi', 'dist': 'MeanDist'
        }
    else:
        context = {
            'filename': '', 'dist': ''}
    return render(request, 'ndex.html', context)


def evaluate(request):
    fc = open('center_json_data.json')
    jcenter= json.load(fc)
    center1 = jcenter['center1']
    center2 = jcenter['center2']
    center3 = jcenter['center3']
    center4 = jcenter['center4']
    fd = open('meanDistance_json_data.json')
    jdist = json.load(fd)
    dist1 = jdist['dist1']
    dist2 = jdist['dist2']
    dist3 = jdist['dist3']
    dist4 = jdist['dist4']
    text = request.GET['text']
    vectorizer = Vectorizer()
    vectorizer.bert(text)
    vectors_bert = vectorizer.vectors
    Tdist1 = spatial.distance.cosine( center1, vectors_bert[0])
    Tdist2 = spatial.distance.cosine(center2, vectors_bert[0])
    Tdist3 = spatial.distance.cosine(center3, vectors_bert[0])
    Tdist4 = spatial.distance.cosine(center4, vectors_bert[0])

    result = ''
    if Tdist1 < dist1:
        result = 'hatespeech'
    elif Tdist2 < dist2:
        result = 'hatespeech'
    elif Tdist3 < dist3:
        result = 'hatespeech'
    elif Tdist4 < dist4:
        result = 'hatespeech'
    else:
        result = 'not hatespeech'
    context = {
        'title': 'evaluating', 'result': result
    }
    return render(request, 'evaluate.html', context)