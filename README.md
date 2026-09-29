# Customer cohorts and recurring revenue

**Independent portfolio case study · simulated data · no client affiliation**

SQL windows · cohort analysis · revenue reconciliation

[Interactive dashboard](https://jahnavinalla1.github.io/analytics-projects/02-customer-retention/) · [Decision memo](results/report.md) · [SQL](analysis.sql) · [Python](analyze.py)

## Business problem

A subscription business needs an acquisition-quality view and an auditable monthly recurring-revenue bridge.

## Reproduce

This is a self-contained repository. Python 3.10+ is the only dependency; no shared portfolio repository, API key, or third-party package is required.

```sh
git clone https://github.com/jahnavinalla1/customer-retention-analysis.git
cd customer-retention-analysis
python3 run.py
```

`run.py` regenerates the seeded dataset, rebuilds the dashboard and reports, and executes the tests. To analyze the included CSV without replacing it:

```sh
python3 analyze.py
python3 -m unittest discover -s tests -v
```

Open `index.html` in your browser to explore the dashboard. Its data is embedded, so no server is needed. The [hosted demo](https://jahnavinalla1.github.io/analytics-projects/02-customer-retention/) is also linked from the portfolio. `generate.py` intentionally overwrites `data.csv` with the same simulated sample; `analyze.py` only reads it and rebuilds outputs.

## Data and provenance

One customer-month snapshot per row for 360 customers acquired January–June 2025; observed through December. Seed 2202. Inactive customers remain in the dataset. Data is authored by the deterministic generator in this folder. It contains no real people, company transactions, or external source material. Patterns in the simulation are intentionally constructed for analytical practice; they are not evidence about actual markets or employers.

| Field | Meaning |
|---|---|
| `customer_id` | Customer key |
| `signup_month` | Acquisition cohort, YYYY-MM |
| `month` | Snapshot month, YYYY-MM |
| `age_month` | Months since signup, with signup at age 0 |
| `channel` | Organic, Paid or Referral |
| `plan` | Basic or Pro; fixed over the observation window |
| `active` | 1 if subscribed at snapshot, else 0 |
| `mrr_cents` | Monthly recurring revenue; 0 when inactive |

## Metric contract and method

Retention at age t = active accounts / observed accounts at that age. The generator emits all age-eligible snapshots including inactive accounts; missing rows in a new source must not silently remove churners. Logo churn = accounts that became inactive / opening active accounts. Closing MRR = opening + new − churned; expansion and reactivation are outside this model.

`analysis.sql` is the actual executed SQL, not a decorative example. Python loads the CSV into constrained in-memory SQLite tables, executes named SQL blocks, validates key invariants, calculates any statistical/scenario outputs, and renders the result files. No network, API key, or paid BI license is needed.

## Stakeholders and decision ownership

Customer success owns onboarding investigation; finance owns the MRR bridge; marketing owns channel definitions.

## Data quality and acceptance

Customer-month keys must be unique; age-0 retention is 100%; all MRR bridges balance. Only observed ages appear; future cohort ages must be blank rather than zero.

## Deliverables

- `data.csv`: complete reproducible source dataset.
- `generate.py`: seeded data-generation logic and business assumptions.
- `analysis.sql` / `analyze.py`: executable analytical logic.
- `index.html`: portable interactive dashboard with filtering and sorting.
- `results/metrics.json` and result CSVs: machine-readable, exportable outputs.
- `results/report.md`: computed findings, recommended actions and limitations.

## Interpretation

Read the decision memo for the actual computed results. Recommendations are proposals for a future pilot; no employer outcome, production deployment, cash saving, or measured improvement is claimed. Replacing the synthetic source requires revisiting schema constraints, hardcoded fixture sizes, missing-data policies and the metric contract.
