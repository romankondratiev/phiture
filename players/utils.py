import pandas as pd 
import csv
from players.models import Player


def turn_to_int(value): #Used to turn Market Value field to a integer
    s = value
    s = s[1:]
    last = s[-1]
    if last == 'M':
        s = s[:-1]
        if '.' in s:
            s = s.replace('.','')
            s = s + '00000'
        else:
            s = s + '000000'
    if last == 'K':
        s = s[:-1]
        if '.' in s:
            s = s.replace('.','')
            s = s + '00'
        else:
            s = s + '000'
    return int(s)



def read_table(sometable): # To populate database with data from .csv file
	df = pd.read_csv(sometable, sep=',', usecols = ['Name', 'Age', 'Photo', 'Nationality', 'Overall','Club', 'Value','Position'])
	for index, row in df.iterrows():
		Player.objects.get_or_create(
			name=row['Name'], 
			age=row['Age'],
			photo=row['Photo'],
			nationality=row['Nationality'],
			overall=row['Overall'],
			club=row['Club'],
			value=row['Value'],
			position=row['Position'],
			value_int=turn_to_int(row['Value']),
			)
	return df