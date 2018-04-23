from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('orphans/', views.OrphanListView.as_view(), name='orphans'),
	path('orphans/create', views.AddOrphan.as_view(), name='orphan-create'),
	path('orphans/<int:pk>', views.OrphanDetailView.as_view(), name='orphan-detail'),
	path('articles/', views.ArticleListView.as_view(), name='articles'),
	path('articles/<int:pk>', views.ArticleDetailView.as_view(), name='article-detail'),
	path('articles/create', views.AddArticle.as_view(), name='article-create'),
]