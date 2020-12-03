from django import forms
from testapp1 import models
class Reg_form(forms.ModelForm):
    class Meta:
        model=models.Registration
        fields='__all__'
        widgets={'OPID':forms.HiddenInput(), }
        exclude=['date_reg']
class Doc_fee_upload_form(forms.Form):
    # title = forms.CharField(max_length=50)
    file = forms.FileField()

class Fee_chart_form(forms.ModelForm):
    class Meta:
        model=models.Fee_chart
        fields='__all__'

class Lab_chart_form(forms.ModelForm):
    class Meta:
        model=models.Lab_chart
        fields='__all__'

class Doc_fee_form(forms.Form):
    CHOICES= [
    ('Internal Medicine', 'Internal Medicine'),
    ('Cardiology', 'Cardiology'),
    ('Cardio Surgen', 'Cardio Surgen'),
    ('Pediatrics', 'Pediatrics'),
    ('Obstetrics & Gynecology', 'Obstetrics & Gynecology'),
    ('Orthopaedics', 'Orthopaedics'),
    ('Skin & Cosmetology', 'Skin & Cosmetology'),
    ('Plastic Surgery', 'Plastic Surgery'),
    ('Urology', 'Urology'),
    ('Dental & Maxillofacial', 'Dental & Maxillofacial'),
    ('Anesthesiology', 'Anesthesiology'),
    ('Physiotherapy', 'Physiotherapy'),
    ('Allergy & Asthma Clinic', 'Allergy & Asthma Clinic'),
    ('Gastroenterology', 'Gastroenterology'),
    ]
    dept=forms.ChoiceField(choices=CHOICES)
    CHOICES= [
    ('WALK_IN', 'WALK_IN'),
    ('ANNUAL_CHECKUP', 'ANNUAL_CHECKUP'),
    ('REF_BY_DOCTOR', 'REF_BY_DOCTOR'),
    ]
    visit_type=forms.ChoiceField(choices=CHOICES,initial='WALK_IN')
    Ref_by=forms.CharField(max_length=10,initial="None")

class Lab_test_query_form(forms.Form):
    test_name=forms.CharField()
    CHOICES= [
    ('WALK-IN', 'WALK-IN'),
    ('ANNUAL_CHECKUP', 'ANNUAL_CHECKUP'),
    ('REF_BY_DOCTOR', 'REF_BY_DOCTOR'),
    ]
    visit_type=forms.ChoiceField(choices=CHOICES,initial='REF_BY_DOCTOR')
    Ref_by=forms.CharField(max_length=10,initial="None")

class Bill_Entry_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       super(Bill_Entry_form, self).__init__(*args, **kwargs)
       self.fields['bill_no'].widget.attrs['readonly'] = True

    class Meta:
        model=models.Bill_Entry
        fields='__all__'
        exclude=['status',]
        widgets={'billed_by':forms.HiddenInput(),'patient_name':forms.HiddenInput(),'reg_entry_ref':forms.HiddenInput(),\
        'mode_of_payment':forms.HiddenInput(),'tx_id_reference':forms.HiddenInput(),'card_issued_bank':forms.HiddenInput(), \
        'paid_by_cash':forms.HiddenInput(),'paid_by_card':forms.HiddenInput(),'return_cash':forms.HiddenInput(),'due_amount':forms.HiddenInput(), \
        'billed_datetime':forms.HiddenInput(),'billed_amount':forms.HiddenInput(),}

class Appointment_form(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(Appointment_form, self).__init__(*args, **kwargs)
        self.fields['OPID'].widget.attrs['readonly'] = True

    class Meta:
        model=models.Appointment_Item
        fields='__all__'
        exclude=['status', 'appt_time','patient_name','reg_entry_ref1','phone']
        # widgets={,}

class List_Appointment_form(forms.Form):
    CHOICES = ( ('Today', 'Today'),('Tomorrow', 'Tomorrow'),('AllNextAppointments', 'AllNextAppointments'))
    report_choice_field = forms.ChoiceField(label='select which report type (Today, Tomorrow..)?',choices=CHOICES, initial='Today')
