from django.test import TestCase
from .scoring import score_task, detect_circular_dependencies
from datetime import date, timedelta

class ScoringTests(TestCase):
    def test_past_due(self):
        t={'title':'A','due_date':(date.today()-timedelta(days=2)).isoformat(),
           'estimated_hours':2,'importance':5,'dependencies':[]}
        s,e=score_task(t)
        self.assertGreater(s,0)

    def test_zero_effort(self):
        t={'title':'B','due_date':None,'estimated_hours':0,'importance':5,'dependencies':[]}
        s,e=score_task(t)
        self.assertGreaterEqual(s,0)

    def test_cycles(self):
        g={1:[2],2:[3],3:[1]}
        cyc=detect_circular_dependencies(g)
        self.assertTrue(len(cyc)>0)
