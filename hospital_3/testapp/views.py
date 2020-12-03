from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from testapp import forms
from testapp import models
from testapp1 import models as rmodels
from testapp1 import views as v1
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView,DetailView,View
from decimal import *
from testapp.utils import render_to_pdf
import datetime
from django.db.models import Count, Sum
from django.core import serializers
import json
import xlwt
from django.conf import settings
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from num2words import num2words
from django.contrib.auth.decorators import login_required
import requests
import sys
import pandas as pd


def home(request):
    return render(request,'testapp/home.html')

# Create your views here.
def create_supplier(request):
    return create_(request,'create_supplier')


def create_customer(request):
    return create_(request,'create_customer')

def create_(request,param):
        my_dict={}
        my_dict['title']=param
        if request.method=='POST':
            if param=='create_customer':
                form=forms.Customer_Address_form(request.POST)
            elif param=='create_supplier':
                form=forms.Supplier_Address_form(request.POST)

            if form.is_valid():
                result=form.save()
                # my_dict['result']
                # x=models.Customer_Address.objects.last()
                # #update entry with OPID
                # reg=models.Registration.objects.filter(id=id).update(OPID=y)
                #  id=result.id
            else:
                if form.errors:
                    my_dict['errors']=form.errors
            if param=='create_supplier':
                areports=models.Supplier_Address.objects.all()
                my_dict['sreports']=areports
                return render(request,'testapp/results.html',my_dict)
            else:
                areports=models.Customer_Address.objects.all()
                my_dict['creports']=areports
                return render(request,'testapp/results_s.html',my_dict)
        else: #GET
            if param=='create_customer':
                form=forms.Customer_Address_form()
                my_dict['form']= form
                return render(request,'testapp/sform1.html',my_dict)
            elif param=='create_supplier':
                form=forms.Supplier_Address_form()
                my_dict['form']= form
                return render(request,'testapp/sform.html',my_dict)

def shome(request):
    my_dict={}
    sname=request.user.username
    print('sname',sname)
    my_dict['sname']=sname
    return render(request, 'testapp/shome.html')

def create_item(request):
    # addItem/
    my_dict={}
    my_dict['title']='Item_Entry'
    if request.method=='POST':
        form=forms.Item_Entry_form(request.POST)
        print('create item',form.is_valid())
        if form.is_valid():
            item_code=form['item_code'].value()
            item_name=form['item_name'].value()
            print_name=form['print_name'].value()
            companyname=form['companyname'].value()
            HSN_code=form['HSN_code'].value()
            tabsPerStrip=form['tabsPerStrip'].value()
            NumStrips=form['NumStrips'].value()
            Mfd_by=form['Mfd_by'].value()
            MRP=form['MRP'].value()
            BatchNo=form['BatchNo'].value()
            Mfd_date=form['Mfd_date'].value()
            Exp_date=form['Exp_date'].value()
            purchase_cost_per_unit=form['purchase_cost_per_unit'].value()
            sell_cost_per_unit=form['sell_cost_per_unit'].value()
            Qty_in=form['Qty_in'].value()
            Qty_out=form['Qty_out'].value()
            amount=form['amount'].value()
            purchased_date=form['purchased_date'].value()
            supplier_ref=form['supplier_ref'].value()
            tax_percent=form["tax_percent"].value()
            Discount_per=form["Discount_per"].value()
            low_stock_ind_per= form["low_stock_ind_per"].value()
            low_stock_ind_status=form["low_stock_ind_status"].value()

        ##logic
            print(type(tabsPerStrip),type(NumStrips))
            print(tabsPerStrip,NumStrips)
            Qty_in= int(tabsPerStrip) *int(NumStrips)
            Qty_out=Qty_in
            tax_amount= round(Decimal(amount) * Decimal(tax_percent),3)
            amount= round(Decimal(sell_cost_per_unit) * Decimal(Qty_in),3)
            print("tax_amount",tax_amount)
            print("amount",amount)
        ##

        initial={
        "item_code":item_code,
        "item_name":item_name,
        "print_name":print_name,
        "companyname":companyname,
        "HSN_code":HSN_code,
        "tabsPerStrip":tabsPerStrip,
        "NumStrips":NumStrips,
        "Mfd_by":Mfd_by,
        "MRP":MRP,
        "BatchNo":BatchNo,
        "Mfd_date":Mfd_date,
        "Exp_date":Exp_date,
        "purchase_cost_per_unit":purchase_cost_per_unit,
        "sell_cost_per_unit":sell_cost_per_unit,
        "Qty_in":Qty_in,
        "Qty_out":Qty_out,
        "Discount_per":Discount_per,
        "tax_percent":tax_percent,
        "amount":amount,
        "purchased_date":purchased_date,
        "supplier_ref":supplier_ref,
        "low_stock_ind_per":low_stock_ind_per,
        "low_stock_ind_status":low_stock_ind_status

        }

        form=forms.Item_Entry_form(request.POST,initial)
        print('is form.is_valid:',form.is_valid())
        if form.is_valid():
            result=form.save()
            print('saving ie, result:',result)
        print( item_code,print_name)


        ##
        try:
            areports=models.Item_Entry.objects.all()
            my_dict['areports']=areports
        except ObjectDoesNotExist:
            message='ObjectDoesNotExist exeception occured itemEntry report'

        ##
        return render(request,'testapp/item_results.html',my_dict)
    else:
        form=forms.Item_Entry_form()
        my_dict['form']= form
        return render(request,'testapp/iform.html',my_dict)
### Form view
# def create_item_new(request):
#     # addItem1/
#     my_dict={}
#     my_dict['title']='Item_Entry'
#     if request.method=='POST':
#         form=forms.Item_Entry_form2(request.POST) # 1-->2 changed , revertback later
#         print('create item',form.is_valid())
#         if form.is_valid()==False:
#             print('form is not valid not created IE')
#         else:    # form is valid
#             item_code=form['item_code'].value()
#             item_name=form['item_name'].value()
#             print_name=form['print_name'].value()
#             companyname=form['companyname'].value()
#             HSN_code=form['HSN_code'].value()
#             tabsPerStrip=form['tabsPerStrip'].value()
#             NumStrips=form['NumStrips'].value()
#             Mfd_by=form['Mfd_by'].value()
#             MRP=form['MRP'].value()
#             BatchNo=form['BatchNo'].value()
#             #Mfd_date=form.cleaned_data['Mfd_date']  #hiding so form does not contain , should not read
#             Exp_date=form.cleaned_data['Exp_date']
#             purchase_rate=form['purchase_rate'].value()
#             # purchase_cost_per_unit=form['purchase_cost_per_unit'].value()
#             # sell_cost_per_unit=form['sell_cost_per_unit'].value()
#             # Qty_in=form['Qty_in'].value()
#             # Qty_available=form['Qty_available'].value()
#             amount=form['amount'].value()
#             # purchased_date=form.cleaned_data['purchased_date']
#             supplier_ref=form['supplier_ref'].value()
#             purchase_ref=form['purchase_ref'].value()
#             tax_percent=form["tax_percent"].value()
#             Discount_per=form["Discount_per"].value()
#             low_stock_ind_per=form["low_stock_ind_per"].value() #26-Sep
#             #low_stock_ind_status=form["low_stock_ind_status"].value() #26-Sep
#             # status=form["status"].value() #30-Sep
#             sch=form["sch"].value()
#         ##logic
#             print(type(tabsPerStrip),type(NumStrips))
#             print(tabsPerStrip,NumStrips)
#             Qty_in= int(tabsPerStrip) *int(NumStrips)
#             Qty_available=0
#             temp=Decimal(Decimal(MRP)/Decimal(tabsPerStrip)) # 1-Oct
#             sell_cost_per_unit= temp/(1+Decimal(tax_percent))   # calculated field sell_cost_per_unit
#             print('IE- sell_cost_per_unit',sell_cost_per_unit)
#             purchase_cost_per_unit=round(Decimal(purchase_rate)/Decimal(tabsPerStrip),3)  # calculated field purchase_cost_per_unit
#             amount= round(Decimal(purchase_cost_per_unit) * Decimal(Qty_in),3)
#             disc_amount=round(Decimal(amount) * Decimal(Discount_per),3)
#             tax_amount= round((Decimal(amount)-Decimal(disc_amount)) * Decimal(tax_percent),3) # apply tax on taking discount
#
#
#             print("tax_amount",tax_amount)
#             print("amount",amount)
#             print('tax_percent, sell_cost_per_unit',tax_percent,sell_cost_per_unit)
#             print('purchase_cost_per_unit',purchase_cost_per_unit)
#
#         ##
#
#             initial={
#             "item_code":item_code,
#             "item_name":item_name.capitalize(),
#             "print_name":print_name.capitalize(),
#             "companyname":companyname,
#             "HSN_code":HSN_code.capitalize(),
#             "tabsPerStrip":tabsPerStrip,
#             "NumStrips":NumStrips,
#             "Mfd_by":Mfd_by,
#             "MRP":MRP,
#             "BatchNo":BatchNo.capitalize(),
#             #"Mfd_date":Mfd_date,
#             "Exp_date":Exp_date,
#             "purchase_rate":purchase_rate,
#             "purchase_cost_per_unit":purchase_cost_per_unit,
#             "sell_cost_per_unit":sell_cost_per_unit,
#             "Qty_in":Qty_in,
#             "Qty_available":Qty_available,
#             "Discount_per":Discount_per,
#             "tax_percent":tax_percent,
#             "amount":amount,
#             "tax_amount":tax_amount,
#             # "purchased_date":purchased_date,
#             "supplier_ref":supplier_ref,
#             "purchase_ref":purchase_ref,
#             "low_stock_ind_per":low_stock_ind_per, #26-Sep
#             #low_stock_ind_status":low_stock_ind_status, #26-Sep   donot read from form
#             # "status":status, #30-Sep
#             "disc_amount":disc_amount, #2-Oct
#             "sch":sch.capitalize(),
#             }
#             initial['tax_amount']=tax_amount
#             try:
#                 se=models.Supplier_Address.objects.get(companyname=companyname)
#                 print('purchase_ref, type(purchase_ref)',purchase_ref,type(purchase_ref))
#                 invoice_no=purchase_ref
#                 print('invoice_no',invoice_no)
#                 pe=models.Purchase_Entry.objects.get(invoice_no=invoice_no)
#                 print(se,pe)
#                 initial['supplier_ref']=se
#                 initial['purchase_ref']=pe
#             except ObjectDoesNotExist:
#                 message='ObjectDoesNotExist exeception occured se itemEntry '
#
#         if form.is_valid():
#
#             record=models.Item_Entry.objects.create(**initial)
#
#
#
#             print('saving ie, record:',record)
#             print( item_code,print_name)
#
#
#         ##
#         try:
#             areports=models.Item_Entry.objects.all()
#             my_dict['areports']=areports
#         except ObjectDoesNotExist:
#             message='ObjectDoesNotExist exeception occured itemEntry report'
#
#         ##
#         return render(request,'testapp/item_results.html',my_dict)
#     else:
#         form=forms.Item_Entry_form2()  # 1 -->2  changed, revert later
#         my_dict['form']= form
#         return render(request,'testapp/iform.html',my_dict)
def process_create_item_new_post(request):
    my_dict={}
    form=forms.Item_Entry_form2(request.POST) # 1-->2 changed , revertback later
    print('create item',form.is_valid())

    if  form.is_valid()==False :
        print('form errors' , form.errors)
        my_dict['errors']=form.errors

    if form.is_valid():
        item_code=form['item_code'].value()
        item_name=form['item_name'].value()
        print_name=form['print_name'].value()
        companyname=form['companyname'].value()
        HSN_code=form['HSN_code'].value()
        tabsPerStrip=form['tabsPerStrip'].value()
        NumStrips=form['NumStrips'].value()
        Mfd_by=form['Mfd_by'].value()
        MRP=form['MRP'].value()
        BatchNo=form['BatchNo'].value()
        #Mfd_date=form.cleaned_data['Mfd_date']  #hiding so form does not contain , should not read
        Exp_date=form.cleaned_data['Exp_date']
        purchase_rate=form['purchase_rate'].value()
        # purchase_cost_per_unit=form['purchase_cost_per_unit'].value()
        # sell_cost_per_unit=form['sell_cost_per_unit'].value()
        # Qty_in=form['Qty_in'].value()
        # Qty_available=form['Qty_available'].value()
        amount=form['amount'].value()
        # purchased_date=form.cleaned_data['purchased_date']
        supplier_ref=form['supplier_ref'].value()
        purchase_ref=form['purchase_ref'].value()
        tax_percent=form["tax_percent"].value()
        Discount_per=form["Discount_per"].value()
        low_stock_ind_per=form["low_stock_ind_per"].value() #26-Sep
        #low_stock_ind_status=form["low_stock_ind_status"].value() #26-Sep
        # status=form["status"].value() #30-Sep
        sch=form["sch"].value()
    ##logic to calculate field sell_cost_per_unit, disc_amount, tax_amount
        print(type(tabsPerStrip),type(NumStrips))
        print(tabsPerStrip,NumStrips)
        Qty_in= int(tabsPerStrip) *int(NumStrips)
        Qty_available=0
        temp=Decimal(Decimal(MRP)/Decimal(tabsPerStrip)) # 1-Oct
        sell_cost_per_unit= temp/(1+Decimal(tax_percent))   # calculated field sell_cost_per_unit
        print('IE- sell_cost_per_unit',sell_cost_per_unit)
        purchase_cost_per_unit=round(Decimal(purchase_rate)/Decimal(tabsPerStrip),3)  # calculated field purchase_cost_per_unit
        amount= round(Decimal(purchase_cost_per_unit) * Decimal(Qty_in),3)
        disc_amount=round(Decimal(amount) * Decimal(Discount_per),3)
        tax_amount= round((Decimal(amount)-Decimal(disc_amount)) * Decimal(tax_percent),3) # apply tax on taking discount


        print("tax_amount",tax_amount)
        print("amount",amount)
        print('tax_percent, sell_cost_per_unit',tax_percent,sell_cost_per_unit)
        print('purchase_cost_per_unit',purchase_cost_per_unit)

    ##

        initial={
        "item_code":item_code,
        "item_name":item_name.capitalize(),
        "print_name":print_name.capitalize(),
        "companyname":companyname,
        "HSN_code":HSN_code.capitalize(),
        "tabsPerStrip":tabsPerStrip,
        "NumStrips":NumStrips,
        "Mfd_by":Mfd_by,
        "MRP":MRP,
        "BatchNo":BatchNo.capitalize(),
        #"Mfd_date":Mfd_date,
        "Exp_date":Exp_date,
        "purchase_rate":purchase_rate,
        "purchase_cost_per_unit":purchase_cost_per_unit,
        "sell_cost_per_unit":sell_cost_per_unit,
        "Qty_in":Qty_in,
        "Qty_available":Qty_available,
        "Discount_per":Discount_per,
        "tax_percent":tax_percent,
        "amount":amount,
        "tax_amount":tax_amount,
        # "purchased_date":purchased_date,
        "supplier_ref":supplier_ref,
        "purchase_ref":purchase_ref,
        "low_stock_ind_per":low_stock_ind_per, #26-Sep
        #low_stock_ind_status":low_stock_ind_status, #26-Sep   donot read from form
        # "status":status, #30-Sep
        "disc_amount":disc_amount, #2-Oct
        "sch":sch.capitalize(),
        }
        initial['tax_amount']=tax_amount
        try:
            se=models.Supplier_Address.objects.get(companyname=companyname)
            print('purchase_ref, type(purchase_ref)',purchase_ref,type(purchase_ref))
            invoice_no=purchase_ref
            print('invoice_no',invoice_no)
            pe=models.Purchase_Entry.objects.get(invoice_no=invoice_no)
            print(se,pe)
            initial['supplier_ref']=se
            initial['purchase_ref']=pe
        except ObjectDoesNotExist:
            message='ObjectDoesNotExist exeception occured se itemEntry '

    if form.is_valid():
        record=models.Item_Entry.objects.create(**initial)
        print('saving ie, record:',record)



    ##
    try:
        # areports=models.Item_Entry.objects.all() #check This
        areports=models.Item_Entry.objects.filter(purchase_ref__invoice_no=invoice_no)
        print('check this process_create_item_new_post()')
        my_dict['areports']=areports
    except ObjectDoesNotExist:
        message='ObjectDoesNotExist exeception occured itemEntry report'

    ##
    return my_dict

def create_item_new(request):
    # addItem1/

    if request.method=='POST':

        my_dict=process_create_item_new_post(request)
        my_dict['title']='Item_Entry'
        return render(request,'testapp/item_results.html',my_dict)
    else:
        my_dict={}
        # abc=request.session.get('abc')   working
        # abc=request.COOKIES.get('xyz')
        # print('reading cookies create_item_new:abc:',abc)
        form=forms.Item_Entry_form2()  # 1 -->2  changed, revert later
        my_dict['form']= form
        return render(request,'testapp/iform_autofill.html',my_dict)
def create_item_new2(request):# may not be using , seems to be just created
    # addItem2/

    if request.method=='POST':
        my_dict=process_create_item_new_post(request)
        my_dict['title']='Item_Entry'
        return render(request,'testapp/item_results_pe.html',my_dict)
    else:
        my_dict={}
        form=forms.Item_Entry_form2()  # 1 -->2  changed, revert later
        my_dict['form']= form
        return render(request,'testapp/iform_autofill.html',my_dict)

