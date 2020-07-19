from django.shortcuts import render
from django.shortcuts import redirect
from testapp.models import *
from testapp import forms
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
import datetime



# Create your views here.
def home_view(request):
    return render(request, 'testapp/home.html')
def contact_view(request):
    return render(request, 'testapp/contact.html')
def student_info_view(request):
    students=Student.objects.all()
    return render(request,'testapp/results.html',{'students':students})
def enquiry_info_view(request):
    form=forms.enquiry_form()
    if request.method=='POST':
        form=forms.enquiry_form(request.POST)
        if form.is_valid():
            print('submitted form is valid priting info')
            fname=form.cleaned_data['name']
            fphone=form.cleaned_data['phone']
            femail=form.cleaned_data['email']
            fmessage=form.cleaned_data['message']
            dd=str(datetime.datetime.today()).split()[0]
            record=Enquiry.objects.get_or_create(date_s=dd,name=fname,phone=fphone,email=femail,message=fmessage)
            ## mail

            subject='Welcome to Doffadils school'
            message = 'Hi'+" "+ fname+ ",\n"
            recepient =[]
            recepient.append(femail)
            recepient.append(settings.EMAIL_HOST_USER)
            message=message+'We got your request, our executive will be get in touch with you shortly '+"\n name:"+ fname +"\n email:"+femail+"\n message:"+fmessage
            if 0:
                send_mail(subject,message, settings.EMAIL_HOST_USER, recepient, fail_silently = False)
            else:
                html_content='<p>We got your request, our executive will be get in touch with you shortly</p> '
                email = EmailMessage(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recepient,
                headers={'Message-ID': 'foo'},
                )

                email.content_subtype = "html"
                email.attach_file('D:\\abc\schoolproj\static\images\school_msg.jpg')
                email.send()
                print('email sent')
            return render(request,'testapp/contact.html',{'form':form})



    return render(request,'testapp/enquiry.html',{'form':form})


def enquiry_report_view(request):
    enquirys=Enquiry.objects.all()
    return render(request,'testapp/enquiry_results.html',{'enquirys': enquirys})

def SM_upload_view(request):
    form=forms.SM_upload_form()
    if request.method=='POST':
        form=forms.SM_upload_form(request.POST,request.FILES)
        if form.is_valid():
            print('valid SM form')
            form.save()
        else:
            print('not valid SM form')
    return render(request, 'testapp/aupload.html',{'form':form,'title':'Study Material UPLOAD Form'})

def Rlink_upload_view(request):
    form=forms.Rlink_upload_form()
    if request.method=='POST':
        form=forms.Rlink_upload_form(request.POST,request.FILES)
        if form.is_valid():
            print('valid Recordings form')
            form.save()
        else:
            print('not valid Recordings form')
    return render(request, 'testapp/aupload.html',{'form':form,'title':'Recordings Links upload Form'})
    #########Modelformset############
def SM_upload_formset_view(request):
    #form=forms.SM_upload_form()
    #SM_formset=modelformset_factory(SM_upload,form=forms.SM_upload_form,extra=1)

    SM_formset=formset_factory(forms.SM_upload_form,extra=2)
    formset=SM_formset()
    if request.method=='POST':
        SM_formset=formset_factory(forms.SM_upload_form,extra=1)
        formset=SM_formset(request.POST,request.FILES)
        if formset.is_valid():
            for form in formset:
                print(form.cleaned_data)
                form.save()
            print('valid SM formset')
            #formset.save() # no method exist
        else:
            print('not valid SM formset')
    return render(request, 'testapp/aupload.html',{'form':formset})

def SM_report_view(request):
    areports=SM_upload.objects.all()
    return render(request,'testapp/a_results.html',{'areports':areports,'title':'Study Material Report'})

def Rlink_report_view(request):
    areports=Rlink_upload.objects.all()
    return render(request,'testapp/r_results.html',{'areports':areports,'title':'Recording Links Report'})

def logout_view(request):
    return render(request,'testapp/logout.html')

@login_required
def student_home_view(request):
    my_dict={}
    rec=Student.objects.filter(sname=request.user.username)
    for r in rec:
        my_dict['email']=r.email
        my_dict['classx']=r.classx
        my_dict['section']=r.section
        my_dict['sname']=r.sname
        print('email',r.email)
    request.session['my_dict']=my_dict  #copy my_dict{}  to session
    return render(request,'testapp/shome.html',my_dict)

def student_home_study_material(request):
    my_dict=request.session.get('my_dict',0)
    #print('my_dict',my_dict)
    if my_dict !=0 :
        #print('xxxxxinside',my_dict)
        classx=my_dict['classx']
        recs=SM_upload.objects.filter(std= int(classx))
        return render(request,'testapp/shomesm.html',{'recs':recs})
    else:
        print('my_dict zero in student home sty Material')
        return redirect('/accounts/login/')


def student_online_view(request):
    my_dict=request.session['my_dict']
    return render(request,'testapp/sonline.html',my_dict)


def student_subject_Maths_view(request):
    return sub_route_fun(request,'Maths')
    # my_dict=request.session.get('my_dict',0)
    # if my_dict !=0 :
    #     my_dict=request.session['my_dict']
    #     classx=my_dict['classx']
    #     recs=SM_upload.objects.filter(std= int(classx),subject='Maths')
    #     return render(request,'testapp/sshomesm.html',{'recs':recs})
    # else:
    #     print('my_dict zero in Mathis sty Material')
    #     return redirect('/accounts/login')


def student_subject_Science_view(request):
    return sub_route_fun(request,'Science')

def student_subject_English_view(request):
    return sub_route_fun(request,'English')

def student_subject_Hindi_view(request):
    return sub_route_fun(request,'Hindi')

def student_subject_Telugu_view(request):
    return sub_route_fun(request,'Telugu')



#### local fucntion
def sub_route_fun(request,lang):
    my_dict=request.session.get('my_dict',0)
    if my_dict !=0 :
        classx=my_dict['classx']
        recs=SM_upload.objects.filter(std= int(classx),subject=lang)
        return render(request,'testapp/shomesm.html',{'recs':recs})
    else:
        print('my_dict zero in {} sty Material'.format(lang))
        return redirect('/accounts/login')
