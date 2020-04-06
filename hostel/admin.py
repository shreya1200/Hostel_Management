from django.contrib import admin
from .models import SignUp, Banner, Leave, Complaint
# Register your models here.
admin.site.register(Banner)
admin.site.register(SignUp)
admin.site.register(Leave)
admin.site.register(Complaint)