import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe

import pprint #package to print beauty values from spreadsheet



scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('PythonGDrive-ef00e608c87d.json', scope)
client = gspread.authorize(creds)

#Open by name
#client.open("PythonTest")

#Open by URL
doc = client.open_by_url('https://docs.google.com/spreadsheets/d/1DacaQTmkr74N6nuOqoF3z0IgG3vuG47Bb2CAHjbVVH0/edit#gid=2064706209')

#data_sheet_old = doc.worksheet('hoja1') #<class 'gspread.models.Worksheet'>
sheet = doc.sheet1 # <class 'gspread.models.Worksheet'>

#Print records
#data_sheet = sheet.get_all_records()
#pp = pprint.PrettyPrinter()
#pp.pprint(data_sheet)

customers_df = get_as_dataframe(sheet, parse_dates=True, usecols=[2,3]) #, skiprows=1, header=None)
#print (responses_df)


#Create sample data for matching
sample_str = '''Juan      Juan@yahoo.com      
AT0000386115      117.7972  
Luis      Luis@asd.com    
AT0000A04967      152.8196'''
sample_data = [line.split() for line in sample_str.split('\n')]
responses_df = pd.DataFrame(sample_data, columns='Nombre Correo_electronico'.split())
#print(sample_df)

#intersected_df = responses_df.merge(sample_df, on=['Nombre','Correo_electronico'], how='inner')
intersected_df = pd.merge(customers_df, responses_df, how='outer',indicator=True).query('_merge=="left_only"').drop('_merge',1)

print(intersected_df)