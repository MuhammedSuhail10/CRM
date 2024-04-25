from django.urls import path
from crmAdmin import views

urlpatterns=[
       path('',views.dash,name="dash"),
       path('dashboard',views.dash,name="dash"),
       path('lead', views.leed, name="leed"),
       path('del_lead/<int:id>',views.del_lead,name="del_lead"),
       path('edit_lead/<int:id>', views.edit_lead, name="edit_lead"),
       path('lead/<int:id>/status', views.lead_status, name="lead_status"),
       path('salesperson',views.salespersons,name='salesperson'),
       path('edit_sales/<int:id>', views.edit_sales, name="edit_sales"),
       path('del_sales/<int:id>', views.del_sales, name="del_sales"),
       path('duty/<int:id>', views.duty, name='duty'),
       path('del_duty/<int:id>', views.del_duty, name='del_duty'),
       path('course', views.courses, name='course'),
       path('edit-course/<int:id>', views.edit_course, name='edit_course'),
       path('delete-course/<int:id>', views.del_course, name='del_course'),
       path('payment',views.payments,name="payments"),
       path('callbacks',views.callbacks,name="callbacks"),
       path('delete-payments/<int:id>', views.del_pay, name='del_pay'),
       path('assign_duties', views.assign, name="assign"),
       path('assign_lead/<int:id>', views.assign_lead, name="assign_lead"),
       path('Leads Won', views.won, name="won"),
       path('login', views.loginpage, name="admin_login"),
       path('logout', views.logoutpage, name='logout'),
       path('followup', views.followup, name='followup'),
       path('delete-user/<int:id>', views.del_suser, name='del_suser'),
       path('settings', views.settings, name='settings'),
       path('edit-admin/<int:id>', views.edit_admin, name='edit_admin'),
       path('reset-todays-leads/', views.reset_todays_leads, name='reset_todays_leads'),

]