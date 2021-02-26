from django.db import models

# Create your models here.

def nameFile(instance,filename):
    # print(filename)
    return "/".join(['images',filename])

class UploadImage(models.Model):
    
    image = models.ImageField(upload_to=nameFile, blank=True,null=True)

