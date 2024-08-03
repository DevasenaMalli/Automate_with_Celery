from django.apps import apps


def get_all_custom_models():
    defaulf_models = ['ContentType', 'Session', 'User', 'Group', 'LogEntry', 'Permission', 'uploads']
    #try to get all the apps

    custom_models = []
    for model in apps.get_models():
        if model.__name__ not in defaulf_models:
            custom_models.append(model.__name__)
    return custom_models