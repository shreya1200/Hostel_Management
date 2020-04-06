from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Banner(models.Model):    #making all the changes in the banner area dynamically using jinja
    status = models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.status
    

class SignUp(models.Model):    #making all the changes in the banner area dynamically using jinja
    name =models.CharField(max_length=100,null=True)
    email = models.EmailField(max_length=250, blank=False, unique=True, error_messages={'required': 'Please provide your email address.','unique' : ' An account with this email already exists'})
    prn = models.IntegerField()
    st_number = models.IntegerField()
    parent_number = models.IntegerField()
    branch = models.CharField(max_length=50,null=True)
    username = models.CharField(max_length=50,null=True)
    password = models.CharField(max_length=50,null=True)
    page = models.CharField(max_length=10, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Profile', null=True)
    #is_college_user = models.BooleanField(default=False)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Leave(models.Model):    #making all the changes in the banner area dynamically using jinja
    profile = models.ForeignKey(SignUp, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    reason = models.CharField(max_length=100, null=True)
    text = models.CharField(max_length=100, null=True)  #parent consent type
    depdate = models.CharField(max_length=100, null=True)
    deptime = models.CharField(max_length=100, null=True)
    arrdate = models.CharField(max_length=100, null=True)
    arrtime = models.CharField(max_length=100, null=True)
    parent_number = models.IntegerField()

    def __str__(self):
        return self.profile.name

class Complaint(models.Model):
    profile = models.ForeignKey(SignUp, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    st_number = models.IntegerField()
    category = models.CharField(max_length=20, null=True)
    problem = models.CharField(max_length=100, null=True)
    room = models.IntegerField()
    user_type = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name
