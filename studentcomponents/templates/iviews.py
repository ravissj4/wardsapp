from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from .utils import render_to_pdf
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import PaymentForm
from .models import StudentDetail, StudentParent, StudentSibling, LookUp, Coordinator, Payment, PaymentPaidRecord,\
    StudentDocument, Assessment
from easy_pdf.views import PDFTemplateView
from django.template.defaultfilters import date
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db.models import Avg, Max, Min, Sum, Count


def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@login_required
def StudentList(request):
    title = 'Student Details'
    filter = 'all'
    status_current = 'CURRENT'
    student_adm_num = StudentDetail.objects.order_by('admission_number').filter(status=status_current)
    if not student_adm_num:
        messages.warning(request, 'No student admitted yet')
        redirect('student_list')
    else:
        student_parents = StudentParent.objects.all()
        student_siblings = StudentSibling.objects.all()
        student_class = StudentDetail.objects.order_by('class1').values_list('class1', flat=True).distinct()
        student_details_all = StudentParent.objects.order_by('student__admission_number').select_related('student').all()
        args = {'student_adm_num': student_adm_num, 'student_class': student_class,
                'student_details_all': student_details_all, 'filter': filter, 'student_parents': student_parents,
                'student_siblings': student_siblings, 'title': title}
        return render(request, 'student_list.html', args)
    return render(request, 'student_list.html', {'title': title})


def StudentListView(request):
    title = 'Student Details'
    student_adm_num = StudentDetail.objects.order_by('admission_number')
    filter = 'admission'
    student_class = StudentDetail.objects.order_by('class1').values_list('class1', flat=True).distinct()
    student_num = request.POST["student_admissionno"]
    option = request.POST["option"]
    if not student_num:
        print('no admission number entered')
        if option == 'print_student':
            if request.method == 'POST':
                list = StudentDetail.objects.order_by('admission_number')
                co = {"student": list}
                pdf = render_to_pdf('student.html', co)
            return HttpResponse(pdf, content_type='application/pdf')

        if option == 'view_all':
            if request.method == 'POST':
                return redirect('student_list')
        if option == 'left_all':
            status_left = 'LEFT'
            filter = 'all'
            student_adm_num = StudentDetail.objects.order_by('admission_number').filter(status=status_left)
            student_parents = StudentParent.objects.all()
            student_siblings = StudentSibling.objects.all()
            student_class = StudentDetail.objects.order_by('class1').values_list('class1',
                                                                                     flat=True).distinct()
            student_details_all = StudentParent.objects.order_by('student__admission_number').select_related(
                    'student').all()
            args = {'student_adm_num': student_adm_num, 'student_class': student_class,
                        'student_details_all': student_details_all,
                        'student_parents': student_parents,
                        'student_siblings': student_siblings, 'title': title, 'filter': filter}
            return render(request, 'student_list.html', args)
        messages.warning(request, 'Please enter admission number to get details of a student!')
        redirect('student_list')
    else:
        student_details = StudentDetail.objects.filter(admission_number=student_num)
        if not student_details:
            messages.warning(request, 'No student found with this admission number !')
            redirect('student_list')
        else:
            if option == 'student_details':
                student_details = StudentDetail.objects.filter(admission_number=student_num)
                siblings = StudentSibling.objects.filter(student__admission_number=student_num).select_related('student')
                father = StudentParent.objects.filter(student__admission_number=student_num).select_related('student').filter(
                    relation_type='FATHER')
                mother = StudentParent.objects.filter(student__admission_number=student_num).select_related('student').filter(
                    relation_type='MOTHER')
                guardian = StudentParent.objects.filter(student__admission_number=student_num).select_related('student').filter(
                    relation_type='GUARDIAN')
                student_count = StudentDetail.objects.aggregate(Count("admission_number"))
                print(student_count)
                args = {'student_adm_num': student_adm_num, 'student_class': student_class,
                        'student_details': student_details,
                        'father': father, 'mother': mother, 'guardian': guardian, 'siblings': siblings, 'filter': filter,
                        'title': title}
                return render(request, 'student_list.html', args)
            if option == 'print_coord':
                report = 'Co-ordinator report'
                w_n = Coordinator.objects.filter(admission_no=student_num)
                context1 = {"student": w_n, 'report': report}
                co_list = Coordinator.objects.all()
                print(context1)
                cord = {"student": co_list}
                pdf = render_to_pdf('coord_report.html', context1)
                return HttpResponse(pdf, content_type='application/pdf')
            if option == 'print_adm_form':
                report = 'Admission form'
                v_n = StudentDetail.objects.filter(admission_number=student_num)
                student_parents = StudentParent.objects.all()
                student_sibling = StudentSibling.objects.all()
                context2 = {"student": v_n, 'student_parents': student_parents, 'student_sibling': student_sibling,
                            'report': report}
                pdf = render_to_pdf('admission_report.html', context2)
                return HttpResponse(pdf, content_type='application/pdf')
            if option == 'print_student':
                if request.method == 'POST':
                    list = StudentDetail.objects.order_by('admission_number')
                    co = {"student": list}
                    pdf = render_to_pdf('student.html', co)
                return HttpResponse(pdf, content_type='application/pdf')
    return render(request, 'student_list.html', {'title': title})


