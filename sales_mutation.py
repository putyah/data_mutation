import pandas as pd
from functools import reduce

df = pd.read_excel (r'sales.xls')

#Change date format + new column
df['Purchase Date Day'] = df['Purchase Date'] 
df['Purchase Hour'] = df['Purchase Date'].str.replace(r'.*2021 ', '')
df['Purchase Year'] = df['Purchase Date'].str.replace(r'.*, ', '')
df['Purchase Year'] = df['Purchase Year'].str.replace(r' .*', '')
df['Purchase Day'] = df['Purchase Date'].str.replace(r',.*', '')
df['Purchase Day'] = df['Purchase Day'].str.replace(r'.* ', '')
df['Purchase Month'] = df['Purchase Date'].str.replace(r' .*', '')
df['Purchase Date Day'] = df['Purchase Day'] + df['Purchase Month'] + df['Purchase Year']

df['Purchase Date Day'] = pd.to_datetime(df['Purchase Date Day'], format='%d%b%Y')
df['Purchase Hour'] = pd.to_datetime(df['Purchase Hour'], format='%I:%M:%S %p')



#Calculate ex taxes + new column
df.loc[df['Customer Group'] == 57, 'Omzet'] = df['Grand Total (Purchased)']
df.loc[df['Customer Group'] != 57, 'Omzet'] = (df['Grand Total (Purchased)'] / 1.21)

#Zakelijke omzet
df.loc[df['Customer Group'] == 58, 'Zakelijke_omzet'] = (df['Grand Total (Purchased)'] / 1.21)
df.loc[df['Customer Group'] == 57, 'Zakelijke_omzet'] = df['Grand Total (Purchased)']
df['Zakelijke_omzet'] = df['Zakelijke_omzet'].fillna(0)
df['Zakelijke_omzet'] = df['Zakelijke_omzet'].round(0)
df['Omzet'] = df['Omzet'].round(0)

#Remove different status
indexNames = df[df['Status'] == 'canceled'].index
df.drop(indexNames , inplace=True)
indexNames = df[df['Status'] == 'closed'].index
df.drop(indexNames , inplace=True)

#Set date as index
revenue_pv = df.groupby(['Purchase Date Day']).Omzet.sum().reset_index()
order_pv = df.groupby(['Purchase Date Day']).Status.count().reset_index()
revenue_zak_pv = df.groupby(['Purchase Date Day']).Zakelijke_omzet.sum().reset_index()
order_zak_pv = df.groupby(['Purchase Date Day']).Zakelijke_omzet.count().reset_index()

#Combine data
df_col = pd.concat([revenue_pv,order_pv,revenue_zak_pv,order_zak_pv], axis=1)

data_frames = [revenue_pv,order_pv,revenue_zak_pv,order_zak_pv]
df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Purchase Date Day'], how='outer'), data_frames)

#Change column name
df_merged.rename(columns={'Status':'Orders', 'Zakelijke_omzet_x':'Zakelijke_omzet','Zakelijke_omzet_y':'Order zakelijk'}, inplace=True)
df.sort_values(by=['Purchase Date Day'])

df_merged.to_csv (r'sales.csv', index = False, header=True)

print(df_merged)

#print(df_merged)
