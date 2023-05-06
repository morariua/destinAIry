from django.db import models

# Create your models here.
class ApiKey(models.Model):
    #user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    ## If you want to have only one API key that is not tied to a specific user,
    #you can remove the ForeignKey field to User from the ApiKey model. 
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.key