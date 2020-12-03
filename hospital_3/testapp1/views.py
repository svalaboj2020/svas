from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from testapp1 import forms
from testapp import forms as forms1
from testapp1 import models

from dateutil.relativedelta import relativedelta
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from testapp.utils import render_to_pdf
from num2words import num2words
from decimal import *
import datetime
import json
from django.views.generic import View
from itertools import chain

# Create your views here.
def home_view(request):
    return render(request, 'testapp1/home.html')
def reg_form_view(request):
# register/
    my_dict={}
    my_dict['title']='Patient_Registration'
    if request.method=='POST':
        form=forms.Reg_form(request.POST)
        print('registration',form.is_valid())
        if form.is_valid():
            #  OPID/hospid generation logic
            dt=str(datetime.date.today().year)+ str(datetime.date.today().month)
            print(type(dt))
            x=models.Registration.objects.last()
            y=dt+str(x.id+1)

            print('opid {}',y)
            result=form.save()
            id=result.id
            #update entry with OPID
            reg=models.Registration.objects.filter(id=id).update(OPID=y)

            message='{} registration is done successfully'.format(result.id)
            print('message :', message)

        else:
            message='registration failed'
            my_dict['errors']=form.errors
        my_dict['msg']=message
        return render(request,'testapp1/reg_form.html',my_dict)
    else:

        form=forms.Reg_form()
        my_dict['form']= form
        return render(request,'testapp1/reg_form.html',my_dict)
def create_chart_from_file(request,id):
    my_dict={}

    if request.method=='POST':

        form=forms.Doc_fee_upload_form(request.POST, request.FILES)

        if form.is_valid():
            f=request.FILES['file']
            if id=="docfee":
                my_dict['title']='Upload Doctor Fees'
                create_fee_chart_from_file(f)
            elif id=="labfee":
                my_dict['title']='Upload Lab Fees'
                create_lab_chart_from_file(f)
            else:
                message='invalid url'
            message='{} file upload is done successfully'.format(f.name)
            my_dict['msg']=message
            return render(request,'testapp1/file_upload_form.html',my_dict)

        else:
            message='fileupload failed'
        my_dict['msg']=message
        return render(request,'testapp1/file_upload_form.html',my_dict)
    else:
        if id=='docfee':
            my_dict['title']='Upload Doctor Fees'
        elif id=='labfee':
            my_dict['title']='Upload Lab Fees'
        form=forms.Doc_fee_upload_form()
        my_dict['form']= form
        return render(request,'testapp1/file_upload_form.html',my_dict)

def reg_sform_view(request):
    # 'regSearch',

    my_dict={}
    my_dict['title']='Search Registration data'
    if request.method=='POST':
        query_option=request.POST['query_option']
        search_word=request.POST['search_word']
        print('query_option,search_word ',query_option,search_word)
        results=search_and_get(search_word,query_option)
        message='{} search is done successfully'.format(results)
        my_dict['results']=results
        return render(request,'testapp1/reg_query_form.html',my_dict)
    else:
        return render(request,'testapp1/reg_query_form.html',my_dict)

def search_and_get(search_word,query_option):
    ret=0
    try:
        if query_option=="by_OPID" :
            ret=models.Registration.objects.get(OPID=search_word)
        elif query_option=="by_phone" :
            ret=models.Registration.objects.filter(phone__contains=search_word)
        else:
            print('seach by name is not implemented')
        return ret
    except ObjectDoesNotExist:
        print('ObjectDoesNotExist in search_and_get() ')
        ret='exception search failed'
        pass
    print('ret:',ret)


def create_fee_chart_from_file(f):
    # f=open("myfile.txt","r")
    df = pd.read_csv(f)
    # form=forms.Fee_chart_form()
    for i in df.index:
        # form=forms.Fee_chart_form(doctor_name=df['doctor_name'][i],dept= df['dept'][i],fee= df['fee'][i],availability=df['availability'][i])
        # ret=form.save()
        obj, created = models.Fee_chart.objects.update_or_create(
            doctor_name=df['doctor_name'][i], dept= df['dept'][i],
            fee= df['fee'][i],availability=df['availability'][i]
        )
        print(created, obj)
    del df

def create_lab_chart_from_file(f):
    df = pd.read_csv(f)
    # print(df)
    for i in df.index:
        print(df['Service_Type'][i], df['Service_Name'][i])
        obj, created = models.Lab_chart.objects.update_or_create(
            Service_Type=df['Service_Type'][i], Service_Name= df['Service_Name'][i],
            charge= df['charge'][i],perc10_Total=df['perc10_Total'][i],perc15=df['perc15'][i],
            perc15_Total=df['perc15_Total'][i]
        )
        print(created, obj)
    del df

def generate_reg_receipt_view(request):

    my_dict={}
    my_dict={'title':'Registration Bill Cum Receipt'}

    l=[]
    t_amount=0
    t_tax_amount=0
    t_grand_total=0
    t_Qty_sold=0
    t_count=0

    my_dict['ie_sum']=t_amount
    my_dict['ie_count']=t_count
    my_dict['ie_tax_amount']=t_tax_amount
    my_dict['ie_Qty_in']=t_Qty_sold
    my_dict['t_grand_total']=t_grand_total
    my_dict['username']=request.user.username
    my_dict['amountInWord']=num2words(36.40,lang ='en_IN')

    print('3333333S',my_dict['amountInWord'])



    # pdf=render_to_pdf('pdf/invoice.html',{'areports':ies,'pe':pe,'ie_count':t_count,'ie_Qty_in':t_Qty_in,'ie_sum':t_amount,'ie_tax_amount':t_tax_amount ,'t_grand_total':t_grand_total}) #working
    pdf=render_to_pdf('pdf/reg_bill_receipt.html',my_dict)
    return HttpResponse(pdf, content_type='application/pdf')  # 'generate_rbill/<str:id>'
def generate_reg_receipt_view(request,name,id,bill_no):
# 'generate_regbill/<str:name>/<int:id>/bill_no'
    my_dict={}
    my_dict={'title':'Registration Bill Cum Receipt'}

    # l=[]
    t_amount=0
    t_tax_amount=0
    t_grand_total=0
    # t_Qty_sold=0
    t_count=0

    try:
        reg=models.Registration.objects.get(id=id)
        my_dict['reg']=reg
        doc=models.Fee_chart.objects.get(doctor_name=name)
        my_dict['doc']=doc
        my_dict['bill_no']=bill_no

        my_dict['username']=request.user.username
        my_dict['amountInWord']=num2words(doc.fee,lang ='en_IN')

