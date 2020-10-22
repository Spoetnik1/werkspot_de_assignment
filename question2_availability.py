import pandasql as ps
import pandas as pd

# Read csv and do some transformations
df = pd.read_csv('event_log.csv', sep=';')
df = df.rename(columns={"professional_id_anonymized": "prof_id", "created_at": "timestamp"})
df = df[['event_id', 'event_type', 'prof_id', 'timestamp']]
df['timestamp'] = pd.to_datetime(df.timestamp, format='%Y-%m-%d %H:%M:%S')
df['date'] = df.timestamp.dt.date

date_vec = pd.DataFrame({'date': pd.date_range('2020-01-01', periods=70, freq='d').date})

# Take the last event of the day, to deal with multiple entries in a single day
q1 = """
SELECT 
prof_id
, event_type
, date
, MAX(timestamp) AS timestamp
FROM df
WHERE event_type IN ('became_able_to_propose', 'became_unable_to_propose')
GROUP BY
prof_id
,event_type
,date
"""
aap = ps.sqldf(q1, locals())

### Create a table like [prof_id, current_event, next_event, current_event_date, next_event_date]
### Add dummy date and dummy 'became_unable_to_propose' to handle currently available professionals
q1 = """SELECT 
prof_id
, event_type AS current_event
, COALESCE(LEAD(event_type) OVER (PARTITION BY prof_id ORDER BY timestamp ASC), 'became_unable_to_propose') AS next_event
, date AS current_event_date
, COALESCE(LEAD(date) OVER (PARTITION BY prof_id ORDER BY timestamp ASC), '9999-03-10') AS next_event_date 
FROM aap
"""
aap = ps.sqldf(q1, locals())

### Take only 
q1 = """SELECT 
DISTINCT prof_id
, current_event_date AS start_date
, next_event_date AS end_date
FROM aap
WHERE current_event = 'became_able_to_propose'
"""
aap = ps.sqldf(q1, locals())

### Date scaffolding
q1 = """SELECT 
date_vec.date
, COUNT( DISTINCT aap.prof_id) AS active_count
FROM date_vec
LEFT JOIN aap
ON date_vec.date >= aap.start_date AND date_vec.date < end_date
GROUP BY date
ORDER BY date ASC
"""
availability = ps.sqldf(q1, locals())

availability.to_csv('availability_snapshot.csv', index=False)