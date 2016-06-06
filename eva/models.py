from passlib.hash import pbkdf2_sha256
from django.db import models
from datetime import datetime


from settings import LOGGING_DIR

<<<<<<< HEAD
class DraftHeader(models.Model):
    id = models.AutoField(primary_key=True)
    
    
    
    

=======
>>>>>>> parent of 624821c... Revert "start"
class User (models.Model):
    user = models.CharField(max_length=200,primary_key=True)
    psw = models.CharField(max_length=34)
    
    def __str__(self):
        return self.user 
    
    def save(self, force_insert=False, force_update=False, using=None, 
             update_fields=None):
        with open(LOGGING_DIR + 'models.User.log', 'b') as f:
            f.write('Der user: %s wurde angeleget' % self.user)
            
        return models.Model.save(self, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
    
    @classmethod
    def create(cls, user, psw):
        cls.objects.create(user=user,psw=cls.to_hash(psw)).save()
        
    
    @classmethod
    def to_hash(cls, psw):
        return pbkdf2_sha256.encrypt(psw,rounds=20000)
    
    @classmethod
    def autenticate(cls, user, psw):
        try:
            user_model = cls.objects.get(user=user)
        if pbkdf2_sha256.verify(psw, user_model.psw):
            return True
        except cls.NOT_FOUND, e:
            pass
        return False
    
    
class DraftHeader(models.Model):
    
    department = models.ForeignObject(Departments, null=True)
    
    def to_fields(self):
        '''
        {
            'name' : 'name der umfrage',
            'field_name' : 'name'                     # for parameter name http get
            'default' : 'option1',
            'type' : '',                             # text, option, calender
            'optinon' : ['option1', 'option2', ...],     # only if type == option
        }
        '''
        return  {
            'department' : {
                'name' : 'Fachbereich',
                'field_name' : 'department',
                'default' : self.department,
                'type' : 'option',
                'optinon' : Departments.as_list(),
            },
        }
        
class ListabelModel:
    @classmethod
    def as_list(cls):
        return [model.option for model in cls.objects.all()]1
         
    
class Departments(models.Model, ListabelModel):
    option = models.CharField(primary_key=True, max_length=20)