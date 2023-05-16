
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

User = settings.AUTH_USER_MODEL

class User(AbstractUser):
    is_advocate = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)

class Client(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
class Advocate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    license_number = models.CharField(max_length=20, null=True, blank=True)
    office_address = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True, default='None')
    experience = models.CharField(max_length=2, null=True, blank=True, default='None')
    SPECIFICATIONS = (
        ('Civil', 'Civil'),
        ('Criminal', 'Criminal'),
        ('Consumer', 'Consumer'),
        ('Labour/Employment', 'Labour/Employment'),
        ('Intellectual Property Rights', 'Intellectual Property Rights'),
        ('Family', 'Family'),
        ('Corporate', 'Corporate'),
        ('Taxation', 'Taxation'),
    )
    Languages = (
        ('English', 'English'),
        ('Hindi', 'Hindi'),
        ('Tamil', 'Tamil'),
        ('Kannada', 'Kannada'),
        ('Telugu', 'Telugu'),
    )

    specifications = models.CharField(max_length=100, choices=SPECIFICATIONS, default='None')
    languages = models.CharField(max_length=20, choices=Languages, default='None')
    description = models.TextField(default='None')
    pimage = models.ImageField(default='default.jpg', upload_to='media')
    dob = models.DateField(null=True, blank=True)
    court = models.CharField(max_length=200, null=True, blank=True, default='None')

    def __str__(self):
        return self.user.username

class Clientcase(models.Model):
    case_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    proof = models.FileField(upload_to='media', null='true', blank='true')
    last_modified = models.DateTimeField(auto_now_add=True)
    is_requested=models.BooleanField(default=False)
    is_pending=models.BooleanField(default=False)
    is_accepted=models.BooleanField(default=False)
    is_rejected=models.BooleanField(default=False)
    is_notrequested=models.BooleanField(default=True)
    defendant_name = models.CharField(max_length=200)
    defendant_address = models.CharField(max_length=300)

    type = (
        ('Civil', 'Civil'),
        ('Criminal', 'Criminal'),
        ('Consumer', 'Consumer'),
        ('Labour/Employment', 'Labour/Employment'),
        ('Intellectual Property Rights', 'Intellectual Property Rights'),
        ('Family', 'Family'),
        ('Corporate', 'Corporate'),
        ('Taxation', 'Taxation'),
    )

    case_type = models.CharField(max_length=100, choices=type, default='N/A')


    def __str__(self):
        return self.title

class Clientprofiles(models.Model):
    user= models.OneToOneField(User, on_delete = models.CASCADE)
    house_name=models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    district= models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    postoffice = models.CharField(max_length=200)
    picode=models.CharField(max_length=20)
    pimage = models.ImageField(default='default.jpg', upload_to='media')
    adult = models.BooleanField(default=False)
    date_of_birth = models.DateField(default=None)
    def is_adult(self):
        import datetime
        if (datetime.date.today() - self.date_of_birth) > datetime.timedelta(days=18 * 365):
            self.adult = True

    def save(self, *args, **kwargs):
        self.is_adult()
        super(Clientprofiles, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class Clientfeedback(models.Model):

    feeddback_choices = [('good','good'),
               ('average','average'),
               ('execellent','execellent'),
               ('bad','bad'),
               ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating=models.CharField(max_length=20,choices=feeddback_choices)
    description = models.TextField()

class contactus(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    message=models.TextField()

    def __str__(self):
        return self.name


class Schedule(models.Model):
    advocate = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.CharField(max_length=200)

class CaseAssignment(models.Model):
    case = models.ForeignKey(Clientcase, on_delete=models.CASCADE)
    advocate = models.ForeignKey(Advocate, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('case', 'advocate')


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    advocate = models.ForeignKey(Advocate, on_delete=models.CASCADE, related_name='reviews_received')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reviews_given')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.user.first_name} {self.client.user.last_name}'s review of Advocate {self.advocate.user.first_name} {self.advocate.user.last_name}"




class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)



class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)

class Defendant(models.Model):
    name = models.CharField(max_length=255,default='N/A')
    address = models.CharField(max_length=255,default='N/A')
    phone_number = models.CharField(max_length=20,default='N/A')
    email = models.EmailField(default='N/A')

    def __str__(self):
        return self.name
class Court(models.Model):
    name = models.CharField(max_length=255,default='N/A')
    year = models.IntegerField(default='N/A')

    def __str__(self):
        return self.name
class Judge(models.Model):
    name = models.CharField(max_length=255,default=None)

    def __str__(self):
        return self.name
class filed_lawsuits(models.Model):
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    refference = models.ForeignKey(Clientcase,on_delete=models.CASCADE)
    title = models.CharField(max_length=255,default=None)
    sub_title =  models.CharField(max_length=255,default=None)
    description = models.TextField(default=None)
    date_filed = models.DateField(default=None)
    # court = models.CharField(max_length=255,default=None)
    cnr = models.CharField(max_length=255,default=None)
    judges = models.ManyToManyField('Judge', blank=True)
    status = models.CharField(max_length=255,default=None)
    outcome = models.CharField(max_length=255,default=None)
    defendants = models.ManyToManyField(Defendant, blank=True)
    courts = models.ManyToManyField(Court, blank=True)


    def __str__(self):
        return self.title

