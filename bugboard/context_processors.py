from django.conf import settings
def user_list(request):
    return {'BUGBOARD_USER_LIST': settings.BUGBOARD_USER_LIST}
