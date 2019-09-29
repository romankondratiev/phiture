from django.db import models
from django.db.models import Q
import itertools


class PlayerQuerySet(models.query.QuerySet): # Custom Queryset includes 2 methods: search() and build_team()
	
	# Searching with a query through lookups in all model instances
	def search(self,query): 
		lookups=(Q(name__icontains=query)
				|Q(club__icontains=query)
				|Q(nationality__icontains=query)
				)
		return self.filter(lookups).distinct()

	# Building a queryset based on a specific budget
	#  1. dividing budget by 11 
	#  2. filtering players based on the budget per player 
	#  3. defining lookups for specific categories (gk, df, mf, fw)
	#  4. building 4 querysets that meet defined lookups
	#  5. combining to 1 final queryset
	#  6. return this final queryset only if 11 players could be found with the budget
	def build_team(self,budget):

		#  1. dividing budget by 11 
		budget_for_player = budget / 11 

		#  2. filtering players based on the budget per player
		all_players_fit = self.filter(value_int__lte=budget_for_player).exclude(value_int=0) #exclude those players who have zeros in their value field

		#  3. defining lookups for specific categories (gk, df, mf, fw)
		lookups_gk=(Q(position__icontains='GK') 
				)
		lookups_df=(Q(position__icontains='DF')
				|Q(position__icontains='RCB')
				|Q(position__icontains='RWB')  	
				|Q(position__icontains='LWB')  
				|Q(position__icontains='LCB')
				|Q(position__icontains='RB')  
				|Q(position__icontains='LB') 
				|Q(position__icontains='CB') 
				)
		lookups_mf=(Q(position__icontains='MF')
				|Q(position__icontains='RAM') 
				|Q(position__icontains='CAM') 
				|Q(position__icontains='LAM') 
				|Q(position__icontains='CDM') 
				|Q(position__icontains='RCM') 
				|Q(position__icontains='RDM') 
				|Q(position__icontains='LCM') 
				|Q(position__icontains='RW')  
				|Q(position__icontains='LW')  
				|Q(position__icontains='LM')  
				|Q(position__icontains='RM')   
				|Q(position__icontains='CM')  
				|Q(position__icontains='LDM') 
				)
		lookups_fw=(Q(position__icontains='CF') 
				|Q(position__icontains='RS') 
				|Q(position__icontains='RF') 
				|Q(position__icontains='LF') 
				|Q(position__icontains='LS') 
				|Q(position__icontains='ST')  
				)

		#  4. building 4 querysets that meet defined lookups
		gk = all_players_fit.filter(lookups_gk).distinct()[:1]
		df = all_players_fit.filter(lookups_df).distinct()[:2]
		mf = all_players_fit.filter(lookups_mf).distinct()[:3]
		fw = all_players_fit.filter(lookups_fw).distinct()[:5]

		#  5. combining to 1 final queryset
		final_q = gk | df | mf | fw

		#  6. return this final queryset only if 11 players could be found with the budget
		if len(final_q) < 11:
			return None
		return final_q



class PlayerManager(models.Manager): #Custom Manager to add  methods search and build_team
	def get_queryset(self):
		return PlayerQuerySet(self.model, using=self._db)

	def search(self, query):
		return self.get_queryset().search(query)

	def build_team(self, budget):
		return self.get_queryset().build_team(budget)



class Player(models.Model):
	name 		= models.CharField(max_length=255, blank=False, null=False)
	age			= models.IntegerField(blank=False, null=False, default=0)
	photo 		= models.CharField(max_length=1000, blank=False, null=False, default='None')
	nationality = models.CharField(max_length=255, blank=False, null=False, default='None')
	overall		= models.IntegerField(blank=False, null=False, default=0)
	club		= models.CharField(max_length=255,blank=False, null=False, default='None')
	value		= models.CharField(max_length=255, blank=False, null=False, default='None')
	position	= models.CharField(max_length=255, blank=False, null=False, default='None')
	value_int 	= models.IntegerField(blank=False, null=False, default=0)

	objects = PlayerManager()

	def __str__(self):
		return self.name

