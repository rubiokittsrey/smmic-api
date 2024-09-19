from django.db import models, transaction
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
import uuid
class AppUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, province, city, barangay, zone, zip_code, email, password=None):
            if not email:
                raise ValueError('An Email is Required')
            if not password:
                raise ValueError('A Password is Required')
            
            email = self.normalize_email(email)
            user = self.model(
                 first_name=first_name, 
                 last_name=last_name,
                 province=province, 
                 city=city, 
                 barangay=barangay, 
                 zone=zone, 
                 zip_code=zip_code,
                 email=email)

            user.set_password(password)
            user.save()

            return user
    def create_superuser(self, email, password=None):
            if not email:
                raise ValueError('An email is required.')
            if not password:
                raise ValueError('A password is required.')
            
            user = self.create_user(email,password)

            user.is_superuser = True
            user.is_staff = True
            user.save()

            return user
    

class CustomUser(AbstractBaseUser,PermissionsMixin):
    UID = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100)
    zone = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=4)
    email=models.EmailField(max_length=255,unique=True)
    password=models.CharField(max_length=288)
    profilepic = models.ImageField(upload_to='profile_pictures', default='default.png')



    is_staff=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = AppUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','province','city','barangay','zone','zip_code']
    objects = AppUserManager()

    def __str__(self):
        return self.email
    
class SinkNode(models.Model):
    SKID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    SK_Name = models.CharField(max_length=100, blank=True, null=True)
    increment_id = models.IntegerField(editable=False, unique=True)  # Custom auto-increment field
    User = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    area_address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)

    #For adding numbers if devcice has no name
    def save(self, *args, **kwargs):
        if not self.increment_id:
            last_increment_id = SinkNode.objects.all().aggregate(models.Max('increment_id'))['increment_id__max']
            self.increment_id = (last_increment_id or 0) + 1
        
        if not self.SK_Name:
            self.SK_Name = f"Sink Node_{self.increment_id}"
        
        super(SinkNode, self).save(*args, **kwargs)

    def __str__(self):
        return self.SK_Name

         
        


class SensorNode(models.Model):
     SNID = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
     SinkNode = models.ForeignKey(SinkNode,on_delete= models.CASCADE, related_name='sensor_nodes')
     SensorNode_Name = models.CharField(max_length=100,blank= True, null=True)
     latitude = models.DecimalField(max_digits=9, decimal_places=6)
     longitude = models.DecimalField(max_digits=9, decimal_places=6)
     increment_id = models.IntegerField(editable=False, unique=False)
     

     def save(self,*args,**kwargs):
          if not self.increment_id:
               last_increment_id = SensorNode.objects.filter(SinkNode = self.SinkNode).aggregate(models.Max("increment_id"))['increment_id__max']
               self.increment_id = (last_increment_id or 0) + 1
        
          if not self.SensorNode_Name:
               self.SensorNode_Name = f"Sensor Node{self.increment_id}"

          super(SensorNode, self).save(*args, **kwargs)

     def __str__(self):
          return f"{self.SinkNode.SK_Name} - {self.SensorNode_Name}"     

class SKReadings(models.Model):
     Sink_Node = models.ForeignKey(SinkNode,on_delete=models.CASCADE)
     battery_level = models.DecimalField(max_digits=10, decimal_places=7)
     timestamp = models.DateTimeField(auto_now_add=False)

class SMSensorReadings(models.Model):
     Sensor_Node = models.ForeignKey(SensorNode,on_delete=models.CASCADE)
     battery_level = models.DecimalField(max_digits=10, decimal_places=7)
     timestamp = models.DateTimeField(auto_now_add=False)
     soil_moisture = models.DecimalField(max_digits=10, decimal_places=7)
     temperature = models.DecimalField(max_digits=10, decimal_places=7)
     humidity = models.DecimalField(max_digits=10, decimal_places=7)

#class AirQualitySensor(models.Model):
     #other attributes







