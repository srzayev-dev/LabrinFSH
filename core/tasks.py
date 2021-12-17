from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from core.models import Post

@shared_task
def delete_posts():
    startdate = timezone.now()
    enddate = startdate - timedelta(days=7)
    posts = Post.objects.filter(created_at__lte=enddate)
    posts.delete()
    
    


