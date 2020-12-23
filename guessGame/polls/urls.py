from django.urls import path
from . import views
urlpatterns = [


    path('', views.index, name='ndex'),
    path('add', views.add, name='add'),
    path('evaluate', views.evaluate, name='evaluate')
]

