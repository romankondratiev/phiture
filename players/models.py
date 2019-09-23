from django.db import models
from django.db.models import Q


class PlayerQuerySet(models.query.QuerySet):
	def search(self,query):
		lookups=(Q(name__icontains=query)
				|Q(club__icontains=query)
				|Q(nationality__icontains=query)
				)
		return self.filter(lookups).distinct()

class PlayerManager(models.Manager):
	def get_queryset(self):
		return PlayerQuerySet(self.model, using=self._db)

	def search(self, query):
		return self.get_queryset().search(query)

# Create your models here.
class Player(models.Model):
	name 		= models.CharField(max_length=255, blank=False, null=False)
	age			= models.IntegerField(blank=False, null=False, default=0)
	photo 		= models.CharField(max_length=1000, blank=False, null=False, default='None')
	nationality = models.CharField(max_length=255, blank=False, null=False, default='None')
	overall		= models.IntegerField(blank=False, null=False, default=0)
	club		= models.CharField(max_length=255,blank=False, null=False, default='None')
	value		= models.CharField(max_length=255, blank=False, null=False, default='None')
	position	= models.CharField(max_length=255, blank=False, null=False, default='None')

	objects = PlayerManager()

	def __str__(self):
		return self.name

