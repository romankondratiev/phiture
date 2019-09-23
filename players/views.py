from django.shortcuts import render
from .utils import read_table
from phiture.settings import BASE_DIR
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView
from players.models import Player
from django.core.paginator import Paginator

# Create your views here.


def dataview(request):

	# table = read_table(os.path.join(BASE_DIR, 'data.csv'))

	return render(request, "players/data.html", {})


# def searchview(request):

# 	# table = read_table(os.path.join(BASE_DIR, 'data.csv'))

# 	return render(request, "players/data.html", {})





class SearchView(ListView):
	#queryset = Product.objects.all()

	template_name = "players/data.html"
	paginate_by = 10
	# def get(self, request, *args, **kwargs):
	# 	if request.is_ajax():
	# 		query=request.GET.get('q')
	# 		filtered_products = []
	# 		all_ = Product.objects.all()
	# 		all_products= []
	# 		for x in all_:
	# 			all_products.append(x.title)
				
	# 		# length = len(all_)
	# 		# for idx, x in all_:
	# 		# 	filtered_products[length-length] = x

	# 		print(filtered_products)
	# 		json_data={
	# 			"query": query,
	# 			"filtered_products": all_products,
	# 		}
	# 		return JsonResponse(json_data, status=200)
	# 	return super(SearchProductView, self).get(request, *args, **kwargs)

	# def get_context_data(self,*args,**kwargs):
	# 	context=super(SearchView,self).get_context_data(*args,**kwargs)

	# 	# user = self.request.user
		
	# 	# query=self.request.GET.get('q')
	# 	context['query']=self.request.GET.get('q')
	# 	context['user']=self.request.user
	# 	# context['wishes']= wished_products
	# 	return context

	def get_queryset(self, *args, **kwargs):
		query=self.request.GET.get('q', None)
		print(query)
		
		if query is not None:
			queryset = Player.objects.search(query)
			return Player.objects.search(query)
		queryset = Player.objects.all()
		return queryset