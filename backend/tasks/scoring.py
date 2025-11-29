from datetime import date, datetime

DEFAULT_WEIGHTS={
 'smart':{'urgency':0.4,'importance':0.4,'effort':0.1,'dependency':0.1},
 'fastest':{'urgency':0.2,'importance':0.2,'effort':0.5,'dependency':0.1},
 'high-impact':{'urgency':0.2,'importance':0.6,'effort':0.1,'dependency':0.1},
 'deadline':{'urgency':0.6,'importance':0.2,'effort':0.1,'dependency':0.1},
}

def parse_date(d):
    if d is None: return None
    if isinstance(d,date): return d
    if isinstance(d,str):
        try: return datetime.fromisoformat(d).date()
        except: return None
    return None

def detect_circular_dependencies(graph):
    visited={}; stack={}; cycles=[]
    def dfs(n,path):
        visited[n]=True; stack[n]=True; path.append(n)
        for nxt in graph.get(n,[]):
            if nxt not in graph: continue
            if not visited.get(nxt): dfs(nxt,path)
            elif stack.get(nxt):
                if nxt in path:
                    i=path.index(nxt); cycles.append(path[i:]+[nxt])
        stack[n]=False; path.pop()
    for k in graph:
        if not visited.get(k): dfs(k,[])
    return cycles

def score_task(t,weights=None,today=None):
    if weights is None: weights=DEFAULT_WEIGHTS['smart']
    if today is None: today=date.today()
    due=parse_date(t.get('due_date'))
    urgency=0
    if due:
        d=(due-today).days
        urgency=10+abs(d) if d<0 else max(0,10-d)
    imp=max(1,min(10,float(t.get('importance',5))))
    eff=float(t.get('estimated_hours',1)) or 0.5
    eff_score=min(10,10/eff)
    dep_score=min(10,len(t.get('dependencies',[]))*2)
    s=urgency*weights['urgency']+imp*weights['importance']+eff_score*weights['effort']+dep_score*weights['dependency']
    expl=f"urgency={urgency},importance={imp},effort_score={eff_score},dependency_score={dep_score}"
    return round(s,2), expl
