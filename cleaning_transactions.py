import pandas as pd
import numpy as np
from sqlalchemy import create_engine
save_to_CSV =True
Save_to_DB =True


df= pd.read_csv("C:\\Users\\first\\Desktop\\Puthon Revision\\transaction.csv")



# Database connection details
DB_USER = "postgres"
DB_PASSWORD = "Aspirine68%23"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "Financial Pipeline"

print(df.head())
print(df.shape)
print(df.columns)
print(df.info())

#converting timestamp to standard date format
df['timestamp']=pd.to_datetime(df['timestamp'])
print(df.head())

#checking for number of missing values
df.isnull().sum()

#checking for duplicate values
df.duplicated().sum()

#column standardization
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
#cleaning transaction_types
df['transaction_type']=df['transaction_type'].str.strip().str.lower()
#cleaning location column
df['location'] = df['location'].str.strip().str.title()


#creating new columns for data categorization
#high value flag
high_value_threshold=10000
df['is high value']=df['amount'] > high_value_threshold

#Extracting hour
df['hour'] = df['timestamp'].dt.hour

start_hour=6
end_hour=22

#defining unusual columns
df['is_unusual_time'] = (df['hour'] < start_hour) | (df['hour'] > end_hour)

if save_to_CSV:
    df.to_csv('cleaned_transctions.csv', index=False)
    print(f"cleaned data saved to cleaned_transations.csv")

if Save_to_DB:
  engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

df.to_sql("staging_transactions", engine, if_exists="replace", index=False)
print("cleaned data loaded into postgres")

print(df.head())



