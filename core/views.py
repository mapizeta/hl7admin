from django.shortcuts import render
from django.http import HttpResponse
from hl7apy import parser
from hl7apy.core import Group, Segment
from hl7apy.exceptions import UnsupportedVersion


def index(request):
    context = {}
    return render(request, 'core/form.html', context)

def process(request):
    msg = request.POST['msg']
    context = {'hl7':showSegments(msg)}
    return render(request, 'core/process.html', context)

def segmentChildrenName(segment):
    listChildren = {segment.name:[]}
    level = ''
    for iterator in segment.children:
        if level != iterator.datatype:
            listChildren[segment.name].append(iterator.datatype)
            level = iterator.datatype 
    return listChildren

def comparaHl7(msg1, msg2):
    for segment in msg1:
        key = list(segment)[0]
        print(key)
        for segment2 in msg2:
            if key == list(segment2)[0]:
                #print(segment2[key])
                print([i for i, j in zip(segment[key], segment2[key]) if i == j])

def showSegments(msg):
    data = ''
    msgParsed = parser.parse_message(msg.replace('\n', '\r'), find_groups=False, validation_level=2)
    for m in msgParsed.children:
        cont = 0
        data += m.name
        #print(m.name,end='\n')
        for component in m.children:
            cont +=1
            data += str(cont)+' '+component.reference[3]+':'+component.value 
            #print(str(cont)+' '+component.reference[3]+':'+component.value)
    return data