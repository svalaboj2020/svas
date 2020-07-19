"""schoolproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from testapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home_view),
    path('contact/', views.contact_view),
    path('student_info/', views.student_info_view),
    path('enquiry/', views.enquiry_info_view),
    path('ereport/', views.enquiry_report_view),
    path('smupload/', views.SM_upload_view),
    path('rlupload/', views.Rlink_upload_view),
    path('auploadset/', views.SM_upload_formset_view),
    path('smreport/', views.SM_report_view),
    path('rlreport/', views.Rlink_report_view),
    path('logout/', views.logout_view),
    path('shome/', views.student_home_view),
    path('shomesm/', views.student_home_study_material),
    path('sonline/', views.student_online_view),
    path('accounts/', include('django.contrib.auth.urls')),
    path('smaths/', views.student_subject_Maths_view),
    path('sscience/', views.student_subject_Science_view),
    path('senglish/', views.student_subject_English_view),
    path('shindi/', views.student_subject_Hindi_view),
    path('stelugu/', views.student_subject_Telugu_view),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
