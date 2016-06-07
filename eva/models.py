from passlib.hash import pbkdf2_sha256
from django.db import models
from datetime import datetime


from settings import LOGGING_DIR

class DraftHeader(models.Model):
    headerID = models.AutoField(primary_key=True)
    headerName = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)
    fachrichtung = models.CharField(max_length=30)
    stufe = models.IntergerField() # 1 = Unterstufe, 2 = Mittelstufe, 3 = Oberstufe
    fach = models.CharField(max_length = 30)
    erstellungsdatum = models.DateField()
    beschreibung = models.CharField(max_length = 500)
    sichtbarkeit = models.BooleanField()

    def add_group(self):
        pass
    
    def update_from_request(self, request):
        pass
    
    def delete_group(self, groupID):
        pass
    
    def create_survey(self):
        pass
    
    @classmethod
    def getHeader(cls, headerID):
        return cls.objects.getGroups.get(headerID = headerID)
    
    def getGroups(self):
        return DraftGroups.objects.filter(headerID = self.headerID)
    
class DraftGroups(models.Model):
    headerID = models.ForeignKey(DraftHeader, on_delete=models.CASCADE)
    groupID = models.IntegerField()
    text = models.CharField(max_length = 30, default='')
    
    def get_questions(self):
        return DraftQuestion.objects.filter(groupID = self.groupID, headerID = self.headerID)
    
    def add_question(self):
        pass
    
    def delete_question(self, questionID):
        for qu in self.get_questions():
            if qu.questionID == questionID:
                qu.delete()
            if qu.questionID > questionID:
                qu.questionID = qu.questionID -1
            else
                continue
            qu.save()
    
    def update_from_request(self, request):
        text = request.GET.get('text', '')
    
    def add_question_from_pool(self, pool_question):
        pass
    
    
class DraftQuestion (models.Model):
    headerID = models.ForeignKey(DraftHeader, on_delete=models.CASCADE)
    groupID = models.ForeignKey(DraftGroups, on_delete=models.CASCADE)
    questionID = models.IntegerField()
    questionText = models.CharField(max_length = 50)
    answerType = models.CharField(max_length = 4) # Text, J/N, Note
    
    @classmethod
    def get_next_id(cls, header, group):
        # TODO get max 
        pass
    
def get_draft_model(header_id, group_id=None, qu_id=None):
    model = DraftHeader.objects.get(header_id=header_id)
    if not group_id:
        return model
    model.get_goup(group_id)
    if not group_id:
        return model
    return model.get_question(qu_id) 
    
###############################################################################    
    
class ActiveDraftHeader(models.Model):
    headerID = models.AutoField(primary_key=True)
    headerName = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)
    fachrichtung = models.CharField(max_length=30)
    stufe = models.IntergerField() # 1 = Unterstufe, 2 = Mittelstufe, 3 = Oberstufe
    fach = models.CharField(max_length = 30)
    erstellungsdatum = models.DateField()
    beschreibung = models.CharField(max_length = 500)
    startdatum = models.DateField()
    enddatum = models.DateField()
    teilnehmer = models.IntegerField()

    @classmethod
    def getHeader(cls, headerID):
        return cls.objects.getGroups.get(headerID = headerID)
    
    def getGroups(self):
        return DraftGroups.objects.filter(headerID = self.headerID)
    
    
class AciveDraftGroups(models.Model):
    headerID = models.ForeignKey(DraftHeader, on_delete=models.CASCADE)
    groupID = models.IntegerField()
    groupName = models.CharField(max_length = 30)

    def getQuestions(self):
        return DraftQuestion.objects.filter(groupID = self.groupID, headerID = self.headerID)
    
    
class ActiveDraftQuestion (models.Model):
    headerID = models.ForeignKey(DraftHeader, on_delete=models.CASCADE)
    groupID = models.ForeignKey(DraftGroups, on_delete=models.CASCADE)
    questionID = models.IntegerField()
    questionText = models.CharField(max_length = 50)
    answerType = models.CharField(max_length = 4) # Text, J/N, Note  
      

###############################################################################

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
        if pbkdf2_sha256.Xverify(psw, user_model.psw):
            return True
        except cls.NOT_FOUND, e:
            pass
        return False
    

class Departments(models.Model, ListabelModel):
    option = models.CharField(primary_key=True, max_length=20)