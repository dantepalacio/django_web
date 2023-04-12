from . import models

def add_variable_to_context(request):
    status_profile = models.Profile.objects.values_list('status')
    return {
        'status_profile': status_profile,
        
    }