def create_item_new1(request,invoice_no):
    # addItem1/<str:invoice_no>/

    my_dict={}
    my_dict['title']='Item_Entry'

    pe=models.Purchase_Entry.objects.get(invoice_no=invoice_no)
    areports=models.Item_Entry.objects.filter(purchase_ref__invoice_no=invoice_no)
    my_dict['areports']=areports
    my_dict['pe']=pe


    if request.method=='POST':
        form=forms.Item_Entry_form2(request.POST) # 1-->2 changed , revertback later
        print('create item',form.is_valid())
        print('sssssssss1234')
        if  form.is_valid()==False :
            print('form errors' , form.errors)
            my_dict['errors']=form.errors


        if form.is_valid():
            item_code=form['item_code'].value()
            item_name=form['item_name'].value()
            print_name=form['print_name'].value()
            companyname=form['companyname'].value()
            HSN_code=form['HSN_code'].value()
            tabsPerStrip=form['tabsPerStrip'].value()
            NumStrips=form['NumStrips'].value()
            Mfd_by=form['Mfd_by'].value()
            MRP=form['MRP'].value()
            BatchNo=form['BatchNo'].value()
            #Mfd_date=form.cleaned_data['Mfd_date']  #hiding so form does not contain , should not read
            Exp_date=form.cleaned_data['Exp_date']
            purchase_rate=form['purchase_rate'].value()
            # purchase_cost_per_unit=form['purchase_cost_per_unit'].value()
            # sell_cost_per_unit=form['sell_cost_per_unit'].value()
            # Qty_in=form['Qty_in'].value()
            # Qty_available=form['Qty_available'].value()
            amount=form['amount'].value()
            # purchased_date=form.cleaned_data['purchased_date']
            supplier_ref=form['supplier_ref'].value()
            purchase_ref=form['purchase_ref'].value()
            tax_percent=form["tax_percent"].value()
            Discount_per=form["Discount_per"].value()
            low_stock_ind_per=form["low_stock_ind_per"].value() #26-Sep
            #low_stock_ind_status=form["low_stock_ind_status"].value() #26-Sep
            # status=form["status"].value() #30-Sep
            sch=form["sch"].value()
        ##logic
            print(type(tabsPerStrip),type(NumStrips))
            print(tabsPerStrip,NumStrips)
            Qty_in= int(tabsPerStrip) *int(NumStrips)
            Qty_available=0
            temp=Decimal(Decimal(MRP)/Decimal(tabsPerStrip)) # 1-Oct
            sell_cost_per_unit= temp/(1+Decimal(tax_percent))   # calculated field sell_cost_per_unit
            print('IE- sell_cost_per_unit',sell_cost_per_unit)
            purchase_cost_per_unit=round(Decimal(purchase_rate)/Decimal(tabsPerStrip),3)  # calculated field purchase_cost_per_unit
            amount= round(Decimal(purchase_cost_per_unit) * Decimal(Qty_in),3)
            disc_amount=round(Decimal(amount) * Decimal(Discount_per),3)
            tax_amount= round((Decimal(amount)-Decimal(disc_amount)) * Decimal(tax_percent),3) # apply tax on taking discount


            print("tax_amount",tax_amount)
            print("amount",amount)
            print('tax_percent, sell_cost_per_unit',tax_percent,sell_cost_per_unit)
            print('purchase_cost_per_unit',purchase_cost_per_unit)

        ##

            initial={
            "item_code":item_code,
            "item_name":item_name.capitalize(),
            "print_name":print_name.capitalize(),
            "companyname":companyname,
            "HSN_code":HSN_code.capitalize(),
            "tabsPerStrip":tabsPerStrip,
            "NumStrips":NumStrips,
            "Mfd_by":Mfd_by,
            "MRP":MRP,
            "BatchNo":BatchNo.capitalize(),
            #"Mfd_date":Mfd_date,
            "Exp_date":Exp_date,
            "purchase_rate":purchase_rate,
            "purchase_cost_per_unit":purchase_cost_per_unit,
            "sell_cost_per_unit":sell_cost_per_unit,
            "Qty_in":Qty_in,
            "Qty_available":Qty_available,
            "Discount_per":Discount_per,
            "tax_percent":tax_percent,
            "amount":amount,
            "tax_amount":tax_amount,
            # "purchased_date":purchased_date,
            "supplier_ref":supplier_ref,
            "purchase_ref":purchase_ref,
            "low_stock_ind_per":low_stock_ind_per, #26-Sep
            #low_stock_ind_status":low_stock_ind_status, #26-Sep   donot read from form
            # "status":status, #30-Sep
            "disc_amount":disc_amount, #2-Oct
            "sch":sch.capitalize(),
            }
            initial['tax_amount']=tax_amount
            try:
                se=models.Supplier_Address.objects.get(companyname=companyname)
                print('purchase_ref, type(purchase_ref)',purchase_ref,type(purchase_ref))
                invoice_no=purchase_ref
                print('invoice_no',invoice_no)
                pe=models.Purchase_Entry.objects.get(invoice_no=invoice_no)
                print(se,pe)
                initial['supplier_ref']=se
                initial['purchase_ref']=pe
            except ObjectDoesNotExist:
                message='ObjectDoesNotExist exeception occured se itemEntry '

        if form.is_valid():
            record=models.Item_Entry.objects.create(**initial)
            print('saving ie, record:',record)
        print('bf cal_ie_amount')
        my_dict1=cal_ie_amount(invoice_no)


        ##
        try:
            areports=models.Item_Entry.objects.filter(purchase_ref__invoice_no=invoice_no)
            my_dict['areports']=areports
            pe=models.Purchase_Entry.objects.get(invoice_no=invoice_no)
            initial_ie={ 'supplier_ref':pe.supplier_ref1, 'purchase_ref':pe}
            form=forms.Item_Entry_form2(initial=initial_ie)  # 1 -->2  changed, revert later
            my_dict['form']= form
            my_dict['pe']=pe
            # my_dict['areports']=areports

        except ObjectDoesNotExist:
            message='ObjectDoesNotExist exeception occured itemEntry report'

        dict={**my_dict1,**my_dict}
        my_dict=dict
        print(my_dict)
        ##
        return render(request,'testapp/item_results_pe.html',my_dict)
        # return render(request,'testapp/iform.html',my_dict)


    else:  #GET
        # based on invoice get supplier_ref1  and initialize in form
        # pe=models.Purchase_Entry.objects.get(invoice_no=invoice_no)
        initial_ie={ 'supplier_ref':pe.supplier_ref1, 'purchase_ref':pe}
        form=forms.Item_Entry_form2(initial=initial_ie)  # 1 -->2  changed, revert later
        my_dict['form']= form
        my_dict1=cal_ie_amount(invoice_no)
        dict={**my_dict1,**my_dict}
        my_dict=dict
        my_dict['pe']=pe
        areports=models.Item_Entry.objects.filter(purchase_ref__invoice_no=invoice_no)
        my_dict['areports']=areports

        # return render(request,'testapp/iform.html',my_dict)
        return render(request,'testapp/item_results_pe.html',my_dict)

def cal_ie_amount(invoice_no):
    my_dict={}
    pe_invoice=invoice_no
    pe=models.Purchase_Entry.objects.get(invoice_no=invoice_no)
    ie_sum=models.Item_Entry.objects.filter(purchase_ref__invoice_no= pe_invoice).aggregate(Sum('amount'))
    ie_taxsum=models.Item_Entry.objects.filter(purchase_ref__invoice_no= pe_invoice).aggregate(Sum('tax_amount'))
    ie_dissum=models.Item_Entry.objects.filter(purchase_ref__invoice_no= pe_invoice).aggregate(Sum('disc_amount'))

    try:
        ie_sum=ie_sum['amount__sum']
        ie_taxsum=ie_taxsum['tax_amount__sum']
        ie_dissum=ie_dissum['disc_amount__sum']
    except KeyError:
        print('KeyError occured in Item_EntryList_based_on_id_View')
    print('ie_sum',ie_sum)
    print('ie_taxsum type 11111',ie_sum,ie_taxsum,ie_dissum )

    if ie_taxsum==None:
        ie_taxsum=0.0
    if ie_sum==None:
        ie_sum=0.0
    if ie_dissum ==None:
        ie_dissum=0.0

    ie_taxsum=round(Decimal(ie_taxsum),2)  #111
    # ie_qtysum=ie_qtysum['Qty_in__sum']
    ie_grandtotal= round((Decimal(ie_sum)+Decimal(ie_taxsum)-Decimal(ie_dissum)),2)

    my_dict={ 'ie_sum':ie_sum,'ie_taxsum': ie_taxsum }
    my_dict['ie_grandtotal']=ie_grandtotal
    ie_grand_tot=int(ie_grandtotal)

    my_dict['ie_grand_tot']=ie_grand_tot
    my_dict['diff_grandtot']=round((Decimal(pe.invoice_amount+pe.adjustment )-Decimal(ie_grandtotal)) ,3)

    my_dict['pe']=pe
    return my_dict

def ie_dict_init(ie):
    ie_dict={
    "item_code":ie.item_code,
    "item_name":ie.item_name.capitalize(),
    "print_name":ie.print_name.capitalize(),
    "companyname":ie.companyname,
    "HSN_code":ie.HSN_code.upper(),
    "tabsPerStrip":ie.tabsPerStrip,
    "NumStrips":ie.NumStrips,
    "Mfd_by":ie.Mfd_by,
    "MRP":ie.MRP,
    "BatchNo":ie.BatchNo,
    "Mfd_date":ie.Mfd_date,
    "Exp_date":ie.Exp_date,
    "purchase_rate":ie.purchase_rate,
    "purchase_cost_per_unit":ie.purchase_cost_per_unit,
    "sell_cost_per_unit":ie.sell_cost_per_unit,
    "Qty_in":ie.Qty_in,
    "Qty_available":ie.Qty_available,
    "Discount_per":ie.Discount_per,
    "tax_percent":ie.tax_percent,
    "amount":ie.amount,
    "purchased_date":ie.purchased_date,
    "supplier_ref":ie.supplier_ref,
    "purchase_ref":ie.purchase_ref,
    "tax_amount":ie.tax_amount,
    "low_stock_ind_per":ie.low_stock_ind_per,     #26-sep
    "low_stock_ind_status":ie.low_stock_ind_status,   #26-sep
    "status":ie.status,                                #30-Sep
    "sch":ie.sch,                                      #1-Oct
    }
    return ie_dict
## clone Item Entry

def clone_item_new(request,id):
    # 'clone_ie/<int:id>'
    print('entering clone_item_new')
    my_dict={}

    ie=models.Item_Entry.objects.get(id=int(id))
    if request.method=='POST':
        print('entering clone_item_new :POST')
        # form=forms.Item_Entry_form2(request.POST)
        # print('create item',form.is_valid())
        # if form.is_valid():
        #     item_code=form['item_code'].value()
        #     item_name=form['item_name'].value()
        #     print_name=form['print_name'].value()
        #     companyname=form['companyname'].value()
        #     HSN_code=form['HSN_code'].value()
        #     tabsPerStrip=form['tabsPerStrip'].value()
        #     NumStrips=form['NumStrips'].value()
        #     Mfd_by=form['Mfd_by'].value()
        #     MRP=form['MRP'].value()
        #     BatchNo=form['BatchNo'].value()
        #     #Mfd_date=form.cleaned_data['Mfd_date']  #hiding so form does not contain , should not read
        #     Exp_date=form.cleaned_data['Exp_date']
        #     purchase_rate=form['purchase_rate'].value()
        #     # purchase_cost_per_unit=form['purchase_cost_per_unit'].value()
        #     # sell_cost_per_unit=form['sell_cost_per_unit'].value()
        #     # Qty_in=form['Qty_in'].value()
        #     # Qty_available=form['Qty_available'].value()
        #     amount=form['amount'].value()
        #     # purchased_date=form.cleaned_data['purchased_date']
        #     supplier_ref=form['supplier_ref'].value()
        #     purchase_ref=form['purchase_ref'].value()
        #     tax_percent=form["tax_percent"].value()
        #     Discount_per=form["Discount_per"].value()
        #     low_stock_ind_per=form["low_stock_ind_per"].value() #26-Sep
        #     #low_stock_ind_status=form["low_stock_ind_status"].value() #26-Sep
        #     # status=form["status"].value() #30-Sep
        #     sch=form["sch"].value()
        # ##logic
        #     print(type(tabsPerStrip),type(NumStrips))
        #     print(tabsPerStrip,NumStrips)
        #     Qty_in= int(tabsPerStrip) *int(NumStrips)
        #     Qty_available=0
        #     temp=Decimal(Decimal(MRP)/Decimal(tabsPerStrip)) # 1-Oct
        #     sell_cost_per_unit= temp/(1+Decimal(tax_percent))
        #     print('IE- sell_cost_per_unit',sell_cost_per_unit)
        #     purchase_cost_per_unit=round(Decimal(purchase_rate)/Decimal(tabsPerStrip),3)
        #     amount= round(Decimal(purchase_cost_per_unit) * Decimal(Qty_in),3)
        #     tax_amount= round(Decimal(amount) * Decimal(tax_percent),3)
        #     disc_amount=round(Decimal(amount) * Decimal(Discount_per),3)
        #
        #     print("tax_amount",tax_amount)
        #     print("amount",amount)
        #     print('tax_percent, sell_cost_per_unit',tax_percent,sell_cost_per_unit)
        #     print('purchase_cost_per_unit',purchase_cost_per_unit)
        #
        # ##
        #
        # initial={
        # "item_code":item_code,
        # "item_name":item_name.capitalize(),
        # "print_name":print_name.capitalize(),
        # "companyname":companyname,
        # "HSN_code":HSN_code.capitalize(),
        # "tabsPerStrip":tabsPerStrip,
        # "NumStrips":NumStrips,
        # "Mfd_by":Mfd_by,
        # "MRP":MRP,
        # "BatchNo":BatchNo.capitalize(),
        # #"Mfd_date":Mfd_date,
        # "Exp_date":Exp_date,
        # "purchase_rate":purchase_rate,
        # "purchase_cost_per_unit":purchase_cost_per_unit,
        # "sell_cost_per_unit":sell_cost_per_unit,
        # "Qty_in":Qty_in,
        # "Qty_available":Qty_available,
        # "Discount_per":Discount_per,
        # "tax_percent":tax_percent,
        # "amount":amount,
        # "tax_amount":tax_amount,
        # # "purchased_date":purchased_date,
        # "supplier_ref":supplier_ref,
        # "purchase_ref":purchase_ref,
        # "low_stock_ind_per":low_stock_ind_per, #26-Sep
        # #low_stock_ind_status":low_stock_ind_status, #26-Sep   donot read from form
        # # "status":status, #30-Sep
        # "disc_amount":disc_amount, #2-Oct
        # "sch":sch.capitalize(),
        # }
        # initial['tax_amount']=tax_amount
        # try:
        #     se=models.Supplier_Address.objects.get(companyname=companyname)
        #     print('purchase_ref, type(purchase_ref)',purchase_ref,type(purchase_ref))
        #     invoice_no=purchase_ref
        #     print('invoice_no',invoice_no)
        #     pe=models.Purchase_Entry.objects.get(invoice_no=invoice_no)
        #     print(se,pe)
        #     initial['supplier_ref']=se
        #     initial['purchase_ref']=pe
        # except ObjectDoesNotExist:
        #     message='ObjectDoesNotExist exeception occured se itemEntry '
        #
        # if form.is_valid():
        #
        #     record=models.Item_Entry.objects.create(**initial)
        #     print('saving ie, record:',record)
        # print( item_code,print_name)
        #
        #
        # ##
        # try:
        #     areports=models.Item_Entry.objects.all()
        #     my_dict['areports']=areports
        # except ObjectDoesNotExist:
        #     message='ObjectDoesNotExist exeception occured itemEntry report'

        ##
        my_dict=process_create_item_new_post(request)
        my_dict['title']='clone_Item_Entry'
        return render(request,'testapp/item_results.html',my_dict)
    else:
        print('entering clone_item_new :GET')
        ie_dict=ie_dict_init(ie)
        print(ie.supplier_ref)
        form=forms.Item_Entry_form2(initial=ie_dict)  #  1 -->2 changed 1-Oct
        my_dict['form']= form
        return render(request,'testapp/iformx.html',my_dict)


def clone_item_Entry_pe_view(request,id,invoice_no):
    # 'clone_ie/<int:id>'
    print('entering clone_item_new')
    my_dict={}

    ie=models.Item_Entry.objects.get(id=int(id))
    if request.method=='POST':
        print('entering clone_item_new :POST')

        my_dict=process_create_item_new_post(request)
        my_dict['title']='clone_Item_Entry'
        return redirect('addItem_1',invoice_no=invoice_no)  #/ie_list/invoice_no
        # return redirect('Item_EntryList_based_on_id',id=invoice_no)  #not prefer
        # return render(request,'testapp/item_results_pe.html',my_dict)  #not prefer

    else:
        print('entering clone_item_new :GET')
        ie_dict=ie_dict_init(ie)
        form=forms.Item_Entry_form2(initial=ie_dict)  #  1 -->2 changed 1-Oct
        my_dict['form']= form
        return render(request,'testapp/iformx.html',my_dict)
##

def create_purchase(request):
    # 'addPE/'  1)creates purchase entry 2) shows relavent item entries
    my_dict={}
    my_dict['title']='Purchase_Entry'
    if request.method=='POST':
        form=forms.Purchase_Entry_form(request.POST)
        print('create pe',form.is_valid())
        if form.is_valid():
            my_dict['result']=form.save()
            pe_invoice=form.cleaned_data['invoice_no']
            request.session['pe_invoice']= pe_invoice  #add PE  to session
            companyname=request.POST['supplier_ref1']
            print('companyname:', companyname)
        #
            try:
                areports=models.Item_Entry.objects.filter(supplier_ref__companyname=companyname)
                my_dict['areports']=areports
                print("type", type(areports))


            except ObjectDoesNotExist:
                message='ObjectDoesNotExist exeception occured itemEntry report'

        #
        return render(request,'testapp/pe_results.html',my_dict)
    else:
        form=forms.Purchase_Entry_form()
        my_dict['form']= form
        return render(request,'testapp/iform.html',my_dict)

def create_purchase1(request):
    # 'addPE/'  1)creates purchase entry 2) show PE list
    my_dict={}
    my_dict['title']='Purchase_Entry'
    if request.method=='POST':
        form=forms.Purchase_Entry_form(request.POST)
        print('create pe',form.is_valid())
        if form.is_valid():
            my_dict['result']=form.save()
            pe_invoice=form.cleaned_data['invoice_no']
            request.session['pe_invoice']= pe_invoice  #add PE  to session
            companyname=request.POST['supplier_ref1']
            print('companyname:', companyname)
        #
            try:
                pe=models.Purchase_Entry.objects.get(invoice_no=pe_invoice)
                my_dict['pe']=pe
                # areports=models.Item_Entry.objects.filter(purchase_ref__invoice_no=pe_invoice)
                # my_dict['areports']=areports
                # print("type", type(areports),areports)


            except ObjectDoesNotExist:
                message='ObjectDoesNotExist exeception occured itemEntry report'
        if form.errors:
            my_dict['error']=form.errors
        #
        return render(request,'testapp/pe_results1.html',my_dict)
    else:
        form=forms.Purchase_Entry_form()
        my_dict['form']= form
        return render(request,'testapp/iform.html',my_dict)

def Item_EntryListView(request):
    # 'ie_list/' list all item entries
    areports=models.Item_Entry.objects.all() #.filter(status='APPROVED')
    return render(request,'testapp/item_entry_list.html',{'title':'Item List','areports':areports})

