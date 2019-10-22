# Third party
from bugboard.models import Project, Task, Comment
from django.db.models import Max, Subquery, OuterRef
from django.views import generic


class UnnassignedView(generic.ListView):
    template_name = "bugboard/task_list.html"
    queryset = Task.objects.filter(assignee=None).order_by("-created_at")
    paginate_by = 100

    def get_ordering(self):
        return self.request.GET.get("order", "-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_tasks"] = Task.objects.all().count()
        context["total_projects"] = Project.objects.all().count()
        return context


class ByMemberView(generic.ListView):
    template_name = "bugboard/task_list.html"
    paginate_by = 100

    def get_ordering(self):
        return self.request.GET.get("order", "-created_at")

    def get_queryset(self):
        # ordering is called inside this function, so call it here
        ordering = self.get_ordering()
        # get correct kapt email from id
        email = str(self.request.GET.get("id", "ad")) + "@kapt.mobi"

        # return custom queryset
        return Task.objects.filter(assignee__email=email).order_by(ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_tasks"] = Task.objects.all().count()
        context["total_projects"] = Project.objects.all().count()
        return context


class CommentedView(generic.ListView):
    template_name = "bugboard/task_list.html"
    paginate_by = 100

    # Thanks https://docs.djangoproject.com/fr/2.2/ref/models/expressions/#subquery-expressions
    newest = Comment.objects.filter(task=OuterRef('pk')).order_by('-created_at')

    queryset = (
        Task.objects
        .exclude(comment=None)  # exclude tasks with no comments
        .annotate(last_com=Max("comment__created_at"))  # add last com in queryset
        .annotate(last_comment_member=Subquery(newest.values('member__member')[:1]))  # add last com mail
        .exclude(last_comment_member=True)  # exclude when last com contain out url in email (member)
        .order_by("-last_com")  # order by last com
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_tasks"] = Task.objects.all().count()
        context["total_projects"] = Project.objects.all().count()
        return context


class CreatedView(generic.ListView):
    template_name = "bugboard/task_list.html"
    queryset = Task.objects.all()
    paginate_by = 100

    # set ordering based on the ?order=PARAM parameter, set -created_at if there is no get
    def get_ordering(self):
        return self.request.GET.get("order", "-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_tasks"] = Task.objects.all().count()
        context["total_projects"] = Project.objects.all().count()
        return context


class AllView(generic.ListView):
    queryset = Task.objects.all()

    def get_ordering(self):
        return self.request.GET.get("order", "-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_tasks"] = Task.objects.all().count()
        context["total_projects"] = Project.objects.all().count()
        return context
