from django.shortcuts import render, get_object_or_404
from .models import Orphan, Article, OrphanInstance
from django.views import generic
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from extra_views import CreateWithInlinesView
from .forms import InstanceInline

# Create your views here.

def index(request):
	#View function for home page of site

	#Generate counts of som eof the main objects
	num_orphans=Orphan.objects.all().count()
	num_instances = OrphanInstance.objects.all().count()
	#Available orphans(status = 'a')
	num_instances_available=OrphanInstance.objects.filter(status='a').count()
	num_articles=Article.objects.count() #The 'all()' is implied

	#Number of visits to this view, as counted in the session variable
	num_visits=request.session.get('num_visits',0)
	request.session['num_visits'] = num_visits + 1
	#Render the HTML template index.html with the data in the context variable
	return render(
		request,
		'index.html',
		context={'num_orphans':num_orphans, 'num_instances':num_instances,'num_instances_available':num_instances_available,'num_articles':num_articles, 'num_visits':num_visits},

		)

class OrphanListView(generic.ListView):
	model = Orphan

class OrphanDetailView(generic.DetailView):
	model = Orphan

class ArticleListView(generic.ListView):
	model = Article

class ArticleDetailView(generic.DetailView):
	model = Article

class AddArticle(CreateView):
	model = Article
	fields = '__all__'


class AddOrphan(CreateWithInlinesView):
	model = Orphan
	fields = '__all__'
	#field_order - {'orphan','status','date'}
	initial = {'date': datetime.datetime.strftime(datetime.datetime.today(),"%m/%d/%Y")}
	inlines = [InstanceInline]
	def clean_boxNum(self):
		data = self.cleaned_data['boxNum']
		if data > self.article.totBoxes:
			raise ValidationError(_('Invalid Box Number: Box Number Greater Than Total Boxes in Article'))