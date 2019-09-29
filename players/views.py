from django.shortcuts import render
from .utils import read_table
from phiture.settings import BASE_DIR
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView
from players.models import Player
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import TeamForm
from django.views.generic.edit import FormView
from django.db.models import Avg


# SearchView https://phiture.herokuapp.com/search
class SearchView(ListView):
	template_name = "players/search.html"
	paginate_by = 10
	
	# To populate empty database with data from .csv file
	#table = read_table(os.path.join(BASE_DIR, 'data.csv')) 

	def get_queryset(self, *args, **kwargs):
		query=self.request.GET.get('q', None)
		if query is not None:
			queryset = Player.objects.search(query)
			return Player.objects.search(query)
		queryset = Player.objects.all()
		return queryset


# HomeView https://phiture.herokuapp.com/
class HomeView(FormView): 
	template_name = "players/home.html"
	form_class = TeamForm
	success_url = '/team'

	def form_valid(self, form):
		self.request.session['budget'] = form.cleaned_data.get('budget') #saving user input in current session
		return super(HomeView, self).form_valid(form)


# TeamView https://phiture.herokuapp.com/team
class TeamView(ListView): 
	template_name = "players/team.html"

	def get_queryset(self, *args, **kwargs):
		user_input=self.request.session['budget']
		if user_input is not None:
			queryset = Player.objects.build_team(user_input)
			return queryset
		queryset = None
		return queryset

	def get_context_data(self, *args, **kwargs): 
		context = super(TeamView, self).get_context_data(*args, **kwargs)  
		context['budget'] = self.request.session['budget']
		qs = self.get_queryset()
		if qs is not None:
			context['avg'] = qs.aggregate(Avg('overall'))
		return context