###    get Bill_Entry

        be=models.Bill_Entry.objects.get(bill_no=bill_no)
        print('reg={}, be={}'.format(reg,be))
        my_dict['date_']=be.billed_datetime
        my_dict['mode_of_payment']=be.mode_of_payment

        ## create bill_item
        visit_type=request.session.get('visit_type','WALK_IN')
        Ref_by=request.session.get('Ref_by','None')
        my_dict['visit_type']=visit_type
        my_dict['Ref_by']=Ref_by
        my_dict['Created_Dt']=be.billed_datetime
        my_dict['Print_Dt']=datetime.datetime.now()
        # try:                            # getting expection during demo
        #     del request.session['visit_type']
        #     del request.session['Ref_by']
        # except:
            # print('exception occured while deleting session keys [visit_type, Ref_by]')

        if be.status!='LOCKED':
            bi,created =models.Bill_Item.objects.get_or_create(patient_name=reg.patient_name,bill_entry_ref=be, service_type='CONSULTATION',\
            service_name=doc.doctor_name,
            service_amount=doc.fee,
            service_tax_amount=0,
            visit_type=visit_type,
            Ref_by=Ref_by)
            print('bi={},created={}'.format(bi,created))


            be.billed_datetime=datetime.datetime.now()
            be.billed_amount=doc.fee
            be.billed_by=request.user.username
            be.status='LOCKED'    #####***************LOCKED   bill Entry**** willnot allow to edit bills
            record=be.save(update_fields=['billed_datetime','billed_amount','billed_by','status'])
            print('record update',record)


##
        pdf=render_to_pdf('pdf/reg_bill_receipt.html',my_dict)
        return HttpResponse(pdf, content_type='application/pdf')  # 'generate_rbill/<str:id>'
    except ObjectDoesNotExist:
        print('exception occured in generate_reg_receipt_view while getting obj from  Model redirecting to regSearch')
        return redirect('/regSearch')

def generate_reg_receipt_view1(request,name,id,bill_no): ##
# 'generate_regbill/<str:name>/<int:id>/bill_no'
#  be.status ==LOCKED only allows to take generate bill otherwise
# it is redirect to pay bill form
    my_dict={}
    my_dict={'title':'Registration Bill Cum Receipt'}
    # t_amount=0
    # t_tax_amount=0
    # t_grand_total=0
    # t_count=0

    try:
        reg=models.Registration.objects.get(id=id)
        my_dict['reg']=reg
        doc=models.Fee_chart.objects.get(doctor_name=name)
        my_dict['doc']=doc
        my_dict['bill_no']=bill_no
        my_dict['username']=request.user.username
        my_dict['amountInWord']=num2words(doc.fee,lang ='en_IN')
        be_ref=models.Bill_Entry.objects.get(bill_no=bill_no)
        my_dict1=create_bi_update_be(request,be_ref,reg,doc) ###
        if be_ref.status=='UN_LOCKED':
            print('generate_reg_receipt_view1, pay before generate bill redirecting to payment')
            return redirect ('pay_bill1',id=bill_no)
        my_dict2={**my_dict,**my_dict1}
        my_dict=my_dict2
##
        pdf=render_to_pdf('pdf/reg_bill_receipt.html',my_dict)
        return HttpResponse(pdf, content_type='application/pdf')  # 'generate_rbill/<str:id>'
    except ObjectDoesNotExist:
        print('exception occured in generate_reg_receipt_view while getting obj from  Model redirecting to regSearch')
        return redirect('/regSearch')

def generate_doc_temp_view(request,name,id,bill_no):
    # generate_doctemp/<str:doctor_name>/<int:id>/<int:bill_no>
    my_dict={}
    my_dict={'title':'doc template'}
    try:
        reg=models.Registration.objects.get(id=id)
        my_dict['reg']=reg
        dob_date=reg.dob
        current_date= datetime.date.today()
        datediff=relativedelta(current_date,dob_date)
        age_years=datediff.years
        age_months=datediff.months
        age_days=datediff.days
        my_dict['age_years']=datediff.years
        my_dict['age_months']=datediff.months
        my_dict['age_days']=datediff.days
        my_dict['date']=current_date
        print('age_years:',age_years ,age_months,age_days)

        doc=models.Fee_chart.objects.get(doctor_name=name)
        my_dict['doc']=doc

    except ObjectDoesNotExist:
        print('exception occured in generate_doc_temp_view() while getting obj from registration Model redirecting to regSearch')
        return redirect('/regSearch')


    pdf=render_to_pdf('pdf/doc_form_.html',my_dict)
    return HttpResponse(pdf, content_type='application/pdf')
def sel_doc_form_view(request,id,bill_no):
    # 'sel_doc/<int:id>/'
    my_dict={}

    my_dict['title']='Select Doctor or Service '

    if request.method=='POST':
        form=forms.Doc_fee_form(request.POST)
        if form.is_valid():
            dept=form.cleaned_data['dept']
            visit_type=form.cleaned_data['visit_type']
            Ref_by=form.cleaned_data['Ref_by']
            request.session['visit_type']=visit_type
            request.session['Ref_by']=Ref_by
            results=models.Fee_chart.objects.filter(dept=dept)
            print(',dept , no of entries',dept, len(results))


##############
        # r_doc_list=[]
        # r_id=request.session.get('id',0)
        # r_doc_list=request.session.get('r_doc_list',[])
        # my_dict['r_id']=r_id
        # my_dict['r_doc_list']=r_doc_list
        # print('r_doc_list', r_doc_list)
 ################
        my_dict['form']=form
        my_dict['id']=id
        my_dict['results']=results
        my_dict['bill_no']=bill_no   # passing bill_no for further use
        my_dict['Ref_by']=Ref_by
        return render(request,'testapp1/doc_lab_query_form.html',my_dict)
    else:
        request.session['id']=id  # storing patient name
        print('saving patient id in session',id)
        form=forms.Doc_fee_form()
        my_dict['form']=form
        my_dict['bill_no']=bill_no
        return render(request,'testapp1/doc_lab_query_form.html',my_dict)
def add_to_session(request,id):
    # 'add_to_session/<str:id>/'
    doc_list=request.session.get('r_doc_list',[])
    doc_list.append(id)
    print('doc name', id)
    request.session['r_doc_list']= doc_list
    print('added {} to doc_list'.format(id))


    p_id= request.session['id']
    print('redirecting to sel_doc')
    return redirect('sel_doc', id=p_id)

