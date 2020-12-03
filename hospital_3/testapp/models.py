from django import forms
from django.db import models

# Create your models here.
class Item_Master(models.Model):
    item_code=models.CharField(max_length=200)
    item_name=models.CharField(max_length=200)
    print_name=models.CharField(max_length=200)
    Mfd_by=models.CharField(max_length=200,null=True,blank=True)
    HSN_code=models.CharField(max_length=20)
    MRP=models.FloatField(default=0.0)
    BatchNo=models.CharField(max_length=20,null=True,blank=True)
    tax_percent=models.FloatField(default=0.12) # purchase tax %
    sch=models.CharField(max_length=1,null=True,blank=True)


class Supplier_Address(models.Model):
    companyname=models.CharField(max_length=200, primary_key=True)
    town=models.CharField(max_length=20)
    city=models.CharField(max_length=20)
    contact_name=models.CharField(max_length=80)
    email=models.EmailField(max_length=80)
    phone=models.CharField(max_length=20)
    def __str__(self):
        return '%s | %s |%s' % (self.companyname, self.email , self.contact_name)

class Customer_Address(models.Model):
    contact_name=models.CharField(max_length=80,null=True,blank=True)
    email=models.EmailField(max_length=80,null=True,blank=True)
    phone=models.CharField(max_length=20,null=True,blank=True)
    Doctor_name=models.CharField(max_length=80,null=True,blank=True)
    hospital_id=models.CharField(max_length=80,default=0)


class Purchase_Entry(models.Model):
    PURCHASE_CHOICES = (
    ("CASH", "CASH"),
    ("CREDIT", "CREDIT"),
    )

    STATUS_CHOICES = (
    ("UN_APPROVED", "UN_APPROVED"),
    ("APPROVED", "APPROVED"),
    )
    purchase_type = models.CharField(max_length=20,choices=PURCHASE_CHOICES,default='CREDIT')
    supplier_ref1=models.ForeignKey(Supplier_Address, on_delete=models.CASCADE, related_name='supplier_ref1',null=True,blank=True)
    invoice_no=models.CharField(max_length=20,primary_key=True)  #1-oct change int to CharField
    invoice_amount=models.DecimalField(max_digits=19, decimal_places=2,default=0.0) #from purchase invoice
    tax_amount=models.DecimalField(max_digits=19, decimal_places=2,default=0.0)
    grand_total=models.DecimalField(max_digits=19, decimal_places=2,default=0.0)
    adjustment=models.DecimalField(max_digits=6, decimal_places=2,default=0.0)
    purchase_date=models.DateTimeField(null=True,blank=True)
    status=models.CharField(max_length=11,choices=STATUS_CHOICES,default='UN_APPROVED')  #
    taxable_amount=models.DecimalField(max_digits=19, decimal_places=2,default=0.0) #23-Nov   from purchase invoice
    CGST_tax_amount=models.DecimalField(max_digits=9, decimal_places=3,default=0.0)  #23-Nov  from purchase invoice
    SGST_tax_amount=models.DecimalField(max_digits=9, decimal_places=3,default=0.0)  #23-Nov  from purchase invoice
    def __str__(self):
        return '%s | %s' % (self.invoice_no, self.supplier_ref1.contact_name)

