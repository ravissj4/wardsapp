from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from Users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from studentcomponents import views as student_views
from page1 import views as page1_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
 path('accounts/', include('django.contrib.auth.urls')),
 path('admin/', admin.site.urls, name='admin'),
 path('register/', user_views.register, name='register'),
 #path('profile/', user_views.profile, name='profile'),
 path('login/', auth_views.LoginView.as_view(template_name='Users/login.html'), name='login'),
 path('logout/', auth_views.LogoutView.as_view(template_name='Users/logout.html'), name='logout'),
 path('password_reset/', auth_views.PasswordResetView.as_view(template_name='Users/password_reset.html'),
      name='password_reset'),
 path('', include('page1.urls')),
 path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
      template_name='Users/password_reset_done.html'),
      name='password_reset_done'
      ),
 path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
      template_name='Users/password_reset_confirm.html'),
      name='password_reset_confirm'
      ),
 path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
      template_name='Users/password_reset_complete.html'),
      name='password_reset_complete'),
 path('', include('page1.urls')),

 path('coord/', student_views.coord, name='coord'),
 #path('submit_student_documents', student_views.submit_assess, name='submit_assess'),
 path('student_list/', student_views.StudentList, name="student_list"),
 path('StudentListView', student_views.StudentListView, name="student_lists"),
 path('StudentClassListView', student_views.StudentClassListView, name="student_class_list"),
 path('student_class_report/', student_views.StudentClassListView, name="student_class_report"),
 path('student_teacher_report/', student_views.StudentClassListView, name="student_teacher_report"),
 path('StudentTeacherListView', student_views.StudentTeacherListView, name="student_teacher_list"),
 path('student_Teacher_report/', student_views.StudentTeacherListView, name="student_teacher_report"),
 path('StudentListViewAll', student_views.StudentListViewAll, name="student_list_all"),
 path('coord_form_submit', student_views.coord_form_submit, name="coord_form_submit"),
 path('admission_process', student_views.admission_process, name="admission_process"),
 path('student_authentication/', student_views.student_auth, name="student_authentication"),
 path('student_auth', student_views.student_auth, name="student_auth"),
 path('coord_form_submit', student_views.coord_form_submit, name="coord_form_submit"),
 path('payment_due/', student_views.payment_due_view, name="payment_due"),
 path('payment_due_view', student_views.payment_due_view, name="payment_due_view"),
 path('payment_form/', student_views.fee_submission, name="payment_form"),
 path('paymentForm', student_views.fee_submission, name="paymentForm"),
 path('student', student_views.student_report, name='student'),
 path('student_report', student_views.student_report, name='student_report'),
 path('student_details_report/', student_views.home1, name='student_details_report'),
 path('submit_admission', student_views.submit_admission, name="submit_admission"),
 path('classreport', student_views.classreport, name="classreport"),
 path('teacherreport', student_views.teacherreport, name="teacherreport"),
 path('assessment_form/', student_views.assessment_form, name="assessment_form"),
 path('submit_assess', student_views.submit_assess, name="submit_assess"),
 path('report', student_views.report, name="report"),
 path('assessment_report_auth_view/', student_views.assessment_report_auth_view, name="assessment_report_auth_view"),
 path('assessment_report_auth_view', student_views.assessment_report_auth_view, name="assessment_report_auth_view"),
 path('assessment_form_submit/', student_views.assessment_form_submit, name="assessment_form_submit"),
 path('assessment_form_submit2', student_views.assessment_form_submit2, name="assessment_form_submit2")

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
