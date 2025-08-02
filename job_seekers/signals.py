import os
import fitz  # PyMuPDF
import docx2txt
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Candidates

def extract_text(file_path):
    ext = os.path.splitext(file_path)[-1].lower()

    try:
        if ext == '.pdf':
            with fitz.open(file_path) as doc:
                return "\n".join(page.get_text() for page in doc)
        elif ext == '.docx':
            return docx2txt.process(file_path)
    except Exception as e:
        print(f"[Resume Extraction Error]: {e}")

    return ""

@receiver(post_save, sender=Candidates)
def parse_resume_text(sender, instance, created, **kwargs):
    if instance.resume:
        file_path = instance.resume.path
        resume_text = extract_text(file_path)

        # Avoid recursive signal call
        Candidates.objects.filter(pk=instance.pk).update(resume_text=resume_text)





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