def Item_EntryList_based_on_id_View(request,id):   #display item_list based on invoice_no of PE
    # 'ie_list/<str:id>' list all item entries based on invoice_no
    print('in ie_list/<int:id>  Item_EntryList_based_on_id_View')
    areports=models.Item_Entry.objects.all().filter(purchase_ref__invoice_no=id)

    pe_invoice=id
    ie_sum=models.Item_Entry.objects.filter(purchase_ref__invoice_no= pe_invoice).aggregate(Sum('amount'))
    ie_taxsum=models.Item_Entry.objects.filter(purchase_ref__invoice_no= pe_invoice).aggregate(Sum('tax_amount'))
    ie_qtysum=models.Item_Entry.objects.filter(purchase_ref__invoice_no= pe_invoice).aggregate(Sum('Qty_in'))
    ie_count=models.Item_Entry.objects.filter(purchase_ref__invoice_no= pe_invoice).count()
    ie_dissum=models.Item_Entry.objects.filter(purchase_ref__invoice_no= pe_invoice).aggregate(Sum('disc_amount'))
    print('ie_count:',ie_count)
    try:
        ie_sum=ie_sum['amount__sum']
        ie_taxsum=ie_taxsum['tax_amount__sum']
        ie_dissum=ie_dissum['disc_amount__sum']
    except KeyError:
        print('KeyError occured in Item_EntryList_based_on_id_View')
    print('ie_sum',ie_sum)
    print('ie_taxsum type 11111',ie_sum,ie_taxsum,ie_dissum )

    if ie_taxsum==None:
        ie_taxsum=0.0
    if ie_sum==None:
        ie_sum=0.0
    if ie_dissum ==None:
        ie_dissum=0.0

    ie_taxsum=round(Decimal(ie_taxsum),2)  #111
    ie_qtysum=ie_qtysum['Qty_in__sum']

    if ie_qtysum==None:
        ie_qtysum=0   #
    ie_grandtotal= round((Decimal(ie_sum)+Decimal(ie_taxsum)-Decimal(ie_dissum)),2)
    pe=models.Purchase_Entry.objects.get(invoice_no= pe_invoice)
    print('ie_qtysum',ie_qtysum)

    my_dict={'areports':areports, 'ie_count':ie_count,'ie_sum':ie_sum,'ie_taxsum': ie_taxsum }
    my_dict['ie_grandtotal']=ie_grandtotal
    # s=str(ie_grandtotal)
    # ie_grand_tot=int(ie_grandtotal)
    ie_grand_tot=int(ie_grandtotal)
    # print('ie_grand_tot',ie_grand_tot)
    my_dict['ie_grand_tot']=ie_grand_tot
    # print('slug ie-grandtot: ',ie_grand_tot)
    my_dict['diff_grandtot']=round(Decimal(pe.invoice_amount+pe.adjustment )-Decimal(ie_grandtotal),3) #pe.grand_total replaced by invoice_amount
    my_dict['ie_qtysum']=ie_qtysum
    my_dict['pe']=pe


    return render(request,'testapp/item_entry_list_id.html',my_dict)

def pe_approval_view(request,id,ie_grand_tot):
    # 'pe_approval/<int:id>/<str:ie_grand_tot>'
    pe_invoice=id
    # ie_grand_tot=ie_grand_tot.replace('-','.')
    print('pe_approval_view: ie_grand_tot ',ie_grand_tot)
    pe=models.Purchase_Entry.objects.get(invoice_no= pe_invoice)
    if pe.status=='APPROVED':
        print('Already approved no need to approve again')
        return redirect('addtoBill',id=id)
    else: # UN_APPROVED
        try:
            ies=models.Item_Entry.objects.all().filter(purchase_ref__invoice_no=id)
            ies_count=len(ies)
            print('ies count,',len(ies))
            if ies_count==0:
                print('no need to approve because no items are added')
                return redirect('addtoBill',id=id)
            else:
                pe_grand_tot=pe.invoice_amount
                pe_adjustment=pe.adjustment
                ie_grand_tot=ie_grand_tot
                print('pe_grand_total:{}, ie_grandtotal:{},pe_adjustment{}'.format(pe_grand_tot,ie_grand_tot,pe_adjustment))
                diff=abs(int(Decimal(pe_grand_tot+pe_adjustment-ie_grand_tot)))  # import take absolute value to avoid failusre incase pe.grandtotal =0
                print('diff:',diff)
                if diff<1:
                    print('matching so mark status to APPROVED')
                    pe.status='APPROVED'
                    pe.save()
                    print('pe status  changed to APPROVED',pe)
                    for ie in ies:
                        ie.status='APPROVED'
                        ie.Qty_available=ie.Qty_in    #Nov-23 missing
                        ie.save()
                        print('ie status  changed to APPROVED', ie)
                else:
                    print('amount diffence between invoice and item received ={}, reduced diff to less 1 and try'.format(diff))
        except ObjectDoesNotExist as e:
            print('no need to approve because no items are added')
            print(e)
            return redirect('addtoBill',id=id)

    return redirect('addtoBill',id=id)

def addto_PEView(request,id):    # not going to use
    # 'addtoPE/<int:id>'  add particular ie entry to Purchase entry bucket
    # ie=models.Item_Entry.objects.get(id=id)
    # print('ie',ie)
    request.session[id]= id
    return redirect('/q_item')

def addto_BillView(request,id):
    # 'addtoBill<int:id>'  add particular ie entry to Purchase entry bucket
    print('invoice_no',id)

    request.session['pe_invoice']= id
    return redirect('Item_EntryList_based_on_id',id=id)

def Purchase_Entry_view(request):
    # pe/ show selected item_entrys in session  # not using righnow
    l=[]
    if request.session:
        try:
            for k,v in request.session.items():
                if k.isnumeric():
                    ie=models.Item_Entry.objects.get(id=k)
                    l.append(ie)
        except ObjectDoesNotExist:
            print('ObjectDoesNotExist in pe/:Purchase_Entry_view')
            pass
    return render(request,'testapp/purchase_entry.html',{'areports':l})

def del_item_view(request, id):
    # 'del_item/<int:id>' deletes ie session entry
    try:
        ldict=request.session['ldict']

        for i in range(len(ldict)):
            if ldict[i]['id'] == id:
                del ldict[i]
                break
        request.session['ldict']=ldict
        print('ldict af',ldict)

    except KeyError:
        print('key error occured: id:', id)

    return redirect('/cart_list')

def update_item_view(request,id):   # going to comment this function
    my_dict={}
    my_dict['title']='update_Item_Entry'
    ie=models.Item_Entry.objects.get(id=int(id))
    if request.method=='POST':
        form=forms.Item_Entry_form(request.POST,instance=ie)
        if form.is_valid():
            form.save()
            print("updated")
            return redirect('/ie_list')
    else:

        item_dict={
        "item_code":ie.item_code,
        "item_name":ie.item_name,
        "print_name":ie.print_name,
        "companyname":ie.companyname,
        "HSN_code":ie.HSN_code,
        "tabsPerStrip":ie.tabsPerStrip,
        "NumStrips":ie.NumStrips,
        "Mfd_by":ie.Mfd_by,
        "MRP":ie.MRP,
        "BatchNo":ie.BatchNo,
        "Mfd_date":ie.Mfd_date,
        "Exp_date":ie.Exp_date,
        "purchase_cost_per_unit":ie.purchase_cost_per_unit,
        "sell_cost_per_unit":ie.sell_cost_per_unit,
        "Qty_in":ie.Qty_in,
        "Qty_out":ie.Qty_out,
        "Discount_per":ie.Discount_per,
        "tax_percent":ie.tax_percent,
        "amount":ie.amount,
        "purchased_date":ie.purchased_date,
        "supplier_ref":ie.supplier_ref

        }
        print(ie.item_code,ie.print_name)
        form=forms.Item_Entry_form(initial=item_dict)

        my_dict['form']= form
        return render(request,'testapp/iformx.html',my_dict)
def create_pbill(request):
    # 'generate_purchase bill/'
    my_dict={}
    my_dict={'title':'create purchase bill'}
    l=[]
    t_amount=0
    t_tax_amount=0
    t_Qty_in=0
    for k,v in request.session.items():
        if k.isnumeric():
            ie=models.Item_Entry.objects.get(id=k)
            l.append(ie)
            t_amount=t_amount+ie.amount
            t_tax_amount=t_tax_amount+ie.tax_amount
            t_Qty_in=t_Qty_in+ie.Qty_in
    my_dict['areports']=l
    my_dict['t_amount']=t_amount
    my_dict['t_tax_amount']=t_tax_amount
    my_dict['t_Qty_in']=t_Qty_in
    return render(request,'testapp/purchase_entry.html',my_dict)

def create_pbill_id(request,id):
    # 'generate_bill/<str:id>'
    my_dict={}
    my_dict={'title':'create purchase bill'}

    l=[]
    t_amount=0
    t_tax_amount=0
    t_grand_total=0
    t_Qty_in=0
    t_count=0
    try:
        pe=models.Purchase_Entry.objects.get(invoice_no=id)
        # my_dict['pe']=property
        # l.append(pe)
    except ObjectDoesNotExist:
        print('exception ObjectDoesNotExist in generate_bill/<str:id>/ create_pbill_id')
        redirect('/pe_list')
    # for k,v in request.session.items():
    #     if k.isnumeric():
    #         ie=models.Item_Entry.objects.get(id=k)
    ies=models.Item_Entry.objects.filter(purchase_ref__invoice_no=id)
    for ie in ies:
        l.append(ie)
        t_amount=t_amount+ie.amount
        t_tax_amount=t_tax_amount+ie.tax_amount
        t_grand_total=t_grand_total+ie.tax_amount+ie.amount
        t_Qty_in=t_Qty_in+ie.Qty_in
        t_count=t_count+1
    # my_dict['areports']=l
    # my_dict['t_amount']=t_amount
    # my_dict['t_tax_amount']=t_tax_amount
    # my_dict['t_Qty_in']=t_Qty_in
    ##
    print('t_count:', t_count)
    print('t_tax_amount:', t_tax_amount)
    print('t_Qty_in:', t_Qty_in)
    print('t_amount:', t_amount)
    print('ies:', ies)

    my_dict['pe']=pe
    my_dict['areports']=ies
    my_dict['ie_sum']=t_amount
    my_dict['ie_count']=t_count
    my_dict['ie_tax_amount']=t_tax_amount
    my_dict['ie_Qty_in']=t_Qty_in
    my_dict['t_grand_total']=t_grand_total
    ##
    # pdf=render_to_pdf('pdf/invoice.html',{'areports':ies,'pe':pe,'ie_count':t_count,'ie_Qty_in':t_Qty_in,'ie_sum':t_amount,'ie_tax_amount':t_tax_amount ,'t_grand_total':t_grand_total}) #working
    pdf=render_to_pdf('pdf/invoice.html',my_dict)
    return HttpResponse(pdf, content_type='application/pdf')

    # return render(request,'testapp/purchase_entry_id.html',my_dict)
###
def create_rbill_id(request,id):
    # 'generate_rbill/<str:id>'
    my_dict={}
    my_dict={'title':'create retail bill'}

    l=[]
    t_amount=0
    t_tax_amount=0
    t_grand_total=0
    t_Qty_sold=0
    t_count=0
    try:
        se=models.Sell_Entry.objects.get(bill_no=int(id))
        if se.status!='LOCKED':
            print('redirect to bill payment')
            return redirect('pay_rbill_name',id=id)
    except ObjectDoesNotExist:
        print('exception ObjectDoesNotExist in generate_ bill/<str:id>/ create_sbill_id')
        redirect('/q_item1')
    # for k,v in request.session.items():
    #     if k.isnumeric():
    #         ie=models.Item_Entry.objects.get(id=k)
    ies=models.Out_Item_Entry.objects.filter(bill_no_ref__bill_no=int(id))
    print('oie  rbill {}, no{} '.format( ies,len(ies)) )
    if len(ies)==0:
        print('no items select first select and pay')
        return redirect('pay_rbill_name',id=id)
    for ie in ies:
        # l.append(ie)
        t_amount=t_amount+ie.bill_item_amount
        t_tax_amount=t_tax_amount+ie.bill_tax_amount
        t_grand_total=t_grand_total+ie.bill_tax_amount+ie.bill_item_amount
        t_Qty_sold=t_Qty_sold+ie.Qty_sold
        t_count=t_count+1
    # my_dict['areports']=l
    # my_dict['t_amount']=t_amount
    # my_dict['t_tax_amount']=t_tax_amount
    # my_dict['t_Qty_in']=t_Qty_in
    ##
    print('t_count:', t_count)
    print('t_tax_amount:', t_tax_amount)
    print('t_Qty_sold:', t_Qty_sold)
    print('t_amount:', t_amount)
    print('ies:', ies)

    my_dict['se']=se
    my_dict['areports']=ies
    my_dict['ie_sum']=t_amount
    my_dict['ie_count']=t_count
    my_dict['ie_tax_amount']=t_tax_amount
    my_dict['ie_Qty_in']=t_Qty_sold
    my_dict['t_grand_total']=t_grand_total
    # my_dict['t_grand_total_in_words']=num2words(round(t_grand_total,0),lang ='en_IN')
    my_dict['username']=request.user.username
    ###  update total retail amount, tax amount, grand total and sell date in Sell_Entry
    if se.status!='LOCKED':
        se.bill_amount=t_amount
        se.tax_amount=t_tax_amount
        se.grand_total=t_grand_total
        se.sell_datetime= datetime.datetime.now()
        # se.status='LOCKED'
        record=se.save(update_fields=['bill_amount','tax_amount','grand_total','sell_datetime','status'])
        print('se update record:',record,se.sell_datetime )
    print('se22 update record:',se.sell_datetime )

    # pdf=render_to_pdf('pdf/invoice.html',{'areports':ies,'pe':pe,'ie_count':t_count,'ie_Qty_in':t_Qty_in,'ie_sum':t_amount,'ie_tax_amount':t_tax_amount ,'t_grand_total':t_grand_total}) #working
    pdf=render_to_pdf('pdf/invoice_retail_1.html',my_dict)
    return HttpResponse(pdf, content_type='application/pdf')

def create_rbill_id_new(request,id): #23-Nov
    # 'generate_rbill/<str:id>'
    my_dict={}
    my_dict={'title':'create retail bill'}

    l=[]
    t_amount=0
    t_tax_amount=0
    t_grand_total=0
    t_Qty_sold=0
    t_count=0
    t_cgst_amt=0
    t_sgst_amt=0

    try:
        se=models.Sell_Entry.objects.get(bill_no=int(id))
        if se.status!='LOCKED':
            print('redirect to bill payment')
            return redirect('pay_rbill_name',id=id)
    except ObjectDoesNotExist:
        print('exception ObjectDoesNotExist in generate_ bill/<str:id>/ create_sbill_id')
        redirect('/q_item1')
    # for k,v in request.session.items():
    #     if k.isnumeric():
    #         ie=models.Item_Entry.objects.get(id=k)
    ies=models.Out_Item_Entry.objects.filter(bill_no_ref__bill_no=int(id))
    print('oie  rbill {}, no{} '.format( ies,len(ies)) )
    if len(ies)==0:
        print('no items select first select and pay')
        return redirect('pay_rbill_name',id=id)
    for ie in ies:
        # l.append(ie)
        t_amount=t_amount+ie.bill_item_amount
        t_tax_amount=t_tax_amount+ie.bill_tax_amount
        t_grand_total=t_grand_total+ie.bill_tax_amount+ie.bill_item_amount
        t_Qty_sold=t_Qty_sold+ie.Qty_sold
        t_count=t_count+1
        t_cgst_amt=t_cgst_amt+ie.CGST_tax_amount
        t_sgst_amt=t_sgst_amt+ie.SGST_tax_amount

    # my_dict['areports']=l
    # my_dict['t_amount']=t_amount
    # my_dict['t_tax_amount']=t_tax_amount
    # my_dict['t_Qty_in']=t_Qty_in
    ##
    print('t_count:', t_count)
    print('t_tax_amount:', t_tax_amount)
    print('t_Qty_sold:', t_Qty_sold)
    print('t_amount:', t_amount)
    print('ies:', ies)

    my_dict['se']=se
    my_dict['areports']=ies
    my_dict['ie_sum']=t_amount
    my_dict['ie_count']=t_count
    my_dict['ie_tax_amount']=t_tax_amount
    my_dict['ie_Qty_in']=t_Qty_sold
    my_dict['ie_grand_total']=t_grand_total
    my_dict['ie_cgst_total']=t_cgst_amt
    my_dict['ie_sgst_total']=t_sgst_amt
    my_dict['net_payment']=se.paid_by_cash+se.paid_by_card


    # my_dict['t_grand_total_in_words']=num2words(round(t_grand_total,0),lang ='en_IN')
    my_dict['username']=request.user.username
    ###  update total retail amount, tax amount, grand total and sell date in Sell_Entry
    if se.status!='LOCKED':
        se.bill_amount=t_amount
        se.tax_amount=t_tax_amount
        se.grand_total=t_grand_total
        se.sell_datetime= datetime.datetime.now()
        # se.status='LOCKED'
        record=se.save(update_fields=['bill_amount','tax_amount','grand_total','sell_datetime','status'])
        print('se update record:',record,se.sell_datetime )
    print('se22 update record:',se.sell_datetime )

    # pdf=render_to_pdf('pdf/invoice.html',{'areports':ies,'pe':pe,'ie_count':t_count,'ie_Qty_in':t_Qty_in,'ie_sum':t_amount,'ie_tax_amount':t_tax_amount ,'t_grand_total':t_grand_total}) #working
    pdf=render_to_pdf('pdf/invoice_retail_2.html',my_dict)
    return HttpResponse(pdf, content_type='application/pdf')
