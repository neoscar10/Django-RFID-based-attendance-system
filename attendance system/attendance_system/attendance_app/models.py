from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    stack = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    card_uid = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    time_in = models.DateTimeField(blank=True, null=True)
    time_out = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return f"{self.user.name} - {self.timestamp}"




# 90 DB E6 20
# F3 89 08 A8
# http://your-django-backend-url/api/register-card/

##417690
# #ffc

# "Airtel 4G MiFi_7FEF";
# const char* password = "50291613";  
# C3 6D E9 A5 