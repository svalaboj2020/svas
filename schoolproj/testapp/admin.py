from django.contrib import admin
from testapp.models import *

class StudentAdmin(admin.ModelAdmin):
    list_display=['sname','pname','email','section','classx','lname']

class ParentAdmin(admin.ModelAdmin):
    list_display=['mother_name','m_email','father_name','f_email']

class EnquiryAdmin(admin.ModelAdmin):
    list_display=['name','phone','email','message']

class SM_uploadAdmin(admin.ModelAdmin):
    list_display=['title','std','sec','pdf']

class Rlink_uploadAdmin(admin.ModelAdmin):
    list_display=['title','std','sec','url']
# Register your models here.
admin.site.register(Student,StudentAdmin)
admin.site.register(Parent,ParentAdmin)
admin.site.register(Enquiry,EnquiryAdmin)
admin.site.register(SM_upload,SM_uploadAdmin)
admin.site.register(Rlink_upload,Rlink_uploadAdmin)
