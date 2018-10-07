# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Question, Choice

# Inlines
class ChoiceInline(admin.TabularInline):
    model = Choice


class QuestionChoices(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']

    inlines = [ChoiceInline]


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]

    inlines = [ChoiceInline]
    list_filter = ['pub_date']
    search_fields = ['question_text']
    list_display = ('question_text', 'get_id', 'pub_date', 'was_published_recently')

# /Inlines


# Registrations
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)