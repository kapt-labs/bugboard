# Third party
from django.urls import path

# Local application / specific library imports
from . import views


urlpatterns = [
    path("", views.UnnassignedView.as_view(), name="unnassigned"),
    path("unnassigned/", views.UnnassignedView.as_view(), name="unnassigned"),
    path("user/", views.ByMemberView.as_view(), name="user"),
    path("commented/", views.CommentedView.as_view(), name="commented"),
    path("created/", views.CreatedView.as_view(), name="created"),
    path("all/", views.AllView.as_view(), name="all"),
]
