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



class SearchView(ListView):
	template_name = "players/search.html"
	paginate_by = 10
	
	#table = read_table(os.path.join(BASE_DIR, 'data.csv'))

	def get_queryset(self, *args, **kwargs):
		query=self.request.GET.get('q', None)
		if query is not None:
			queryset = Player.objects.search(query)
			return Player.objects.search(query)
		queryset = Player.objects.all()
		return queryset



class HomeView(FormView):
	template_name = "players/home.html"
	paginate_by = 10
	form_class = TeamForm
	success_url = '/team'

	def form_valid(self, form):
		budget = form.cleaned_data.get('budget')
		self.request.session['bla'] = form.cleaned_data.get('budget')
		return super(HomeView, self).form_valid(form)



class TeamView(ListView): # Go to Result if team is found
	template_name = "players/team.html"

	def get_queryset(self, *args, **kwargs):
		budget=self.request.session['bla']
		if budget is not None:
			queryset = Player.objects.build_team(budget)
			return Player.objects.build_team(budget)
		queryset = None
		return queryset

	def get_context_data(self, *args, **kwargs): #overwrite method
		context = super(TeamView, self).get_context_data(*args, **kwargs)  #default method
		context['budget'] = self.request.session['bla']
		qs = self.get_queryset()
		if qs is not None:
			context['avg'] = qs.aggregate(Avg('overall'))
		return context


