"""Behavioral tests for this standalone analytical project."""
import importlib.util,math,sqlite3,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from common import queries

def module(slug):
    spec=importlib.util.spec_from_file_location(slug,ROOT/'analyze.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def fixture(slug,table,rows):
    m=module(slug);db=sqlite3.connect(':memory:');db.row_factory=sqlite3.Row
    db.execute('CREATE TABLE '+table+' ('+m.SCHEMA+')')
    db.executemany('INSERT INTO '+table+' VALUES ('+','.join('?' for _ in rows[0])+')',rows)
    return queries(db,ROOT/'analysis.sql')

class AnalystTests(unittest.TestCase):
    def test_cohort_age_and_churn_bridge(self):
        t=fixture('02-customer-retention','subscriptions',[
          ('a','2025-01','2025-01',0,'Paid','Basic',1,2900),
          ('a','2025-01','2025-02',1,'Paid','Basic',0,0),
          ('b','2025-02','2025-02',0,'Organic','Basic',1,2900)])
        feb=t['monthly_bridge'][1]
        self.assertEqual((feb['opening_mrr'],feb['new_mrr'],feb['churned_mrr'],feb['closing_mrr']),(29,29,29,29))
        self.assertEqual(feb['logo_churn_pct'],100)
        self.assertFalse(any(r['signup_month']=='2025-02' and r['age_month']==1 for r in t['cohort_retention']))
    def test_full_analysis_runs_and_exports(self):
        result=module('standalone').run()
        self.assertTrue(result)
        self.assertTrue((ROOT/'index.html').is_file())
        self.assertTrue((ROOT/'results/metrics.json').is_file())
if __name__=='__main__':unittest.main()
