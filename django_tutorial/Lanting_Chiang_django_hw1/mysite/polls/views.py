from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
#from django.template import loader
from .models import Question, Choice

# Create your views here.

#ListView - list of objects
class IndexView(generic.ListView):
  template_name = 'polls/index.html'
  context_object_name = 'latest_question_list'

#get_queryset is method of ListView; gets items for this view (takes in iterable)
  def get_queryset(self):
    return Question.objects.order_by('-pub_date')[:5]

#DetailView - display detail page for particular type of object
#expects promary key value from url to be called "pk" (set in urls.py)
#uses template called <app name>/<model name>/_detail.html by default
class DetailView(generic.DetailView):
  #generic view needs to know the model that the view will act upon
  model = Question
  #set template_name attribute to use this specific template instead of default
  template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
  model = Question
  template_name = 'polls/results.html'

"""
def index(request):
  latest_question_list = Question.objects.order_by('-pub_date')[:5]
  #template = loader.get_template('polls/index.html')
  context = {
    'latest_question_list': latest_question_list,
  }
  #return HttpResponse(template.render(context, request))
  #returns HttpResponse object of given template rendered with goven context
  return render((request, 'polls/index.html', context))

def detail(request, question_id):
  
  try:
    question = Question.objects.get(pk=question_id)
  except Question.DoesNotExist:
    raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/detail.html', {'question':question})

def results(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/results.html', {'question':question})
"""

def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    #access submitted data with request.POST(keyname); returns ID of selected choice as string
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  #check for KeyError raised by request.POST if choice wasn't provided in POST data
  except (KeyError, Choice.DoesNotExist):
    return render(request, 'polls/detail.html', {
      'question':question,
      'error_message': "You didn't select a choice."
    }) 
  else:
    selected_choice.votes += 1
    selected_choice.save()
    #return HttpResponseRedirect after POST to prevent posting twice if use hits back button
    #HttpResponseRedirect takes in the URL the user will be redirected to
    #args=(question.id) is variable portion of URL pattern that points to the results view
    #returns string 'polls/:id/results'
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
