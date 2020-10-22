import mysql.connector
from sqlalchemy import create_engine
import pandas as pd

# sqlalchemy and pymsql for running Pandas integration.
db_connection_str = 'mysql+pymysql://root:root@127.0.0.1/professional_activity'
db_connection = create_engine(db_connection_str)

### Extract data and apply basic transformations
df = pd.read_csv('event_log.csv', sep=';')
df = df.rename(columns={"professional_id_anonymized": "prof_id_anonymized", "created_at": "time_stamp"})
df['time_stamp'] = pd.to_datetime(df.time_stamp, format='%Y-%m-%d %H:%M:%S')

### Perform required transformations
df_proposals = df[df.event_type == 'proposed']
df_proposals.meta_data = df_proposals.meta_data.str.replace('-', ' ')
df_proposals[['service_id', 
              'name_nl', 
              'name_en', 
              'lead_fee']] = df_proposals.meta_data.str.split('_',expand=True) 

df_services = df_proposals[['service_id', 
                            'name_nl', 
                            'name_en']].drop_duplicates()

df_proposals = df_proposals[['event_id', 
                             'prof_id_anonymized', 
                             'service_id', 
                             'lead_fee', 
                             'time_stamp']]

df_account_activity = df[df.event_type.isin(['created_account', 
                                             'became_able_to_propose', 
                                             'became_unable_to_propose'])]
df_account_activity = df_account_activity.drop('meta_data', axis=1)

### Load resutls to MySQL
df_account_activity.to_sql('account_status_events', 
                           con=db_connection, 
                           if_exists='append', 
                           chunksize=1000, 
                           index=False)

df_services.to_sql('services_info', 
                   con=db_connection, 
                   if_exists='append', 
                   chunksize=1000, 
                   index=False)

df_proposals.to_sql('proposal_events', 
                   con=db_connection, 
                   if_exists='append', 
                   chunksize=1000, 
                   index=False)