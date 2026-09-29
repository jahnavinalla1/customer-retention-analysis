import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import database,queries,publish
F=Path(__file__).resolve().parent
SCHEMA='customer_id TEXT,signup_month TEXT,month TEXT,age_month INTEGER CHECK(age_month>=0),channel TEXT,plan TEXT,active INTEGER CHECK(active IN(0,1)),mrr_cents INTEGER CHECK(mrr_cents>=0),PRIMARY KEY(customer_id,month)'
def run():
    db=database(F,'subscriptions',SCHEMA);t=queries(db,F/'analysis.sql');last=t['monthly_bridge'][-1];c=t['channel_month6'];worst=c[0]
    assert db.execute('SELECT COUNT(DISTINCT customer_id) FROM subscriptions').fetchone()[0]==360
    for r in t['monthly_bridge']:assert abs(r['opening_mrr']+r['new_mrr']-r['churned_mrr']-r['closing_mrr'])<.001
    assert db.execute('SELECT COUNT(*) FROM subscriptions WHERE (active=0 AND mrr_cents!=0) OR (age_month=0 AND active!=1)').fetchone()[0]==0
    six=100*sum(r['retained'] for r in c)/sum(r['eligible_customers'] for r in c)
    publish(F,'Customer cohorts and recurring revenue','Which acquisition cohorts need a retention investigation?',
    {'Customers':'360','Month 6 retention':f'{six:.1f}%','December MRR':f"${last['closing_mrr']:,.0f}",'December logo churn':f"{last['logo_churn_pct']:.1f}%"},t,
    [f"{worst['channel']} has the lowest observed month-6 retention ({worst['retention_pct']}%, n={worst['eligible_customers']}).",
     f"December revenue reconciles: ${last['opening_mrr']:,.0f} opening + ${last['new_mrr']:,.0f} new − ${last['churned_mrr']:,.0f} churn = ${last['closing_mrr']:,.0f} closing MRR.",
     'Cohorts are compared at equal customer age, avoiding comparisons between immature and mature cohorts.'],
    ['Audit acquisition expectations and onboarding for the lowest-retention channel.',
     'Run a controlled onboarding pilot; use age-3 retention as its outcome and support volume as a guardrail.',
     'Assign customer success ownership of the monthly MRR reconciliation and investigate any unmatched changes.'],
    'Synthetic subscription snapshots through December 2025. No reactivation, expansion or downgrades are modeled. The month-6 comparison only includes customers observed at that age. Channel differences are descriptive and may reflect selection; they do not establish acquisition-channel effects.',
    {'title':'Month 6 retention by acquisition channel','note':'Active customers divided by customers with a complete month-6 observation.','unit':'%',
     'rows':[{'label':r['channel'],'value':r['retention_pct']} for r in c]})
    return t
if __name__=='__main__':run()