class Item_Entry(models.Model):
    STATUS_CHOICES = (
    ("UN_APPROVED", "UN_APPROVED"),
    ("APPROVED", "APPROVED"),
    )
    item_code=models.CharField(max_length=200)
    item_name=models.CharField(max_length=200)
    print_name=models.CharField(max_length=200)
    companyname=models.CharField(max_length=200)
    HSN_code=models.CharField(max_length=20)
    tabsPerStrip=models.IntegerField(default=10)
    NumStrips=models.IntegerField(default=1)
    Mfd_by=models.CharField(max_length=200,null=True,blank=True)
    MRP=models.DecimalField(max_digits=9, decimal_places=2,default=0.0)
    BatchNo=models.CharField(max_length=20,null=True,blank=True)  #1-oct change int to CharField
    Mfd_date=models.DateField(null=True,blank=True)
    Exp_date=models.DateField(null=True,blank=True)
    purchase_rate=models.DecimalField(max_digits=9, decimal_places=3,default=0.0)  #2-oct added for simplicity #Rate
    purchase_cost_per_unit=models.DecimalField(max_digits=9, decimal_places=3,default=0.0)      #calculated field
    sell_cost_per_unit=models.DecimalField(max_digits=9, decimal_places=3,default=0.0)          #calculated field
    Qty_in=models.IntegerField(null=True,blank=True)                                #Qty        #calculated field
    Qty_available=models.IntegerField(null=True,blank=True)                                     #calculated field
    Discount_per=models.DecimalField(max_digits=9, decimal_places=3,default=0.0) # purchase disc %
    disc_amount=models.DecimalField(max_digits=19, decimal_places=2,default=0.0) # purchase disc amount  #calculated field
    tax_percent=models.DecimalField(max_digits=9, decimal_places=3,default=0.12) # purchase tax %
    tax_amount=models.DecimalField(max_digits=19, decimal_places=2,default=0.0) # purchase tax amount   #calculated field
    amount=models.DecimalField(max_digits=19, decimal_places=2,default=0.0)     #purchase taxable amount #calculated field
    purchased_date=models.DateField(null=True,blank=True)
    # sell_Discount_per=models.DecimalField(max_digits=9, decimal_places=3,default=0.0) # sell disc %     #23-Nov
    # sell_disc_amount=models.DecimalField(max_digits=19, decimal_places=2,default=0.0) # sell disc amount  #calculated field  23-Nov
    supplier_ref=models.ForeignKey(Supplier_Address, on_delete=models.CASCADE, related_name='supplier_ref',null=True,blank=True)
    purchase_ref=models.ForeignKey(Purchase_Entry, on_delete=models.CASCADE, related_name='purchase_ref',null=True,blank=True)
    low_stock_ind_per=models.DecimalField(max_digits=2, decimal_places=2,default=0.3)
    low_stock_ind_status=models.CharField(max_length=3,null=True,blank=True,default='OFF')          #status field
    status=models.CharField(max_length=11,choices=STATUS_CHOICES,default='UN_APPROVED')  # UN_APRROVED -under entering data, APPROVED - ready to sell, LOCKED - after exhauting stock
    sch=models.CharField(max_length=3,null=True,blank=True,default='')


    def __str__(self):
        return '%s | %s |%s' % (self.item_code, self.item_name , self.Qty_in)

class Sell_Entry(Customer_Address):   # customer Address detail are inherited
    PAYMENT_CHOICES = (
    ("CASH", "CASH"),
    ("CARD", "CARD"),
    ("BOTH", "BOTH"),
    )
    STATUS_CHOICES = (
    ("UNLOCKED", "UNLOCKED"),
    ("LOCKED", "LOCKED"),
    )
    bill_no=models.IntegerField(primary_key=True)
    bill_amount=models.DecimalField(max_digits=9, decimal_places=2,default=0.0)
    tax_amount=models.DecimalField(max_digits=9, decimal_places=2,default=0.0)
    grand_total=models.DecimalField(max_digits=9, decimal_places=2,default=0.0)
    sell_datetime=models.DateTimeField(null=True,blank=True)
    status=models.CharField(max_length=10, choices=STATUS_CHOICES,default='UNLOCKED')  # UNLOCKED - able to sell,  LOCKED - not able to edit or update
    mode_of_payment=models.CharField(max_length=10, choices=PAYMENT_CHOICES,default='CASH')
    tx_id_reference=models.CharField(max_length=4,default='empt')
    card_issued_bank=models.CharField(max_length=10,default='empty')
    paid_by_cash=models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    paid_by_card=models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    return_cash=models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    discount_amount=models.DecimalField(max_digits=10, decimal_places=2,default=0.0) #23-Nov

    def __str__(self):
        return '%d |%s' % (self.bill_no,self.contact_name)