###
def create_return_rbill_id(request,id):
    # 'generate_return_rbill/<str:id>'     rbill_no=id
    my_dict={}
    my_dict={'title':'create retail bill'}

    l=[]
    t_amount=0
    t_tax_amount=0
    t_grand_total=0
    t_Qty_returned=0
    t_count=0
    try:
        rse=models.Returned_Sell_Entry.objects.get(rbill_no=int(id))
        # my_dict['pe']=property
        # l.append(pe)
    except ObjectDoesNotExist:
        print('exception ObjectDoesNotExist in generate_ bill/<str:id>/ create_return_rbill_id')
        redirect('/q_item1')
    # for k,v in request.session.items():
    #     if k.isnumeric():
    #         ie=models.Item_Entry.objects.get(id=k)
    ies=models.Returned_Out_Item_Entry.objects.filter(rbill_no_ref__rbill_no=int(id))
    print('roie  rbill ', ies)
    for ie in ies:

        t_amount=t_amount+ie.rbill_item_amount
        t_tax_amount=t_tax_amount+ie.rbill_tax_amount
        t_grand_total=t_grand_total+ie.rbill_tax_amount+ie.rbill_item_amount
        t_Qty_returned=t_Qty_returned+ie.Qty_returned
        t_count=t_count+1

    ##
    print('t_count:', t_count)
    print('t_tax_amount:', t_tax_amount)
    print('t_Qty_returned:', t_Qty_returned)
    print('t_amount:', t_amount)
    print('roies:', ies)

    my_dict['rse']=rse
    my_dict['areports']=ies
    my_dict['ie_sum']=t_amount
    my_dict['ie_count']=t_count
    my_dict['ie_tax_amount']=t_tax_amount
    my_dict['ie_Qty_in']=t_Qty_returned
    my_dict['t_grand_total']=t_grand_total   #23-Nov
    my_dict['username']=request.user.username

    se_grand_total=rse.sell_entry_ref.grand_total
    se_discount_amount=rse.sell_entry_ref.discount_amount
    net_rpayment_bycash= t_grand_total*(1-(se_discount_amount/se_grand_total)) # calculate proportional discount
    my_dict['net_rpayment_bycash']=net_rpayment_bycash
    print('net_rpayment_bycash',net_rpayment_bycash)

    ###  update total retail amount, tax amount, grand total and sell date in Sell_Entry
    if rse.status!='LOCKED':
        rse.rbill_amount=t_amount
        rse.rbill_tax_amount=t_tax_amount
        rse.rbill_grand_total=t_grand_total
        rse.returned_sell_datetime= datetime.datetime.now()
        # rse.rpayment_by_cash=t_grand_total
        rse.rpayment_by_cash=net_rpayment_bycash  #
        rse.status='LOCKED'

        record=rse.save(update_fields=['rbill_amount','rbill_tax_amount','rbill_grand_total','returned_sell_datetime','rpayment_by_cash','status'])
        print('rse update record:',record,rse.returned_sell_datetime )

        ## lock  Roie entries as well  (so it does not allow to delete or update)
        roies=models.Returned_Out_Item_Entry.objects.all().filter(rbill_no_ref__rbill_no=rse.rbill_no)
        for roie in roies:
            roie.status='LOCKED'
            roie.save()
            print('generate_return_rbill/rbill_no={}>: pay_retail_bill_view...  roie status is LOCKED'.format(id,roie))


    print('se33 update record:',rse.returned_sell_datetime )

    # pdf=render_to_pdf('pdf/invoice_return_rretail.html',my_dict)
    pdf=render_to_pdf('pdf/invoice_return_rretail_2.html',my_dict)
    return HttpResponse(pdf, content_type='application/pdf')



##
def Purchase_EntryListView(request):
    # 'pe_list/'
    my_dict={}
    my_dict={'title':'Purchase Entry List'}
    print('entering Purchase_EntryListView')
    purchase_entry_list=models.Purchase_Entry.objects.all()
    my_dict['purchase_entry_list']=purchase_entry_list
    return render(request,'testapp/purchase_entry_list.html',my_dict)

# class PurchaseEntryListView(ListView):
#     model=PurchaseEntry
#     print('entering Purchase_EntryListView')
#     template_name='testapp/purchase_entry_list.html'
#     context_object_name='purchase_entry_list'
def del_Purchase_Entry_view(request, id):
    try:
        pe=models.Purchase_Entry.objects.get(invoice_no=id)
        pe.delete()
    except ObjectDoesNotExist:
        print('ObjectDoesNotExist exception occured in del_Purchase_Entry_view: id:', id)

    return redirect('/pe_list')
def  pe_dict_init(pe):
    pe_dict={
    "purchase_type":pe.purchase_type,
    "supplier_ref1":pe.supplier_ref1,
    "invoice_no":pe.invoice_no,
    "invoice_amount":pe.invoice_amount,
    "tax_amount":pe.tax_amount,
    "grand_total":pe.grand_total,
    "purchase_date":pe.purchase_date,
    "adjustment":pe.adjustment,
    "taxable_amount":pe.taxable_amount,
    "CGST_tax_amount":pe.CGST_tax_amount,
    "SGST_tax_amount":pe.SGST_tax_amount,

    }
    return pe_dict
def update_Purchase_Entry_view(request,id):
    function_name=sys._getframe().f_code.co_name
    my_dict={}
    my_dict['title']='update_Purchase_Entry'
    pe=models.Purchase_Entry.objects.get(invoice_no=id)

    if pe.status=='APPROVED':
        print(function_name, 'upd_pe/<int:id>: pe={} status is APPROVED , it cannot be updated'.format(pe.invoice_no))
        return redirect('/pe_list')

    if request.method=='POST':
        form=forms.Purchase_Entry_form(request.POST,instance=pe)
        if form.is_valid():
            invoice_amount=form.cleaned_data['invoice_amount']
            tax_amount=form.cleaned_data['tax_amount']
            taxable_amount= form.cleaned_data['taxable_amount']
            CGST_tax_amount=form.cleaned_data['CGST_tax_amount']
            SGST_tax_amount=form.cleaned_data['SGST_tax_amount']
            grand_total=Decimal(invoice_amount)+Decimal(tax_amount)
            ### update with calculated field
            form=forms.Purchase_Entry_form(request.POST,instance=pe)
            if form.is_valid():
                form.save()  # same form data into db, but it will not update calculated values, below Qty_in,amount,tax_amount
                x=models.Purchase_Entry.objects.filter(invoice_no=id).update(grand_total=grand_total, \
                taxable_amount=taxable_amount,CGST_tax_amount=CGST_tax_amount,SGST_tax_amount=SGST_tax_amount)
                print('upd/<str:id, PE upated',x)
            print("updated pe")
            # return redirect('/pe_list')
            return redirect('addItem_1', invoice_no=id)
    else:

        pe_dict=pe_dict_init(pe)
        print(pe.invoice_no,pe.supplier_ref1.companyname)
        form=forms.Purchase_Entry_form(initial=pe_dict)

        my_dict['form']= form
        return render(request,'testapp/iformx.html',my_dict)
#supplier
def del_Supplier_Address_view(request, id):
    try:
        pe=models.Supplier_Address.objects.get(companyname=id)
        pe.delete()
    except ObjectDoesNotExist:
        print('ObjectDoesNotExist exception occured in del_Purchase_Entry_view: id:', id)

    return redirect('/sup_list')

def update_Supplier_Address_view(request,id):
    # url: 'upd_sup/<str:id>'
    my_dict={}
    my_dict['title']='update_Purchase_Entry'
    pe=models.Supplier_Address.objects.get(companyname=id)
    if request.method=='POST':
        form=forms.Supplier_Address_form(request.POST,instance=pe)
        if form.is_valid():
            form.save()
            print("updated Supplier")
            return redirect('/sup_list') ## check
    else:

        pe_dict={
        "companyname":pe.companyname,
        "town":pe.town,
        "city":pe.city,
        "contact_name":pe.contact_name,
        "email":pe.email,
        "phone":pe.phone

        }

        form=forms.Supplier_Address_form(initial=pe_dict)

        my_dict['form']= form
        return render(request,'testapp/iformx.html',my_dict)

def supplier_address_list(request):
    #'sup_list/',
    my_dict={}
    my_dict['title']='supplier_address_list'
    areports=models.Supplier_Address.objects.all()
    my_dict['areports']=areports
    return render(request,'testapp/supplier_list.html',my_dict)
#
def customer_address_list(request):
    #'cus_list/',
    my_dict={}
    my_dict['title']='customer_address_list'
    areports=models.Customer_Address.objects.all()
    my_dict['areports']=areports
    return render(request,'testapp/customer_list.html',my_dict)

def del_customer_Address_view(request, id):
    # url: 'del_cus/<str:id>'
    my_dict={}
    my_dict['title']='Delete_Customer_Entry'
    try:
        cus=models.Customer_Address.objects.get(id=id)
        cus.delete()
    except ObjectDoesNotExist:
        print('ObjectDoesNotExist exception occured in del_customer_Address_view: id:', id)

    return redirect('/cus_list')

def update_customer_address_view(request,id):
    # url: 'upd_cus/<str:id>'
    my_dict={}
    my_dict['title']='Update_Customer_Entry'
    cus=models.Customer_Address.objects.get(id=int(id))
    if request.method=='POST':
        form=forms.Customer_Address_form(request.POST,instance=cus)
        if form.is_valid():
            form.save()
            print("updated customer")
            return redirect('/cus_list') ## check
    else:
        cus_dict={
        "contact_name":cus.contact_name,
        "email":cus.email,
        "phone":cus.phone,
        "Doctor_name":cus.Doctor_name,
        "hospital_id":cus.hospital_id,
        }
        form=forms.Customer_Address_form(initial=cus_dict)

        my_dict['form']= form
        return render(request,'testapp/iformx.html',my_dict)

# utili
def form_to_dict(form):
    # if form.is_valid():
    #     item_code=form.cleaned_data['item_code']
    #     item_name=form.cleaned_data['item_name']
    #     print_name=form.cleaned_data['print_name']
    #     companyname=form.cleaned_data['companyname']
    #     HSN_code=form.cleaned_data['HSN_code']
    #     tabsPerStrip=form.cleaned_data['tabsPerStrip']
    #     NumStrips=form.cleaned_data['NumStrips']
    #     Mfd_by=form.cleaned_data['Mfd_by']
    #     MRP=form.cleaned_data['MRP']
    #     BatchNo=form.cleaned_data['BatchNo']
    #     Mfd_date=form.cleaned_data['Mfd_date']
    #     Exp_date=form.cleaned_data['Exp_date']
    #     purchase_cost_per_unit=form.cleaned_data['purchase_cost_per_unit']
    #     sell_cost_per_unit=form.cleaned_data['sell_cost_per_unit']
    #     Qty_in=form.cleaned_data['Qty_in']
    #     Qty_out=form.cleaned_data['Qty_out']
    #     amount=form.cleaned_data['amount']
    #     purchased_date=form.cleaned_data['purchased_date']
    #     supplier_ref=form.cleaned_data['supplier_ref']
    #     tax_percent=form.cleaned_data["tax_percent"]
    #     Discount_per=form.cleaned_data["Discount_per"]
    #
    #
    # ##logic
    #
    # Qty_in=tabsPerStrip * NumStrips
    # Qty_out=Qty_in
    # tax_amount= round(Decimal(amount) * Decimal(tax_percent),3)
    # amount= round(Decimal(sell_cost_per_unit) * Decimal(Qty_in),3)
    # ##
    #
    # item_dict={
    # "item_code":item_code,
    # "item_name":item_name,
    # "print_name":print_name,
    # "companyname":companyname,
    # "HSN_code":HSN_code,
    # "tabsPerStrip":tabsPerStrip,
    # "NumStrips":NumStrips,
    # "Mfd_by":Mfd_by,
    # "MRP":MRP,
    # "BatchNo":BatchNo,
    # "Mfd_date":Mfd_date,
    # "Exp_date":Exp_date,
    # "purchase_cost_per_unit":purchase_cost_per_unit,
    # "sell_cost_per_unit":sell_cost_per_unit,
    # "Qty_in":Qty_in,
    # "Qty_out":Qty_out,
    # "Discount_per":Discount_per,
    # "tax_percent":tax_percent,
    # "amount":amount,
    # "purchased_date":purchased_date,
    # "supplier_ref":supplier_ref
    #
    # }
    #
    # form=forms.Item_Entry_form(initial=item_dict)
    # result=form.save()
    print('result',result, item_code,print_name)

#
def del_Item_Entry_view(request, id):
    # del_ie/<int:id>
    try:

        ie=models.Item_Entry.objects.get(id=id)
        if ie.status!='APPROVED':
            ie.delete()
        else:
            print('ie={} status is APPROVED , it cannot be deleted'.format(ie.id))

    except ObjectDoesNotExist:
        print('ObjectDoesNotExist exception occured in del_Item_Entry_view: id:', id)

    return redirect('/ie_list')

def del_Item_Entry_view1(request, id):
    # del_ie/<int:id>
    try:

        ie=models.Item_Entry.objects.get(id=id)
        if ie.status!='APPROVED':
            ie.delete()
        else:
            print('ie={} status is APPROVED , it cannot be deleted'.format(ie.id))

    except ObjectDoesNotExist:
        print('ObjectDoesNotExist exception occured in del_Item_Entry_view: id:', id)

    return redirect('Item_EntryList_based_on_id',id=ie.purchase_ref.invoice_no )

def del_Item_Entry_pe_view(request, id,invoice_no):
    #it will render back to item_results_pe.html
    # del_ie/<int:id>
    try:

        ie=models.Item_Entry.objects.get(id=id)
        if ie.status!='APPROVED':
            ie.delete()
        else:
            print('ie={} status is APPROVED , it cannot be deleted'.format(ie.id))

    except ObjectDoesNotExist:
        print('ObjectDoesNotExist exception occured in del_Item_Entry_view: id:', id)

    return redirect('addItem_1', invoice_no=invoice_no)



def update_Item_Entry_view(request,id):
    # 'upd_ie/<int:id>'
    function_name=sys._getframe().f_code.co_name
    my_dict={}
    my_dict['title']='update_Item_Entry'
    ie=models.Item_Entry.objects.get(id=int(id))
    if ie.status=='APPROVED':
        print(function_name, 'upd_ie/<int:id>: ie={} status is APPROVED , it cannot be updated 1111'.format(ie.id))

        return redirect('/ie_list')
    if request.method=='POST':
        process_upd_ie_post_view(request,id,ie)
        return redirect('/ie_list')

    else:

        my_dict=process_upd_ie_get_view(request,id,ie)
        my_dict['title']='update_Item_Entry'
        return render(request,'testapp/iformx.html',my_dict)

def update_Item_Entry_view1(request,id):
    # 'upd_ie/<int:id>'
    # after upd redirect to /ie_list/invoice_no
    function_name=sys._getframe().f_code.co_name
    my_dict={}
    my_dict['title']='update_Item_Entry'
    ie=models.Item_Entry.objects.get(id=int(id))
    if ie.status=='APPROVED':
        print(function_name, 'ie={} status is APPROVED , it cannot be updated 222'.format(ie.id))
        return redirect('Item_EntryList_based_on_id',id=ie.purchase_ref.invoice_no)

    if request.method=='POST':
        process_upd_ie_post_view(request,id,ie)
        return redirect('Item_EntryList_based_on_id',id=ie.purchase_ref.invoice_no)

    else:

        my_dict=process_upd_ie_get_view(request,id,ie)
        my_dict['title']='update_Item_Entry'
        return render(request,'testapp/iformx.html',my_dict)

def function_name():
    return (sys._getframe().f_code.co_name)

def update_Item_Entry_pe_view(request,id,invoice_no):
    # 'upd_ie/<int:id>/<str:invoice_no>'
    function_name=sys._getframe().f_code.co_name
    my_dict={}
    my_dict['title']='update_Item_Entry'
    ie=models.Item_Entry.objects.get(id=int(id))
    if ie.status=='APPROVED':
        print( function_name, ': ie={} status is APPROVED , it cannot be updated '.format(ie.id))

        return redirect('addItem_1',invoice_no=invoice_no)
    if request.method=='POST':
        process_upd_ie_post_view(request,id,ie)
        return redirect('addItem_1',invoice_no=invoice_no)

    else:
        my_dict=process_upd_ie_get_view(request,id,ie)
        my_dict['title']='update_Item_Entry'
        return render(request,'testapp/iformx.html',my_dict)


def process_upd_ie_post_view(request,id,ie):
    #id = ie id
    #ie = item_entry_ref
    #called by  update_Item_Entry_view and update_Item_Entry_pe_view


    tabsPerStrip=request.POST['tabsPerStrip']
    NumStrips=request.POST['NumStrips']
    #sell_cost_per_unit=request.POST['sell_cost_per_unit']  #hidding in form so donot read
    tax_percent=request.POST['tax_percent']
    # purchase_cost_per_unit=request.POST['purchase_cost_per_unit']   #hidding in form so donot read
    purchase_rate=request.POST['purchase_rate']
    Discount_per=request.POST['Discount_per']
    MRP=request.POST['MRP']
    sch=request.POST['sch']
    if sch!=None:
        sch=sch.capitalize()

    #logic to calculate derived
    Qty_in=int(tabsPerStrip) * int( NumStrips)
    print('Qty_in',Qty_in)

    temp=Decimal(Decimal(MRP)/Decimal(tabsPerStrip)) # 1-Oct
    sell_cost_per_unit= temp/(1+Decimal(tax_percent))
    print('IE-update sell_cost_per_unit',sell_cost_per_unit)

    # sell_cost_per_unit=Decimal(Decimal(MRP)/Decimal(tabsPerStrip)) # 1-Oct
    purchase_cost_per_unit=round(Decimal(purchase_rate)/Decimal(tabsPerStrip),3)
    amount= round(Decimal(purchase_cost_per_unit) * Decimal(Qty_in),3)
    disc_amount=round(Decimal(amount) * Decimal(Discount_per),3)
    tax_amount= round((Decimal(amount)-Decimal(disc_amount)) * Decimal(tax_percent),3) # apply tax on taking discount
    print('purchase_cost_per_unit:{} amount:{} tax_amount{} disc_amount:{}'.format(purchase_cost_per_unit,amount,tax_amount, disc_amount))

    print('upd_ie/<int:id>',Qty_in,amount,tax_amount)


    form=forms.Item_Entry_form2(request.POST,instance=ie)  #  1 -->2 changed 1-Oct
    if form.is_valid():
        form.save()  # same form data into db, but it will not update calculated values, below Qty_in,amount,tax_amount
        x=models.Item_Entry.objects.filter(id=int(id)).update(Qty_in=Qty_in,amount=amount,tax_amount=tax_amount,sell_cost_per_unit=sell_cost_per_unit,sch=sch,purchase_cost_per_unit=purchase_cost_per_unit,disc_amount=disc_amount)
    print("updated ie")
def process_upd_ie_get_view(request,id,ie):
    #id = ie id
    #ie = item_entry_ref
    #called by  update_Item_Entry_view and update_Item_Entry_pe_view

    my_dict={}
    ie_dict={
    "item_code":ie.item_code,
    "item_name":ie.item_name.capitalize(),
    "print_name":ie.print_name.capitalize(),
    "companyname":ie.companyname,
    "HSN_code":ie.HSN_code.upper(),
    "tabsPerStrip":ie.tabsPerStrip,
    "NumStrips":ie.NumStrips,
    "Mfd_by":ie.Mfd_by,
    "MRP":ie.MRP,
    "BatchNo":ie.BatchNo,
    "Mfd_date":ie.Mfd_date,
    "Exp_date":ie.Exp_date,
    "purchase_rate":ie.purchase_rate,
    "purchase_cost_per_unit":ie.purchase_cost_per_unit,
    "sell_cost_per_unit":ie.sell_cost_per_unit,
    "Qty_in":ie.Qty_in,
    "Qty_available":ie.Qty_available,
    "Discount_per":ie.Discount_per,
    "tax_percent":ie.tax_percent,
    "amount":ie.amount,
    "purchased_date":ie.purchased_date,
    "supplier_ref":ie.supplier_ref,
    "purchase_ref":ie.purchase_ref,
    "tax_amount":ie.tax_amount,
    "low_stock_ind_per":ie.low_stock_ind_per,     #26-sep
    "low_stock_ind_status":ie.low_stock_ind_status,   #26-sep
    "status":ie.status,                                #30-Sep
    "sch":ie.sch,                                      #1-Oct
    }
    print(ie.supplier_ref)
    form=forms.Item_Entry_form2(initial=ie_dict)  #  1 -->2 changed 1-Oct

    my_dict['form']= form
    return my_dict

