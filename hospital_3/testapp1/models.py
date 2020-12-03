from django.db import models
from  datetime import datetime
from dateutil.relativedelta import relativedelta

# Create your models here.
class Registration(models.Model):
    SEX_CHOICES = (
    ("MALE", "MALE"),
    ("FEMALE", "FEMALE"),
    ("TRANSGENDER", "TRANSGENDER"),
    )
    MARTIAL_STATUS=(
    ("MARRIED","MARRIED"),
    ("SINGLE","SINGLE"),
    )
    NATIONALITY_CHOICES=(
    ("INDIAN","INDIAN"),
    ("FOREIGNER","FOREIGNER")
    )

    DATE_INPUT_FORMATS = ['%d-%m-%Y']
    patient_name=models.CharField(max_length=50)
    address=models.CharField(max_length=250, blank=True)
    city=models.CharField(max_length=20)
    pincode=models.IntegerField(default=501501)
    dob=models.DateField(null=True,blank=True)
    occupation=models.CharField(max_length=20)
    gender=models.CharField(max_length=15, choices=SEX_CHOICES,default='MALE')
    martial_status=models.CharField(max_length=15, choices=MARTIAL_STATUS,default='SINGLE')
    nationality=models.CharField(max_length=15, choices=NATIONALITY_CHOICES,default='INDIAN')
    email=models.EmailField(max_length=80,null=True,blank=True)
    phone=models.CharField(max_length=10,null=True,blank=True)
    date_reg=models.DateTimeField(default=datetime.now())
    reg_validity=models.DateTimeField(default=datetime.now()+ relativedelta(years=1))
    OPID=models.CharField(max_length=50,null=True,blank=True)
    def __str__(self):
        return '%s | %s |%s' % (self.patient_name, self.id , self.phone)
        # return '%s' % (self.patient_name)

class Fee_chart(models.Model):
    doctor_name=models.CharField(max_length=50,primary_key=True)
    dept=models.CharField(max_length=25, blank=True)
    fee=models.DecimalField(max_digits=8, decimal_places=2,default=0.0)
    availability=models.CharField(max_length=150,null=True,blank=True)
    def __str__(self):
        return '%s | %s |%s' % (self.doctor_name, self.dept , self.fee)

class Lab_chart(models.Model):
    Service_Name=models.CharField(max_length=50,primary_key=True)
    Service_Type=models.CharField(max_length=25)
    charge=models.FloatField(default=0.0)
    perc10_Total=models.FloatField(default=0.0)
    perc15=models.FloatField(default=0.0)
    perc15_Total=models.FloatField(default=0.0)

    def __str__(self):
        return '%s | %s |%s' % (self.Service_Name, self.charge , self.perc15_Total)
class Bill_Entry(models.Model):
    ADM_TYPES=(
    ("IN_PATIENT","IN_PATIENT"),
    ("OUT_PATIENT","OUT_PATIENT")
    )
    STATUS=(
    ("UN_LOCKED","UN_LOCKED"),
    ("LOCKED","LOCKED"),
    )
    PAYMENT_CHOICES = (
    ("CASH", "CASH"),
    ("CARD", "CARD"),
    ("BOTH", "BOTH"),
    )
    patient_name=models.CharField(max_length=50,null=True,blank=True)
    reg_entry_ref=models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='reg_entry_ref',null=True,blank=True)
    bill_no=models.IntegerField(primary_key=True)
    admission_type=models.CharField(max_length=15, choices=ADM_TYPES,default='OUT_PATIENT')
    billed_datetime=models.DateTimeField(null=True,blank=True)
    billed_amount=models.DecimalField(max_digits=8, decimal_places=2,default=0.0)
    billed_by=models.CharField(max_length=50,null=True,blank=True)
    status=models.CharField(max_length=15, choices=STATUS,default='UN_LOCKED')

    mode_of_payment=models.CharField(max_length=10, choices=PAYMENT_CHOICES,default='CASH')
    tx_id_reference=models.CharField(max_length=4,default='empt')
    card_issued_bank=models.CharField(max_length=10,default='empty')
    paid_by_cash=models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    paid_by_card=models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    return_cash=models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    due_amount=models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    def __str__(self):
        return '%s | %s ' % (self.patient_name, self.bill_no )
#
class Bill_Item(models.Model):
    SERVICE_TYPE=(
    ("CONSULTATION","CONSULTATION"),
    ("LAB_TESTS","LAB_TESTS"),
    ("OTHERS","OTHERS")
    )
    STATUS=(
    ("UN_LOCKED","UN_LOCKED"),
    ("LOCKED","LOCKED"),
    )
    patient_name=models.CharField(max_length=50)
    bill_entry_ref=models.ForeignKey(Bill_Entry, on_delete=models.CASCADE, related_name='bill_entry_ref',null=True,blank=True)
    service_type=models.CharField(max_length=15, choices=SERVICE_TYPE,default='CONSULTATION')
    service_name=models.CharField(max_length=150)
    service_amount=models.DecimalField(max_digits=8, decimal_places=2,default=0.0)
    service_tax_amount=models.DecimalField(max_digits=8, decimal_places=2,default=0.0)
    visit_type=models.CharField(max_length=20,default='WALK_IN')
    Ref_by=models.CharField(max_length=20,default="None")
    status=models.CharField(max_length=15, choices=STATUS,default='UN_LOCKED')
    def __str__(self):
        return '%s | %s ' % (self.patient_name, self.bill_entry_ref.bill_no )

class Appointment_Item(models.Model):
    SERVICE_TYPE=(
    ("CONSULTATION","CONSULTATION"),
    ("LAB_TESTS","LAB_TESTS"),
    ("FOLLOW_UP","FOLLOW_UP")
    )
    STATUS=(
    ("SCHEDULED","SCHEDULED"),
    ("COMPLETED","COMPLETED"),
    )
    patient_name=models.CharField(max_length=50,null=True,blank=True)
    OPID=models.CharField(max_length=15)
    reg_entry_ref1=models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='reg_entry_ref1',null=True,blank=True)
    appt_type=models.CharField(max_length=15, choices=SERVICE_TYPE,default='CONSULTATION')
    appt_purpose=models.CharField(max_length=150,null=True,blank=True)
    appt_date=models.DateField(null=True,blank=True)
    # appt_time=models.TimeField(null=True,blank=True)
    Ref_by=models.CharField(max_length=20,default="None")
    status=models.CharField(max_length=15, choices=STATUS,default='SCHEDULED')
    phone=models.CharField(max_length=10,null=True,blank=True)  #redunant to simply alert report
    def __str__(self):
        return '%s | %s ' % (self.patient_name, self.OPID )
    # @property
    # def phone(self):
    #     return '%s' % (self.reg_entry_ref1.phone)
