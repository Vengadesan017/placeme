# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Candidates, Documents

# @receiver(post_save, sender=Candidates)
# def create_documents(sender, instance, created, **kwargs):
#     """
#     Signal to create a Documents row whenever a new Candidates instance is created.
#     """
#     if created:
#         # Create a corresponding Documents instance
#         Documents.objects.create(candidate=instance)
