from django.urls import path
from daycareApp import views
from django.contrib.auth import views as auth_views

# app urls 
urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
     path('login/', auth_views.LoginView.as_view(template_name='daycareApp/login.html'), name='login'),

    # sitter urls
    path('sitter-reg/', views.sitterReg, name='sitter-reg'),
    path('sitters/', views.sitters, name='sitters'),
    path('details/<int:id>', views.viewSitter, name="details"),
    path('edit/<int:id>/', views.edit_sitterdetails, name='edit_sitter'),
    path('delete/<int:id>/', views.deleteSitter, name="delete"),
    path('onduty/', views.onduty, name='onduty'),
    path('allonduty/', views.allonduty, name='allonduty'),
    path('editOnduty/<int:id>/', views.editOnduty, name='editOnduty'),
    
    
    path('sitterpay/', views.sitterpay, name='sitterpay'),
    path('sitteredit/<int:id>/', views.sitteredit, name= 'sitteredit'),
    path('sitteradd/', views.sitteradd, name='sitteradd'),

    



    # baby urls
    path('babyreg/', views.babyReg, name='babyreg'),
    path('babies/', views.babys, name='babys'),
    # path('edit/<int:item_id>/', views.edit_baby, name='edit_baby'),
    path('delete/<int:id>/', views.deleteBaby, name="delete"),
    path('babypay/', views.babyPay, name='babypay'),
    path('babyedit/<int:id>/', views.babyedit, name= 'babyedit'),
    path('babyadd/', views.babyadd, name='babyadd'),

  

    #sales
    path('sale/', views.sale, name='sale'),
    path('selling/<str:pk>/', views.selling, name='selling'),
    path('salesrecord/', views.salesrecord, name='salerecord'),
    path('sale/addstock/', views.addItem, name='addstock'),
    path('addmore/<int:id>/', views.addmore, name='addmore'),
    
    

    # admin logs urls
    path("login/", auth_views.LoginView.as_view(template_name='daycareApp/login.html'), name="login"), 
    path('logout/', views.logout_view, name='logout'),
]