from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin 

admin.site.site_header = 'Blogging administration'

admin.site.register(Post)
admin.site.register(Post_category)

class CustomMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
admin.site.register(Comment, CustomMPTTModelAdmin)