def StudentClassListView(request):
    title = 'Class-wise List'
    class_type = 'class_type'
    student_adm_num = StudentDetail.objects.order_by('admission_number')
    student_class = StudentDetail.objects.order_by('class1').values_list('class1', flat=True).distinct()
    print(student_class)
    if request.method == 'POST':
        student_class_assigned = request.POST["student_class_assigned"]
        student_details = StudentDetail.objects.filter(class1=student_class_assigned)
        student_teacher = student_details.order_by('class_teacher').values_list('class_teacher',
                                                                                flat=True).distinct()
        print(student_teacher)
        father = StudentParent.objects.filter(student__class1=student_class_assigned).select_related('student').filter(relation_type='FATHER')
        mother = StudentParent.objects.filter(student__class1=student_class_assigned).select_related('student').filter(
            relation_type='MOTHER')
        guardian = StudentParent.objects.filter(student__class1=student_class_assigned).select_related('student').filter(
            relation_type='GAURDIAN')
        args = {'student_adm_num': student_adm_num,
                'student_class': student_class, 'student_details': student_details,
                'father': father, 'mother': mother, 'guardian': guardian, 'class_type': class_type,
                'student_class_assigned': student_class_assigned, 'student_teacher': student_teacher, 'title': title}
        return render(request, 'student_class_report.html', args)
    return render(request, 'student_class_report.html', {'student_class': student_class})


def StudentListViewAll(request):
    title = 'Student Details'
    student_list = StudentParent.objects.order_by('student__admission_number').select_related('student').all()
    print(student_list)
    args = {'student_list': student_list, 'title': title}
    return render(request, 'student_list.html', args)


def StudentTeacherListView(request):
    title = 'Teacher-wise List'
    class_type = 'teacher_type'
    student_adm_num = StudentDetail.objects.order_by('admission_number')
    student_teacher = StudentDetail.objects.order_by('class_teacher').values_list('class_teacher', flat=True).distinct()
    print(student_teacher)
    #student_teacher = student_class.class_teacher
    if request.method == 'POST':
        student_teacher_assigned = request.POST["student_teacher_assigned"]
        print(student_teacher_assigned)
        student_details = StudentDetail.objects.filter(class_teacher=student_teacher_assigned)
        print(student_details)
        student_teacher_name = student_details.order_by('class_teacher').values_list('class_teacher',
                                                                                     flat=True).distinct()
        print(student_teacher_name)
        father = StudentParent.objects.filter(student__class1=student_teacher_assigned).select_related('student').filter(relation_type='FATHER')
        mother = StudentParent.objects.filter(student__class1=student_teacher_assigned).select_related('student').filter(
            relation_type='MOTHER')
        guardian = StudentParent.objects.filter(student__class1=student_teacher_assigned).select_related('student').filter(
            relation_type='GAURDIAN')
        args = {'student_adm_num': student_adm_num,
                'student_teacher': student_teacher, 'student_details': student_details,
                'father': father, 'mother': mother, 'guardian': guardian, 'class_type': class_type,
                'student_teacher_assigned': student_teacher_assigned, 'student_teacher': student_teacher,
                'student_teacher_name': student_teacher_name, 'title': title}
        return render(request, 'student_teacher_report.html', args)
    return render(request, 'student_teacher_report.html', {'student_teacher': student_teacher})


