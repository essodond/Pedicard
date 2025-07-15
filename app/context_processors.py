from .models import Notification  # si tu as un modèle de notification
from django.contrib.auth.decorators import login_required

from .models import Notification

def notifications_processor(request):
    if request.user.is_authenticated and request.user.role == 'Médecin':
        notifications = Notification.objects.filter(
            utilisateur=request.user,
            est_lu=False
        ).order_by('-date')
        return {
            'notifications': notifications,
            'notification_count': notifications.count()
        }
    return {}
