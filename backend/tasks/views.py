from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import date, datetime
import json

from .serializers import TaskInputSerializer
from .scoring import score_task, DEFAULT_WEIGHTS, detect_circular_dependencies

def index(request):
    return JsonResponse({'message':'Tasks API backend is working.'})

def _assign_ids(tasks):
    out=[]
    for i,t in enumerate(tasks,1):
        nt=dict(t); nt.setdefault('id',i); out.append(nt)
    return out

def _weights(s):
    return DEFAULT_WEIGHTS.get((s or 'smart').lower(), DEFAULT_WEIGHTS['smart'])

@api_view(['POST'])
def analyze_tasks(request):
    if not isinstance(request.data,list):
        return Response({'error':'Expected a JSON list.'},400)
    w=_weights(request.query_params.get('strategy'))
    valid=[]
    for item in request.data:
        ser=TaskInputSerializer(data=item)
        if not ser.is_valid(): return Response({'error':'Invalid task','details':ser.errors},400)
        valid.append(ser.validated_data)
    valid=_assign_ids(valid)
    graph={t['id']:t.get('dependencies',[]) for t in valid}
    cycles=detect_circular_dependencies(graph)
    cyc_ids={n for c in cycles for n in c}
    out=[]
    for t in valid:
        s,exp=score_task(t,weights=w)
        if t['id'] in cyc_ids: s*=0.6; exp+=' | circular_dependency'
        due=t.get('due_date')
        if isinstance(due,str):
            try: due=datetime.fromisoformat(due).date()
            except: pass
        if isinstance(due,date) and due<date.today(): exp+=' | past_due'
        nt=dict(t); nt['score']=s; nt['explanation']=exp; out.append(nt)
    out.sort(key=lambda x:x['score'], reverse=True)
    return Response(out)

@api_view(['GET','POST'])
def suggest_tasks(request):
    w=_weights(request.query_params.get('strategy'))
    top=int(request.query_params.get('top',3))
    if request.method=='POST': data=request.data
    else:
        raw=request.query_params.get('tasks')
        if not raw: return Response({'error':'Provide tasks.'},400)
        try: data=json.loads(raw)
        except: return Response({'error':'Invalid tasks JSON.'},400)
    valid=[]
    for item in data:
        ser=TaskInputSerializer(data=item)
        if not ser.is_valid(): return Response({'error':'Invalid task','details':ser.errors},400)
        valid.append(ser.validated_data)
    valid=_assign_ids(valid)
    graph={t['id']:t.get('dependencies',[]) for t in valid}
    cycles=detect_circular_dependencies(graph)
    cyc_ids={n for c in cycles for n in c}
    scored=[]
    for t in valid:
        s,exp=score_task(t,weights=w)
        if t['id'] in cyc_ids: s*=0.6; exp+=' | circular_dependency'
        scored.append({'id':t['id'],'title':t['title'],'score':s,'explanation':exp})
    scored.sort(key=lambda x:x['score'],reverse=True)
    return Response(scored[:top])
