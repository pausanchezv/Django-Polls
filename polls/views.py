# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect

from django.utils import timezone


# Create your views here.

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from polls.models import Question, Choice


def index(request):

    question_list = Question.objects.all().order_by('-pub_date')

    context = {
        'question_list': question_list
    }

    return render(request, 'index.html', context)


def detail(request, question_id):

    '''try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("This question does not exist")'''

    question = get_object_or_404(Question, id=question_id)

    context = {
        'question': question
    }

    return render(request, 'detail.html', context)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {'question': question})


def vote(request, question_id):

    question = get_object_or_404(Question, pk=question_id)

    context = {
        'question': question
    }

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        context.update({'error_message': 'No choice selected'})

    else:
        #selected_choice.votes += 1
        selected_choice.votes = F('votes') + 1
        selected_choice.save()

    #return redirect('/polls/{}/results'.format
    return HttpResponseRedirect(reverse('results', args=(question.id,)))



class DetailView(generic.DetailView):
    model = Question
    template_name = 'detail.html'

    # 404 for future questions
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())




class ResultsView(generic.DetailView):
    model = Question
    template_name = 'results.html'


'''class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'context'

    context = {'pau': 'paaaaau', 'la': 122, 'question_list': Question.objects.order_by('-pub_date')}

    def get_queryset(self):
        return self.context'''

class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        #return Question.objects.order_by('-pub_date')

        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')

