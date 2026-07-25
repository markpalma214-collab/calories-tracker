from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('tracker/', views.tracker, name='tracker'),
    path('view/', views.trackerview, name='view' ),
    path('totalcalories/', views.summary_hard, name='totalcalories'),
    path('updatetotalcalories/<int:pk>', views.update_form, name='updatetotalcalories'),
    path('deletetotalcalories/<int:pk>', views.delete, name='deletetotalcalories'),
    path('authentication/', views.authentication, name='authentication'),
    path('logout/', views.logoutuser, name='logout'),
    path('history/', views.history, name='history'),




]

