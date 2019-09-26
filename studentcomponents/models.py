from django.db import models
from multiselectfield import MultiSelectField
from datetime import datetime


class StudentDetail(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    ]
    CASTE_CHOICES = [
        ('General', 'General'),
        ('OBC', 'OBC'),
        ('SC', 'SC'),
        ('ST', 'ST'),
    ]
    FOOD_CHOICES = [
        ('Vegetarian', 'Vegetarian'),
        ('Non-Vegetarian', 'Non-Vegetarian'),
    ]
    BLOODGROUP_CHOICES = [
        ('A+', 'A+'),
        ('B+', 'B+'),
        ('O+', 'O+'),
        ('AB+', 'AB+'),
        ('A-', 'A-'),
        ('B-', 'B-'),
        ('O-', 'O-'),
        ('AB-', 'AB-'),
    ]
    STATUS = [
        ('CURRENT', 'CURRENT'),
        ('LEFT', 'LEFT')
    ]
    student = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    student_birthday = models.DateField(null=True, verbose_name="Date of Birth")
    religion = models.CharField(max_length=15, null=True)
    caste = models.CharField(max_length=15, null=True, choices=CASTE_CHOICES)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES)
    identification_mark = models.CharField(max_length=300, verbose_name="Identification Marks", null=True)
    blood_group = models.CharField(max_length=8, verbose_name="Blood Group", null=True, choices=BLOODGROUP_CHOICES)
    admission_number = models.ForeignKey('Coordinator', on_delete=models.CASCADE)
    date_of_join = models.DateField(null=True)
    referred_by = models.CharField(max_length=50, verbose_name="Referred By", null=True)
    last_attended_institute_name = models.CharField(max_length=100, verbose_name="Last attended Institute Name",
                                                    null=True)
    reason_for_leaving = models.CharField(max_length=200, verbose_name="Reason for leaving", null=True)
    disability = models.CharField(max_length=100, null=True)
    disability_percentage = models.CharField(max_length=5, default=10)
    languages_known = models.CharField(verbose_name="Languages Known", max_length=50)
    food_preference = models.CharField(max_length=15, verbose_name="Food Preference", choices=FOOD_CHOICES)
    weight = models.IntegerField(verbose_name="Weight", null=True)
    class1 = models.CharField(max_length=50, null=True)
    class_teacher = models.CharField(max_length=100)
    attendance = models.IntegerField(null=True)
    height = models.CharField(max_length=5, null=True)
    status = models.CharField(max_length=100, choices=STATUS, default="CURRENT")
    address = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return ('%s %s %s' % (self.admission_number, self.first_name, self.last_name))

    def upper_case_name(obj):
        return ("%s %s" % (obj.first_name, obj.last_name)).upper()

    def __unicode__(self):
        return self.admission_number


    @property
    def age(self):
        return int((datetime.now().date() - self.student_birthday).days / 365.25)

    upper_case_name.short_description = 'Name'


class StudentParent(models.Model):
    RELATIONSHIP_CHOICES = [
        ('MOTHER', 'MOTHER'),
        ('FATHER', 'FATHER'),
        ('GUARDIAN', 'GUARDIAN'),
    ]
    student_parent = models.AutoField(primary_key=True)
    parent_name = models.CharField(max_length=50)
    student = models.ForeignKey('StudentDetail',on_delete=models.CASCADE)
    relation_type = models.CharField(max_length=15, verbose_name="Relation type",null=True, choices=RELATIONSHIP_CHOICES)
    occupation = models.CharField(max_length=12, null=True)
    phone_number = models.CharField(max_length=12, verbose_name="Phone number", null=True)
    email_id = models.EmailField(max_length=70, blank=True, null= True, verbose_name="Email Id")
    address = models.CharField(max_length=300, null=True)

    def __str__(self):
        return ('%s %s' % (self.parent_name, self.student))


