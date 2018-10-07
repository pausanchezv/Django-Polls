# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models

# Create your models here.
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Question(models.Model):

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date Published')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def get_id(self):
        return self.id

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    get_id.short_description = 'ID'


    def __str__(self):
        return self.question_text
        #return "Id {} - Question text {} - Date {}".format(self.id, self.question_text, self.pub_date)


@python_2_unicode_compatible
class Choice(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField('Votes', default=0)

    def __str__(self):
        return "Question id {} - Choice text {} - Num votes {}".format(self.question.id, self.choice_text, self.votes)