def coord_form_submit(request):
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    disability = request.POST["disability"]
    self_help_skill = request.POST.get("self_help_skill")
    admission_no = request.POST["adm"]
    class1 = request.POST["class"]
    class_teacher = request.POST["ct"]
    assess = Coordinator(first_name=first_name, last_name=last_name, disability=disability, self_help_skill=self_help_skill, admission_number=admission_no, class1=class1, class_teacher=class_teacher)
    assess.save()
    return render(request, 'coord.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:view_profile'))
        else:
            return redirect(reverse('accounts:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)


def coord(request):
    title = 'Student Co-ordinator Form'
    self_help = LookUp.objects.filter(lookup_type='Admission').filter(lookup_name='Self Help')
    comments = LookUp.objects.filter(lookup_type='Admission').filter(lookup_name='Multi Line Comment')
    context = {'self_help': self_help, 'comments': comments, 'title': title}
    return render(request, 'coord.html', context)


def admission_process(request):
    return render(request, 'admission_process.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:view_profile'))
        else:
            return redirect(reverse('accounts:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)


def student_auth(request):
    title = 'Student Authentication'
    if request.method == 'POST':
        admission_number = request.POST["admission_number"]
        if StudentDetail.objects.filter(admission_number=admission_number).exists():
            messages.warning(request, 'Admission form already Submitted, Please find student details below !')
            return redirect('student_list')
        else:
            if Coordinator.objects.filter(admission_no=admission_number).exists():
                title1 = 'Admission Form'
                student = Coordinator.objects.get(admission_no=admission_number)
                first_name = student.first_name
                last_name = student.last_name
                disability = student.disability
                class1 = student.class1
                class_teacher = student.class_teacher
                latest_question_list = LookUp.objects.all()
                lookup_language = LookUp.objects.filter(lookup_name="language")
                lookup_religion = LookUp.objects.filter(lookup_name="religion")
                context = {'admission': admission_number, 'first_name': first_name, 'last_name': last_name,
                           'class1': class1,
                           'class_teacher': class_teacher, 'disability': disability,
                           'latest_question_list': latest_question_list,
                           'lookup_language': lookup_language, 'lookup_religion': lookup_religion, 'title': title1}
                return render(request, 'admission_process.html', context)
            else:
                messages.warning(request, 'Student not found, please fill co-ordinator form !')
                return redirect('coord')
    return render(request, 'student_authentication.html', {'title': title})


def payment_due_view(request):
    title = 'Payment Details'
    student_details = StudentDetail.objects.all()
    lookup_ptype = LookUp.objects.filter(lookup_name="paymentType")
    if request.method == 'POST':
        from_date = request.POST["from_date"]
        to_date = request.POST["to_date"]
        type_of_payment = request.POST["type_of_payment"]
        print(type_of_payment)
        admission_number = request.POST["student_admissionno"]

        if from_date and to_date:
            if not admission_number:
                messages.warning(request, 'No admission number selected, Please select !')
                redirect('payment_due')
            else:
                admission_fee = Payment.objects.all()
                uniform_fee = Payment.objects.all()
                fee_set = Payment.objects.filter(student__admission_number=admission_number)
                print(fee_set)
                payment_paid = PaymentPaidRecord.objects.filter(
                    fees_paid_type=type_of_payment).filter(
                    fees_paid_date__range=[from_date, to_date])
                payment_paid_total = list(PaymentPaidRecord.objects.filter(
                    payment__admission_number=admission_number).filter(fees_paid_type=type_of_payment).filter(
                    fees_paid_date__range=[from_date, to_date]).aggregate(total=Sum('fees_paid')).values())[0]
                args = {'type_of_payment': type_of_payment, 'fee_set': fee_set,
                        'admission_fee': admission_fee, 'uniform_fee': uniform_fee, 'payment_paid': payment_paid,
                        'payment_paid_total': payment_paid_total, 'title': title, 'lookup_ptype': lookup_ptype}
                return render(request, 'payment_due.html', args)
        else:
            messages.warning(request, 'No date selected, Please select !')
            redirect('payment_due')
    return render(request, 'payment_due.html', {'title': title, 'student_details': student_details,
                                                'lookup_ptype': lookup_ptype})


def fee_submission(request):
    student_adm_num = Payment.objects.all()
    print(student_adm_num)
    lookup_ptype = LookUp.objects.filter(lookup_name="paymentType")
    if request.method == 'POST':
        payment = request.POST["student_admissionno"]
        print(payment)
        student_pay = StudentDetail.objects.get(admission_number=payment)
        print(student_pay)
        paytype = request.POST["paytype"]
        pay_amount = request.POST["pay_amount"]
        dop = request.POST["dop"]
        paymentFormObj = PaymentPaidRecord(payment=student_pay, fees_paid_type=paytype, fees_paid=pay_amount,
                                           fees_paid_date=dop)
        paymentFormObj.save()
        messages.success(request, 'Successfully Saved Payment Form !')
        redirect('/')
    args = {'student_adm_num': student_adm_num, 'lookup_ptype': lookup_ptype}
    return render(request, 'payment_form.html', args)


def home1(request):
    title = 'Student Details Report'
    student_details = StudentDetail.objects.order_by('admission_number')
    return render(request, 'student_details_report.html', {'student_details': student_details, 'title': title})


def student_report(request):
    if request.method == 'POST':
        list = StudentDetail.objects.order_by('admission_number')
        co = {"student": list}
        pdf = render_to_pdf('student.html', co)
    return HttpResponse(pdf, content_type='application/pdf')


# submit coordinator form data
def coord_form_submit(request):
    title = 'Admission Form'
    if request.method == 'POST':
        admission_no = request.POST["adm"]
        if Coordinator.objects.filter(admission_no=admission_no).exists():
            if StudentDetail.objects.filter(admission_number=admission_no).exists():
                messages.warning(request, 'Student co-ordinator and admission form already submitted, Find student details below !')
                return redirect('student_list')
            else:
                messages.warning(request, 'Student co-ordinator form already submitted, Proceed with admission form !')
                return redirect('student_authentication')
        else:
            title = 'Admission Form'
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            disability = request.POST["disability"]
            self_help = request.POST.getlist("self_help_skill")
            print(self_help)
            class1 = request.POST["class1"]
            class_teacher = request.POST["ct"]
            latest_question_list = LookUp.objects.all()
            lookup_language = LookUp.objects.filter(lookup_name="language")
            lookup_religion = LookUp.objects.filter(lookup_name="religion")
            behaviour = request.POST["behaviour"]
            medication = request.POST["medication"]
            allergy = request.POST["allergy"]
            remarks = request.POST["remarks"]
            context = {'admission': admission_no, 'first_name': first_name, 'last_name': last_name, 'class1': class1,
                       'class_teacher': class_teacher, 'disability': disability, 'latest_question_list': latest_question_list,
                       'lookup_language': lookup_language, 'lookup_religion': lookup_religion, 'title': title}
            assess = Coordinator(first_name=first_name, last_name=last_name, disability=disability,
                                 self_help_skill=self_help, admission_no=admission_no, class1=class1,
                                 class_teacher=class_teacher, behavioural_issues=behaviour, medication_taken=medication,
                                 allergy=allergy, remarks=remarks)
            assess.save()
            return render(request, 'admission_process.html', context)
    return render(request, 'coord.html', {'title': title})


# to submit data from stepper form of admission form
def submit_admission(request):
    if request.method == 'POST':
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        student_birthday = request.POST["student_birthday"]
        religion = request.POST["religion"]
        caste = request.POST["caste"]
        gender = request.POST["gender"]
        blood_group = request.POST["blood_group"]
        identification_mark = request.POST["identification_mark"]
        admission_number = request.POST["admission_number"]
        date_of_join = request.POST["doj"]
        referred_by = request.POST["referred_by"]
        last_attended_institute_name = request.POST["last_attended_institute_name"]
        reason_for_leaving = request.POST["reason_for_leaving"]
        disability = request.POST["disability"]
        disability_percentage = request.POST["disability_percentage"]
        languages_known = request.POST.getlist("language")
        #other_languages_known = request.POST("others")
        food_preference = request.POST["food_preference"]
        class1 = request.POST["class1"]
        class_teacher = request.POST["class_teacher"]
        address = request.POST["address"]
        adm = Coordinator.objects.get(admission_no=admission_number)
        studentobj = StudentDetail(first_name=first_name, last_name=last_name, student_birthday=student_birthday,
                                   religion=religion, caste=caste, gender=gender, identification_mark=identification_mark,
                                   blood_group=blood_group, date_of_join=date_of_join,
                                   referred_by=referred_by, last_attended_institute_name=last_attended_institute_name,
                                   reason_for_leaving=reason_for_leaving, disability=disability,
                                   disability_percentage=disability_percentage, languages_known=languages_known,
                                   food_preference=food_preference, admission_number=adm, class1=class1,
                                   class_teacher=class_teacher, address=address)
        if StudentDetail.objects.filter(admission_number=adm).exists():
            messages.warning(request,
                             'Student admission form already submitted, Find student details below !')
            return redirect('student_list')
        else:
            studentobj.save()
        #payment data form submission
        admission_fee = request.POST["admfee"]
        monthly_fee = request.POST["monFee"]
        admission_fee_paid = request.POST["admfeepaid"]
        uniform_fee = request.POST["unifee"]
        uniform_fee_paid = request.POST["uniFeePaid"]
        admS = StudentDetail.objects.get(admission_number=adm)
        paymentobj = Payment(student=admS,admission_fees_set=admission_fee, monthly_fees_set=monthly_fee,
                             uniform_fees_set=uniform_fee, admission_fees_paid=admission_fee_paid,
                             uniform_fees_paid=uniform_fee_paid)
        paymentobj.save()
        paymentpaid = Payment.objects.get(student__admission_number=adm)
        print(paymentpaid)
        admission = 'ADMISSION'
        uniform = 'UNIFORM'
        # submit to parent table
        menu_entries = request.POST.getlist('menu_entries')
        i = 0
        for menu_entry in menu_entries:
            entry = menu_entry.split(",")
        for ent in entry:
            print(ent)
            i = i + 1
            if i == 1:
                relation_type = ent
            if i == 2:
                parent_name = ent
            if i == 3:
                occupation = ent
            if i == 4:
                phone_number = ent
            if i == 5:
                i = 0
                email_id = ent
                parent = StudentParent(student=admS, parent_name=parent_name, relation_type=relation_type,
                                       occupation=occupation, phone_number=phone_number, email_id=email_id)
                parent.save()

        menu_entries_sib = request.POST.getlist('menu_entries_sib')
        i = 0
        for menu_entry in menu_entries_sib:
            entry = menu_entry.split(",")
        for ent in entry:
            print(ent)
            i = i + 1
            if i == 1:
                parent_name = ent
            if i == 2:
                relation_type = ent
            if i == 3:
                occupation = ent
                i = 0
                student = StudentSibling(student=admS, sibling_name=parent_name, sibling_age=relation_type,
                                         sibling_occupation=occupation)
                if parent_name:
                    student.save()
        fs = FileSystemStorage()
        if 'assessment_sheet' in request.FILES:
            myfile = request.FILES['assessment_sheet']
            filename = fs.save(myfile.name, myfile)
        else:
            filename = 'blank.txt'
        if 'student_pic' in request.FILES:
            mypic = request.FILES['student_pic']
            mypicfile = fs.save(mypic.name, mypic)
        else:
            mypicfile = 'blank.txt'
        if 'adhaar_card_student' in request.FILES:
            student_adhaar = request.FILES['adhaar_card_student']
            myadhaarfile = fs.save(student_adhaar.name, student_adhaar)
        else:
            myadhaarfile = 'blank.txt'
        if 'adhaar_card_guardian' in request.FILES:
            guardian_adhaar = request.FILES['adhaar_card_guardian']
            myguardianadhaarfile = fs.save(guardian_adhaar.name, guardian_adhaar)
        else:
            myguardianadhaarfile = 'blank.txt'
        if 'student_disability_card' in request.FILES:
            student_disability_card = request.FILES['student_disability_card']
            mydisbcardfile = fs.save(student_disability_card.name, student_disability_card)
        else:
            mydisbcardfile = 'blank.txt'
        if 'student_birth_certificate' in request.FILES:
            student_birth_cert = request.FILES['student_birth_certificate']
            mybirthcertfile = fs.save(student_birth_cert.name, student_birth_cert)
        else:
            mybirthcertfile = 'blank.txt'
        if 'student_Niramaya_card' in request.FILES:
            student_niramaya_card = request.FILES['student_Niramaya_card']
            mynircardfile = fs.save(student_niramaya_card.name, student_niramaya_card)
        else:
            mynircardfile = 'blank.txt'
        if 'student_caste_certificate' in request.FILES:
            student_caste_cert = request.FILES['student_caste_certificate']
            mycastefile = fs.save(student_caste_cert.name, student_caste_cert)
        else:
            mycastefile = 'blank.txt'
        table = StudentDocument(assessment_sheet=filename, student_picture=mypicfile, admission_number=admS,
                                adhaar_card_student=myadhaarfile, adhaar_card_guardian=myguardianadhaarfile,
                                student_disability_card=mydisbcardfile, student_birth_certificate=mybirthcertfile,
                                student_caste_certificate=mycastefile, student_Niramaya_card=mynircardfile)
        table.save()
        messages.success(request, 'Successfully Saved Admission Form !')
        return redirect('/')
    return render(request, 'coord.html')

def classreport(request):
    if request.method == 'POST':
        student = request.POST["student_class_assigned"]
        print (student)
        m_n = StudentDetail.objects.filter(class1=student)
        context = {"student": m_n}
        list = StudentDetail.objects.all()
        ww = {"j": m_n}
        pdf = render_to_pdf('class_teacher_report.html', ww)
    return HttpResponse(pdf, content_type='application/pdf')

def teacherreport(request):
    if request.method == 'POST':
        student1 = request.POST["student_teacher_assigned"]
        print (student1)
        f_n = StudentDetail.objects.filter(class_teacher=student1)
        ff_n = f_n.order_by('class_teacher').values_list('class_teacher',flat=True).distinct()
        print(ff_n)
        context1 = {"student": ff_n }
        list1 = StudentDetail.objects.all()
        w = {"l": ff_n,"k":f_n}
        print(f_n)
        pdf = render_to_pdf('teacher_wise_report.html', w)
    return HttpResponse(pdf, content_type='application/pdf')


def assessment_form(request):
    scholastic = LookUp.objects.all().filter(lookup_name='Scholastic')
    creative = LookUp.objects.all().filter(lookup_name='CreativeArts')
    concept = LookUp.objects.all().filter(lookup_name='Concept Formation')
    other = LookUp.objects.all().filter(lookup_name='Others')
    student = StudentDetail.objects.all()
    return render(request, 'assessment.html', {'scholastic': scholastic, 'student': student, 'creative': creative,
                                               'concept': concept, 'other': other})


def submit_assess(request):
    assessment_list = LookUp.objects.filter(lookup_type="Assessment")
    stud = request.POST.get("student_admissionno")
    print(stud)
    adme = StudentDetail.objects.get(admission_number=stud)
    for item in assessment_list:
        grade = request.POST.get("a+"+str(item.id))
        adm = LookUp.objects.get(lookup_inputvalue=item.lookup_inputvalue)
        assess = Assessment(lookup_type=adm, admission_number=adme, grade=grade)
        assess.save()
    return render(request, 'assessment.html')


def report(request):
    student_details = StudentDetail.objects.get(admission_number='101')
    scholastic = LookUp.objects.filter(lookup_name='Scholastic')
    creative = LookUp.objects.filter(lookup_name='CreativeArts')
    concept = LookUp.objects.filter(lookup_name='Concept Formation')
    other = LookUp.objects.filter(lookup_name='Others')
    assess = Assessment.objects.filter(admission_number=student_details)
    args = {'student_details': student_details,'scholastic': scholastic,'creative': creative,'concept': concept,'other':other,'assess':assess}
    return render(request, 'assessmentreport.html', args)


def assessment_report_auth_view(request):
    if request.method == 'POST':
        student = request.POST['admission_number']
        print(student)
        parent = request.user.get_full_name()
        parent_from_table = StudentParent.objects.filter(student__admission_number=student)
        parent_name = parent_from_table.order_by('parent_name').values_list('parent_name', flat=True)
        print(parent)
        print(parent_name)
        x = 0
        for i in parent_name:
            if i == parent:
                print('match')
                x = 1
            else:
                print('not match')
        print(x)
        if x == 1:
            student_details = StudentDetail.objects.get(admission_number=student)
            scholastic = LookUp.objects.filter(lookup_name='Scholastic')
            creative = LookUp.objects.filter(lookup_name='CreativeArts')
            concept = LookUp.objects.filter(lookup_name='Concept Formation')
            other = LookUp.objects.filter(lookup_name='Others')
            assess = Assessment.objects.filter(admission_number=student_details)
            args = {'student_details': student_details, 'scholastic': scholastic, 'creative': creative,
                    'concept': concept,
                    'other': other, 'assess': assess}
            return render(request, 'assessmentreport.html', args)
        else:
            messages.warning(request, 'Sorry, no matching data found !')
    return render(request, 'parentcomponents/parentHomePage.html')




