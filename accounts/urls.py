from django.urls import path
from . import views
from .views import activate

urlpatterns = [
    path('', views.home, name ="home"),
    path('login/', views.loginuser, name ="login"),
    path('register/', views.Regtype, name="regtype"),
    path('clientsignup/', views.Client_register, name="clientsignup"),
    path('message/', views.message, name="message"),
    path('Advocate_register/', views.Advocate_register, name="Advocate_register"),
    path('features/', views.Features, name="features"),
    path('testimonial/', views.Testimonials, name="testimonial"),
    path('Clientcaseregister/', views.Clientcaseregister, name="Clientcaseregister"),
    path('Clientprofile/', views.Clientprofile, name="Clientprofile"),
    path('clientprofileupdate/<str:pk>/', views.clientprofileupdate, name="clientprofileupdate"),
    path('feedbackclientview/', views.feedbackclientview, name="feedbackclientview"),
    path('clientheaderview/', views.clientheaderview, name="clientheaderview"),
    path('clientcaseview/',views.clientcaseview, name="clientcaseview"),
    path('clientcaseupdate/<str:pk>/', views.clientcaseupdate, name="clientcaseupdate"),
    path('deleteclientcase/<str:pk>/', views.deleteclientcase, name="deleteclientcase"),
    path('pdf/<pk>', views.users_render_pdf_view, name='user_pdf_view'),
    path('contactus/', views.Contactus, name="contactus"),
    path('clienthome/', views.Clienthome, name="clienthome"),
    path('cprofileview/', views.cprofileview, name="cprofileview"),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'),
    path('logout/', views.logoutUser, name="logout"),


    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   CLIENT      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    path('Clientfindanadvocate/', views.Clientfindanadvocate, name="Clientfindanadvocate"),
    path('advocate/<int:id>/', views.advocate_details, name='advocate_details'),
    path('Client_case_management/', views.Client_case_management, name="Client_case_management"),
    path('client_case_management_view', views.client_case_management_view, name='client_case_management_view'),
    path('advocate_list/', views.advocate_list, name='advocate_list'),
    path('Client_case_option/', views.Client_case_option, name='Client_case_option'),
    path('Client_service_option/', views.Client_service_option, name='Client_service_option'),
    path('search/', views.search, name='search'),
    path('assign_case/<int:id>/', views.assign_case, name='assign_case'),
    path('add_review/<int:id>/', views.add_review, name='add_review'),
    path('client_request_cancel/<int:pk>/', views.client_request_cancel, name='client_request_cancel'),
    path('recommendation/<str:case_type>/', views.advocate_recommendation_view, name='advocate_recommendation_view'),
    path('advocate/<int:advocate_id>/feedback/', views.view_feedback, name='view_feedback'),
    path('chat/', views.chat, name="chat"),
    path('chat/<int:advocate_id>/', views.chat, name='chat_with_advocate'),

    #@@@@@@@@@@@@@@@@@@@@@@@@@@@$$$$$$$$$$$   ADVOCATE   $$$$$$$$$$$$@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    path('advocatehome/', views.advocatehome, name="advocatehome"),
    path('Advclient/', views.Advclient, name="Advclient"),
    path('feedbackadvocateview/', views.feedbackadvocateview, name="feedbackadvocateview"),
    path('advocatemessage/', views.advocatemessage, name="advocatemessage"),
    path('AdvocateContactus/', views.AdvocateContactus, name="AdvocateContactus"),
    path('Advocateprofile/', views.advocate_profile, name="Advocateprofile"),
    path('update_advocate/<int:id>/', views.update_advocate, name="update_advocate"),
    path('advocate_caserequest_assignments_view/', views.advocate_caserequest_assignments_view, name='advocate_caserequest_assignments_view'),
    path('schedule/', views.schedule_view, name='schedule_view'),
    path('schedule/create/', views.add_schedule, name='add_schedule'),
    path('schedule/<int:pk>/update/', views.edit_schedule, name='edit_schedule'),
    path('schedule/delete/<int:pk>/', views.delete_schedule, name='schedule_delete'),
    path('accept_assignment/<int:id>/', views.accept_assignment, name='accept_assignment'),
    path('reject_assignment/<int:id>/', views.reject_assignment, name='reject_assignment'),
    path('create_case/', views.create_case, name='create_case'),
    path('advocate_chat/', views.advocate_chat, name="advocate_chat"),
    path('advocate_chat/<int:client_id>/', views.advocate_chat, name='chat_with_client'),
    path('client-case-details/<int:assignment_id>/',views.client_case_details, name='client_case_details'),
    path('predict_document_type/', views.predict_document_type, name="predict_document_type"),

]