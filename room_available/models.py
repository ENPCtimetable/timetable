from django.db import models

# Create your models here.


class Room_type(models.Model):
    type_name = models.CharField(max_length=100)
    def __str__(self):
        return self.type_name


class Room(models.Model):
   room_name = models.CharField(max_length=100)
   room_type = models.ForeignKey('Room_type')
   def __str__(self):
        return self.room_name

