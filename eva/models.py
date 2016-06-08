from passlib.hash import pbkdf2_sha256
from django.db import models
import uuid
from django.db.models import Max
import re

from settings import LOGGING_DIR

class DraftHeader(models.Model):
    headerID = models.AutoField(primary_key=True)
    headerName = models.CharField(max_length=30, default='')
    autor = models.CharField(max_length=30, default = '')
    fachrichtung = models.CharField(max_length=30, default = '')
    stufe = models.IntegerField(null = True) 
    # 1 = Unterstufe, 2 = Mittelstufe, 3 = Oberstufe
    fach = models.CharField(max_length = 30, null = True)
    erstellungsdatum = models.DateField(null = True)
    beschreibung = models.CharField(max_length = 500, default = '')
    sichtbarkeit = models.CharField(max_length=1,null = True)

    @classmethod
    def get_tabel_dict(cls, filter):
        '''
        
        filter - {autor : SWagner}
        
        -> {'tabel' : [
             ['umfrage1','24-01-2017',''],
             ['umfrage1','24-01-2017',],],}

        '''
        rows = []
        for row in DraftHeader.objects.filter(**filter):
            rows.append([
                row.headerID, row.headerName, row.erstellungsdatum, 
                row.fach, row.fachrichtung, row.stufe,
            ])
        return {'tabel' :  rows,}

    def get_edit_dict(self):
        return [
            self.headerID, self.erstellungsdatum, self.name, 
            self.sichtbarkeit, self.fach, self.fachrichtung, self.stufe,
        ]

    def add_group(self):
        DraftGroups.objects.create(headerID = self, groupID = DraftGroups.nextGroupID(headerID=self))
    
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
    
    def get_goup(self, goup_id):
        return DraftGroups.objects.get(headerID=self,groupID=goup_id)
    
class DraftGroups(models.Model):
    headerID = models.ForeignKey(DraftHeader, on_delete=models.CASCADE)
    groupID = models.IntegerField()
    text = models.CharField(max_length = 30, default='')
    
    @classmethod
    def nextGroupID(cls, headerID):
        result = cls.objects.filter(headerID = headerID).aggregate(Max('groupID'))['groupID__max']
        if not result:
            return 1 
        return result + 1
    
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
            else:
                continue
            qu.save()
    
    def update_from_request(self, request):
        self.text = request.GET.get('text', '')
        self.save()
    
    def add_question_from_pool(self, pool_question):
        pass
    
    def get_edit_dict(self):
        return [self.groupID, self.text,]
    
class DraftQuestion (models.Model):
    headerID = models.ForeignKey(DraftHeader, on_delete=models.CASCADE)
    groupID = models.ForeignKey(DraftGroups, on_delete=models.CASCADE)
    questionID = models.IntegerField()
    questionText = models.CharField(max_length = 50, default = '')
    answerType = models.CharField(max_length = 4 ,default = '')                 # Text, J/N, Note
    
    @classmethod
    def nextQuestionID(cls, headerID, groupID):
        result = cls.objects.filter(groupID = groupID, headerID = headerID).aggregate(Max('questionID'))
        return result.get('questionID__max', 0) + 1
    
    def get_edit_dict(self):
        return [self.questionID, self.text, self.answerType,]
       
###############################################################################    
    
class ActiveDraftHeader(models.Model):
    headerID = models.AutoField(primary_key=True)
    headerName = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)
    fachrichtung = models.CharField(max_length=30)
    stufe = models.IntegerField() # 1 = Unterstufe, 2 = Mittelstufe, 3 = Oberstufe
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
        ''
        return DraftGroups.objects.filter(headerID = self.headerID)
    
    def count_active(self):
        pass
    
    def get_csv_table(self):
        result = []
        for goup in self.getGroups():
            for question in goup.getQuestions():
                result.append(question.to_csv_row())
                
        return result

        
    def create_answers(self, request):
        for name, value in request.POST.items():
            if not value:
                continue
            group_id, question_id = _resolve_to_pos(name)
            qu = get_survey_model(self.headerID, group_id, question_id)
            qu.create_answer(value, self) 
        