# Returned Sell Entry  ( for returned items from customer)
class Returned_Sell_Entry(models.Model):

    RETURN_PAYMENT_CHOICES = (
    ("CASH", "CASH"),
    ("CARD", "CARD"),

    )

    sell_entry_ref=models.ForeignKey(Sell_Entry, on_delete=models.CASCADE, related_name='sell_entry_ref',null=True,blank=True)
    rbill_no=models.IntegerField(primary_key=True) #return bill no
    rbill_amount=models.DecimalField(max_digits=9, decimal_places=2,default=0.0)
    rbill_tax_amount=models.DecimalField(max_digits=9, decimal_places=2,default=0.0)
    rbill_grand_total=models.DecimalField(max_digits=9, decimal_places=2,default=0.0)
    returned_sell_datetime=models.DateTimeField(null=True,blank=True)
    status=models.CharField(max_length=10, default='UNLOCKED')  # UNLOCKED - able to sell,  LOCKED - not able to sell
    rmode_of_payment=models.CharField(max_length=10, choices=RETURN_PAYMENT_CHOICES,default='CASH')
    rtx_id_reference=models.CharField(max_length=4,default='empt')
    card_issued_bank=models.CharField(max_length=10,default='empty')
    rpayment_by_cash=models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    rpayment_by_card=models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    def __str__(self):
        return '%d  ' % (self.rbill_no)
    def get_id(self):
        return '%d' % (self.rbill_no)
class Out_Item_Entry(models.Model):
    STATUS_CHOICES = (
    ("UNLOCKED", "UNLOCKED"),
    ("LOCKED", "LOCKED"),
    )
    bill_no_ref=models.ForeignKey(Sell_Entry, on_delete=models.CASCADE, related_name='bill_no_ref',null=True,blank=True)
    BatchNo=models.CharField(max_length=20,null=True,blank=True)
    item_entry_ref=models.ForeignKey(Item_Entry, on_delete=models.CASCADE, related_name='item_entry_ref',null=True,blank=True)
    Qty_sold=models.IntegerField(null=True,blank=True)
    bill_item_amount=models.DecimalField(max_digits=9, decimal_places=3,default=0.0)
    bill_tax_amount=models.DecimalField(max_digits=9, decimal_places=3,default=0.0)
    bill_tax_per=models.DecimalField(max_digits=9, decimal_places=2,default=0.0)
    # sell_disc_per=models.DecimalField(max_digits=9, decimal_places=2,default=0.0)  # copied from Item Entry
    CGST_tax_amount=models.DecimalField(max_digits=9, decimal_places=3,default=0.0)
    SGST_tax_amount=models.DecimalField(max_digits=9, decimal_places=3,default=0.0)
    billed_amount=models.DecimalField(max_digits=9, decimal_places=2,default=0.0)
    CGST_tax_per=models.DecimalField(max_digits=9, decimal_places=3,default=0.0)  # bill_tax_per* 0.5
    SGST_tax_per=models.DecimalField(max_digits=9, decimal_places=3,default=0.0)  # bill_tax_per* 0.5

    status=models.CharField(max_length=10, choices=STATUS_CHOICES,default='UNLOCKED')

    def __str__(self):
        return '%s'  % (self.item_entry_ref)

class Returned_Out_Item_Entry(models.Model):
    STATUS_CHOICES = (
    ("UNLOCKED", "UNLOCKED"),
    ("LOCKED", "LOCKED"),
    )
    rbill_no_ref=models.ForeignKey(Returned_Sell_Entry, on_delete=models.CASCADE, related_name='rbill_no_ref',null=True,blank=True)
    BatchNo=models.CharField(max_length=20,null=True,blank=True)
    item_entry_ref1=models.ForeignKey(Item_Entry, on_delete=models.CASCADE, related_name='item_entry_ref1',null=True,blank=True)
    Qty_returned=models.IntegerField(null=True,blank=True)
    rbill_item_amount=models.DecimalField(max_digits=9, decimal_places=2,default=0.0)
    rbill_tax_amount=models.DecimalField(max_digits=9, decimal_places=2,default=0.0)
    status=models.CharField(max_length=10, choices=STATUS_CHOICES,default='UNLOCKED')
    def __str__(self):
        return '%s'  % (self.item_entry_ref1)

class Staff(models.Model):
    sname=models.CharField(max_length=20)
    EmpId=models.IntegerField()
    email=models.EmailField(max_length=30,blank=True)
    phone=models.IntegerField()
    dept=models.CharField(max_length=15)
    lname=models.CharField(max_length=20)
    role=models.CharField(max_length=20,blank=True)
class FYear_table(models.Model):
    Year=models.CharField(max_length=15)
    def __str__(self):
        return '%s ' % (self.Year)
    def get_list(self):
        l=self.Year.split('-')
        return l
