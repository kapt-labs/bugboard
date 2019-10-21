from django.urls import path

from . import views

urlpatterns = [
    path('', views.UnnassignedView.as_view(), name='unnassigned'),
    path(
        'unnassigned/',
        views.UnnassignedView.as_view(),
        name='unnassigned',
    ),
    path(
        'kapt/',
        views.ByMemberView.as_view(),
        name='kapt',
    ),
    path(
        'commented/',
        views.CommentedView.as_view(),
        name='commented',
    ),
    path(
        'created/',
        views.CreatedView.as_view(),
        name='created',
    ),
    path(
        'all/',
        views.AllView.as_view(),
        name='all',
    ),
]
