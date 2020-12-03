from django import forms
from testapp.models import *
from django.utils import timezone
from bootstrap_datepicker_plus import DatePickerInput
from django.conf import settings
import datetime

class Supplier_Address_form(forms.ModelForm):
    class Meta:
        model=Supplier_Address
        fields='__all__'

class Customer_Address_form(forms.ModelForm):
    class Meta:
        model=Customer_Address
        fields='__all__'

class Item_Entry_form(forms.ModelForm):
    class Meta:
        model=Item_Entry
        fields='__all__'

class Out_Item_Entry_form(forms.ModelForm):
    class Meta:
        model=Out_Item_Entry
        fields='__all__'
        widgets = {'bill_no_ref':forms.HiddenInput(),'BatchNo':forms.HiddenInput(),'item_entry_ref':forms.HiddenInput(),
                    'bill_item_amount':forms.HiddenInput(),'bill_tax_per':forms.HiddenInput(),'status':forms.HiddenInput(),
                    'CGST_tax_per':forms.HiddenInput(),'SGST_tax_per':forms.HiddenInput(),'IGST_tax_per':forms.HiddenInput(),
                    'CGST_tax_amount':forms.HiddenInput(),'SGST_tax_amount':forms.HiddenInput(),'IGST_tax_amount':forms.HiddenInput(),
                    'bill_tax_amount':forms.HiddenInput(),'billed_amount':forms.HiddenInput(),}

class Returned_Out_Item_Entry_form(forms.ModelForm):
    class Meta:
        model=Returned_Out_Item_Entry
        fields='__all__'
        widgets = {'bill_no_ref':forms.HiddenInput(),'BatchNo':forms.HiddenInput(),'item_entry_ref':forms.HiddenInput(),
                    'rbill_item_amount':forms.HiddenInput(),'rbill_tax_amount':forms.HiddenInput()}

class MenuModelChoiceField(forms.ModelChoiceField): ####
    def label_from_instance(self, obj):
        return "%s) %s" % (1,obj.companyname)

class Item_Entry_form2(forms.ModelForm):
    # supplier_ref=MenuModelChoiceField(queryset=Supplier_Address.objects.all())

    class Meta:
        model=Item_Entry
        fields='__all__'
        exclude=['status','low_stock_ind_status','Mfd_date','Qty_available','Qty_in','purchase_cost_per_unit','sell_cost_per_unit','purchased_date']
        # widget={'status':forms.HiddenInput(),}
    # def __init__(self, *args, **kwargs):
    #     super(Item_Entry_form2, self).__init__(*args, **kwargs)
    #     self.fields['status'].widget.attrs['disabled'] = True


class Purchase_Entry_form(forms.ModelForm):
    class Meta:
        model=Purchase_Entry
        fields='__all__'
        exclude=['status',]
        # widgets = {'tax_amount':forms.HiddenInput(),'grand_total':forms.HiddenInput()}
    # def __init__(self, *args, **kwargs):
    #     super(Purchase_Entry_form, self).__init__(*args, **kwargs)
    #     self.fields['tax_amount'].widget.attrs['disabled'] = True
    #     self.fields['grand_total'].widget.attrs['disabled'] = True

class Sell_Entry_form(forms.ModelForm):
    class Meta:
        model=Sell_Entry
        fields='__all__'
        exclude=['status','tx_id_reference','card_issued_bank','paid_by_cash','paid_by_card','return_cash','sell_datetime','bill_amount','tax_amount','grand_total']

class Returned_Sell_Entry_form(forms.ModelForm):
    class Meta:
        model=Returned_Sell_Entry
        fields='__all__'
        exclude=['status',]

class Item_Entry_form1(forms.Form):
    item_code=forms.CharField(max_length=200)
    item_name=forms.CharField(max_length=200)
    print_name=forms.CharField(max_length=200)
    companyname=forms.CharField(max_length=200)
    HSN_code=forms.CharField(max_length=20)
    tabsPerStrip=forms.IntegerField(initial=10)
    NumStrips=forms.IntegerField(initial=1)
    Mfd_by=forms.CharField(initial='xyz supplier')
    MRP=forms.DecimalField(max_digits=19, decimal_places=5,initial=0.0)
    BatchNo=forms.IntegerField(initial=0)
    Mfd_date=forms.DateField(initial=timezone.now())
    Exp_date=forms.DateField(initial=timezone.now())
    purchase_cost_per_unit=forms.DecimalField(max_digits=19, decimal_places=2,initial=0.0)
    sell_cost_per_unit=forms.DecimalField(max_digits=19, decimal_places=2,initial=0.0)
    Qty_in=forms.IntegerField(initial=0)
    Qty_available=forms.IntegerField(initial=0)
    Discount_per=forms.DecimalField(max_digits=9, decimal_places=2,initial=0.0)
    tax_percent=forms.DecimalField(max_digits=9, decimal_places=2,initial=0.18)
    amount=forms.DecimalField(max_digits=19, decimal_places=2,initial=0.0)
    purchased_date=forms.DateField(initial=timezone.now())

