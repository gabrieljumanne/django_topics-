from django.db import models
from django.utils import timezone
from datetime import date, time, timedelta

# Create your models here.

# illustration of recursive model using many-to-one relationship 
# company - employee management system 

class Employee(models.Model):
    name = models.CharField("Employee name", max_length=100, null=False)
    job_title = models.CharField("Job Title", max_length=100, null=False)
    team = models.ForeignKey('Team', on_delete= models.CASCADE, related_name= "team_members" )
    
    def __str__(self) -> str:
        return f"{self.name} ({self.team})"
    

class Team(models.Model):
    name = models.CharField("Team name", max_length=100, null=True )
    lead = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="team_members")
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name="teams")
    
    def __str__(self) -> str:
        return f"{self.name} ({self.department})"
    

class Department(models.Model):
    name = models.CharField("Department name", max_length=100)
    manager = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True, related_name="departments" )
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='departments')

    

class Company(models.Model):
    name = models.CharField(max_length=100)
    ceo = models.OneToOneField("Employee", on_delete=models.CASCADE, related_name="company")
    







