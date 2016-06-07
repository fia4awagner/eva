from django.db import models
from passlib.hash import pbkdf2_sha256

from settings import LOGGING_DIR

PBKDF2_SHA256_HASROUNDS=20000

class Design_Umfrage_Knkopf(models.Model):
    id = models.AutoField(primary_key=True)

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
        return pbkdf2_sha256.encrypt(psw, rounds=PBKDF2_SHA256_HASROUNDS)
    
    @classmethod
    def autenticate(cls, user, psw):
        try:
            user_model = cls.objects.get(user=user)
            if pbkdf2_sha256.verify(psw, user_model.psw):
                return True
        except cls.NOT_FOUND, e:
            pass
        return False
    
    
