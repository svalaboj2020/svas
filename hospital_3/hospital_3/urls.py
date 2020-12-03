"""hospital_2 URL Configuration

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
from testapp import views as v1
from testapp1 import views as v2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', v1.home),
    path('addSup/', v1.create_supplier),
    path('addCus/', v1.create_customer),
    path('dash_board/', v1.dash_board_view),

    #Item Entry
    path('addItem/', v1.create_item),
    path('addItem1/', v1.create_item_new), #need to add
    path('addItem1/<str:invoice_no>', v1.create_item_new1, name='addItem_1'), #need to add
    path('q_item/', v1.item_query_form_view),
    path('q_item1/', v1.item_query_form_new_view),
    path('ie_list/', v1.Item_EntryListView),
    path('ie_list/<str:id>', v1.Item_EntryList_based_on_id_View, name='Item_EntryList_based_on_id'),  #based on invoice_no in PE
    path('del_ie/<int:id>', v1.del_Item_Entry_view),
    path('del_ie1/<int:id>', v1.del_Item_Entry_view1), # after del redirect to ie_list/invoice_no
    path('del_ie/<int:id>/<str:invoice_no>', v1.del_Item_Entry_pe_view),
    path('upd_ie/<int:id>', v1.update_Item_Entry_view),
    path('upd_ie1/<int:id>', v1.update_Item_Entry_view1), # after upd redirect to ie_list/invoice_no
    path('upd_ie/<int:id>/<str:invoice_no>', v1.update_Item_Entry_pe_view),
    path('clone_ie/<int:id>', v1.clone_item_new),
    path('clone_ie/<int:id>/<str:invoice_no>', v1.clone_item_Entry_pe_view), # after cloning redirect to ie_list/invoice_no
    path('addtoPE/<int:id>', v1.addto_PEView),
    path('addtoBill/<str:id>', v1.addto_BillView, name='addtoBill'),
    path('pe_approval/<str:id>/<int:ie_grand_tot>', v1.pe_approval_view),
    # path('generate_bill/', v1.create_pbill),
    path('generate_bill/<str:id>', v1.create_pbill_id),
    # path('generate_rbill/<str:id>', v1.create_rbill_id, name='generate_rbill_name'),
    path('generate_rbill/<str:id>', v1.create_rbill_id_new, name='generate_rbill_name'), #23-Nov
    path('generate_return_rbill/<str:id>', v1.create_return_rbill_id),
    # path('pay_rbill/<str:id>',v1.pay_retail_bill_view, name='pay_rbill_name'),
    path('pay_rbill/<str:id>',v1.pay_retail_bill_view1, name='pay_rbill_name'), #23-Nov adding discount_amount

    path('upload_im/', v1.create_Item_Master_from_file),
    #Purchase Entry
    # path('addPE/', v1.create_purchase),
    path('addPE/', v1.create_purchase1),
    path('pe/', v1.Purchase_Entry_view),
    path('pe_list/', v1.Purchase_EntryListView),
    path('cart_list/', v1.cart_list_view),
    path('del_pe/<str:id>', v1.del_Purchase_Entry_view),
    path('upd_pe/<str:id>', v1.update_Purchase_Entry_view),

    path('del_item/<int:id>', v1.del_item_view),
    path('upd_item/<int:id>', v1.update_item_view),

    #Supplier Entry
    path('sup_list/', v1.supplier_address_list),
    path('del_sup/<str:id>', v1.del_Supplier_Address_view),
    path('upd_sup/<str:id>', v1.update_Supplier_Address_view),

    # customer customer_address_list
    path('cus_list/', v1.customer_address_list),
    path('del_cus/<int:id>', v1.del_customer_Address_view),
    path('upd_cus/<int:id>', v1.update_customer_address_view),

    path('genpdf/', v1.GeneratePdf.as_view()),
    # Sell_Entry
    path('addSE/', v1.create_sell),
    path('se_list/', v1.list_se),
    path('addbts/<int:id>', v1.addBilltoSession, name='addBilltoSession'),

    # Out_Item_Entry
    path('addtoOIE/<int:id1>/<int:id2>', v1.create_Out_IE),   # id1= id  id2=bill_no
    path('oie_list/<int:id>', v1.oie_list, name='oie_list_based_on_id'),  # based on bill_no (id=bill_no)  list all oie items
    path('del_oie/<int:id>', v1.del_Out_Item_Entry_view),    #upd_oie  not implementing right now

    # Returned Sell_Entry
    path('addRSE/', v1.create_retunred_sell_new),
    path('roie_list/<int:id>', v1.roie_list, name='roie_list_based_on_id'),
    path('retOIE/<int:id1>/<int:id2>/<int:id3>', v1.create_Returned_Out_IE , name='create_Returned_Out_IE'),
    path('del_roie/<int:id1>', v1.del_retunred_Out_Item_Entry_view),
    path('rse_list/', v1.list_rse),

    # path('rse_list/', v1.list_rse),

    # reports
    path('report/<str:id>', v1.report_exp),
    path('report_disp/<str:id>', v1.report_low_summary_stock),
    path('expiry_report/<int:id>', v1.expiry_report),
    path('exp_expiry_rep/<int:months>', v1.export_expiry_report),
    path('balance_sheet_report/', v1.sell_balance_sheet_form_rep),
    path('exp_balance_sheet_report/', v1.export_sell_balance_report_1), #export_sell_balance_report
    path('finreport/', v1.Fin_report),

    path('shome/', v1.staff_home_view), #shome
    path('logout/', v1.logout_view),
    path('accounts/', include('django.contrib.auth.urls')),
    ###
    #receiption module
    ###
    path('register/', v2.reg_form_view),
    path('regSearch',v2.reg_sform_view),
    path('generate_regbill/',v2.generate_reg_receipt_view),
    path('generate_regbill/<str:name>/<int:id>/<int:bill_no>',v2.generate_reg_receipt_view1), #generate_reg_receipt_view #old - testing new
    path('generate_lab_bill/<int:id>/<int:bill_no>',v2.generate_lab_bill_view),
    path('generate_lab_bill1/<int:id>/<int:bill_no>',v2.generate_lab_bill_view1), #testing new
    path('generate_doctemp/<str:name>/<int:id>/<int:bill_no>',v2.generate_doc_temp_view),   #
    path('upload/<str:id>/', v2.create_chart_from_file),
    path('sel_doc/<int:id>/<int:bill_no>', v2.sel_doc_form_view, name='sel_doc'),
    path('sel_lab/<int:id>/<int:bill_no>', v2.sel_lab_form_view, name='sel_lab'),
    path('add_to_session/<str:id>/', v2.add_to_session, name='add_to_session'),
    path('add_test_to_session/<str:id>/<int:bill_no>', v2.add_test_to_session),
    path('del_from_session/<str:id>/', v2.del_from_session),
    path('del_test_from_session/<str:id>/<int:bill_no>', v2.del_test_from_session),
    path('create_Bill_Register/<int:id>/', v2.create_Bill_Register_view),
    path('del_bill_item/<int:id>/<int:bill_no>', v2.del_bill_item),
    path('generate_doc_lab_receipt/<int:bill_no>',v2.generate_doc_lab_receipt_view), #generate_doc_lab_receipt_view
    path('generate_doc_lab_receipt1/<int:bill_no>',v2.generate_doc_lab_receipt_view1), #generate_doc_lab_receipt_view
    path('appt_m/<str:id>',v2.Appointment_form_view),  # make an Appointment
    path('list_appt/',v2.Appointment_query_form_view),  # list appointments
    #BE
    path('be_list/', v2.list_be),
    path('bi_list/<int:id>', v2.bi_list,name='bi_list'),
    path('bi_add/<int:bill_no>', v2.add_bi_view),
    path('bill_hist/<str:opid>', v2.bill_history_view),
    #Lab_chart
    path('list_Fee_chart/', v2.list_Fee_chart_view),
    path('list_lab_chart/', v2.list_Lab_chart_view),

    path('receiption_bal_sheet_rep/', v2.receiption_balance_report),
    path('pay_bill/<int:id>/',v2.pay_retail_bill_view,name='pay_bill'),
    path('pay_bill1/<int:id>/',v2.pay_retail_bill_view1,name='pay_bill1'),
    # REST api
    # path('japi4/<str:id>/', v1.reg_data_json_view4),
    path('japi4/<str:id>/', v1.cus_reg_data_json_view4),
    path('appt_japi4/<str:opt>/', v2.appt_data_json_view4.as_view()),
    #Item_Master
    path('add_item_to_IM/', v1.add_item_to_IM_view),
    path('list_IM/', v1.list_IM_view),
    path('upd_IM_item/<int:id>/', v1.upd_IM_item_view),
    path('del_IM_item/<int:id>/', v1.del_IM_item_view),
    path('im_list_japi/', v1.im_list_json.as_view()),
    path('im_item/<int:id>/', v1.get_im_id_view),
    path('im_entry/<str:item_n>/', v1.get_im_entry_view),
]
