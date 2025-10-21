from django.db import models
from django.utils import timezone

# Create your models here.
class Farmer(models.Model):
    name = models.CharField(max_length=50)
    farm = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    
    class Meta:
        db_table = 'farmer'
    
    def __str__(self):
        return f"{self.name}, {self.farm}"

class Student(models.Model):
        """Student model for registering students in the attendance app."""
        name = models.CharField(max_length=100)
        age = models.IntegerField(null=True, blank=True)
        address = models.CharField(max_length=255, null=True, blank=True)
        phone_number = models.CharField(max_length=20, null=True, blank=True)
        email = models.EmailField(null=True, blank=True)
        school = models.CharField(max_length=150, null=True, blank=True)
        notes = models.TextField(null=True, blank=True)

        class Meta:
            db_table = 'student'

        def __str__(self):
            return self.name

class Attendance(models.Model):
    date = models.DateField(default=timezone.now)
    is_present = models.BooleanField(default=False)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'attendance'
    
    def __str__(self):
        return f"{self.farmer.name} - {self.date}"