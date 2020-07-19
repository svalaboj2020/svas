from django.db import models

# Create your models here.
class Student(models.Model):
    sname=models.CharField(max_length=20)
    pname=models.CharField(max_length=20)
    DOB=models.CharField(max_length=20)
    email=models.EmailField(max_length=30)
    section=models.CharField(max_length=6)
    classx=models.CharField(max_length=3)
    lname=models.CharField(max_length=20)
    #def __str__(self):
        #return (self.sname, self.pname , self.email)
class Parent(models.Model):
    mother_name=models.CharField(max_length=20)
    m_email=models.EmailField(max_length=30)
    m_phone=models.CharField(max_length=14)
    father_name=models.CharField(max_length=20)
    f_email=models.EmailField(max_length=30)
    f_phone=models.CharField(max_length=14)
    guardian_name=models.CharField(max_length=20,blank=True)
    g_email=models.EmailField(max_length=30,blank=True)
    g_phone=models.CharField(max_length=14,blank=True)

class Enquiry(models.Model):
    name=models.CharField(max_length=30)
    phone=models.IntegerField()
    email=models.EmailField()
    message=models.CharField(max_length=255)
    date_s=models.DateField(null=True)

class SM_upload(models.Model):
    title=models.CharField(max_length=40)
    subject=models.CharField(max_length=20)
    std=models.IntegerField()
    sec=models.CharField(max_length=1)
    pdf=models.FileField(upload_to='books/pdfs',blank=True)


class Rlink_upload(models.Model):
    title=models.CharField(max_length=40)
    subject=models.CharField(max_length=20)
    std=models.IntegerField()
    sec=models.CharField(max_length=1)
    url=models.URLField()
