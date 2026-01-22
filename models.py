from django.db import models
from datetime import date

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    dob = models.DateField()
    role = models.CharField(max_length=10, choices=[('Worker', 'Worker'), ('Employer', 'Employer')])
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Job(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    date = models.DateField()
    pay = models.IntegerField()
    pay_type = models.CharField(max_length=10, choices=[('Fixed', 'Fixed'), ('Hourly', 'Hourly')])
    category = models.CharField(max_length=50)
    required_workers = models.IntegerField(default=1)
    
    # Link to the Employer who posted it
    employer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posted_jobs')
    
    # Store Applicants (Many-to-Many relationship)
    applicants = models.ManyToManyField(UserProfile, related_name='applied_jobs', blank=True)

    def __str__(self):
        return self.title

    # Helper to count applicants
    def applicant_count(self):
        return self.applicants.count()

    # Helper to check if full
    def is_full(self):
        return self.applicants.count() >= self.required_workers