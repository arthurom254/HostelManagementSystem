from django.db import models
from django.contrib.auth.models import User

class Admin(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    updation_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"User-{self.user}"


class AdminLog(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    ip = models.BinaryField(max_length=16)
    login_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Admin Logs {self.admin}"


class Course(models.Model):
    course_code = models.CharField(max_length=255)
    course_sn = models.CharField(max_length=255)
    course_fn = models.CharField(max_length=255)
    posting_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course_code} {self.course_fn}"

class Registration(models.Model):
    room_no = models.IntegerField()
    seater = models.IntegerField()
    fees_pm = models.IntegerField()
    food_status = models.IntegerField()
    stay_from = models.DateField()
    duration = models.IntegerField()
    course = models.CharField(max_length=500)
    reg_no = models.CharField(max_length=255)
    first_name = models.CharField(max_length=500)
    middle_name = models.CharField(max_length=500, blank=True, null=True)
    last_name = models.CharField(max_length=500)
    gender = models.CharField(max_length=250)
    contact_no = models.BigIntegerField()
    email_id = models.EmailField()
    egy_contact_no = models.BigIntegerField()
    guardian_name = models.CharField(max_length=500)
    guardian_relation = models.CharField(max_length=500)
    guardian_contact_no = models.BigIntegerField()
    corres_address = models.CharField(max_length=500)
    corres_city = models.CharField(max_length=500)
    corres_state = models.CharField(max_length=500)
    corres_pincode = models.IntegerField()
    permanent_address = models.CharField(max_length=500)
    permanent_city = models.CharField(max_length=500)
    permanent_state = models.CharField(max_length=500, blank=True, null=True)
    permanent_pincode = models.IntegerField(blank=True, null=True)
    posting_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room reg:{self.reg_no} seater: {self.seater}"

class Room(models.Model):
    seater = models.IntegerField()
    room_no = models.IntegerField(unique=True)
    fees = models.IntegerField()
    posting_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Room{self.room_no} for {self.seater} students. price:{self.fees}"

class State(models.Model):
    state = models.CharField(max_length=150, blank=True, null=True)
    
    def __str__(self):
        return f"{self.state}"


class UserRegistration(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    contact_no = models.BigIntegerField(blank=True, null=True)
    updation_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    pass_update_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user} {self.reg_no}"

class UserLog(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    user_ip = models.CharField(max_length=16)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    login_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user} {self.user_ip}"