######Out Item_Entry functions

def del_Out_Item_Entry_view(request, id):
    # del_oie/<int:id>   #  1) adds Qty_sold to ie Qty_available field 2) deletes out item entry
    try:

        oie=models.Out_Item_Entry.objects.get(id=id) # id -  OIE table id
        if oie.status !='LOCKED':
            print('oie delete',oie.id, oie.Qty_sold)
            Qty_sold=oie.Qty_sold       # get qty to be reverted
            Qty_available=oie.item_entry_ref.Qty_available
            ie_id=oie.item_entry_ref.id
            print('Qty_available , ie_id',Qty_available, ie_id)
            Qty_available=Qty_available+Qty_sold
            print('Qty_available',Qty_available)
            record=models.Item_Entry.objects.filter(id=ie_id).update(Qty_available=Qty_available)
            print('record', record,id)
            oie.delete()
        else:
            print('tried to deleted LOCKED status OIE')
    except ObjectDoesNotExist:
        print('ObjectDoesNotExist exception occured in del_Item_Entry_view: id:', id)

    return redirect('/q_item1')



####
def del_retunred_Out_Item_Entry_view(request, id1):
    # del_roie/<int:id>   #  1) deducts Qty_sold from ie Qty_available field 2) deletes returned out item entry
    try:

        roie=models.Returned_Out_Item_Entry.objects.get(id=id1) # id -  OIE table id
        if roie.status!='LOCKED':
            print('roie delete',roie.id, roie.Qty_returned)
            Qty_returned=roie.Qty_returned       # get qty to be reverted
            Qty_available=roie.item_entry_ref1.Qty_available
            ie_id=roie.item_entry_ref1.id
            print('Qty_available , ie_id',Qty_available, ie_id)
            if Qty_available>Qty_returned :
                Qty_available=Qty_available-Qty_returned
            else:
                print('error in return cancellation : Qty_available={},Qty_returned={} '.format(Qty_available,Qty_returned))
            print('Qty_available',Qty_available)
            record=models.Item_Entry.objects.filter(id=ie_id).update(Qty_available=Qty_available)
            print('record', record,id1)
            roie.delete()
        else:
            print('del_retunred_Out_Item_Entry_view: return OIE is locked',id1)
    except ObjectDoesNotExist:
        print('ObjectDoesNotExist exception occured in del_Item_Entry_view: id:', id1)
    ## get request.session  oie_id, bill_no, rbill_no
    l_oie=request.session.get('loie',0)
    oie_id=l_oie.pop()
    print('oie_id:',oie_id)
    bill_no=request.session.get('bill_no',0)
    rbill_no=request.session.get('rbill_no',0)
    if l_oie==0:
        print('l_oie session retrival error')
    if bill_no==0:
        print('bill_no session retrival error')
    if rbill_no==0:
        print('rbill_no session retrival error')
    return redirect('create_Returned_Out_IE',id1=oie_id, id2=bill_no, id3=rbill_no)
    # return render(request,'testapp/return_item_query.html')

    ##

def logout_view(request):
    try:
        del request.session['my_dict']
    except KeyError:
        pass
    return render(request,'testapp/logout.html')
