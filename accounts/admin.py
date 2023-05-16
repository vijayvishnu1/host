from django.contrib import admin
# Register your models here.

from .models import *

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Advocate)
admin.site.register(Clientcase)
admin.site.register(Clientprofiles)
admin.site.register(Clientfeedback)
admin.site.register(contactus)
admin.site.register(Schedule)
admin.site.register(CaseAssignment)
admin.site.register(UserStatus)
admin.site.register(Message)
admin.site.register(Review)
admin.site.register(filed_lawsuits)
admin.site.register(Judge)
admin.site.register(Court)
admin.site.register(Defendant)
# admin.site.register(Chat)
# admin.site.register(Friend_List)
# admin.site.register(Chat)
# admin.site.register(Friend_List)
# admin.site.register(Chat)


