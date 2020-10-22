from sqlalchemy import create_engine
import pandasql as ps
import pandas as pd

# Create SQL engine for pandas <> MySQL integration
db_connection_str = 'mysql+pymysql://root:root@127.0.0.1/professional_activity'
db_connection = create_engine(db_connection_str)

df_proposals = pd.read_sql_query(
            """SELECT * FROM professional_activity.proposal_events""",
            db_connection)
df_proposals.to_csv('proposal_events.csv', index=False)

df_services = pd.read_sql_query(
            """SELECT * FROM professional_activity.services_info""",
            db_connection)
df_services.to_csv('services_info.csv', index=False)

df_account_status = pd.read_sql_query("""SELECT * FROM professional_activity.account_status_events""", 
            db_connection)
df_account_status.to_csv('account_status_events.csv', index=False)