def add_test_to_session(request,id,bill_no):
    # 'add_test_to_session/<str:id>/'
    lab_test_list=request.session.get('r_lab_test_list',[])
    lab_test_list.append(id)
    print('lab test name', id)
    request.session['r_lab_test_list']= lab_test_list
    print('added {} to r_lab_test_list'.format(id))


    p_id= request.session['id']
    print('redirecting to sel_doc')
    return redirect('sel_lab', id=p_id,bill_no=bill_no)
def del_from_session(request,id):
    # 'del_to_session/<str:id>/'
    print('222222')
    doc_list=request.session.get('r_doc_list',[])
    try:
        print('id in del_from_session',id)
        ret=doc_list.remove(id)
        print('ret:',ret)
    except:
        print('exception occured in deleting doctor from list')
        pass
    print('doc name', id ,doc_list)
    request.session['r_doc_list']= doc_list
    print('deleted {} to doc_list'.format(id))
    print(doc_list)


    p_id= request.session['id']
    print('redirecting to sel_doc')
    return redirect('sel_doc', id=p_id)

def del_test_from_session(request,id,bill_no):
    # 'del_to_session/<str:id>/'
    print('33333')
    lab_test_list=request.session.get('r_lab_test_list',[])
    try:
        print('id in del_from_session',id)
        ret=lab_test_list.remove(id)
        print('ret:',ret)
    except:
        print('exception occured in deleting doctor from lab_test_list')
        pass
    print('doc name', id ,lab_test_list)
    request.session['r_lab_test_list']= lab_test_list
    print('deleted {} to lab_test_list'.format(id))
    print(lab_test_list)


    p_id= request.session['id']
    print('redirecting to sel_lab')
    return redirect('sel_lab', id=p_id,bill_no=bill_no)
def sel_lab_form_view(request,id,bill_no):
    # 'sel_lab/<int:id>/<int:bill_no>'
    my_dict={}

    my_dict['title']='Select Lab Service '

    if request.method=='POST':
        reg=models.Registration.objects.get(id=id)
        form=forms.Lab_test_query_form(request.POST)
        if form.is_valid():
            test_name=form.cleaned_data['test_name']
            Ref_by=form.cleaned_data['Ref_by']
            visit_type=form.cleaned_data['visit_type']
            item=models.Lab_chart.objects.get(Service_Name__iexact=test_name)
            # item=models.Lab_chart.objects.get(Service_Name=test_name)
            print(',test_name ',test_name)
####   create bill item as we query

            # get Bill Entry using bill_no
            be=models.Bill_Entry.objects.get(bill_no=bill_no)
            print('sel_lab: reg={}, be={}'.format(reg,be))

            my_dict['visit_type']=visit_type
            my_dict['Ref_by']=Ref_by


            #### create Bill Item
            if be.status!='LOCKED' :  #if status is LOCKED it will not allow to add new bill items
                bi,created =models.Bill_Item.objects.get_or_create(patient_name=reg.patient_name,bill_entry_ref=be, service_type='LAB_TESTS',\
                service_name=item.Service_Name,
                service_amount=item.charge,
                service_tax_amount=item.perc15,
                visit_type=visit_type,
                Ref_by=Ref_by)
                print('sel_lab: bi={},created={}'.format(bi,created))

            my_dict['Created_Dt']=be.billed_datetime
            my_dict['Print_Dt']=datetime.datetime.now()
####datetime.
        bireports= models.Bill_Item.objects.all().filter(bill_entry_ref__bill_no=be.bill_no)   # print('item',item)
        r_id=request.session.get('id',0)

        my_dict['r_id']=r_id

 ################
        my_dict['form']=form
        my_dict['id']=id
        my_dict['bireports']=bireports
        my_dict['bill_no']=bill_no
        print('bin post: sel_lab_form_view')
        return render(request,'testapp1/lab_test_query_form.html',my_dict)
    else: #GET
        request.session['id']=id  # storing patient
        print('saving patient id in session',id)
        # earlier retrive earlier stored list from add_to_session
        # r_lab_test_list=request.session.get('r_lab_test_list',[])
        my_dict['r_id']=id  # check we can remove if it is not used
        my_dict['id']=id
        my_dict['bill_no']=bill_no



        #############
        form=forms.Lab_test_query_form()
        my_dict['form']=form
        return render(request,'testapp1/lab_test_query_form.html',my_dict)

def generate_lab_bill_view(request,id,bill_no):
# 'generate_lab_bill/<str:name>/<int:id>'  ## not complete yet
    my_dict={}
    my_dict={'title':'Lab Bill Receipt'}

    l=[]
    t_amount=0
    t_tax_amount=0
    t_grand_total=0
    t_count=0

    try:
        reg=models.Registration.objects.get(id=id)
        my_dict['reg']=reg
        ########## from list  get test name
        r_id=request.session.get('id',0)
        # r_lab_test_list=request.session.get('r_lab_test_list',[])
        my_dict['r_id']=r_id

        be=models.Bill_Entry.objects.get(bill_no=bill_no)
        # print('generate_lab_bill: reg={}, be={}'.format(reg,be))
        visit_type=request.session.get('visit_type','WALK_IN')
        Ref_by=request.session.get('Ref_by','None')
        my_dict['visit_type']=visit_type
        my_dict['Ref_by']=Ref_by
        my_dict['Created_Dt']=be.billed_datetime
        my_dict['Print_Dt']=datetime.datetime.now()


        #get all Bill Items and pass to template
        results= models.Bill_Item.objects.all().filter(bill_entry_ref__bill_no=be.bill_no)   # print('item',item)
        for r in results:
            t_amount=t_amount+r.service_amount
            t_tax_amount=t_tax_amount+r.service_tax_amount
        t_grand_total=t_tax_amount+t_amount

        print('bireports',results)

        ### update Bill entry and status to LOCKED
        if be.status!="LOCKED":
            be.billed_datetime=datetime.datetime.now()
            be.billed_amount=t_grand_total
            be.billed_by=request.user.username
            be.status='LOCKED'    #####***************LOCKED   bill Entry**** willnot allow to edit bills
            record=be.save(update_fields=['billed_datetime','billed_amount','billed_by','status'])
            print('record update',record)
        else:
            print('Bill Entry status is LOCKED, you cannot add any bill items')

        my_dict['date_']=datetime.datetime.now()
        my_dict['username']=request.user.username
        my_dict['t_grand_total']=t_grand_total
        my_dict['amountInWord']=num2words(t_grand_total,lang ='en_IN')
        my_dict['bireports']=results
        my_dict['bill_no']=bill_no

        print("22222 before rendering to pdf")
        pdf=render_to_pdf('pdf/lab_bill_receipt.html',my_dict)
        return HttpResponse(pdf, content_type='application/pdf')  # 'generate_rbill/<str:id>'
    except ObjectDoesNotExist as e:
        print('exception occured in generate_reg_receipt_view while getting obj from  Model redirecting to regSearch')
        print(e)
        return redirect('/regSearch')