class StudentSibling(models.Model):
    sibling = models.AutoField(primary_key=True)
    student = models.ForeignKey('StudentDetail',on_delete=models.CASCADE)
    sibling_name = models.CharField(max_length=50)
    sibling_age = models.IntegerField(null=True)
    sibling_occupation = models.CharField(max_length=12, null=True)

    def __str__(self):
        return ('%s' % (self.sibling_name))


class LookUp(models.Model):
    LOOKUP_TYPE_CHOICES = [
        ('Assessment', 'Assessment'),
        ('Admission', 'Admission'),
        ('Payment', 'Payment')
    ]
    lookup_type = models.CharField(max_length=15,
                                   default="Assessment",
                                   choices=LOOKUP_TYPE_CHOICES)
    lookup_name = models.CharField(max_length=100)
    lookup_inputvalue = models.CharField(max_length=100)
    lookup_outputvalue = models.CharField(max_length=100, null=True, blank=True)

   # def __str__(self):
        #return ('%s %s %s %s' % (self.lookup_type,self.lookup_name,self.lookup_inputvalue,self.lookup_outputvalue))


class Coordinator(models.Model):
    SELF_HELP = [
        ('Eating', 'Eating'),
        ('Sleeping', 'Sleeping'),
        ('Brushing', 'Brushing'),
        ('Bathing', 'Bathing'),
        ('Toilet Training', 'ToiletTraining')
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    disability = models.CharField(max_length=50)
    self_help_skill = MultiSelectField(verbose_name="Self Help", choices=SELF_HELP)
    behavioural_issues = models.CharField(max_length=500,null=True)
    medication_taken = models.CharField(max_length=500,null=True)
    allergy = models.CharField(max_length=500,null=True)
    remarks = models.CharField(max_length=500,null=True)
    admission_no = models.IntegerField(primary_key=True)
    class1 = models.CharField(max_length=100)
    class_teacher = models.CharField(max_length=100)

    def __str__(self):
        return ('%s' % (self.admission_no))


class Payment(models.Model):
    student = models.ForeignKey('StudentDetail', on_delete=models.CASCADE)
    admission_fees_set = models.CharField(max_length=100)
    admission_fees_paid = models.CharField(max_length=100)
    monthly_fees_set = models.CharField(max_length=100)
    uniform_fees_set = models.CharField(max_length=100)
    uniform_fees_paid = models.CharField(max_length=100)

    def __str__(self):
        return ('%s' % (self.student))


class PaymentPaidRecord(models.Model):
    payment = models.ForeignKey('StudentDetail', on_delete=models.CASCADE, verbose_name="Student")
    fees_paid_type = models.CharField(max_length=50, blank=False,
                                      verbose_name="Payment Type:")
    fees_paid = models.IntegerField(blank=False, verbose_name="Fee Amount (in Rs.)")
    fees_paid_date = models.DateField(null=True, blank=False, verbose_name="Fee Payment Date")
    def __str__(self):
        return ('%s' % (self.payment))


class StudentDocument(models.Model):
    admission_number = models.ForeignKey('StudentDetail', on_delete=models.CASCADE)
    assessment_sheet = models.FileField(null=True)
    student_picture = models.FileField(null=True)
    gaurdian_picture = models.FileField(null=True)
    adhaar_card_student = models.FileField(null=True)
    adhaar_card_guardian = models.FileField(null=True)
    student_disability_card = models.FileField(null=True)
    student_birth_certificate = models.FileField(null=True)
    student_caste_certificate = models.FileField(null=True)
    student_Niramaya_card = models.FileField(null=True)

    def __str__(self):
        return ('%s' % (self.admission_number))


class Assessment(models.Model):
    admission_number = models.ForeignKey('StudentDetail', on_delete=models.CASCADE)
    lookup_type = models.ForeignKey('LookUp', on_delete=models.CASCADE)
    grade = models.CharField(null=True, max_length=5)
