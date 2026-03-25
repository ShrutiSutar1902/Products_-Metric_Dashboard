import pandas as pd
from datetime import timedelta

# -----------------------------
# 1. Load Data (Provide your CSV files)
# -----------------------------
users = pd.read_csv('users.csv')
activity = pd.read_csv('activity.csv')

# -----------------------------
# 2. Data Cleaning
# -----------------------------
users['signup_date'] = pd.to_datetime(users['signup_date'])
activity['activity_date'] = pd.to_datetime(activity['activity_date'])

# -----------------------------
# 3. User Growth (Monthly)
# -----------------------------
user_growth = users.groupby(users['signup_date'].dt.to_period('M')).size()
print("\nUser Growth (Monthly):\n", user_growth)

# -----------------------------
# 4. Active Users (DAU / MAU)
# -----------------------------
# DAU (latest date)
latest_date = activity['activity_date'].max()
dau = activity[activity['activity_date'] == latest_date]['user_id'].nunique()
print("\nDAU:", dau)

# MAU
mau = activity.groupby(activity['activity_date'].dt.to_period('M'))['user_id'].nunique()
print("\nMAU:\n", mau)

# -----------------------------
# 5. Retention Analysis (Cohort)
# -----------------------------
users['cohort'] = users['signup_date'].dt.to_period('M')
activity = activity.merge(users[['user_id', 'cohort']], on='user_id')

activity['activity_month'] = activity['activity_date'].dt.to_period('M')
activity['cohort_index'] = (activity['activity_month'] - activity['cohort']).apply(lambda x: x.n)

cohort_data = activity.groupby(['cohort', 'cohort_index'])['user_id'].nunique().reset_index()
cohort_pivot = cohort_data.pivot(index='cohort', columns='cohort_index', values='user_id')

print("\nCohort Retention Table:\n", cohort_pivot)

# -----------------------------
# 6. Churn Calculation
# -----------------------------
last_30_days = latest_date - timedelta(days=30)

active_recent_users = activity[activity['activity_date'] >= last_30_days]['user_id'].unique()

churned_users = users[~users['user_id'].isin(active_recent_users)]
churn_rate = len(churned_users) / len(users)

print("\nChurn Rate:", churn_rate)

# -----------------------------
# 7. Export for Power BI
# -----------------------------
user_growth.to_csv('user_growth.csv')
mau.to_csv('mau.csv')
cohort_pivot.to_csv('cohort_retention.csv')

print("\nAnalysis completed. Files ready for Power BI!")