#####invoice_no
class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data = {
             'today': datetime.date.today(),
             'amount': 39.99,
            'customer_name': 'Sreenivas Valaboju',
            'order_id': 1233434,
        }
        pdf = render_to_pdf('pdf/invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


####
def item_query_form_view(request):  # it is not currently used
# 'q_item/'
    ldict=[]
    my_dict={}
    my_dict['title']='item_query_form'
    l=[]
    if request.method=='POST':
        initial_ie={}
        cart_dict ={}
        form=forms.Item_query_form(request.POST)
        if form.is_valid():
            # form.save()
            bill_no=form.cleaned_data['bill_no']
            q_item=form.cleaned_data['item_name']
            tabsReq=form.cleaned_data['tabsReq']
            areports=models.Item_Entry.objects.filter(item_name__contains=q_item).order_by('Exp_date','-Discount_per') #111
            for a in areports:
                print ('ie.id',a.id)
            t_Qty_avail=models.Item_Entry.objects.filter(item_name__contains=q_item).aggregate(Sum('Qty_available'))
            t_Qty_avail=t_Qty_avail['Qty_available__sum']
            if tabsReq > t_Qty_avail:
                msg=' {} requested {} is not available, current stock is {}, so reduce count'.format(q_item,tabsReq,t_Qty_avail)
                initial_ie={'tabsReq':tabsReq,'item_name':q_item}
            else:
                msg=' {} requested {} is available, current stock is {}'.format(q_item,tabsReq,t_Qty_avail)


                ldict=request.session.get('ldict',[])  # retriving old entries

                json_data = serializers.serialize("json", areports,fields=('id','item_code','item_name', \
                'print_name',\
                'MRP',
                'Mfd_by',
                'BatchNo',
                'Mfd_date',
                'Exp_date',
                'sell_cost_per_unit',
                'Qty_in',
                'Qty_available',
                'Discount_per',
                ))
                # print('ser data:',json_data)
                pdict=json.loads(json_data) # converting Json to dict{}
                #print('pdict=',pdict)
                x={}
                y={}
                z={}
                for object in pdict:
                    pk=object['pk']
                    x={'id':pk,'tabsReq':tabsReq}
                    y= object['fields']  # storing in session
                    z={**x,**y}
                    ldict.append(z)
                    print('type z',type(z), z)
                    # print('pk',object['pk'])

                print('\n  ldict', ldict)
                request.session['ldict']=ldict
                initial_ie=None

            my_dict['msg']=msg
            # for k,v in request.session.items():
            #     if k.isnumeric():
            #         ie=models.Item_Entry.objects.get(id=k)

            print(msg)
            my_dict['areports']=areports
            print("item_query_form_view POST, ", q_item)
        form=forms.Item_query_form(initial=initial_ie)
        my_dict['form']= form
        return render(request,'testapp/item_query.html',my_dict)
    else:
        form=forms.Item_query_form()
        my_dict['form']= form
        return render(request,'testapp/item_query.html',my_dict)
##
def item_query_form_new_view(request):
# 'q_item1/'
    print('entering item_query_form_new_view')
    ldict=[]
    my_dict={}
    my_dict['title']='item_query_form'
    l=[]
    if request.method=='POST':
        initial_ie={}
        cart_dict ={}
        form=forms.Item_query_form(request.POST)
        if form.is_valid():
            # form.save()
            bill_no=form.cleaned_data['bill_no']
            q_item=form.cleaned_data['item_name']
            tabsReq=form.cleaned_data['tabsReq']
            areports=models.Item_Entry.objects.filter(item_name__contains=q_item ).exclude(Qty_available=0).order_by('Exp_date','-Discount_per') #111
            t_Qty_avail=models.Item_Entry.objects.filter(item_name__contains=q_item).aggregate(Sum('Qty_available'))
            t_Qty_avail=t_Qty_avail['Qty_available__sum']
            if t_Qty_avail==None:
                t_Qty_avail=0
            print('q_item={},tabsReq={} t_Qty_avail={}'.format(q_item,tabsReq,t_Qty_avail))
            if tabsReq > t_Qty_avail:

                msg=' {} requested {} is not available, current stock is {}, so reduce count'.format(q_item,tabsReq,t_Qty_avail)
                initial_ie={'bill_no':bill_no,'tabsReq':tabsReq,'item_name':q_item}
            else:
                msg=' {} requested {} is available, current stock is {}'.format(q_item,tabsReq,t_Qty_avail)

                billno=request.session.get('billno',0)
                if billno!=bill_no: # store bill_no :
                    request.session['billno']=bill_no # store new bill_no  replace old bill_no
                initial_ie={'bill_no':bill_no,}


            ###  session
            l_ie=[]
            for areport in areports:
                l_ie.append(areport.id)
            request.session['l_ie']=l_ie  # will be read in addtoOIE/id/bill_no
######################### session end
#out Item Entry list all entry for given billno
            oareports=models.Out_Item_Entry.objects.filter(bill_no_ref__bill_no=bill_no)
            my_dict['oareports']=oareports
######
            print(msg)
            my_dict['bill_no']=bill_no
            my_dict['msg']=msg
            my_dict['areports']=areports

        form=forms.Item_query_form(initial=initial_ie)
        my_dict['form']= form
        return render(request,'testapp/item_query.html',my_dict)
    else:   #GET
        billno=request.session.get('billno',0)
######################### session end
#out Item Entry list all entry for given billno
        if billno!=0:
            oareports=models.Out_Item_Entry.objects.filter(bill_no_ref__bill_no=billno)
            my_dict['oareports']=oareports
######
            lreport=[]
            ####getting session list variable
            l_ie=request.session.get('l_ie',[])
            print('l_ie',l_ie)
            for ie in l_ie:
                print('ie',ie)
                lreport.append(models.Item_Entry.objects.get(id=ie))

            print('lreport',lreport)
            my_dict['areports']=lreport
            my_dict['bill_no']=billno  ##**bill_no
######
        #ldict=request.session.get('ldict',[])
        initial_ie={'bill_no':billno,}
        form=forms.Item_query_form(initial=initial_ie)
        my_dict['form']= form
        #my_dict['areports']=ldict
        return render(request,'testapp/item_query.html',my_dict)
        #return render(request,'testapp/iform.html',my_dict)


##
def cart_list_view(request):
    l=[]

    ldict=[]
    my_dict={'title':'cart list_view'}
    if request.session:

        ldict=request.session.get('ldict',[])
        # for dict in ldict:
        #     ldict.append(dict)
        my_dict['areports']=ldict

    return render(request,'testapp/sell_entry.html',my_dict)

def create_sell(request):
# addSE/', 1)creates sell entry 2) shows relavent item entries
    my_dict={}
    se_bill_no_ref={}
    my_dict['title']='Sell_Entry'
    if request.method=='POST':
        form=forms.Sell_Entry_form(request.POST)
        print('create se',form.is_valid())
        if form.is_valid():
            my_dict['result']=form.save()
            se_bill_no=form.cleaned_data['bill_no']
            print('se_bill_no:', se_bill_no)
            #request.session['se_bill_no']= se_bill_no  #add PE  to session

            try:
                areports=models.Out_Item_Entry.objects.filter(bill_no_ref__bill_no=se_bill_no)
                my_dict['areports']=areports

            except ObjectDoesNotExist:
                message='ObjectDoesNotExist exeception occured create_sell '
        # return redirect('/se_list')
        return redirect ('addBilltoSession', id=se_bill_no)
        # return render(request,'testapp/se_results.html',my_dict)
    else:
        se=models.Sell_Entry.objects.last()
        bill_no=se.bill_no
        bill_no=bill_no+1
        initial_se={'bill_no':bill_no,}
        print('bill_no',bill_no)
        form=forms.Sell_Entry_form(initial=initial_se)
        my_dict['form']= form
        return render(request,'testapp/iform2.html',my_dict)
#### Returned Sell Entry

def create_retunred_sell(request):
# addRSE/', 1)creates returned sell entry 2) shows relavent item entries purchased earlier
    my_dict={}
    se_bill_no_ref={}
    my_dict['title']='Return Sell_Entry'
    if request.method=='POST':
        form=forms.Returned_Sell_Entry_form(request.POST)
        print('create rse',form.is_valid())
        if form.is_valid():
            my_dict['result']=form.save()   # saving RSE
            rse_bill_no=form.cleaned_data['rbill_no']
            print('rse_bill_no:', rse_bill_no)
            #request.session['se_bill_no']= se_bill_no  #add PE  to session

            try:
                areports=models.Returned_Out_Item_Entry.objects.filter(rbill_no_ref__rbill_no=rse_bill_no)
                my_dict['areports']=areports

            except ObjectDoesNotExist:
                message='ObjectDoesNotExist exeception occured create_sell '

        return render(request,'testapp/rse_results.html',my_dict)
    else:  #GET
        try:
            rse=models.Returned_Sell_Entry.objects.last()
        except ObjectDoesNotExist:
            rbill_no=0
        rbill_no=rse.rbill_no
        rbill_no=rbill_no+1
        initial_se={'rbill_no':rbill_no,}
        print('rbill_no',rbill_no)
        form=forms.Returned_Sell_Entry_form(initial=initial_se)
        my_dict['form']= form
        return render(request,'testapp/iform.html',my_dict)

def create_retunred_sell_new(request):
# addRSE/', 1)creates returned sell entry 2) shows relavent item entries purchased earlier
    my_dict={}
    # se_bill_no_ref={}
    my_dict['title']='Return_Sell_Entry'
    if request.method=='POST':
        form=forms.bill_search_form(request.POST)
        print('create rse :post',form.is_valid())
        if form.is_valid():
            bill_no=form.cleaned_data['bill_no']
            sell_entry_ref=models.Sell_Entry.objects.get(bill_no=bill_no)
            # check if already returned items on bill_no,  then  donot process return
            ret=models.Returned_Sell_Entry.objects.filter(sell_entry_ref__bill_no=bill_no)
            if len(ret)!=0:
                my_dict['message']='already processed return items on this bill no={}, cannot return again'.format(bill_no)
                print('already processed return items on this bill no={}, cannot return again, {}'.format(bill_no , len(ret)))
                return render(request,'testapp/rse_results.html',my_dict)
            try:
                rse=models.Returned_Sell_Entry.objects.last()
                if(rse==None) :
                    rbill_no=0
                else:
                    rbill_no=rse.rbill_no
            except ObjectDoesNotExist:
                rbill_no=0

            rbill_no=rbill_no+1
            rse1,created =models.Returned_Sell_Entry.objects.get_or_create(sell_entry_ref=sell_entry_ref,rbill_no=rbill_no,\

            rbill_amount=0,status='UNLOCKED')
            print('is form.is_valid:',form.is_valid(), rse, rse1)
            my_dict['se']=  sell_entry_ref
            my_dict['rse']=  rse1
            print('rse1_rbillno{}'.format(rse1.rbill_no))
            print('bill_no:{},rse:{},rse1:{}, create:{}, ret1.id', bill_no,rse,rse1,created)
            #request.session['se_bill_no']= se_bill_no  #add PE  to session

            try:
                oie_reports=models.Out_Item_Entry.objects.filter(bill_no_ref__bill_no=bill_no)
                my_dict['areports']=oie_reports

                roie_reports=models.Returned_Out_Item_Entry.objects.filter(rbill_no_ref__rbill_no=rbill_no)
                my_dict['roie_reports']=roie_reports

            except ObjectDoesNotExist:
                message='ObjectDoesNotExist exeception occured create_sell '

        return render(request,'testapp/rse_results.html',my_dict)
    else:  #GET

        form=forms.bill_search_form()
        my_dict['form']= form
        return render(request,'testapp/iform3.html',my_dict)
#
def list_se(request):
# addSE/', 1)list all sell entry 2) shows relavent item entries
    my_dict={}
    se_bill_no_ref={}
    my_dict['title']='Sell_Entry_list'
    try:
        areports=models.Sell_Entry.objects.all()
        my_dict['areports']=areports

    except ObjectDoesNotExist:
        message='ObjectDoesNotExist exeception occured create_sell '

    return render(request,'testapp/se_results.html',my_dict)

def list_rse(request):
# addSE/', 1)list all sell entry 2) shows relavent item entries
    my_dict={}
    my_dict['title']='Return Sell_Entry_list'

    areports=models.Returned_Sell_Entry.objects.all()
    my_dict['rses']=areports

    return render(request,'testapp/rse_list_results.html',my_dict)

def oie_list(request, id):
# oie_list/id', 1)list all sell entry based on bill_no 2) shows relavent item entries
    my_dict={}
    se_bill_no_ref={}
    my_dict['title']='Out Item_Entry_list'
    try:
        areports=models.Out_Item_Entry.objects.filter(bill_no_ref__bill_no=id)
        my_dict['areports']=areports
        se=models.Sell_Entry.objects.get(bill_no=id)
        my_dict['se']=se
    except ObjectDoesNotExist:
        message='ObjectDoesNotExist exeception occured create_sell '

    return render(request,'testapp/out_item_results.html',my_dict)
#
def roie_list(request, id):
# roie_list/id', 1)list all return sell entry based on rbill_no 2) shows relavent returned  item entries
    my_dict={}
    se_bill_no_ref={}
    my_dict['title']='Returned Out Item_Entry_list'
    try:
        areports=models.Returned_Out_Item_Entry.objects.filter(rbill_no_ref__rbill_no=id)
        my_dict['areports']=areports
        rse=models.Returned_Sell_Entry.objects.get(rbill_no=id)
        my_dict['rse']=rse
    except ObjectDoesNotExist:
        message='ObjectDoesNotExist exeception occured create_sell '

    return render(request,'testapp/return_out_item_results.html',my_dict)
#
def addBilltoSession(request,id):
# addOIE/id',   id=bill_no 1)list all sell entry 2) shows relavent item entries
    my_dict={}
    se_bill_no_ref={}
    my_dict['title']='Sell_Entry_list'
    try:
        request.session['billno']= id
        print('billno {} added to session'.format(id))
        return redirect('/q_item1')
    except KeyError:
        message='KeyError exeception occured addOIE '

    return render(request,'testapp/se_results.html',my_dict)

def create_Out_IE(request, id1, id2):
    # 'addtoOIE/id1/id2'  1) id1=ie_id 2) id2=bill_no
    # add or create Out_Item_Entry with bill no and ie_id reference
    # deduct ie balance
    # add to shopping cart for review
    my_dict={}
    result=0
    my_dict['title']='Out_Item_Entry'
    if request.method=='POST':
        form=forms.Out_Item_Entry_form(request.POST)
        se_rec=models.Sell_Entry.objects.get(bill_no=id2)

        if se_rec.status!='LOCKED':    #status =='UNLOCKED'
            print('create se',form.is_valid())
            if form.is_valid():
                Qty_sold=form.cleaned_data['Qty_sold']
                # updating IE Qty_available count
                item_entry_ref=models.Item_Entry.objects.get(id=id1)  # storing obj refencen in  item_entry_ref
                print('item_entry_ref',item_entry_ref)
                Qty_available=item_entry_ref.Qty_available
                Qty_in=item_entry_ref.Qty_in
                low_stock_ind_per=item_entry_ref.low_stock_ind_per
                low_stock_ind_status=item_entry_ref.low_stock_ind_status
                print('Qty_available',Qty_available)

                # update IE
                if item_entry_ref.Qty_available >=Qty_sold:
                    Qty_available=item_entry_ref.Qty_available-Qty_sold
                    record=models.Item_Entry.objects.filter(id=id1).update(Qty_available=Qty_available)
                    if (Qty_available< Qty_in* Decimal(low_stock_ind_per)):
                        if(low_stock_ind_status=='OFF'):
                            record=models.Item_Entry.objects.filter(id=id1).update(low_stock_ind_status='ON')
                            print('low stock indication set to ON')
                    else:   # qty avail > thres, prev ind was ON change to OFF
                        if(low_stock_ind_status=='ON'):
                            record=models.Item_Entry.objects.filter(id=id1).update(low_stock_ind_status='OFF')
                            print('low stock indication set to OFF')

                    print("updated out ie Qty_available -deducted count",record)
                    item_entry_ref=models.Item_Entry.objects.get(id=id1)
                    print(" Qty_available {} -deducted count".format(item_entry_ref.Qty_available))

                # calcuting amount, tax_amount, and setting data for creating Out IE
                    BatchNo=item_entry_ref.BatchNo
                    bill_no_ref=models.Sell_Entry.objects.get(bill_no=id2)  # storing obj refencen in  bill_no_ref
                    print('bill_no_ref',bill_no_ref)
                    bill_item_amount= round((Decimal(item_entry_ref.sell_cost_per_unit) * Qty_sold),2)
                    Discount_per=item_entry_ref.Discount_per
                    tax_percent=item_entry_ref.tax_percent
                    disc_amount=round((Decimal(bill_item_amount)*Decimal(Discount_per)),2)
                    bill_tax_amount=bill_item_amount*tax_percent
                    bill_tax_per= item_entry_ref.tax_percent  #23-Nov

                    try:  #OPTION is defined in setting.py
                        if settings.CGST_GST_RATIO:
                            if settings.CGST_GST_RATIO <=1 and settings.CGST_GST_RATIO>=0:
                              CGST_GST_RATIO=settings.CGST_GST_RATIO #23-Nov
                    except AttributeError:
                        CGST_GST_RATIO=0.5
                        print('No attribute CGST_GST_RATIO field is defined in settings.py so by default CGST_GST_RATIO is 0.5')

                    print('CGST_GST_RATIO={}'.format(CGST_GST_RATIO))
                    CGST_tax_per=round((Decimal(bill_tax_per)*Decimal(CGST_GST_RATIO)),3)
                    SGST_tax_per=round((Decimal(bill_tax_per)*Decimal(1-CGST_GST_RATIO)),3)
                    billed_amount=bill_item_amount+bill_tax_amount
                    CGST_tax_amount= round((Decimal(bill_item_amount)*Decimal(CGST_tax_per)),3)
                    SGST_tax_amount= round((Decimal(bill_item_amount)*Decimal(SGST_tax_per)),3)



                    #   creating Out Item entry
                    # initial={
                    # 'bill_no_ref':bill_no_ref,
                    # 'BatchNo':BatchNo,
                    # 'item_entry_ref':item_entry_ref,
                    # 'Qty_sold':Qty_sold,
                    # 'bill_item_amount':bill_item_amount,
                    # 'bill_tax_amount':bill_tax_amount
                    # }

                    result=models.Out_Item_Entry.objects.create(bill_no_ref=bill_no_ref,BatchNo=BatchNo,\
                    item_entry_ref=item_entry_ref,Qty_sold=Qty_sold,bill_item_amount=bill_item_amount,bill_tax_amount=bill_tax_amount, \
                    bill_tax_per=bill_tax_per ,CGST_tax_per=CGST_tax_per, SGST_tax_per=SGST_tax_per, billed_amount=billed_amount, \
                    CGST_tax_amount=CGST_tax_amount, SGST_tax_amount=SGST_tax_amount,)
                    # print('is form.is_valid:',form.is_valid())
                    # if form.is_valid():

                    print('saving out item entry, result:',result)
                lreport=[]
                ####getting session list variable
                l_ie=request.session.get('l_ie',[])
                print('l_ie',l_ie)
                for ie in l_ie:
                    print('ie',ie)
                    lreport.append(models.Item_Entry.objects.get(id=ie))

                print('lreport',lreport)
                my_dict['areports']=lreport
                #########
                areport=result    # extra  remove later
                my_dict['result']=result
                ## feching all records having same bill_no in Out_Item_Entry
                areports=models.Out_Item_Entry.objects.all()
                print('11111111111check this point create_Out_IE')

                my_dict['oareports']=areports # selected or allocated Out Item Entry


                ### q_item1 setting condictions
                #my_dict['areports']=ldict  #setting query list before entering to this fuction
                billno=request.session.get('billno',0)
                initial_ie={'bill_no':billno,}
                form=forms.Item_query_form(initial=initial_ie)
                my_dict['form']=form
                my_dict['bill_no']=billno
                my_dict['title']='Query_Item_Entry'
                print('existing post section addtoOIE, entering to q_item1')
        else:
                Emsg='Sell Entry is Locked you cannot add any items'
                print(Emsg)
                my_dict['ErrorMsg']=Emsg

        return redirect('/q_item1')
                ##
        # return render(request,'testapp/out_item_results.html',my_dict)
        # return render(request,'testapp/item_query.html',my_dict)
    else:
        print('addtoOIE/id1/id2/ create_Out_IE get method')
        ###
        oareports=models.Out_Item_Entry.objects.filter(bill_no_ref__bill_no=id2)
        my_dict['oareports']=oareports
        ###
        form=forms.Out_Item_Entry_form()
        my_dict['form']= form
        #return render(request,'testapp/iform.html',my_dict)
        return render(request,'testapp/item_query.html',my_dict)

##

def create_Returned_Out_IE(request, id1, id2,id3):
    # '/retOIE/id1/id2/id3'  1) id1=oie_id 2) id2=bill_no 3) id3= rbill_no
    # get qty to return from user
    # add or create Returned_Out_Item_Entry with rbill no and ie_id reference
    # deduct ie balance
    # add to shopping cart for review

    my_dict={}
    result=0
    my_dict['title']='Returned_Out_Item_Entry'
    if request.method=='POST':
        print('create_Returned_Out_IE :POST')
        form=forms.qty_return_form(request.POST)
        if form.is_valid():
            Qty_returned=form.cleaned_data['Qty_returned']
            my_dict['xxx']=id3
            print('333  id3',id3)
            print('Qty_returned:{}, id1 {}, id2 {}, id3 {}'.format(Qty_returned, id1, id2, id3))

            # get item_entry_ref and find IE id from OIE id
            oie=models.Out_Item_Entry.objects.get(id=id1)
            Qty_sold=oie.Qty_sold
            if Qty_returned==0:
                my_dict['msg']='cancelled return item'
                oareports,roie_areports,my_dict= create_Returned_Out_IE_utils(id2,id3,my_dict)
                return render(request,'testapp/return_item_query.html',my_dict)
            if Qty_returned<=0 :
                my_dict['msg']='invalid input entered input than 0 and less than or equal to {}'.format(Qty_sold)
                oareports,roie_areports,my_dict= create_Returned_Out_IE_utils(id2,id3,my_dict)
                return render(request,'testapp/return_item_query.html',my_dict)
            elif Qty_returned > Qty_sold:
                my_dict['msg']='invalid input entered input than 0 and less than or equal to {}'.format(Qty_sold)
                oareports,roie_areports,my_dict= create_Returned_Out_IE_utils(id2,id3,my_dict)
                return render(request,'testapp/return_item_query.html',my_dict)



            # return create_Returned_Out_IE_error(request,id2,id3,my_dict,Qty_returned,Qty_sold)
            item_entry_ref=oie.item_entry_ref
            print('item_entry_ref',item_entry_ref.id)
            ie_id=item_entry_ref.id
            print('item_entry_ref',item_entry_ref)

            #updating IE Qty_available count
            Qty_available=item_entry_ref.Qty_available
            Qty_in=item_entry_ref.Qty_in
            low_stock_ind_per=item_entry_ref.low_stock_ind_per
            low_stock_ind_status=item_entry_ref.low_stock_ind_status
            print('Qty_available',Qty_available)

            #check enter OIE id alredy returned same item (BatchNo, rbill_no, item_name) check ,
            #if yes  then donot update IE and create ROIE  just return
            BatchNo= oie.BatchNo
            # rbill_no=id3
            item_name=item_entry_ref.item_name  #item_entry_ref  already got prior
            print('item_name',item_name)
            print('checking whether item already entered prior')

            temp_roie=models.Returned_Out_Item_Entry.objects.filter(Q(rbill_no_ref__rbill_no=id3) & Q(BatchNo=BatchNo) & Q(item_entry_ref1__item_name=item_name))
            print('temp_roie',temp_roie)
            for troie in temp_roie:
                if troie.item_entry_ref1.item_name==item_name:
                    my_dict['msg']='alredy returned batchno {} and item name {} rbill_no {} first cancel earlier return and retry '.format(BatchNo,item_name,id3)
                    oareports,roie_areports,my_dict= create_Returned_Out_IE_utils(id2,id3,my_dict)
                    return render(request,'testapp/return_item_query.html',my_dict)

            # update IE (increment count by returned items)
            Qty_available=item_entry_ref.Qty_available + Qty_returned
            record=models.Item_Entry.objects.filter(id=ie_id).update(Qty_available=Qty_available)
            if (Qty_available< Qty_in* Decimal(low_stock_ind_per)):
                if(low_stock_ind_status=='OFF'):
                    record=models.Item_Entry.objects.filter(id=ie_id).update(low_stock_ind_status='ON')
                    print('low stock indication set to ON')
            else:   # qty avail > thres, prev ind was ON change to OFF
                if(low_stock_ind_status=='ON'):
                    record=models.Item_Entry.objects.filter(id=ie_id).update(low_stock_ind_status='OFF')
                    print('low stock indication set to OFF')

            print("updated out ie Qty_available -incremented count",record)
            item_entry_ref1=models.Item_Entry.objects.get(id=ie_id)   #use this value while creating ROIE
            print(" Qty_available {} -incremented count".format(item_entry_ref.Qty_available))

            #*****get required data to create Returned Out_Item_Entry (ROIE)
            rbill_no_ref=models.Returned_Sell_Entry.objects.get(rbill_no=id3)
            my_dict['rse']=rbill_no_ref
            print('444 rse',rbill_no_ref)
            # BatchNo= oie.BatchNo        # copy from OIE  already get prior , so use same
            # Qty_returned

            print('rbill_no_ref:{},BatchNo:{},item_entry_ref1:{},Qty_returned:{}'.format (rbill_no_ref,BatchNo,item_entry_ref1,Qty_returned))
            # calcuting rbill_item_amount, rbill_tax_amount, and setting data for creating Returned Out IE

            rbill_item_amount= round((Decimal(item_entry_ref.sell_cost_per_unit) * Qty_returned),2)
            tax_percent=item_entry_ref.tax_percent
            rbill_tax_amount=rbill_item_amount*tax_percent

            roie=models.Returned_Out_Item_Entry.objects.create(rbill_no_ref=rbill_no_ref,BatchNo=BatchNo,item_entry_ref1=item_entry_ref1,Qty_returned=Qty_returned,rbill_item_amount=rbill_item_amount,rbill_tax_amount=rbill_tax_amount)
            print('roie {},'.format(roie))
            #get reports
            oareports=models.Out_Item_Entry.objects.filter(bill_no_ref__bill_no=id2)
            roie_areports=models.Returned_Out_Item_Entry.objects.filter(rbill_no_ref__rbill_no=id3)
            print('id3',id3)

            my_dict['oareports']=oareports
            my_dict['roie_areports']=roie_areports
            # return oareports,roie_areports,my_dict
            # oareports,roie_areports,my_dict= create_Returned_Out_IE_utils(id2,id3,my_dict)
            return render(request,'testapp/return_item_query.html',my_dict)
            # return redirect('create_Returned_Out_IE', id1=id1,id2=id2,id3=id3)
    else:# goes to GET method
        print('/retOIE/id1={}/id2={}/id3={} in create_Returned_Out_IE'.format(id1,id2,id3))
        ###
        oareports=models.Out_Item_Entry.objects.filter(id=id1)
        rse=models.Returned_Sell_Entry.objects.get(rbill_no=id3)
        l_oie=[]
        oie_records=models.Out_Item_Entry.objects.filter(bill_no_ref__bill_no=id2).values('id')

        for oie in oie_records:
            # print('ioe',oie['id'])
            l_oie.append(oie['id'])
        print('list oie', l_oie)
        request.session['loie']=l_oie
        request.session['bill_no']=id2
        request.session['rbill_no']=id3


        my_dict['oareports']=oareports
        my_dict['xxx']=id3
        ###
        form=forms.qty_return_form()
        my_dict['form']= form
        #return render(request,'testapp/iform.html',my_dict)
    return render(request,'testapp/return_item_query.html',my_dict)

#utilties
def create_Returned_Out_IE_utils(id2,id3,my_dict):
    oareports=models.Out_Item_Entry.objects.filter(bill_no_ref__bill_no=id2)
    roie_areports=models.Returned_Out_Item_Entry.objects.filter(rbill_no_ref__rbill_no=id3)
    my_dict['oareports']=oareports
    my_dict['roie_areports']=roie_areports
    return oareports,roie_areports,my_dict

def create_Returned_Out_IE_error(request,id2,id3,my_dict,Qty_returned,Qty_sold):
    if Qty_returned==0:
        my_dict['msg']='cancelled return item'
        oareports,roie_areports,my_dict= create_Returned_Out_IE_utils(id2,id3,my_dict)
        return render(request,'testapp/return_item_query.html',my_dict)
    if Qty_returned<=0 :
        my_dict['msg']='invalid input entered input than 0 and less than or equal to {}'.format(Qty_sold)
        oareports,roie_areports,my_dict= create_Returned_Out_IE_utils(id2,id3,my_dict)
        return render(request,'testapp/return_item_query.html',my_dict)
    elif Qty_returned > Qty_sold:
        my_dict['msg']='invalid input entered input than 0 and less than or equal to {}'.format(Qty_sold)
        oareports,roie_areports,my_dict= create_Returned_Out_IE_utils(id2,id3,my_dict)
        return render(request,'testapp/return_item_query.html',my_dict)
#
def report_exp(request, id):
    # 'stock_rep/'
    print('report_exp entered')
    response = HttpResponse(content_type='application/ms-excel')
    filename="stock_report_{}.xls".format(datetime.date.today())
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(id)  # low_stock, summary

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    if id=='low_stock':
        print('low_stock section entered')
        columns = ['item_name', 'print_name', 'supplier_ref', 'Qty_in','Qty_available', ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = models.Item_Entry.objects.all().filter(low_stock_ind_status='ON').values_list('item_name', 'print_name', 'supplier_ref', 'Qty_in','Qty_available')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
    elif id=='summary':
        print('summary section entered')
        columns = ['item_name','sum Qty_available', ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        rows=models.Item_Entry.objects.filter(Qty_available__gt=0)
        x={}
        y={}
        for row in rows:
            x=models.Item_Entry.objects.filter(item_name= row.item_name).aggregate(Sum('Qty_available'))
            y[row.item_name]=x['Qty_available__sum']

        for k,v in y.items():
            row_num += 1

            ws.write(row_num, 0, k, font_style)
            ws.write(row_num, 1, v, font_style)
        print(y)


    wb.save(response)
    return response
def report_low_summary_stock(request, id):
    # 'stock_rep/'
    print('report_low_summary_stock')
    my_dict={}
    if id=='low_stock':
        my_dict['title']='Low Stock'
        print('low_stock section entered')

        rows = models.Item_Entry.objects.all().filter(low_stock_ind_status='ON').values('item_name', 'print_name', 'supplier_ref', 'Qty_in','Qty_available')
        my_dict['ie_low_stock']=rows

    elif id=='summary':
        my_dict['title']='Current Stock'
        print('summary section entered')

        rows=models.Item_Entry.objects.filter(Qty_available__gt=0).values('item_name', 'print_name', 'supplier_ref', 'Qty_in','Qty_available')
        x={}
        y={}
        for row in rows:
            x=models.Item_Entry.objects.filter(item_name= row['item_name']).aggregate(Sum('Qty_available'))
            y[row['item_name']]=x['Qty_available__sum']
        my_dict['ie_current_stock']=y
        # print('y',y)

    return render(request,'testapp/low_cur_stock.html',my_dict)
def expiry_report(request,id):

    if request.method=='POST':
        form=forms.Item_expiry_query_form(request.POST)
        print('post: expiry',form.is_valid())
        if form.is_valid():
            months=form.cleaned_data['months']

            current_date=datetime.date.today()
            end_date=current_date+ relativedelta(months=months)

            areports=models.Item_Entry.objects.filter(Q(Exp_date__range=[current_date,end_date]) &Q(Qty_available__gt=0)) # filtering on date range
            print(areports)
            my_dict={'title':'Expiry Report','areports':areports}
            my_dict['range']='Range is from {} to {}'.format(current_date,end_date)
            my_dict['months']=months

        else:
            print('expiry_report  form is not valid')
        return render(request,'testapp/item_expiry_report.html',my_dict)
    else:   # GET section
        my_dict={}  # setting variables afresh
        my_dict['title']='Expiry Report Form'
        initial_f={'months':id}
        form=forms.Item_expiry_query_form(initial=initial_f)
        my_dict['form']=form
        return render(request,'testapp/item_expiry_report.html',my_dict)

def export_expiry_report(request,months):
    print('export_expiry_report entered')
    response = HttpResponse(content_type='application/ms-excel')
    filename="expiry_report_{}.xls".format(datetime.date.today())
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

    current_date=datetime.date.today()
    end_date=current_date+ relativedelta(months=months)


    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('expiry_report_{}_months'.format(months))  # low_stock, summary

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True


    print('low_stock section entered')
    columns = ['item_code','item_name', 'print_name','companyname','BatchNo','Mfd_date','Exp_date','Qty_in','Qty_available', 'supplier__companyname',  ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()


    rows=models.Item_Entry.objects.filter(Q(Exp_date__range=[current_date,end_date])& Q(Qty_available__gt=0)).values_list('item_code','item_name', 'print_name','companyname','BatchNo','Mfd_date','Exp_date','Qty_in','Qty_available', 'supplier_ref__companyname') # filtering on date range

    for row in rows:
        row_num += 1
        # for col_num in range(len(row)):
        #     ws.write(row_num, col_num, row[col_num], font_style)
        ws.write(row_num, 0, row[0], font_style) #item_code
        ws.write(row_num, 1, row[1], font_style) #item_name
        ws.write(row_num, 2, row[2], font_style) #print_name
        ws.write(row_num, 3, row[3], font_style) #companyname
        ws.write(row_num, 4, row[4], font_style) #'BatchNo'
        ws.write(row_num, 5, str(row[5]), font_style) #'Mfd_date'
        ws.write(row_num, 6, str(row[6]), font_style) #'Exp_date'
        ws.write(row_num, 7, row[7], font_style) #'Qty_in'
        ws.write(row_num, 8, row[8], font_style) #'Qty_available'
        ws.write(row_num, 9, row[9], font_style) #'supplier_ref__companyname'




    wb.save(response)
    return response

def sell_balance_sheet_form_rep(request):
    if request.method=='POST':
        my_dict={}
        form=forms.Balance_sheet_query_form(request.POST)
        print('post: balance sheet',form.is_valid())
        if form.is_valid():

            singleday=form.cleaned_data['singledate']
            start_date=form.cleaned_data['start_date']
            end_date=form.cleaned_data['end_date']
            if(singleday=='singleday'):
                current_date=start_date
                print('current_date',current_date)

                tot_bill_item_amount=models.Out_Item_Entry.objects.filter(bill_no_ref__purchase_date=current_date).aggregate(Sum('bill_item_amount')) # filtering on date range
                tot_bill_tax_amount=models.Out_Item_Entry.objects.filter(bill_no_ref__purchase_date=current_date).aggregate(Sum('bill_tax_amount'))
                tot_bill_item_amount=tot_bill_item_amount['bill_item_amount__sum']
                tot_bill_tax_amount=round(tot_bill_tax_amount['bill_tax_amount__sum'],2)
                tot_bill_grand_amount=round(Decimal(tot_bill_item_amount)+Decimal(tot_bill_tax_amount),2)
                print('total OIE amount:{}, total_amount_sum:{},tot_grand_total{}'.format(tot_bill_item_amount,tot_bill_tax_amount,tot_bill_grand_amount))

                tot_item_amount=models.Sell_Entry.objects.filter(purchase_date=current_date).aggregate(Sum('bill_amount')) # filtering on date range
                tot_tax_amount=models.Sell_Entry.objects.filter(purchase_date=current_date).aggregate(Sum('tax_amount'))
                tot_grand_total=models.Sell_Entry.objects.filter(purchase_date=current_date).aggregate(Sum('grand_total'))
                tot_item_amount=tot_item_amount['bill_amount__sum']
                tot_tax_amount=round(tot_tax_amount['tax_amount__sum'],2)
                tot_grand_total=round(tot_grand_total['grand_total__sum'],2)

                print('total SE amount:{}, total_amount_sum:{},tot_grand_total{}'.format(tot_item_amount,tot_tax_amount,tot_grand_total))

                my_dict['title']='Daily balance sheet Report'
                my_dict['current_date']=current_date
                my_dict['tot_item_amount']=tot_item_amount  #SE
                my_dict['tot_tax_amount']=tot_tax_amount
                my_dict['tot_grand_total']=tot_grand_total

                my_dict['tot_bill_item_amount']=tot_bill_item_amount  #O IE
                my_dict['tot_bill_tax_amount']=tot_bill_tax_amount
                my_dict['tot_bill_grand_amount']=tot_bill_grand_amount

                areports=models.Sell_Entry.objects.filter(purchase_date=current_date)
                my_dict['areports']=areports
            else: # date range

                ##############
                print('date range ')
                current_date=start_date
                print('current_date',current_date)

                tot_bill_item_amount=models.Out_Item_Entry.objects.filter(bill_no_ref__sell_datetime__range=[current_date,end_date]).aggregate(Sum('bill_item_amount')) # filtering on date range
                tot_bill_tax_amount=models.Out_Item_Entry.objects.filter(bill_no_ref__sell_datetime__range=[current_date,end_date]).aggregate(Sum('bill_tax_amount'))
                tot_bill_item_amount=tot_bill_item_amount['bill_item_amount__sum']
                tot_bill_tax_amount=round(tot_bill_tax_amount['bill_tax_amount__sum'],2)
                tot_bill_grand_amount=round(Decimal(tot_bill_item_amount)+Decimal(tot_bill_tax_amount),2)
                print('total OIE amount:{}, total_amount_sum:{},tot_grand_total{}'.format(tot_bill_item_amount,tot_bill_tax_amount,tot_bill_grand_amount))

                tot_item_amount=models.Sell_Entry.objects.filter(sell_datetime__range=[current_date,end_date]).aggregate(Sum('bill_amount')) # filtering on date range
                tot_tax_amount=models.Sell_Entry.objects.filter(sell_datetime__range=[current_date,end_date]).aggregate(Sum('tax_amount'))
                tot_grand_total=models.Sell_Entry.objects.filter(sell_datetime__range=[current_date,end_date]).aggregate(Sum('grand_total'))
                tot_item_amount=tot_item_amount['bill_amount__sum']
                tot_tax_amount=round(tot_tax_amount['tax_amount__sum'],2)
                tot_grand_total=round(tot_grand_total['grand_total__sum'],2)

                print('total SE amount:{}, total_amount_sum:{},tot_grand_total{}'.format(tot_item_amount,tot_tax_amount,tot_grand_total))

                my_dict['title']='Daily balance sheet Report'
                my_dict['current_date']=current_date
                my_dict['tot_item_amount']=tot_item_amount  #SE
                my_dict['tot_tax_amount']=tot_tax_amount
                my_dict['tot_grand_total']=tot_grand_total

                my_dict['tot_bill_item_amount']=tot_bill_item_amount  #O IE
                my_dict['tot_bill_tax_amount']=tot_bill_tax_amount
                my_dict['tot_bill_grand_amount']=tot_bill_grand_amount

                areports=models.Sell_Entry.objects.filter(sell_datetime__range=[current_date,end_date])
                my_dict['areports']=areports
                #################
            return render(request,'testapp/balance_sheet_report.html',my_dict)
        else:
            print('form not valid')
    else:   #GET section
        my_dict={}  # starting afresh
        my_dict['title']='Daily balance sheet Report'
        form=forms.Balance_sheet_query_form()
        my_dict['form']=form
        return render(request,'testapp/balance_sheet_report.html',my_dict)


def export_sell_balance_report(request):
    my_dict={}
    my_dict['title']='exp_balance_sheet_report'
    print('export_sell_balance_report entered')
    response = HttpResponse(content_type='application/ms-excel')
    filename="balance_report_{}.xls".format(datetime.date.today())
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

    current_date=datetime.date.today()



    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('balance_report_{}'.format(current_date))  # low_stock, summary

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    print('export_sell_balance_report entered')
    columns = ['bill_no','bill_amount', 'tax_amount','grand_total','sell_datetime' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    # font_style1=xlwt.Style.easyxf(num_format_str="dd/mm/yyyy")
    font_style.font.bold = False
    rows=models.Sell_Entry.objects.filter(sell_datetime__year=current_date.year,sell_datetime__month=current_date.month,sell_datetime__day=current_date.day ).values_list('bill_no','bill_amount', 'tax_amount','grand_total','sell_datetime') # filtering on date
    print('rows',rows)
    for row in rows:
        row_num += 1
        # for col_num in range(len(row)):
        #     ws.write(row_num, col_num, row[col_num], font_style)
        ws.write(row_num, 0, row[0], font_style)
        ws.write(row_num, 1, row[1], font_style)
        ws.write(row_num, 2, row[2], font_style)
        ws.write(row_num, 3, row[3], font_style)
        ws.write(row_num, 4, str(row[4]), font_style)

    print('helleelleelelelel')
    wb.save(response)
    # return response

    my_dict['se_reports']=rows
    print('11111111112')
    return render(request,'testapp/item_expiry_report.html',my_dict)

def export_sell_balance_report_1(request):
    my_dict={}
    t_se_grand_total=0
    t_rse_grand_total=0
    t_se_paid_by_cash=0
    t_se_paid_by_card=0
    t_se_disc_amount=0

    my_dict['title']='balance_sheet_report'.upper()
    print('export_sell_balance_report_new')
    current_date=datetime.date.today()
    se_rows=models.Sell_Entry.objects.filter(sell_datetime__year=current_date.year,sell_datetime__month=current_date.month,sell_datetime__day=current_date.day ). \
        values('bill_no','bill_amount', 'tax_amount','grand_total','sell_datetime', 'mode_of_payment','paid_by_cash','paid_by_card','discount_amount') # filtering on date #added discount_amount on 23-Nov
    # print(se_rows)

    for se in se_rows:
        t_se_grand_total=t_se_grand_total+se['grand_total']
        t_se_paid_by_cash=t_se_paid_by_cash+se['paid_by_cash']
        t_se_paid_by_card=t_se_paid_by_card+se['paid_by_card']
        t_se_disc_amount=t_se_disc_amount+se['discount_amount']

    my_dict['t_se_grand_total']= t_se_grand_total
    my_dict['t_se_paid_by_cash']= t_se_paid_by_cash
    my_dict['t_se_paid_by_card']= t_se_paid_by_card
    my_dict['t_se_disc_amount']= t_se_disc_amount

    rse_rows=models.Returned_Sell_Entry.objects.filter(returned_sell_datetime__year=current_date.year,returned_sell_datetime__month=current_date.month,returned_sell_datetime__day=current_date.day ). \
        values('sell_entry_ref__bill_no','rbill_no', 'rbill_amount','rbill_tax_amount','rbill_grand_total', 'returned_sell_datetime','rmode_of_payment','rpayment_by_cash','rpayment_by_card') # filtering on date
    print(rse_rows)

    for rse in rse_rows:
        t_rse_grand_total=t_rse_grand_total+rse['rbill_grand_total']
    my_dict['t_rse_grand_total']= t_rse_grand_total
    my_dict['net_balance']= t_se_grand_total - t_rse_grand_total-t_se_disc_amount

    my_dict['se_reports']=se_rows
    my_dict['rse_reports']=rse_rows

    # print('11111111112')
    return render(request,'testapp/item_expiry_report.html',my_dict)

def cal_upd_SE(request,id):
    # 'generate_rbill/<str:id>'

    t_amount=0
    t_tax_amount=0
    t_grand_total=0
    t_Qty_sold=0
    t_count=0
    try:
        se=models.Sell_Entry.objects.get(bill_no=int(id))

    except ObjectDoesNotExist:
        print('exception ObjectDoesNotExist in generate_ bill/<str:id>/ create_sbill_id')
        redirect('/q_item1')

    ies=models.Out_Item_Entry.objects.filter(bill_no_ref__bill_no=int(id))
    print('oie  rbill ', ies)
    for ie in ies:

        t_amount=t_amount+ie.bill_item_amount
        t_tax_amount=t_tax_amount+ie.bill_tax_amount
        t_grand_total=t_grand_total+ie.bill_tax_amount+ie.bill_item_amount
        t_Qty_sold=t_Qty_sold+ie.Qty_sold
        t_count=t_count+1

    print('t_count:', t_count)
    print('t_tax_amount:', t_tax_amount)
    print('t_Qty_sold:', t_Qty_sold)
    print('t_amount:', t_amount)
    print('ies:', ies)

    if se.status!='LOCKED':
        se.bill_amount=t_amount
        se.tax_amount=t_tax_amount
        se.grand_total=t_grand_total
        se.sell_datetime= datetime.datetime.now()
        # se.status='LOCKED'  #only paybill will only lock status
        record=se.save(update_fields=['bill_amount','tax_amount','grand_total','sell_datetime','status'])
        print('se update record:',record,se.sell_datetime )
    return t_count, se

def pay_retail_bill_view(request,id):
    my_dict={}
    message=''
    my_dict['title']='submit_pay_retail_bill'
    print('id in pay_retail_bill',id)
    se=models.Sell_Entry.objects.get(bill_no=id)
    # for i in se:
    #     print('se',i)
    my_dict['bill_amount']= se.grand_total
    if request.method=='POST':
        form=forms.payment_form(request.POST)
        print('is valid',form.is_valid())
        if form.is_valid():

            billed_amount=se.grand_total
            mode_of_payment=form.cleaned_data['mode_of_payment']
            tx_id_reference=form.cleaned_data['tx_id_reference']
            paid_by_cash=form.cleaned_data['paid_by_cash']
            paid_by_card=form.cleaned_data['paid_by_card']
            card_issued_bank=form.cleaned_data['card_issued_bank']
            #logic
            tot_bill_payment=round(Decimal(paid_by_cash)+Decimal(paid_by_card),2)
            balance=billed_amount-tot_bill_payment
            print('billed_amount {},mode_of_payment {}'.format(billed_amount,mode_of_payment))
            print('tx_id_reference {} paid_by_cash{} paid_by_card{}'.format(tx_id_reference, paid_by_cash, paid_by_card))
            print('tot_bill_payment {} balance{}'.format(tot_bill_payment,balance))

            if mode_of_payment=="CARD":

                initial_ie={'paid_by_card':se.paid_by_card,'paid_by_cash':0.0}
                if paid_by_card >billed_amount :
                    my_dict['msg']='entered card amount is more than billed amount , enter correct value'
                    form=forms.payment_form(initial=initial_ie)
                    my_dict['form']= form
                    return render(request,'testapp/pay_rbill_form.html',my_dict)
                elif paid_by_card < billed_amount:
                    my_dict['msg']='entered card amount is less than billed amount , enter correct value'
                    form=forms.payment_form(initial=initial_ie)
                    my_dict['form']= form
                    return render(request,'testapp/pay_rbill_form.html',my_dict)
                elif tx_id_reference=='empt':
                    my_dict['msg']='entered traction id is empt please fill correct value'
                    form=forms.payment_form(initial=initial_ie)
                    my_dict['form']= form
                    return render(request,'testapp/pay_rbill_form.html',my_dict)

                elif card_issued_bank=='empty' :
                    my_dict['msg']='entered card_issued_bank  is empty please fill correct value'
                    form=forms.payment_form(initial=initial_ie)
                    my_dict['form']= form
                    print('hi 111110 payment')
                    return render(request,'testapp/pay_rbill_form.html',my_dict)
                elif billed_amount ==tot_bill_payment: #success case
                    return_cash=paid_by_card-billed_amount
                    x=models.Sell_Entry.objects.filter(bill_no=id).update( \
                    mode_of_payment=mode_of_payment,
                    tx_id_reference=tx_id_reference,
                    card_issued_bank=card_issued_bank,
                    paid_by_cash=0.0,
                    paid_by_card=paid_by_card,
                    return_cash=return_cash,
                    status='LOCKED'
                    )
            elif mode_of_payment=="CASH":
                print('hi 111111 payment')
                if  paid_by_cash> billed_amount :
                    message='return change ={}'.format(balance)
                    return_cash=paid_by_cash-billed_amount


                if billed_amount <=tot_bill_payment: #success case
                    x=models.Sell_Entry.objects.filter(bill_no=id).update( \
                    mode_of_payment=mode_of_payment,
                    tx_id_reference=tx_id_reference,
                    card_issued_bank=card_issued_bank,
                    paid_by_cash=billed_amount,
                    paid_by_card=0.0,
                    return_cash=return_cash,
                    status='LOCKED'
                    )
            elif mode_of_payment=="BOTH":
                initial_ie={'paid_by_card':0.0,'paid_by_cash':0.0}

                if tx_id_reference=='empt':
                    my_dict['msg']='entered traction id is empt please fill correct value'
                    form=forms.payment_form(initial=initial_ie)
                    my_dict['form']= form
                    return render(request,'testapp/pay_rbill_form.html',my_dict)

                elif card_issued_bank=='empty' :
                    my_dict['msg']='entered card_issued_bank  is empty please fill correct value'
                    form=forms.payment_form(initial=initial_ie)
                    my_dict['form']= form
                    print('hi 111110 payment')
                    return render(request,'testapp/pay_rbill_form.html',my_dict)

                elif paid_by_card >billed_amount :  # not allowing to bill on card more than billed_amount
                    my_dict['msg']='entered card amount is more than billed amount , enter correct value'
                    form=forms.payment_form(initial=initial_ie)
                    my_dict['form']= form
                    return render(request,'testapp/pay_rbill_form.html',my_dict)
                elif billed_amount <=tot_bill_payment:  #success case
                    return_cash=tot_bill_payment-billed_amount
                    x=models.Sell_Entry.objects.filter(bill_no=id).update( \
                    mode_of_payment=mode_of_payment,
                    tx_id_reference=tx_id_reference,
                    card_issued_bank=card_issued_bank,
                    paid_by_cash=billed_amount-paid_by_card,
                    paid_by_card=paid_by_card,
                    return_cash=return_cash,
                    status='LOCKED'
                    )
            print('this bf se.status LOCK check ,', se.status)
            se=models.Sell_Entry.objects.get(bill_no=id) # to get latest status
            if se.status=='LOCKED':  #lock all OIE entries ( it does not allow to delete or update)
                oies=models.Out_Item_Entry.objects.all().filter(bill_no_ref__bill_no=id)
                for oie in oies:
                    oie.status='LOCKED'
                    oie.save()
                    print('pay_retail_bill_view...  oie status is LOCKED',oie)
        return redirect('oie_list_based_on_id',id=id)
        # print('sss id',id)
        # return redirect('generate_rbill_name', id=id)
        # return render(request,'testapp/pay_rbill_form.html',my_dict)
    else:   #GET
        oie_count, se= cal_upd_SE(request,id)

        if oie_count==0:
            msg='For bill_no={} no items are added , please first add items and pay'.format(id)

            if se.status=='LOCKED':
                msg+='\n, unlocking entry '
                se.status='UN_LOCKED'
                se.save(update_fields=['status',])
            my_dict['msg']=msg
            return render(request,'testapp/pay_rbill_form.html',my_dict)

        elif se.status !='LOCKED':  #UNLOCKED
            initial_ie={'paid_by_cash':se.grand_total}
            form=forms.payment_form()
            my_dict['form']= form
            my_dict['bill_amount']= se.grand_total
        else:
            msg='already paid , you cannot initiate again payment method'
            print(msg)
            my_dict['msg']=msg
        return render(request,'testapp/pay_rbill_form.html',my_dict)

def pay_retail_bill_view1(request,id):  #23-Nov  adding discount_amount
    #adding discount field to form and corresponding entry in SE
    #billed_amount=se.grand_total - discount_amount (form field)
    # update discount_amount in  SE as well

    my_dict={}
    message=''
    my_dict['title']='submit_pay_retail_bill'
    print('id in pay_retail_bill',id)
    se=models.Sell_Entry.objects.get(bill_no=id)
    # for i in se:
    #     print('se',i)
    my_dict['bill_amount']= se.grand_total
    if request.method=='POST':
        form=forms.payment_form1(request.POST)
        print('is valid',form.is_valid())
        if form.is_valid():
            discount_amount=form.cleaned_data['discount_amount']
            billed_amount=se.grand_total-discount_amount

            mode_of_payment=form.cleaned_data['mode_of_payment']
            tx_id_reference=form.cleaned_data['tx_id_reference']
            paid_by_cash=form.cleaned_data['paid_by_cash']
            paid_by_card=form.cleaned_data['paid_by_card']
            card_issued_bank=form.cleaned_data['card_issued_bank']
            #logic
            tot_bill_payment=round(Decimal(paid_by_cash)+Decimal(paid_by_card),2)
            balance=billed_amount-tot_bill_payment
            print('billed_amount {},mode_of_payment {}'.format(billed_amount,mode_of_payment))
            print('tx_id_reference {} paid_by_cash{} paid_by_card{} discount_amount{}'.format(tx_id_reference, paid_by_cash, paid_by_card,discount_amount))
            print('tot_bill_payment {} balance{}'.format(tot_bill_payment,balance))

            if mode_of_payment=="CARD":

                initial_ie={'paid_by_card':se.paid_by_card,'paid_by_cash':0.0}
                if paid_by_card >billed_amount :
                    my_dict['msg']='entered card amount is more than billed amount , enter correct value'
                    form=forms.payment_form1(initial=initial_ie)
                    my_dict['form']= form
                    return render(request,'testapp/pay_rbill_form.html',my_dict)
                elif paid_by_card < billed_amount:
                    my_dict['msg']='entered card amount is less than billed amount , enter correct value'
                    form=forms.payment_form1(initial=initial_ie)
                    my_dict['form']= form
                    return render(request,'testapp/pay_rbill_form.html',my_dict)
                elif tx_id_reference=='empt':
                    my_dict['msg']='entered traction id is empt please fill correct value'
                    form=forms.payment_form1(initial=initial_ie)
                    my_dict['form']= form
                    return render(request,'testapp/pay_rbill_form.html',my_dict)

                elif card_issued_bank=='empty' :
                    my_dict['msg']='entered card_issued_bank  is empty please fill correct value'
                    form=forms.payment_form1(initial=initial_ie)
                    my_dict['form']= form
                    print('hi 111110 payment')
                    return render(request,'testapp/pay_rbill_form.html',my_dict)
                elif billed_amount ==tot_bill_payment: #success case
                    return_cash=paid_by_card-billed_amount
                    x=models.Sell_Entry.objects.filter(bill_no=id).update( \
                    mode_of_payment=mode_of_payment,
                    tx_id_reference=tx_id_reference,
                    card_issued_bank=card_issued_bank,
                    paid_by_cash=0.0,
                    paid_by_card=paid_by_card,
                    return_cash=return_cash,
                    discount_amount=discount_amount, #23-Nov
                    status='LOCKED'
                    )
            elif mode_of_payment=="CASH":
                print('hi 111111 payment')
                if  paid_by_cash> billed_amount : #success case
                    message='return change ={}'.format(balance)
                    return_cash=paid_by_cash-billed_amount


                if billed_amount <=tot_bill_payment: #success case
                    return_cash=paid_by_cash-billed_amount
                    x=models.Sell_Entry.objects.filter(bill_no=id).update( \
                    mode_of_payment=mode_of_payment,
                    tx_id_reference=tx_id_reference,
                    card_issued_bank=card_issued_bank,
                    paid_by_cash=billed_amount,
                    paid_by_card=0.0,
                    return_cash=return_cash,
                    discount_amount=discount_amount, #23-Nov
                    status='LOCKED'
                    )
            elif mode_of_payment=="BOTH":
                initial_ie={'paid_by_card':0.0,'paid_by_cash':0.0}

                if tx_id_reference=='empt':
                    my_dict['msg']='entered traction id is empt please fill correct value'
                    form=forms.payment_form1(initial=initial_ie)
                    my_dict['form']= form
                    return render(request,'testapp/pay_rbill_form.html',my_dict)

                elif card_issued_bank=='empty' :
                    my_dict['msg']='entered card_issued_bank  is empty please fill correct value'
                    form=forms.payment_form1(initial=initial_ie)
                    my_dict['form']= form
                    print('hi 111110 payment')
                    return render(request,'testapp/pay_rbill_form.html',my_dict)

                elif paid_by_card >billed_amount :  # not allowing to bill on card more than billed_amount
                    my_dict['msg']='entered card amount is more than billed amount , enter correct value'
                    form=forms.payment_form1(initial=initial_ie)
                    my_dict['form']= form
                    return render(request,'testapp/pay_rbill_form.html',my_dict)
                elif billed_amount <=tot_bill_payment:  #success case
                    return_cash=tot_bill_payment-billed_amount
                    x=models.Sell_Entry.objects.filter(bill_no=id).update( \
                    mode_of_payment=mode_of_payment,
                    tx_id_reference=tx_id_reference,
                    card_issued_bank=card_issued_bank,
                    paid_by_cash=billed_amount-paid_by_card,
                    paid_by_card=paid_by_card,
                    return_cash=return_cash,
                    discount_amount=discount_amount, #23-Nov
                    status='LOCKED'
                    )
            print('this bf se.status LOCK check ,', se.status)
            se=models.Sell_Entry.objects.get(bill_no=id) # to get latest status
            if se.status=='LOCKED':  #lock all OIE entries ( it does not allow to delete or update)
                oies=models.Out_Item_Entry.objects.all().filter(bill_no_ref__bill_no=id)
                for oie in oies:
                    oie.status='LOCKED'
                    oie.save()
                    print('pay_retail_bill_view...  oie status is LOCKED',oie)
        return redirect('oie_list_based_on_id',id=id)
        # print('sss id',id)
        # return redirect('generate_rbill_name', id=id)
        # return render(request,'testapp/pay_rbill_form.html',my_dict)
    else:   #GET
        oie_count, se= cal_upd_SE(request,id)

        if oie_count==0:
            msg='For bill_no={} no items are added , please first add items and pay'.format(id)

            if se.status=='LOCKED':
                msg+='\n, unlocking entry '
                se.status='UN_LOCKED'
                se.save(update_fields=['status',])
            my_dict['msg']=msg
            return render(request,'testapp/pay_rbill_form.html',my_dict)

        elif se.status !='LOCKED':  #UNLOCKED
            initial_ie={'paid_by_cash':se.grand_total}
            form=forms.payment_form1()
            my_dict['form']= form
            my_dict['bill_amount']= se.grand_total
        else:
            msg='already paid , you cannot initiate again payment method'
            print(msg)
            my_dict['msg']=msg
        return render(request,'testapp/pay_rbill_form.html',my_dict)

def reg_data_json_view4(request,id):
    print('id',id)
    l=[]
    data={}
    try:
        p_data= rmodels.Registration.objects.filter(phone=id.strip())
        print(p_data, len(p_data))
        print('id',id)

        if len(p_data)!=0:
            # print('p_data.patient_name{}, phone{}, email{},hospital_id '.format( p_data.patient_name,p_data.phone, p_data.email, p_data.OPID))
            for p in p_data:
                print(p)
        else:
            print('p_data length=0')
        for p in p_data:
            # data['patient_name']=p.patient_name,
            # data['phone']=p.phone,
            # data['hospital_id']=p.OPID,
            # data['email']=p.email,

            data={
            'patient_name':p.patient_name,
            'phone':p.phone,
            'hospital_id':p.OPID,
            'email':p.email
            }
            l.append(data)
        print('l',len(l))
        if len(l)==0:
            return JsonResponse({"error":"No data"})
        else:
            return JsonResponse(l[0])

    except ObjectDoesNotExist:
        print('exception in model get() reg_data_json_view4, id',id)
    return JsonResponse(data)


def cus_reg_data_json_view4(request,id):
    print('id',id)
    l=[]
    data={}
    try:
        p_data= models.Customer_Address.objects.filter(phone=id.strip())
        if len(p_data)==0:
            print('customer table is not having data, searching customer address table')
            p_data= rmodels.Registration.objects.filter(phone=id.strip())
        print(p_data, len(p_data),type(p_data))
        print('id',id)

        if len(p_data)!=0:
            print('type models.Customer_Address:',type(p_data[0]))
            customer = isinstance(p_data[0], models.Customer_Address) #[0] needed to test models.Customer_Address type
            print('customer flg',customer)
            if customer:
                for p in p_data:
                    data={
                    'patient_name':p.contact_name,
                    'phone':p.phone,
                    'hospital_id':p.hospital_id,
                    'email':p.email
                    }
                    l.append(data)
            else: # patient -Registration_table
                for p in p_data:
                    data={
                    'patient_name':p.patient_name,
                    'phone':p.phone,
                    'OPID':p.OPID,
                    'email':p.email
                    }
                    l.append(data)
        else:
            print('p_data length=0')

        print('l',len(l))
        if len(l)==0:
            return JsonResponse({"error":"No data"})
        else:
            return JsonResponse(l[0])

    except ObjectDoesNotExist:
        print('exception in model get() cus_reg_data_json_view4, id',id)
    return JsonResponse(data)
### login_required
@login_required
def staff_home_view(request):
    my_dict={}
    try:
        r=models.Staff.objects.get(lname=request.user.username)

    except ObjectDoesNotExist:
        error= 'user doesnot exist , please login with correct username'
        print('ObjectDoesNotExist : Staff.objects in admin_home_view')
        return render(request,'testapp/error.html',{'title':'Student home page','error':error,'my_dict':my_dict})

    my_dict['email']=r.email
    my_dict['sname']=r.sname
    my_dict['role']=r.role

    request.session['my_dict']=my_dict

    if r.role =='Pharmacist':
        print('role',r.role)
        print('renderingto  Pharmasist page')
        return render(request,'testapp/shome.html', my_dict)

    elif  r.role =='Admin':
        print('role',r.role)
        print('renderingto admin home page')

        response=render(request,'testapp/ahome.html',  my_dict)
        return response
    else:
        my_dict['role']='Receiptionist'
        print('role',r.role)
        print('Receiptionist ',{'sname':r.sname, 'role':r.role})
        # request.session['my_dict']=my_dict  #copy my_dict{}  to session
        # json api -getting error 'Object of type QuerySet is not JSON serializable'
        # BASE_URL='127.0.0.1:8000/'
        END_POINT='appt_japi4/Today/'
        json_resp=requests.get(settings.BASE_URL+END_POINT)

        print(json_resp.status_code)
        alert_resp=json_resp.json()
        print(alert_resp)

        # alert_resp= json.loads(json_resp)
        # for i in alert_resp:
        #     print( i)
        # print('type(json_resp)', type(json_resp))
        # my_dict['alert_resp'],my_dict['message']=v1.Appointment_report('AllNextAppointments')
        # -getting error
        # alert_resp,message=v1.Appointment_report('AllNextAppointments')
        # print(alert_resp, message)
        # my_dict['alert_resp']=alert_resp
        # current_date=datetime.date.today()
        # areports=rmodels.Appointment_Item.objects.filter(appt_date =current_date)
        # print(areports)
        # my_dict['alert_resp1']=areports
        my_dict['alert_resp']=alert_resp
        # return render(request,'testapp/shome.html',my_dict)
        return render(request,'testapp1/rhome.html',my_dict)


def add_item_to_IM_view(request):
# add_item_to_IM/', 1)adds entry in Item Master 2) shows relavent item entries
    my_dict={}
    se_bill_no_ref={}
    my_dict['title']='Item_Master_Entry'
    if request.method=='POST':
        form=forms.Item_Master_form(request.POST)
        print('create im',form.is_valid())
        if form.is_valid():
            my_dict['result']=form.save()
        if form.errors:
            my_dict['error']=form.errors
        return redirect('/list_IM')
        # return render(request,'testapp/im_results.html',my_dict)
    else:

        form=forms.Item_Master_form()
        my_dict['form']= form
        return render(request,'testapp/iform.html',my_dict)
def list_IM_view(request):
# im_list/', 1)list all Item_Master entries
    my_dict={}

    my_dict['title']='Item_Master_list'
    try:
        areports=models.Item_Master.objects.all()
        my_dict['areports']=areports

    except ObjectDoesNotExist:
        message='ObjectDoesNotExist exeception occured list_IM_view '

    return render(request,'testapp/im_results.html',my_dict)
def upd_IM_item_view(request,id):
    # url: 'upd_IM_item/<int:id>'
    my_dict={}
    my_dict['title']='Update_IM_Item'
    im_item=models.Item_Master.objects.get(id=int(id))
    if request.method=='POST':
        form=forms.Item_Master_form(request.POST,instance=im_item)
        if form.is_valid():
            form.save()
            print("updated IM_Item")
            return redirect('/list_IM') ## check
    else:
        im_dict={
        'item_code':im_item.item_code,
        'item_name':im_item.item_name,
        'print_name':im_item.print_name,
        'Mfd_by':im_item.Mfd_by,
        'HSN_code':im_item.HSN_code,
        'MRP':im_item.MRP,
        'BatchNo':im_item.BatchNo,
        'tax_percent':im_item.tax_percent,
        'sch':im_item.sch,
        }
        form=forms.Item_Master_form(initial=im_dict)

        my_dict['form']= form
        return render(request,'testapp/iformx.html',my_dict)
def del_IM_item_view(request, id):
    # /del_IM_item/<int:id>'
    try:
        im=models.Item_Master.objects.get(id=id)
        im.delete()

    except ObjectDoesNotExist:
        print('ObjectDoesNotExist exception occured in del_Item_Entry_view: id:', id)

    return redirect('/list_IM')

class im_list_json(View):
    # im_list_japi/
    def get(self, request,*args, **kwargs):

        # p_data=models.Item_Master.objects.all()
        # json_data=serializers.serialize('json',p_data)
        # print('json_data',json_data)
        # final_list=[]
        # p_data= json.loads(json_data)
        # for obj in p_data:
        #     ob=obj['fields']
        #     final_list.append(ob)
        #     print('----',ob)
        # json_data=json.dumps(final_list)
        # print('f json_data',json_data)
        # print('type ',type(json_data))
        # # return HttpResponse(json_data,content_type='applicaiton/json')
        # return HttpResponse(json_data,'application/json',status=200)

        p_data=models.Item_Master.objects.all()
        # print(p_data)
        json_data=serializers.serialize('json',p_data)
        # print('json_data',json_data)
        final_list=[]
        p_data= json.loads(json_data)
        for obj in p_data:
            ob1=obj['fields']
            ob=ob1["item_name"]
            final_list.append(ob)
            # print('----',ob)
        json_data=json.dumps(final_list)
        # print('f json_data',json_data)
        # print('type ',type(json_data))

        return HttpResponse(json_data,'application/json',status=200)

def get_im_id_view( request,id,*args,**kwargs):
        print('id',id)
        p_data=models.Item_Master.objects.get(id=id)
        json_data=serializers.serialize('json',[p_data,])
        print('json_data',json_data)
        final_list=[]
        p_data= json.loads(json_data)
        for obj in p_data:
            ob=obj['fields']
            final_list.append(ob)
            print('----',ob)
        json_data=json.dumps(final_list)
        print('f json_data',json_data)
        print('type ',type(json_data))
        # return HttpResponse(json_data,content_type='applicaiton/json')
        return HttpResponse(json_data,'application/json',status=200)
def get_im_entry_view( request,item_n,*args,**kwargs):
        print('item name',item_n)
        q=models.Item_Master.objects.filter(item_name=item_n)
        q=q.first()

        print('q',q)

        json_data=serializers.serialize('json',[q,])  # .first() solves AttributeError: 'QuerySet' object has no attribute '_meta'
        print('json_data',json_data)
        final_list=[]
        p_data= json.loads(json_data)
        for obj in p_data:
            ob=obj['fields']
            final_list.append(ob)
            print('----',ob)

        #
        json_data=json.dumps(final_list)

        # print('type ',type(json_data))
        return HttpResponse(json_data,'application/json',status=200)

def import_Item_Master_from_file(f):
    print('f:',f)
    df = pd.read_csv(f)
    # print(df)
    for i in df.index:
        print(df['item_code'][i], df['item_name'][i])
        obj, created = models.Item_Master.objects.update_or_create(
            item_code=df['item_code'][i], item_name= df['item_name'][i],
            print_name= df['print_name'][i],Mfd_by=df['Mfd_by'][i],HSN_code=df['HSN_code'][i],
            MRP=df['MRP'][i],BatchNo= df['BatchNo'][i],tax_percent=df['tax_percent'][i],sch=df['sch'][i],

        )
        print(created, obj)
    del df
def create_Item_Master_from_file(request):
    # upload_im/', v1.create_Item_Master_from_file
    my_dict={}
    my_dict['title']='Import_Item_Master_from_file'
    if request.method=='POST':
        form=forms.IM_upload_form(request.POST, request.FILES)

        if form.is_valid():
            f=request.FILES['file']
            import_Item_Master_from_file(f)
            return render(request,'testapp/im_results.html',my_dict)
        else:
            message='fileupload failed'
            my_dict['error']=form.errors
            return render(request,'testapp/im_results.html',my_dict)
    else:
        print('get IM upload form')
        form=forms.IM_upload_form()
        my_dict['form']= form
        return render(request,'testapp/file_upload_form.html',my_dict)

def dash_board_view(request):
    my_dict={'title':'Dash Board'}

    ## Low Stock
    ie_low_stock = models.Item_Entry.objects.all().filter(low_stock_ind_status='ON').values('item_name', 'print_name', 'supplier_ref', 'Qty_in','Qty_available')
    my_dict['ie_low_stock']=ie_low_stock

    ## Near to Expiry Stock
    current_date=datetime.date.today()
    end_date=current_date+ relativedelta(months=7)
    ie_expiry_stock=models.Item_Entry.objects.filter(Q(Exp_date__range=[current_date,end_date]) & Q(Qty_available__gt=0 )).\
    values('item_name', 'print_name', 'supplier_ref', 'BatchNo','Exp_date','Qty_available','purchase_ref__invoice_no')
    my_dict['ie_expiry_stock']=ie_expiry_stock

    ## Current Stock
    rows=models.Item_Entry.objects.filter(Qty_available__gt=0)
    x={}
    y={}
    for row in rows:
        x=models.Item_Entry.objects.filter(item_name= row.item_name).aggregate(Sum('Qty_available'))
        y[row.item_name]=x['Qty_available__sum']
    my_dict['ie_current_stock']= y


    return render(request,'testapp/dash_board.html',my_dict)

def Fin_report(request):
    my_dict={'title':'Finance Report'}
    if request.method=='POST':
        form=forms.financial_report_form(request.POST)
        print('Fin_report:post',form.is_valid())
        if form.is_valid():
            F_Year=form.cleaned_data['F_Year']
            print('fyear:',F_Year, type(F_Year))
            s=F_Year.get_list()  # s=[2020,21]




        else:
            my_dict['error']=form.errors
        return render(request,'testapp/rse_results.html',my_dict)
    else:  #GET

        form=forms.financial_report_form()
        my_dict['form']= form
        return render(request,'testapp/iform3.html',my_dict)

    return render(request,'testapp/iform3.html',my_dict)
