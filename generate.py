import random,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import write_csv

def generate():
    rng=random.Random(2202);rows=[]
    # Complete monthly snapshots; a churned account stays inactive (no reactivation).
    for i in range(360):
        start=rng.randrange(6);plan=rng.choice(['Basic','Pro']);channel=rng.choice(['Organic','Paid','Referral']);active=1
        for m in range(start,12):
            if m>start and active:active=int(rng.random()>({'Organic':.065,'Paid':.12,'Referral':.04}[channel]))
            rows.append(dict(customer_id=f'C{i:04}',signup_month=f'2025-{start+1:02}',month=f'2025-{m+1:02}',
              age_month=m-start,channel=channel,plan=plan,active=active,mrr_cents=(2900 if plan=='Basic' else 7900)*active))
    write_csv(Path(__file__).with_name('data.csv'),rows)
if __name__=='__main__':generate()