def generate_lab_bill_view1(request,id,bill_no):
# 'generate_lab_bill/<str:name>/<int:id>'  ## not complete yet
    my_dict={}
    my_dict={'title':'Lab Bill Receipt'}

    l=[]
    t_amount=0
    t_tax_amount=0
    t_grand_total=0
    t_count=0

    try:
        reg=models.Registration.objects.get(id=id)
        my_dict['reg']=reg
        ########## from list  get test name
        r_id=request.session.get('id',0)
        # r_lab_test_list=request.session.get('r_lab_test_list',[])
        my_dict['r_id']=r_id

        be=models.Bill_Entry.objects.get(bill_no=bill_no)
        # print('generate_lab_bill: reg={}, be={}'.format(reg,be))
        visit_type=request.session.get('visit_type','WALK_IN')
        Ref_by=request.session.get('Ref_by','None')
        my_dict['visit_type']=visit_type
        my_dict['Ref_by']=Ref_by
        my_dict['Created_Dt']=be.billed_datetime
        my_dict['Print_Dt']=datetime.datetime.now()



        #get all Bill Items and pass to template
        results= models.Bill_Item.objects.all().filter(bill_entry_ref__bill_no=be.bill_no)   # print('item',item)
        for r in results:
            t_amount=t_amount+r.service_amount
            t_tax_amount=t_tax_amount+r.service_tax_amount
        t_grand_total=t_tax_amount+t_amount

        print('bireports',results)

        ### update Bill entry and status to LOCKED
        if be.status!="LOCKED":
            be.billed_datetime=datetime.datetime.now()
            be.billed_amount=t_grand_total
            be.billed_by=request.user.username
            # be.status='LOCKED'    #####***************LOCKED   bill Entry**** willnot allow to edit bills
            record=be.save(update_fields=['billed_datetime','billed_amount','billed_by','status'])
            print('record update',record)

            print('generate_lab_bill_view1, pay before generate bill redirecting to payment')
            return redirect ('pay_bill1',id=bill_no)

        else:
            print('Bill Entry status is LOCKED, you cannot add any bill items')

        my_dict['date_']=datetime.datetime.now()
        my_dict['username']=request.user.username
        my_dict['t_grand_total']=t_grand_total
        my_dict['amountInWord']=num2words(t_grand_total,lang ='en_IN')
        my_dict['bireports']=results
        my_dict['bill_no']=bill_no
        my_dict['mode_of_payment']=be.mode_of_payment

        pdf=render_to_pdf('pdf/lab_bill_receipt.html',my_dict)
        return HttpResponse(pdf, content_type='application/pdf')  # 'generate_rbill/<str:id>'
    except ObjectDoesNotExist as e:
        print('exception occured in generate_reg_receipt_view while getting obj from  Model redirecting to regSearch')
        print(e)
        return redirect('/regSearch')

def create_Bill_Register_view(request,id):
# addSE/', 1)creates Bill Register entry
    my_dict={}
    se_bill_no_ref={}
    my_dict['title']='Create_Bill_Register'
    if request.method=='POST':
        form=forms.Bill_Entry_form(request.POST)
        print('create Bill_Register',form.is_valid())
        if form.is_valid():
            bill_no=form.cleaned_data['bill_no']
            result=form.save()
            print('result.bill_no', result.bill_no,result.patient_name)
            reg_entry_ref=models.Registration.objects.get(id=id)

            print('patient_name:', reg_entry_ref.patient_name)
            print("create bill result",result)
            # models.Bill_Register.objects.create()
            be=models.Bill_Entry.objects.get(bill_no=bill_no)
            be.reg_entry_ref=reg_entry_ref
            be.patient_name=reg_entry_ref.patient_name
            record=be.save(update_fields=['reg_entry_ref','patient_name'])
            print('be update record:',record,be.reg_entry_ref )
            my_dict['areport']=be
            my_dict['id']=id
            return render(request,'testapp1/bill_register_results.html',my_dict)
        return render(request,'testapp1/bill_register_results.html',my_dict)
    else: #GET
        print('222222  in get create br')
        try:
            br=models.Bill_Entry.objects.last()
            if br==None:
                bill_no=0
            else:
                bill_no=br.bill_no
        except ObjectDoesNotExist:
            bill_no=0

        bill_no=bill_no+1
        initial_se={'bill_no':bill_no,}
        print('bill_no',bill_no)
        form=forms.Bill_Entry_form(initial=initial_se)
        my_dict['form']= form
        return render(request,'testapp1/bill_register_results.html',my_dict)

def del_bill_item(request,id,bill_no):
# third bill_no
    try:
        print('id in del_bill_item',id)
        be=models.Bill_Entry.objects.get(bill_no=bill_no)
        if be.status=='LOCKED':
            print('Bill Entry status is LOCKED so bill item will be not deleted')
            return redirect('sel_lab', id=id, bill_no=bill_no)
        ret=models.Bill_Item.objects.remove(id)
        print('ret:',ret)
    except:
        print('exception occured in deleting doctor from list')
        pass

    print('redirecting to sel_doc')
    return redirect('sel_lab', id=id, bill_no=bill_no)

## receiption balance sheet (current day)
def receiption_balance_report(request):
    my_dict={}
    t_be_grand_total=0


    my_dict['title']='Receiption balance_sheet_report'.upper()
    print('receiption_balance_report')
    current_date=datetime.date.today()


    be_rows=models.Bill_Entry.objects.filter(billed_datetime__year=current_date.year,billed_datetime__month=current_date.month,billed_datetime__day=current_date.day ). \
        values('bill_no', 'billed_amount','admission_type','billed_datetime') # filtering on date
    print(be_rows)

    for be in be_rows:
        t_be_grand_total=t_be_grand_total+be['billed_amount']

    my_dict['t_be_grand_total']= t_be_grand_total
    my_dict['be_reports']=be_rows

    return render(request,'testapp1/receiption_bal_report.html',my_dict)