class Item_query_form(forms.Form):
    bill_no=forms.IntegerField(initial=0)
    item_name=forms.CharField()
    tabsReq=forms.IntegerField(initial=10)

class Item_expiry_query_form(forms.Form):
    months=forms.IntegerField(initial=3,help_text='Enter value in months, it will calculate from current date')

class Balance_sheet_query_form(forms.Form):
    CHOICES= [
    ('singledate', 'singleday'),
    ('daterange', 'daterange'),
    ]
    singledate=forms.ChoiceField(choices=CHOICES)
    start_date = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'))
    end_date = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'))

class report_form(forms.Form):
    Qty_available=forms.IntegerField(initial=0) # dummy


class bill_search_form(forms.Form):
    bill_no=forms.IntegerField(initial=0) # dummy

class qty_return_form(forms.Form):
    Qty_returned=forms.IntegerField(initial=0) # dummy

class payment_form(forms.Form):
    PAYMENT_CHOICES = (
    ("CASH", "CASH"),
    ("CARD", "CARD"),
    ("BOTH", "BOTH"),
    )

    mode_of_payment=forms.ChoiceField( choices=PAYMENT_CHOICES,initial='BOTH')
    tx_id_reference=forms.CharField(max_length=4,help_text='enter last 4digits card no',initial='empt',min_length=4)
    card_issued_bank=forms.CharField(max_length=10,help_text='enter bank name',initial='empty')
    paid_by_cash=forms.DecimalField(max_digits=10, decimal_places=2,initial=0.0)
    paid_by_card=forms.DecimalField(max_digits=10, decimal_places=2,initial=0.0)

class payment_form1(forms.Form):
    PAYMENT_CHOICES = (
    ("CASH", "CASH"),
    ("CARD", "CARD"),
    ("BOTH", "BOTH"),
    )

    mode_of_payment=forms.ChoiceField( choices=PAYMENT_CHOICES,initial='BOTH')
    tx_id_reference=forms.CharField(max_length=4,help_text='enter last 4digits card no',initial='empt',min_length=4)
    card_issued_bank=forms.CharField(max_length=10,help_text='enter bank name',initial='empty')
    paid_by_cash=forms.DecimalField(max_digits=10, decimal_places=2,initial=0.0)
    paid_by_card=forms.DecimalField(max_digits=10, decimal_places=2,initial=0.0)
    try:  #OPTION is defined in setting.py
        if settings.DISCOUNT_AMOUNT_FIELD_VISIBLE:
            if settings.DISCOUNT_AMOUNT_FIELD_VISIBLE.upper()=='Y' or settings.DISCOUNT_AMOUNT_FIELD_VISIBLE.upper()=='YES':
              discount_amount=forms.DecimalField(max_digits=10, decimal_places=2,initial=0.0) #23-Nov
    except AttributeError:
        print('No attribute DISCOUNT_AMOUNT_FIELD_VISIBLE field is defined in settings.py so by default DISCOUNT_AMOUNT_FIELD_VISIBLE is disabled')

class Item_Master_form(forms.ModelForm):
    class Meta:
        model=Item_Master
        fields='__all__'

class  IM_upload_form(forms.Form):
    file = forms.FileField()

class financial_report_form(forms.Form):

    QWARTER_CHOICES = (
    ("Q1", "APR-JUN"),
    ("Q2", "JUL-SEP"),
    ("Q3", "OCT-DEC"),
    ("Q4", "JAN-MAR"),
    )

    MONTH_CHOICES = (
    ("JAN", "JAN"),
    ("2", "FEB"),
    ("Q3", "OCT-DEC"),
    ("Q4", "JAN-MAR"),
    )

    F_Year = forms.ModelChoiceField(queryset=FYear_table.objects.all())
    F_Month= forms.ChoiceField( choices=MONTH_CHOICES,initial='JAN')

    def __init__(self):

        self.current_date =datetime.date.today()
        print('current_day',self.current_date)
        self.current_month= self.current_date.month
        self.current_year= self.current_date.year
