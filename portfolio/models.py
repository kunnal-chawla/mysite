from django.db import models
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import AbstractBaseUser
from .managers import MyUserManager
import random



def generate_user_id():
	user_id = "".join([random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVXYZ') for i in range(10)])
	return user_id

def generate_registration_number():
    registration_number = "".join([random.choice('123456789') for i in range(1)])
    registration_number = registration_number + "".join([random.choice('0123456789') for i in range(8)])
    return registration_number


class MyUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Contact(models.Model):
    contact_name = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=70, null=False)
    subject = models.CharField(max_length=40, null=False)
    message = models.TextField(null=True)
    created_date = CreationDateTimeField()
    updated_date = ModificationDateTimeField()


class State(models.Model):
    state_name = models.CharField(max_length=200, null=False)


class Address(models.Model):
    location = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=70, null=True, editable=True, db_index=True)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING, related_name='address_state')
    pin = models.CharField(max_length=10, null=True)
    country = models.CharField(max_length=50, null=True)
    created_date = CreationDateTimeField()
    updated_date = ModificationDateTimeField()
    history = HistoricalRecords()


class Portfolio(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, related_name='protfoilo_user')
    about = models.TextField(max_length=600, null=True)
    email = models.CharField(unique=True, max_length=70, null=True, editable=True,db_index=True)
    mobile_number = models.CharField(unique=True, max_length=20, null=True, editable=True,db_index=True)
    dob = models.DateField(blank=True, null=True, editable=True)
    link = models.CharField(max_length=1000, null=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, related_name='portfolio_address')
    created_date = CreationDateTimeField()
    updated_date = ModificationDateTimeField()
    history = HistoricalRecords()

