from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Choice, Question
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    #automatically generated context variable is question_list. 
    #To override this we provide the context_object_name attribute, 
    #specifying that we want to use latest_question_list instead
    context_object_name = 'latest_question_list'

    def get_query_set(self):
        #return last five published question
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    # DetailView generic view expects the primary key value captured from the URL to be called "pk"
    # DetailView generic view uses a template called <app name>/<model name>_detail.html.
    #"polls/question_detail.html"
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        #request.POST['choice'] returns the ID of the selected choice, as a string
        #keyError if choice not provided in POST data
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data. 
        # This prevents data from being posted twice if a user hits the Back button.
        # reverse function helps avoid having to hardcode a URL in the view function.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    return HttpResponse("You're voting on question %s." % question_id)

