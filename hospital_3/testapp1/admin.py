from django.contrib import admin
from .models import *
#
class RegistrationAdmin(admin.ModelAdmin):
    list_display=[ 'patient_name','address','city','dob','occupation','gender','email','phone','date_reg','id','OPID',]
class Fee_chartAdmin(admin.ModelAdmin):
        list_display=[ 'doctor_name','dept','fee','availability']
class Lab_chartAdmin(admin.ModelAdmin):
        list_display=[ 'Service_Type','Service_Name','charge','perc10_Total','perc15','perc15_Total']

class Bill_EntryAdmin(admin.ModelAdmin):
        list_display=[ 'patient_name','reg_entry_ref','bill_no','admission_type','billed_datetime','billed_amount','billed_by','status',]
class Bill_ItemAdmin(admin.ModelAdmin):
        list_display=[ 'patient_name','service_type','service_name','service_amount','service_tax_amount','status','bill_entry_ref',]

class Appointment_ItemAdmin(admin.ModelAdmin):
        list_display=[ 'patient_name','reg_entry_ref1','appt_type','appt_purpose','appt_date','status','Ref_by',]


# Register your models here.
admin.site.register(Registration,RegistrationAdmin)
admin.site.register(Fee_chart,Fee_chartAdmin)
admin.site.register(Lab_chart,Lab_chartAdmin)
admin.site.register(Bill_Entry,Bill_EntryAdmin)
admin.site.register(Bill_Item,Bill_ItemAdmin)
admin.site.register(Appointment_Item,Appointment_ItemAdmin)
