from django.db import models

class MissingChild(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(default=0)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')
    image = models.ImageField(upload_to='')
    image_encoding = models.BinaryField()
    date_missing = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    last_seen = models.CharField(max_length=100)
    guardian_name = models.CharField(max_length=100)
    guardian_contact = models.CharField(max_length=50)
    isverified = models.BooleanField(default=False)

    class Meta:
        unique_together = ('name', 'age', 'gender', 'date_missing')
        
    def __str__(self):
        return self.name
    
class FoundPerson(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
     
    name = models.CharField(max_length=100, default="Unknown")
    image = models.ImageField(upload_to='found_person')
    place_found = models.CharField(max_length=100)
    date_found = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')
    time_found = models.TimeField()
    image_encoding = models.BinaryField()
    samaritan_name = models.CharField(max_length=100)
    samaritan_contact = models.CharField(max_length=50)
    isverified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name