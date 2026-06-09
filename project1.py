import pandas as pd
from sqlalchemy import create_engine,inspect
engine = create_engine('mysql+pymysql://root:Sumit123%40%40@localhost/CCrashTable')
file_path = r'C:\Users\sumit\Desktop\module\Traffic_CrashesData.csv'
df=pd.read_csv(r'C:\Users\sumit\Desktop\module\Traffic_CrashesData.csv')
inspector=inspect(engine)
sql_columns=[c['name']for c in inspector.get_columns('CrashTable')]
missing_columns=[col for col in df.columns if col not in sql_columns]
print("missing column in SQL:", missing_columns)
df.to_sql(name='CrashTable',con=engine, if_exists='append',index=False)
print("Data is sucessfully transfered to MYSQL ")
print(df)


