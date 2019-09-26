from django.contrib import admin
from .models import StudentDetail, StudentParent, StudentSibling, LookUp, Coordinator,\
    Payment, PaymentPaidRecord, StudentDocument, Assessment
from daterange_filter.filter import DateRangeFilter

admin.site.site_header = 'WARDS Admin Page'


class LookUpAdmin(admin.ModelAdmin):
    list_display = ('lookup_type', 'lookup_name', 'lookup_inputvalue', 'lookup_outputvalue')


class StudentDetailAdmin(admin.ModelAdmin):
    list_display = ('admission_number', 'upper_case_name', 'gender', 'date_of_join')
    list_filter = ['admission_number', 'date_of_join']


class StudentParentAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'relation_type', 'parent_name', 'phone_number', 'email_id')
    list_filter = ['student__admission_number', 'relation_type']

    def student_name(self, instance):
        return (str(instance.student.admission_number) + " " + (
                    instance.student.first_name + " " + instance.student.last_name).upper())


class StudentSiblingAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'sibling_name', 'sibling_age')
    list_filter = ['student__admission_number']

    def student_name(self, instance):
        return (str(instance.student.admission_number) + " " + (
                    instance.student.first_name + " " + instance.student.last_name).upper())


class CoordinatorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'self_help_skill')


class PaymentPaidRecordAdmin(admin.ModelAdmin):
    list_display = ('payment', 'fees_paid_type', 'fees_paid', 'fees_paid_date')
    list_filter = [('fees_paid_date', DateRangeFilter), 'fees_paid_type', 'payment']


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'admission_fees_set', 'admission_fees_paid', 'uniform_fees_set', 'uniform_fees_paid')


admin.site.register(StudentDetail, StudentDetailAdmin)
admin.site.register(StudentParent, StudentParentAdmin)
admin.site.register(StudentSibling, StudentSiblingAdmin)
admin.site.register(LookUp, LookUpAdmin)
admin.site.register(Coordinator)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentPaidRecord, PaymentPaidRecordAdmin)
admin.site.register(StudentDocument)
admin.site.register(Assessment)

