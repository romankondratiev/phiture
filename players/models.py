from django.db import models
from django.db.models import Q
import itertools


class PlayerQuerySet(models.query.QuerySet):
	
	def search(self,query):
		lookups=(Q(name__icontains=query)
				|Q(club__icontains=query)
				|Q(nationality__icontains=query)
				)
		return self.filter(lookups).distinct()

	def build_team(self,budget):

		budget_for_player = budget // 11  
		all_players_fit = self.filter(value_int__lte=budget_for_player).exclude(value_int=0)

		lookups_gk=(Q(position__icontains='GK')
				)
		lookups_df=(Q(position__icontains='DF')
				|Q(position__icontains='SW')
				|Q(position__icontains='RWB')
				|Q(position__icontains='LWB')
				|Q(position__icontains='RB')
				|Q(position__icontains='LB')
				|Q(position__icontains='CB')
				)
		lookups_mf=(Q(position__icontains='MF')
				|Q(position__icontains='DM')
				|Q(position__icontains='RW')
				|Q(position__icontains='LW')
				|Q(position__icontains='LM')
				|Q(position__icontains='RM')
				|Q(position__icontains='CM')
				|Q(position__icontains='AM')
				)
		lookups_fw=(Q(position__icontains='CF')
				|Q(position__icontains='FW')
				|Q(position__icontains='RF')
				|Q(position__icontains='LF')
				|Q(position__icontains='ST')
				)

		gk = all_players_fit.filter(lookups_gk).distinct()[:1]
		df = all_players_fit.filter(lookups_df).distinct()[:2]
		mf = all_players_fit.filter(lookups_mf).distinct()[:3]
		fw = all_players_fit.filter(lookups_fw).distinct()[:5]

		all_ = gk.union(df, mf, fw)
		final_q = gk | df | mf | fw
		if len(final_q) < 11:
			return None

		return final_q




class PlayerManager(models.Manager):
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

