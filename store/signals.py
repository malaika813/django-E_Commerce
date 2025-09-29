# store/signals.py
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from django.db.models import Avg, Count
from .models import Review, Product



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        
        

@receiver([post_save, post_delete], sender=Review)
def update_product_rating(sender, instance, **kwargs):
    product = instance.product
    stats = product.reviews.aggregate(
        avg_rating=Avg('rating'),
        count=Count('id')
    )
    product.rating = stats['avg_rating'] or 0
    product.reviews_count = stats['count']
    product.save()