PATTERN_POS = re.compile(r'(\d+)-(\d+)')

def _resolve_to_pos(input_name):
    m = re.match(PATTERN_POS, input_name)
    return (m.group(1), m.group(2))
        
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
    
    def to_csv_row(self):
        desciption = '%i-%i: %s' % (self.groupID.groupID, self.questionID, self.questionText)
        row = None
        
        if self.answerType == 'Text':
            row = [answer.rs_text for answer in self.get_answers()]
        elif self.answerType == 'J/N':
            row = [
                'JA: %i' % sum(answer for answer in self.get_answers() if answer.rs_bool == 'y'),
                'NEIN: %i' % sum(answer for answer in self.get_answers() if answer.rs_bool == 'n'),
            ]
        elif self.answerType == 'Note':
            counts = {}
            for answer in self.get_answers():
                counts[answer.rs_range] = counts.get(answer.rs_range, 0) + 1 
            row = [
                '1: %i' % counts.get(1, 0),
                '2: %i' % counts.get(2, 0),
                '3: %i' % counts.get(3, 0),
                '4: %i' % counts.get(4, 0),
                '5: %i' % counts.get(5, 0),
                '6: %i' % counts.get(6, 0),
            ]
        return row
    
    def get_answers(self):
        return Answer.objects.filter(header=self.headerID, group=self.groupID, question=self.questionID)
    
class Answer(models.Model):
    answerID = models.AutoField()
    header = models.ForeignKey(ActiveDraftHeader, on_delete=models.CASCADE)
    group = models.ForeignKey(AciveDraftGroups, on_delete=models.CASCADE)
    question = models.ForeignKey(ActiveDraftQuestion, on_delete=models.CASCADE)
    
    rs_text = models.CharField(max_length=30, null=True)
    rs_range = models.IntegerField(null=True)
    rs_bool = models.CharField(max_length=1, null=True)     # y : true, n = false
    
    @classmethod
    def create_answer(cls, value, question):
        new_answer = cls.objects.create(header=question.headerID,group=question.groupID, question=question)
        if question.answerType == 'Text':
            new_answer.rs_text = value
        if question.answerType == 'J/N':
            new_answer.rs_bool = value
        if question.answerType == 'Note':
            new_answer.rs_range = int(value)
             
    

class SurveyMember(models.Model):
    header = models.ForeignKey(ActiveDraftHeader)
    token = models.CharField(max_length=32)
    
    @classmethod
    def create_token(cls, cnt_tokens, header):
        token_list = [SurveyMember.get_token() for i in range(cnt_tokens)]
        for token in token_list:
            cls.objects.create(header=header, token=token)
        return token_list
    
    @classmethod
    def check(cls, token, header):  
        try:
            cls.objects.get(token=token, header=header)
            return True
        except cls.DoesNotExist as e:
            pass
        return False
        
        
    
    @classmethod
    def get_token(cls):  
       return uuid.uuid4().hex 
   
   
###############################################################################

class User (models.Model):
    user = models.CharField(max_length=200,primary_key=True)
    psw = models.CharField(max_length=34)
    
    def __str__(self):
        return self.user 
    
    
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
        except cls.DoesNotExist, e:
            pass
        return False
    
class Departments(models.Model):
    option = models.CharField(primary_key=True, max_length=20)
    
    @classmethod
    def to_list_(cls):
        return [option for option in cls.objects.all()]


def get_draft_model(header_id, group_id=None, question_id=None):
    return _get_model(DraftHeader.objects.get(headerID=header_id), group_id, question_id)


def get_survey_model(header_id, group_id=None, question_id=None):
    return _get_model(ActiveDraftHeader.objects.get(id=header_id), group_id, question_id)

def _get_model(header_model, group_id, question_id):
    if not group_id:
        return header_model
    model = header_model.get_goup(group_id)
    if not question_id:
        return model
    return model.get_question(question_id) 


