import pandas as pd 
import csv
from players.models import Player

def read_table(sometable):
	df = pd.read_csv(sometable, sep=',', usecols = ['Name', 'Age', 'Photo', 'Nationality', 'Overall','Club', 'Value','Position'])
	print(list(df))
	for index, row in df.iterrows():
		print(row['Name'], row['Age'])
		Player.objects.get_or_create(
			name=row['Name'], 
			age=row['Age'],
			photo=row['Photo'],
			nationality=row['Nationality'],
			overall=row['Overall'],
			club=row['Club'],
			value=row['Value'],
			position=row['Position'],
			)
	return df


