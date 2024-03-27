from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import auth,messages
from .models import UserRegistration,Room,Registration, Course,UserLog, Admin
from django.utils import timezone
from django.contrib.auth.models import User
from .mails import send_mail_after_booking
from .mpesa import mpesa_pay

from threading import Thread

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username, password=password)
        n='/student/dashboard'
        if user is not None:
            if user.is_superuser:
                n='/admin/dashboard'
        
        next=request.GET.get('next', n)

        if user is not None:
            auth.login(request, user)
            if user.is_superuser:
                reg, c=UserRegistration.objects.get_or_create(user=user)
                pass
            else:
                reg, c=UserRegistration.objects.get_or_create(user=user)
                log=UserLog.objects.create(user=reg, user_ip=request.META.get('REMOTE_ADDR'))
                log.save()
            return redirect(f'{next}')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect(f'/login?next={next}')

    else:
        if request.user.is_authenticated:
            return redirect('/student/dashboard')
        else:
            return render(request, 'auth/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/login')

def index(request):
    return redirect("/login")


def student(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    student_count=UserRegistration.objects.count()
    room_count=Room.objects.count()
    booked_count=Registration.objects.count()
    course_count=Course.objects.count()
    context={
        'student_count':student_count,
        'room_count':room_count,
        'booked_count':booked_count,
        'course_count':course_count
    }
    return render(request, 'student/dashboard.html', context)


def acc_setting(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    context={}
    return render(request, 'student/acc-setting.html', context)


def book_hostel(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    user_profile=UserRegistration.objects.get(user=request.user)

    courses=Course.objects.all()
    rooms=Room.objects.all()

    booked=False
    if Registration.objects.filter(reg_no=user_profile.reg_no).exists():
        booked=True

    if request.method == 'POST' and booked == False:
        roomno = request.POST.get('room')
        seater = request.POST.get('seater')
        feespm = request.POST.get('fpm')
        foodstatus = request.POST.get('foodstatus')
        stayfrom = request.POST.get('stayf')
        duration = request.POST.get('duration')
        course = request.POST.get('course')
        regno = user_profile.reg_no
        fname = request.user.first_name
        mname = user_profile.middle_name
        lname = request.user.last_name
        gender = request.POST.get('gender')
        contactno = request.POST.get('contact')
        emailid = request.POST.get('email')
        emcntno = request.POST.get('econtact')
        gurname = request.POST.get('gname')
        gurrelation = request.POST.get('grelation')
        gurcntno = request.POST.get('gcontact')
        caddress = request.POST.get('address')
        ccity = request.POST.get('city')
        cpincode = request.POST.get('pincode')
        paddress = request.POST.get('paddress')
        pcity = request.POST.get('pcity')
        ppincode = request.POST.get('ppincode')
        mp=request.POST.get('mp')
        ta=request.POST.get('ta')
        registration = Registration.objects.create(
            room_no = roomno,
            seater = seater,
            fees_pm = feespm,
            food_status = foodstatus,
            stay_from = stayfrom,
            duration = duration,
            course = course,
            reg_no = regno,
            first_name = fname,
            middle_name = mname,
            last_name = lname,
            gender = gender,
            contact_no =contactno,
            email_id =emailid,
            egy_contact_no = emcntno,
            guardian_name = gurname,
            guardian_relation = gurrelation,
            guardian_contact_no =gurcntno,
            corres_address = caddress,
            corres_city = ccity,
            corres_pincode = cpincode,
            permanent_address = paddress,
            permanent_city = pcity,
            permanent_pincode = ppincode
        )
        phone=mp
        amount=int(ta)
        callback='https://shahibu.com/'
        user_id=request.user.username
        reason='Booking for the hostel'
        # d=mpesa_pay(phone, amount, callback, user_id, reason)
        c={
            "user":request.user,
            "room":roomno,
            "date":stayfrom,
            "seater":seater,
            "total":ta,
        }
        
        # send_mail_after_booking()
        mpesa_pay(phone, amount, callback, user_id, reason)
        threadedmail=Thread(target=send_mail_after_booking, args=(request.user, c) )
        threadedmail.start()
        return redirect(book_hostel)

    context={
        'user_profile':user_profile,
        'courses':courses,
        'rooms':rooms,
        'booked':booked
    }
    return render(request, 'student/book-hostel.html', context)

def room_details(request): 
    if not request.user.is_authenticated:
        return redirect("/login")   
    user_profile=UserRegistration.objects.get(user=request.user)
    booked_rooms=Registration.objects.filter(reg_no=user_profile.reg_no)
    context={
        'booked_rooms':booked_rooms
    }
    return render(request, 'student/room-details.html', context)


def log_activity(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    reg, c=UserRegistration.objects.get_or_create(user=request.user)
    logs=UserLog.objects.filter(user=reg)
    context={
        'logs':logs
    }
    return render(request, 'student/log-activity.html', context)


def student_profile(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    user_profile=UserRegistration.objects.get(user=request.user)
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('fname')
        user.last_name = request.POST.get('lname')
        user.save()
        user_profile.middle_name=request.POST.get('mname')
        user_profile.contact_no=request.POST.get('contact')
        user_profile.gender=request.POST.get('gender')
        user_profile.updation_date=timezone.now()
        user_profile.save()
        return redirect(student_profile)
    context={
        'user_profile':user_profile
    }
    return render(request, 'student/profile.html', context)



# Admin

def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if not request.user.is_superuser:
        return redirect('/student/dashboard/')
    student_count=UserRegistration.objects.count()
    room_count=Room.objects.count()
    booked_count=Registration.objects.count()
    course_count=Course.objects.count()
    logs=UserLog.objects.all()
    context={
        'student_count':student_count,
        'room_count':room_count,
        'booked_count':booked_count,
        'course_count':course_count,
        'logs':logs
    }
    return render(request, 'administrator/dashboard.html', context)

def admin_profile(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if not request.user.is_superuser:
        return redirect('/student/dashboard/')
    if request.method == 'POST':
        email = request.POST['emailid']
        user=request.user
        user.email=email
        user.save()
        return redirect(admin_profile)
    student_count=UserRegistration.objects.count()
    room_count=Room.objects.count()
    booked_count=Registration.objects.count()
    course_count=Course.objects.count()
    admin_user,c=Admin.objects.get_or_create(user=request.user)
    context={
        'student_count':student_count,
        'room_count':room_count,
        'booked_count':booked_count,
        'course_count':course_count,
        'admin_user':admin_user
    }
    return render(request, 'administrator/profile.html', context)


def admin_view_students_acc(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if not request.user.is_superuser:
        return redirect('/student/dashboard/')
    if 'del' in request.GET:
        userid=request.GET['del']
        u=get_object_or_404(User,id=userid).delete()
        # u=User.objects.get(id=userid).delete()
        return redirect(admin_view_students_acc)
    user_registration=UserRegistration.objects.all()
    context={
        "user_registration":user_registration
    }
    return render(request, 'administrator/view-students-acc.html', context)

def admin_register_students_acc(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if not request.user.is_superuser:
        return redirect('/student/dashboard/')
    if request.method == 'POST':
        regno = request.POST['regno']
        fname = request.POST['fname']
        mname = request.POST['mname']
        lname = request.POST['lname']
        gender = request.POST['gender']
        contactno = request.POST['contact']
        emailid = request.POST['email']
        password = request.POST['password']
        user=User.objects.create_user(first_name=fname, last_name=lname, username=emailid, email=emailid)
        user_reg=UserRegistration.objects.create(
            user=user,
            reg_no=regno,
            middle_name=mname,
            gender=gender,
            contact_no=contactno,
        )
        messages.success(request, 'Student has been Registered!')

        return redirect(admin_register_students_acc)
    context={
    }
    return render(request, 'administrator/register-student.html', context)

def admin_view_booking(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if not request.user.is_superuser:
        return redirect('/student/dashboard/')
        
    if request.method == 'POST':
        roomno = request.POST.get('room')
        seater = request.POST.get('seater')
        feespm = request.POST.get('fpm')
        foodstatus = request.POST.get('foodstatus')
        stayfrom = request.POST.get('stayf')
        duration = request.POST.get('duration')
        course = request.POST.get('course')
        regno =  request.POST.get('regno')
        fname =  request.POST.get('fname')
        mname =  request.POST.get('mname')
        lname =  request.POST.get('lname')
        gender = request.POST.get('gender')
        contactno = request.POST.get('contact')
        emailid = request.POST.get('email')
        emcntno = request.POST.get('econtact')
        gurname = request.POST.get('gname')
        gurrelation = request.POST.get('grelation')
        gurcntno = request.POST.get('gcontact')
        caddress = request.POST.get('address')
        ccity = request.POST.get('city')
        cpincode = request.POST.get('pincode')
        paddress = request.POST.get('paddress')
        pcity = request.POST.get('pcity')
        ppincode = request.POST.get('ppincode')
        registration = Registration.objects.create(
            room_no = roomno,
            seater = seater,
            fees_pm = feespm,
            food_status = foodstatus,
            stay_from = stayfrom,
            duration = duration,
            course = course,
            reg_no = regno,
            first_name = fname,
            middle_name = mname,
            last_name = lname,
            gender = gender,
            contact_no =contactno,
            email_id =emailid,
            egy_contact_no = emcntno,
            guardian_name = gurname,
            guardian_relation = gurrelation,
            guardian_contact_no =gurcntno,
            corres_address = caddress,
            corres_city = ccity,
            corres_pincode = cpincode,
            permanent_address = paddress,
            permanent_city = pcity,
            permanent_pincode = ppincode
        )
        return redirect(admin_view_booking)
    courses=Course.objects.all()
    rooms=Room.objects.all()
    context={
        'courses':courses,
        'rooms':rooms
    }
    return render(request, 'administrator/bookings.html', context)



def admin_manage_students(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if not request.user.is_superuser:
        return redirect('/student/dashboard/')
        
    if request.method == 'POST':
        pass

    if 'view' in request.GET:
        uid=request.GET.get('view')
        student=get_object_or_404(Registration, id=uid)
        # student=Registration.objects.get(id=uid)
        context={
        'student':student
        }
        return render(request,'administrator/students-profile.html',context)
    
    if 'del' in request.GET:
        uid=request.GET.get('del')
        student= get_object_or_404(Registration,id=uid).delete()
        # student=Registration.objects.get(id=uid).delete()
        print("uid",uid, "student:",student)
        return redirect(admin_manage_students)

    registration=Registration.objects.all()

    context={
        'registration':registration
    }
    return render(request, 'administrator/manage-students.html', context)


def admin_manage_rooms(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if not request.user.is_superuser:
        return redirect('/student/dashboard/')
    
    if 'action' in request.GET and 'id' in request.GET:
        uid=request.GET.get('id')
        action=request.GET.get('action')

        if action == 'del':
            rm=get_object_or_404(Room, id=uid)
            rm.delete()
            return redirect(admin_manage_rooms)
        
        elif action == 'edit':
            rm=get_object_or_404(Room, id=uid)
            if request.method == 'POST':
                seater = request.POST['seater']
                fees = request.POST['fees']       
                room = rm
                room.seater = seater
                room.fees = fees
                room.save()
                messages.success(request, 'Room details updated successfully')
                return redirect(admin_manage_rooms)            

            context={
                'room':rm
            }
            return render(request, 'administrator/edit-room.html', context)
        else:
            pass
        context={
        'student':student
        }
        return render(request,'administrator/students-profile.html',context)
    
    if 'del' in request.GET:
        uid=request.GET.get('del')
        student= get_object_or_404(Registration, id=uid).delete()
        # student=Registration.objects.get(id=uid).delete()
        return redirect(admin_manage_rooms)

    if 'new' in request.GET:
        print("NEW")
        if request.method == 'POST':
            seater = request.POST['seater']
            roomno = request.POST['rmno']
            fees = request.POST['fee']
            
            room_exists = Room.objects.filter(room_no=roomno).exists()
            if room_exists:
                messages.error(request, 'Room already exists!')
            else:
                Room.objects.create(seater=seater, room_no=roomno, fees=fees)
                messages.success(request, 'Room has been added')

            return redirect(admin_manage_rooms)
        context={}
        return render(request, 'administrator/add-rooms.html', context)

    rooms=Room.objects.all()

    context={
        'rooms':rooms
    }
    return render(request, 'administrator/manage-rooms.html', context)


def admin_manage_courses(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if not request.user.is_superuser:
        return redirect('/student/dashboard/')
    
    if 'action' in request.GET and 'id' in request.GET:
        uid=request.GET.get('id')
        action=request.GET.get('action')

        if action == 'del':
            courses=get_object_or_404(Course, id=uid)
            courses.delete()
            return redirect(admin_manage_courses)
        
        elif action == 'edit':
            courses=get_object_or_404(Course, id=uid)
            if request.method == 'POST':
                coursecode = request.POST['cc']
                coursesn = request.POST['cns']
                coursefn = request.POST['cnf']
                courses.course_code = coursecode
                courses.course_sn = coursesn
                courses.course_fn = coursefn
                courses.save()
                messages.success(request, 'Room details updated successfully')
                return redirect(admin_manage_courses)            

            context={
                'courses':courses
            }
            return render(request, 'administrator/edit-courses.html', context)

    if 'new' in request.GET:
        if request.method == 'POST':
            coursecode = request.POST['cc']
            coursesn = request.POST['cns']
            coursefn = request.POST['cnf']
            course_exists = Course.objects.filter(course_code=coursecode).exists()
            if course_exists:
                messages.error(request, 'Course already exists!')
            else:
                Course.objects.create(course_code=coursecode, course_sn=coursesn, course_fn=coursefn)
                messages.success(request, 'Course has been added successfully')
            return redirect(admin_manage_courses)
        
        context={}
        return render(request, 'administrator/add-courses.html', context)

    courses=Course.objects.all()
    context={
        'courses':courses
    }
    return render(request, 'administrator/manage-courses.html', context)

def administrator_acc_setting(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if not request.user.is_superuser:
        return redirect('/student/dashboard/')
    
    admin_user,c=Admin.objects.get_or_create(user=request.user)
    context={
        "admin_user":admin_user
    }
    return render(request, 'administrator/acc-setting.html', context)