def pay_retail_bill_view(request,id):
    # id  = bill_no  amount=fee
    my_dict={}
    message=''
    my_dict['title']='submit_pay_bill'
    print('id in  pay_bill',id)
    be=models.Bill_Entry.objects.get(bill_no=id)
    # if be.status=='LOCKED':   # need to correct
    #     print(' Bill Entry status is already blocked, you cannot pay again')
    #     return redirect('/be_list')

    my_dict['billed_amount']= be.billed_amount

    if request.method=='POST':
        form=forms1.payment_form(request.POST)
        print('is valid',form.is_valid())
        if form.is_valid():

            billed_amount= float(be.billed_amount) #be.billed_amount
            mode_of_payment=form.cleaned_data['mode_of_payment']
            tx_id_reference=form.cleaned_data['tx_id_reference']
            paid_by_cash=form.cleaned_data['paid_by_cash']
            paid_by_card=form.cleaned_data['paid_by_card']
            card_issued_bank=form.cleaned_data['card_issued_bank']
            #logic
            tot_bill_payment=round(Decimal(paid_by_cash)+Decimal(paid_by_card),2)
            balance=Decimal(billed_amount)-Decimal(tot_bill_payment)
            print('billed_amount {},mode_of_payment {}'.format(billed_amount,mode_of_payment))
            print('tx_id_reference {} paid_by_cash{} paid_by_card{}'.format(tx_id_reference, paid_by_cash, paid_by_card))
            print('tot_bill_payment {} balance{}'.format(tot_bill_payment,balance))

            if mode_of_payment=="CARD":

                initial_ie={'paid_by_card':be.paid_by_card,'paid_by_cash':0.0}
                if paid_by_card >billed_amount :
                    my_dict['msg']='entered card amount is more than billed amount , enter correct value'
                    form=forms1.payment_form(initial=initial_ie)
                    my_dict['form']= form
                    return render(request,'testapp1/pay_rbill_form.html',my_dict)
                elif paid_by_card < billed_amount:
                    my_dict['msg']='entered card amount is less than billed amount , enter correct value'
                    form=forms1.payment_form(initial=initial_ie)
                    my_dict['form']= form
                    return render(request,'testapp1/pay_rbill_form.html',my_dict)
                elif tx_id_reference=='empt':
                    my_dict['msg']='entered traction id is empt please fill correct value'
                    form=forms1.payment_form(initial=initial_ie)
                    my_dict['form']= form
                    return render(request,'testapp1/pay_rbill_form.html',my_dict)

                elif card_issued_bank=='empty' :
                    my_dict['msg']='entered card_issued_bank  is empty please fill correct value'
                    form=forms1.payment_form(initial=initial_ie)
                    my_dict['form']= form
                    print('hi 111110 payment')
                    return render(request,'testapp1/pay_rbill_form.html',my_dict)
                elif billed_amount ==tot_bill_payment: #success case
                    return_cash=Decimal(paid_by_card)-Decimal(billed_amount)
                    x=models.Bill_Entry.objects.filter(bill_no=id).update( \
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
                if  paid_by_cash>= billed_amount :
                    message='return change ={}'.format(balance)
                    return_cash=Decimal(paid_by_cash)-Decimal(billed_amount)


                if billed_amount <=tot_bill_payment: #success case
                    x=models.Bill_Entry.objects.filter(bill_no=id).update( \
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
                    form=forms1.payment_form(initial=initial_ie)
                    my_dict['form']= form
                    return render(request,'testapp1/pay_rbill_form.html',my_dict)

                elif card_issued_bank=='empty' :
                    my_dict['msg']='entered card_issued_bank  is empty please fill correct value'
                    form=forms1.payment_form(initial=initial_ie)
                    my_dict['form']= form
                    print('hi 111110 payment')
                    return render(request,'testapp1/pay_rbill_form.html',my_dict)

                elif paid_by_card >billed_amount :  # not allowing to bill on card more than billed_amount
                    my_dict['msg']='entered card amount is more than billed amount , enter correct value'
                    form=forms1.payment_form(initial=initial_ie)
                    my_dict['form']= form
                    return render(request,'testapp1/pay_rbill_form.html',my_dict)
                elif billed_amount <=tot_bill_payment:  #success case
                    return_cash=Decimal(tot_bill_payment)-Decimal(billed_amount)
                    x=models.Bill_Entry.objects.filter(bill_no=id).update( \
                    mode_of_payment=mode_of_payment,
                    tx_id_reference=tx_id_reference,
                    card_issued_bank=card_issued_bank,
                    paid_by_cash=Decimal(billed_amount)-Decimal(paid_by_card),
                    paid_by_card=paid_by_card,
                    return_cash=return_cash,
                    status='LOCKED'
                    )
            print('this bf be.status LOCK check ,', be.status)
            be=models.Bill_Entry.objects.get(bill_no=id) # to get latest status
            if be.status=='LOCKED':  #lock all OIE entries ( it does not allow to delete or update)
                bies=models.Bill_Item.objects.all().filter(bill_entry_ref__bill_no=id)
                for bie in bies:
                    bie.status='LOCKED'
                    bie.save()
                    print('pay_retail_bill_view...  bie status is LOCKED',bie)
        # return redirect('bie_list_based_on_id',id=id)
        # return render(request,'testapp1/pay_rbill_form.html',my_dict)
        return redirect('/be_list')
    else:   #GET
        bi_count, be =cal_upd_BE(request,id) #redirect to be_list
        print('bi_count',bi_count)
        if bi_count==0:
            msg='For bill_no={} no items are added , please first add items and pay'.format(id)

            if be.status=='LOCKED':
                msg+='\n, unlocking entry '
                be.status='UN_LOCKED'
                be.save(update_fields=['status',])
            my_dict['msg']=msg
            return render(request,'testapp1/pay_rbill_form.html',my_dict)

        #
        if be.status !='LOCKED':  #UNLOCKED
            initial_ie={'paid_by_cash': be.billed_amount}
            form=forms1.payment_form()
            my_dict['form']= form
            my_dict['bill_amount']= be.billed_amount
        else:
            if be.billed_amount!=0:
                msg='already paid , you cannot initiate again payment method'
                print(msg)
                my_dict['msg']=msg
        return render(request,'testapp1/pay_rbill_form.html',my_dict)
    #
def pay_retail_bill_view1(request,id):  # may not use
    # id  = bill_no
    my_dict={}
    message=''
    my_dict['title']='submit_pay_bill'
    print('id in  pay_bill',id)


    return payment_form_process(request,id)


def list_be(request):
# addSE/', 1)list all sell entry 2) shows relavent item entries
    my_dict={}
    se_bill_no_ref={}
    my_dict['title']='Bill_Entry_list'
    try:
        areports=models.Bill_Entry.objects.all()
        my_dict['areports']=areports

    except ObjectDoesNotExist:
        message='ObjectDoesNotExist exeception occured create_sell '

    return render(request,'testapp1/be_results.html',my_dict)

def bi_list(request, id):
# bi_list/id', 1)list all sell entry based on bill_no 2) shows relavent bill item entries
    my_dict={}
    se_bill_no_ref={}
    my_dict['title']='Bill_Item List'
    try:
        areports=models.Bill_Item.objects.filter(bill_entry_ref__bill_no=id)
        my_dict['areports']=areports
        be=models.Bill_Entry.objects.get(bill_no=id)
        my_dict['be']=be
    except ObjectDoesNotExist:
        message='ObjectDoesNotExist exeception occured create_sell '

    return render(request,'testapp1/bill_item_results.html',my_dict)

def add_bi_view(request, bill_no):
# bi_add/bill_no', 1)list all sell entry based on bill_no 2) shows relavent bill item entries
    my_dict={}
    se_bill_no_ref={}
    my_dict['title']='add Bill_Item '
    try:
        be=models.Bill_Entry.objects.get(bill_no=bill_no)
        my_dict['areport']=be
        id=be.reg_entry_ref.id
        print('id',id)
        my_dict['id']=id
    except ObjectDoesNotExist:
        message='ObjectDoesNotExist exeception occured create_sell '

    return render(request,'testapp1/bill_register_results.html',my_dict)

def generate_doc_lab_receipt_view(request,bill_no):
# generate_receipt/<int:bill_no>
# it will list bill_item  based on bill_no  calls  generate_regbill/<int:id>/bill_no' or generate_lab_bill/<int:id>/<int:bill_no>
# 'generate_regbill/<int:id>/bill_no'
    my_dict={}
    my_dict={'title':'Registration'}

    be=models.Bill_Entry.objects.get(bill_no=bill_no)

    print('be',be.reg_entry_ref.id)
    id=be.reg_entry_ref.id
    bies=models.Bill_Item.objects.filter(bill_entry_ref__bill_no=bill_no)
    print('xxxxxx1111', bies, len(bies))
    if len(bies):
        print('bill items ')
        if len(bies)==1:
            if bies[0].service_type =='CONSULTATION':
                print('CONSULTATION')
                name=bies[0].service_name
                return generate_reg_receipt_view(request,name,id,bill_no)
            elif bies[0].service_type =='LAB_TESTS':
                print('LAB TESTs')
                return generate_lab_bill_view(request,id,bill_no)
        else:
            if bies[0].service_type =='LAB_TESTS':
                print('LAB TESTs')
                return generate_lab_bill_view(request,id,bill_no)
    else:
        # return generate_lab_bill_view(request,id,bill_no)
        print('type , len()', type(bies), len(bies))
    return redirect('/be_list')
    #
    #
def generate_doc_lab_receipt_view1(request,bill_no):
# generate_receipt/<int:bill_no>
# it will list bill_item  based on bill_no  calls  generate_regbill/<int:id>/bill_no' or generate_lab_bill/<int:id>/<int:bill_no>
# 'generate_regbill/<int:id>/bill_no'
    my_dict={}
    my_dict={'title':'Registration'}

    be=models.Bill_Entry.objects.get(bill_no=bill_no)
    if be.status=='UN_LOCKED':  #only LOCKED status we generate recipt
        print('be.status in unlocked so redirecting paybill form')
        return redirect('pay_bill1',id=bill_no)

    print('be',be.reg_entry_ref.id)
    id=be.reg_entry_ref.id
    bies=models.Bill_Item.objects.filter(bill_entry_ref__bill_no=bill_no)
    print('xxxxxx1111', bies, len(bies))
    if len(bies):
        print('bill items ')
        if len(bies)==1:
            if bies[0].service_type =='CONSULTATION':
                print('CONSULTATION')
                name=bies[0].service_name
                return generate_reg_receipt_view(request,name,id,bill_no)
            elif bies[0].service_type =='LAB_TESTS':
                print('LAB TESTs')
                return generate_lab_bill_view(request,id,bill_no)
        else:
            if bies[0].service_type =='LAB_TESTS':
                print('LAB TESTs')
                return generate_lab_bill_view(request,id,bill_no)
    else:
        # return generate_lab_bill_view(request,id,bill_no)
        print('type , len()', type(bies), len(bies))
    return redirect('/be_list')

def list_Fee_chart_view(request):
    my_dict={}
    se_bill_no_ref={}
    my_dict['title']='List_Fee_chart'
    try:
        fee_reports=models.Fee_chart.objects.all()
        my_dict['fee_reports']=fee_reports

    except ObjectDoesNotExist:
        message='ObjectDoesNotExist exeception occured create_sell '
    return render(request,'testapp1/file_upload_form.html',my_dict)

def list_Lab_chart_view(request):
    my_dict={}
    se_bill_no_ref={}
    my_dict['title']='List_Lab_chart'
    try:
        lab_reports=models.Lab_chart.objects.all()
        my_dict['lab_reports']=lab_reports

    except ObjectDoesNotExist:
        message='ObjectDoesNotExist exeception occured create_sell '
    return render(request,'testapp1/file_upload_form.html',my_dict)

def Appointment_form_view(request,id):
    # 'appt_m/<int:id>'

    my_dict={}
    my_dict['title']='make appointment'
    print('opid', id)

    if request.method=='POST':
        form=forms.Appointment_form(request.POST)
        print('create item',form.is_valid())
        if form.is_valid():
            # patient_name=form.cleaned_data['patient_name']
            OPID=form.cleaned_data['OPID']
            appt_type=form.cleaned_data['appt_type']
            appt_purpose=form.cleaned_data['appt_purpose']
            appt_date=form.cleaned_data['appt_date']
            print('11111',appt_date)
            # appt_time=form['appt_time']
            Ref_by=form.cleaned_data['Ref_by']

            reg_entry_ref1=models.Registration.objects.get(OPID=id)
            OPID=reg_entry_ref1.OPID
            patient_name=reg_entry_ref1.patient_name
            phone=reg_entry_ref1.phone
            print('reg_entry_ref1',reg_entry_ref1)
            d_time=datetime.datetime.now()
            # appt_time = d_time.strftime("%H:%M:%S")

            initial_={
            'patient_name':patient_name,
            'OPID':OPID,
            'reg_entry_ref1':reg_entry_ref1,
            'appt_type':appt_type,
            'appt_purpose':appt_purpose,
            'appt_date':appt_date,
            # 'appt_time':appt_time,
            'Ref_by':Ref_by,
            'phone':phone,
            #'status':
            }
            record=models.Appointment_Item.objects.create(**initial_)
            message='{} appointment is scheduled successfully, {}'.format(patient_name, record)

        else:
            message='appointment not scheduled'
            print( form.errors)
        my_dict['message']=message
        return render(request,'testapp1/Appt_item_results.html',my_dict)
    else: #GET
        init_appt={'OPID':id}
        form=forms.Appointment_form(initial=init_appt)
        my_dict['form']=form
        return render(request,'testapp1/reg_form.html',my_dict)

def Appointment_query_form_view(request):
    # 'list_appt/'

    my_dict={}
    my_dict['title']='List Appointments'

    if request.method=='POST':
        form=forms.List_Appointment_form(request.POST)
        print('is form valid:',form.is_valid())
        if form.is_valid():
            report_choice_field=form.cleaned_data['report_choice_field']

            current_date=datetime.date.today()
            if report_choice_field=='Today':
                areports=models.Appointment_Item.objects.filter(appt_date =current_date)
            elif report_choice_field=='Tomorrow':
                tomorrow_date=current_date+ relativedelta(days=1)
                areports=models.Appointment_Item.objects.filter(appt_date =tomorrow_date)
            elif report_choice_field=='AllNextAppointments':
                areports=models.Appointment_Item.objects.filter(appt_date__gt= current_date)
            my_dict['areports']=areports
        else:
            message='Appointment_query_form_view: form not valid'
            print( form.errors)
            my_dict['message']=message
        return render(request,'testapp1/Appt_item_results.html',my_dict)
    else: #GET
        form=forms.List_Appointment_form()
        my_dict['form']=form
        return render(request,'testapp1/reg_form.html',my_dict)

def Appointment_report(opt):
     # this function call from testapp login time
    report_choice_field=opt
    areports=None
    message='nothing'
    current_date=datetime.date.today()
    if report_choice_field=='Today':
        areports=models.Appointment_Item.objects.filter(appt_date =current_date)
    elif report_choice_field=='Tomorrow':
        tomorrow_date=current_date+ relativedelta(days=1)
        areports=models.Appointment_Item.objects.filter(appt_date =tomorrow_date)
    elif report_choice_field=='AllNextAppointments':
        areports=models.Appointment_Item.objects.filter(appt_date__gt= current_date)
    else:
        message='Appointment option is not valid'

    # my_dict['message']=message
    return areports , message


class appt_data_json_view4(View):
    # appt_japi4/<str:opt>/
    def get(self, request,opt):
        print('opt',opt)
        current_date=datetime.date.today()
        if opt=='Today':
            p_data=models.Appointment_Item.objects.filter(appt_date =current_date)

            # q=[]
            # for a_ele  in p_data:
            #     a_qs=models.Appointment_Item.objects.get(id=a_ele.id)
            #     r_qs=models.Registration.objects.get(OPID=a_ele.OPID)
            #     qs=list(chain(a_qs, r_qs))
            #     q.append(qs)
            #
            #
            # print('q:',q )

        elif opt=='Tomorrow':
            tomorrow_date=current_date+ relativedelta(days=1)
            p_data=models.Appointment_Item.objects.filter(appt_date =tomorrow_date)
        elif opt=='AllNextAppointments':
            # p_data=models.Appointment_Item.objects.filter(appt_date__gt= current_date).values('patient_name','OPID','appt_type','appt_date','reg_entry_ref1__phone')
            p_data=models.Appointment_Item.objects.filter(appt_date__gt= current_date)
            print('p_data:',p_data)
        json_data=serializers.serialize('json',p_data)
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
def cal_upd_BE(request,id):
#id - bill_no   <input>
#len  return  0-  no items, +ve some items
# calculate bill amount and update Bill Entry
    print('cal_upd_BE: id ',id)
    my_dict={}
    t_amount=0
    t_tax_amount=0
    t_grand_total=0
    # t_Qty_sold=0
    t_count=0
    try:
        be=models.Bill_Entry.objects.get(bill_no=id)

    except ObjectDoesNotExist:
        print('exception ObjectDoesNotExist in generate_ bill/<str:id>/ create_sbill_id')
        # redirect('/q_item1')

    bis=models.Bill_Item.objects.filter(bill_entry_ref__bill_no=int(id))
    print('bis  bill {} , count:{}'.format( bis, len(bis)) )
    print('bf len(bis)')
    # if len(bis)==0:
    #     print('af len(bis)')
    #     msg='For bill_no={} no items are added , please first add items and pay'.format(id)
    #     my_dict['msg']=msg
    #     # return render(request,'testapp/pay_rbill_form.html',my_dict)
    #     return redirect('/be_list')
    for bi in bis:

        t_amount=t_amount+bi.service_amount
        t_tax_amount=t_tax_amount+bi.service_tax_amount
        t_grand_total=t_grand_total+bi.service_tax_amount+bi.service_amount

        t_count=t_count+1

    print('t_count:', t_count)
    print('t_tax_amount:', t_tax_amount)

    print('t_amount:', t_amount)
    print('bis:', bis)

    if be.status!='LOCKED':
        be.billed_amount=t_grand_total
        # se.tax_amount=t_tax_amount
        # se.grand_total=t_grand_total
        be.billed_datetime= datetime.datetime.now()
        # be.status='LOCKED'
        record=be.save(update_fields=['billed_amount','billed_datetime','status'])
        print('be update record:',record,be.billed_datetime )
    return t_count, be


def  payment_form_process(request,id):
    my_dict={}
    my_dict['title']='bill_payment'
    be=models.Bill_Entry.objects.get(bill_no=id)
    if request.method=='POST':
        form=forms1.payment_form(request.POST)
        print('is valid',form.is_valid())
        if form.is_valid():

            billed_amount= float(be.billed_amount) #be.billed_amount
            my_dict['billed_amount']= be.billed_amount
            mode_of_payment=form.cleaned_data['mode_of_payment']
            tx_id_reference=form.cleaned_data['tx_id_reference']
            paid_by_cash=form.cleaned_data['paid_by_cash']
            paid_by_card=form.cleaned_data['paid_by_card']
            card_issued_bank=form.cleaned_data['card_issued_bank']
            #logic
            tot_bill_payment=round(Decimal(paid_by_cash)+Decimal(paid_by_card),2)
            balance=Decimal(billed_amount)-Decimal(tot_bill_payment)
            print('billed_amount {},mode_of_payment {}'.format(billed_amount,mode_of_payment))
            print('tx_id_reference {} paid_by_cash{} paid_by_card{}'.format(tx_id_reference, paid_by_cash, paid_by_card))
            print('tot_bill_payment {} balance{}'.format(tot_bill_payment,balance))

            if mode_of_payment=="CARD":

                initial_ie={'paid_by_card':be.paid_by_card,'paid_by_cash':0.0}
                if paid_by_card >billed_amount :
                    my_dict['msg']='entered card amount is more than billed amount , enter correct value'
                    form=forms1.payment_form(initial=initial_ie)
                    my_dict['form']= form
                    return render(request,'testapp1/pay_rbill_form.html',my_dict)
                elif paid_by_card < billed_amount:
                    my_dict['msg']='entered card amount is less than billed amount , enter correct value'
                    form=forms1.payment_form(initial=initial_ie)
                    my_dict['form']= form
                    return render(request,'testapp1/pay_rbill_form.html',my_dict)
                elif tx_id_reference=='empt':
                    my_dict['msg']='entered traction id is empt please fill correct value'
                    form=forms1.payment_form(initial=initial_ie)
                    my_dict['form']= form
                    return render(request,'testapp1/pay_rbill_form.html',my_dict)

                elif card_issued_bank=='empty' :
                    my_dict['msg']='entered card_issued_bank  is empty please fill correct value'
                    form=forms1.payment_form(initial=initial_ie)
                    my_dict['form']= form
                    print('hi 111110 payment')
                    return render(request,'testapp1/pay_rbill_form.html',my_dict)
                elif billed_amount ==tot_bill_payment: #success case
                    return_cash=Decimal(paid_by_card)-Decimal(billed_amount)
                    x=models.Bill_Entry.objects.filter(bill_no=id).update( \
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
                if  paid_by_cash>= billed_amount :
                    message='return change ={}'.format(balance)
                    return_cash=Decimal(paid_by_cash)-Decimal(billed_amount)


                if  paid_by_cash< billed_amount :
                    print('entered amount is less than billed amount please enter equal or more')


                if billed_amount <=tot_bill_payment: #success case
                    x=models.Bill_Entry.objects.filter(bill_no=id).update( \
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
                    form=forms1.payment_form(initial=initial_ie)
                    my_dict['form']= form
                    return render(request,'testapp1/pay_rbill_form.html',my_dict)

                elif card_issued_bank=='empty' :
                    my_dict['msg']='entered card_issued_bank  is empty please fill correct value'
                    form=forms1.payment_form(initial=initial_ie)
                    my_dict['form']= form
                    print('hi 111110 payment')
                    return render(request,'testapp1/pay_rbill_form.html',my_dict)

                elif paid_by_card >billed_amount :  # not allowing to bill on card more than billed_amount
                    my_dict['msg']='entered card amount is more than billed amount , enter correct value'
                    form=forms1.payment_form(initial=initial_ie)
                    my_dict['form']= form
                    return render(request,'testapp1/pay_rbill_form.html',my_dict)
                elif billed_amount <=tot_bill_payment:  #success case
                    return_cash=Decimal(tot_bill_payment)-Decimal(billed_amount)
                    x=models.Bill_Entry.objects.filter(bill_no=id).update( \
                    mode_of_payment=mode_of_payment,
                    tx_id_reference=tx_id_reference,
                    card_issued_bank=card_issued_bank,
                    paid_by_cash=Decimal(billed_amount)-Decimal(paid_by_card),
                    paid_by_card=paid_by_card,
                    return_cash=return_cash,
                    status='LOCKED'
                    )
            print('this bf be.status LOCK check ,', be.status)
            be=models.Bill_Entry.objects.get(bill_no=id) # to get latest status
            if be.status=='LOCKED':  #lock all OIE entries ( it does not allow to delete or update)
                bies=models.Bill_Item.objects.all().filter(bill_entry_ref__bill_no=id)
                for bie in bies:
                    bie.status='LOCKED'
                    bie.save()
                    print('pay_retail_bill_view...  bie status is LOCKED',bie)

        return redirect('bi_list',id=id)
    else:   #GET
        bi_count, be =cal_upd_BE(request,id) #redirect to be_list
        print('bi_count',bi_count)
        if bi_count==0:
            msg='For bill_no={} no items are added , please first add items and pay'.format(id)

            if be.status=='LOCKED':
                msg+='\n, unlocking entry '
                be.status='UN_LOCKED'
                be.save(update_fields=['status',])
            my_dict['msg']=msg
            return render(request,'testapp1/pay_rbill_form.html',my_dict)

        #
        if be.status !='LOCKED':  #UNLOCKED
            initial_ie={'paid_by_cash': be.billed_amount}
            form=forms1.payment_form()
            my_dict['form']= form
            my_dict['bill_amount']= be.billed_amount
        else:
            if be.billed_amount!=0:
                msg='already paid , you cannot initiate again payment method'
                print(msg)
                my_dict['msg']=msg
        return render(request,'testapp1/pay_rbill_form.html',my_dict)

def create_bi_update_be(request, be,reg,doc):
    #creates bi , updates be
    my_dict={}
    ###    get Bill_Entry
    # be=models.Bill_Entry.objects.get(bill_no=bill_no)

    my_dict['date_']=be.billed_datetime

    ## create bill_item
    visit_type=request.session.get('visit_type','WALK_IN')
    Ref_by=request.session.get('Ref_by','None')
    my_dict['visit_type']=visit_type
    my_dict['Ref_by']=Ref_by
    my_dict['Created_Dt']=be.billed_datetime
    my_dict['Print_Dt']=datetime.datetime.now()



    if be.status!='LOCKED':
        bi,created =models.Bill_Item.objects.get_or_create(patient_name=reg.patient_name,bill_entry_ref=be, service_type='CONSULTATION',\
        service_name=doc.doctor_name,
        service_amount=doc.fee,
        service_tax_amount=0,
        visit_type=visit_type,
        Ref_by=Ref_by)
        print('bi={},created={}'.format(bi,created))


        be.billed_datetime=datetime.datetime.now()
        be.billed_amount=doc.fee
        be.billed_by=request.user.username
        # be.status='LOCKED'    #####***************LOCKED   bill Entry**** willnot allow to edit bills
        record=be.save(update_fields=['billed_datetime','billed_amount','billed_by','status'])
        print('record update',record)
    return my_dict

def bill_history_view(request, opid):
# /bill_hist/{{result.OPID} shows bills for current month & year
    my_dict={}
    my_dict['title']='Patient_Bill_Current_Month_History'

    current_date=datetime.date.today()
    bes=models.Bill_Entry.objects.all().filter(reg_entry_ref__OPID=opid, billed_datetime__year= current_date.year,billed_datetime__month= current_date.month)

    apts=models.Appointment_Item.objects.all().filter(OPID=opid,appt_date__year= current_date.year,appt_date__month= current_date.month)
    my_dict['areports']=bes
    my_dict['apts']=apts

    return render(request,'testapp1/patient_bill_history.html',my_dict)
