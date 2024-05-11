from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Student
from .utils import geocode_and_save_addresses

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=Student)
def update_student_eligibility(sender, instance, **kwargs):
    instance.check_eligibility()

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student
import logging
logging.basicConfig(level=logging.INFO,format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# #@receiver(post_save, sender=Student)
# def geocode_student_address(sender, instance, created, **kwargs):
#     logging.info("******************************************************")
#     print("***   *****    ****** created         **    ***********   ***")
#     if created:
#         logger.info("Signal triggered successfully for new student creation.")
#         geocode_and_save_addresses(instance)

# post_save.connect(geocode_student_address, sender=Student)
