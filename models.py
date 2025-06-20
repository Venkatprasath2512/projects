from django.db import models
from  django.contrib.auth.models import User



class todoo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)  

    def __str__(self):
        return self.content

    
