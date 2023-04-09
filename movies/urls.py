from django.contrib import admin
from django.urls import path
from movies import views

urlpatterns = [
    path("", views.index,name='home'),
    path("movie/<str:m_id>/", views.movie,name='movie'),
    path("language/<str:rlang>/", views.language,name='language'),
    path("category/<str:rcat>/", views.category,name='category'),
    path("year/<str:year>/", views.year,name='year'),
    path("sort/<str:sort>/", views.sort,name='sort'),
    path("ratings", views.ratings,name='ratings'),
    path("signup", views.signup,name='signup'),
    path("signin", views.signin,name='signin'),
    path("signout", views.signout,name='signout'),
    path("search", views.search,name='search'),
    path("contact", views.contact,name='contact'),
]