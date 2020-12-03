from django.contrib import admin
from testapp.models import *
##
class Supplier_AddressAdmin(admin.ModelAdmin):
    list_display=['companyname','town','city','email','phone']

class Customer_AddressAdmin(admin.ModelAdmin):
    list_display=['contact_name','email','phone','id']
class Item_EntryAdmin(admin.ModelAdmin):
    list_display=[
    'item_code','item_name','print_name','companyname','HSN_code','status',
    'supplier_ref','id','purchase_ref','amount','status','Qty_in','Qty_available',
    ]

class Purchase_EntryAdmin(admin.ModelAdmin):
    list_display=[
    'invoice_no','purchase_type','supplier_ref1','status'

    ]
class Sell_EntryAdmin(admin.ModelAdmin):
    list_display=[
    'bill_no','bill_amount','tax_amount','grand_total','sell_datetime','phone','contact_name','id','status',

    ]

class Out_Item_EntryAdmin(admin.ModelAdmin):
    list_display=[
    'bill_no_ref','BatchNo','item_entry_ref','Qty_sold','bill_item_amount','bill_tax_amount','id','status'

    ]
class Returned_Sell_EntryAdmin(admin.ModelAdmin):
    list_display=[
    'sell_entry_ref','rbill_no','rbill_amount','rbill_tax_amount','rbill_grand_total','returned_sell_datetime','status','get_id',

    ]

class Returned_Out_Item_EntryAdmin(admin.ModelAdmin):
    list_display=[
    'rbill_no_ref','BatchNo','item_entry_ref1','Qty_returned','rbill_item_amount','rbill_tax_amount','id','status',
    ]
class StaffAdmin(admin.ModelAdmin):
    list_display=[
    'sname','email','role','id'
    ]

class Item_MasterAdmin(admin.ModelAdmin):
    list_display=[
    'item_code','item_name','print_name','Mfd_by','HSN_code','MRP','BatchNo','tax_percent','sch','id',
    ]

class FYear_tableAdmin(admin.ModelAdmin):
    list_display=[ 'Year',]

# Register your models here.
admin.site.register(Supplier_Address, Supplier_AddressAdmin)
admin.site.register(Customer_Address, Customer_AddressAdmin)
admin.site.register(Item_Entry, Item_EntryAdmin)
admin.site.register(Purchase_Entry, Purchase_EntryAdmin)
admin.site.register(Sell_Entry, Sell_EntryAdmin)
admin.site.register(Out_Item_Entry, Out_Item_EntryAdmin)
admin.site.register(Returned_Sell_Entry, Returned_Sell_EntryAdmin)
admin.site.register(Returned_Out_Item_Entry, Returned_Out_Item_EntryAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Item_Master, Item_MasterAdmin)
admin.site.register(FYear_table, FYear_tableAdmin)
