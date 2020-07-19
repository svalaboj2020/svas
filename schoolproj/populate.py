
#from testapp import models
import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','schoolproj.settings')
django.setup()

from faker import Faker
from testapp.models import *

fake=Faker()
#models.s=Student()
#n=int(sys.argv[1])

def populate(n):
    for i in range(n):
        fsname=fake.name()
        fpname=fake.name()
        fDOB=fake.date()
        femail=fake.email()
        fsection=fake.random_element(elements=('A','B','C','D','E','F','G','H'))
        student_emp=Student.objects.get_or_create(sname= fsname,pname=fpname,DOB=fDOB,email=femail,section=fsection)
        print()

populate(200)
