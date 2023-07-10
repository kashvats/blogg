from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(post)
admin.site.register(contactus)
admin.site.register(comment)
