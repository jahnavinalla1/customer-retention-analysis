-- name: cohort_retention
SELECT signup_month,age_month,COUNT(*) cohort_size,SUM(active) retained,
 ROUND(100.0*SUM(active)/COUNT(*),2) retention_pct
FROM subscriptions GROUP BY signup_month,age_month ORDER BY signup_month,age_month;
-- name: channel_month6
SELECT channel,COUNT(*) eligible_customers,SUM(active) retained,
 ROUND(100.0*SUM(active)/COUNT(*),2) retention_pct
FROM subscriptions WHERE age_month=6 GROUP BY channel ORDER BY retention_pct;
-- name: monthly_bridge
WITH previous AS (
 SELECT *,LAG(active) OVER(PARTITION BY customer_id ORDER BY month) prev_active,
 LAG(mrr_cents) OVER(PARTITION BY customer_id ORDER BY month) prev_mrr
 FROM subscriptions
)
SELECT month,
 ROUND(SUM(COALESCE(prev_mrr,0))/100.0,2) opening_mrr,
 ROUND(SUM(CASE WHEN prev_active IS NULL THEN mrr_cents ELSE 0 END)/100.0,2) new_mrr,
 ROUND(SUM(CASE WHEN prev_active=1 AND active=0 THEN prev_mrr ELSE 0 END)/100.0,2) churned_mrr,
 ROUND(SUM(mrr_cents)/100.0,2) closing_mrr,
 SUM(CASE WHEN prev_active=1 THEN 1 ELSE 0 END) opening_customers,
 SUM(CASE WHEN prev_active=1 AND active=0 THEN 1 ELSE 0 END) churned_customers,
 ROUND(100.0*SUM(CASE WHEN prev_active=1 AND active=0 THEN 1 ELSE 0 END)/
 NULLIF(SUM(CASE WHEN prev_active=1 THEN 1 ELSE 0 END),0),2) logo_churn_pct
FROM previous GROUP BY month ORDER BY month;
