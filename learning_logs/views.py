from django.http.response import Http404
from django.shortcuts import redirect, render
from .models import Entry, Topic
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    """ home of learning_log """
    return render(request, "learning_logs/index.html")

@login_required
def topics(request):
    """ show all topics """
    # topics = Topic.objects.order_by('date_added')
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """ show detail of specific topic """
    topic = Topic.objects.get(id = topic_id)
    # check owner
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {"topic": topic, "entries":entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """ add a new topic """
    if request.method != 'POST':
        """ not submit dada create a new form """
        form = TopicForm()
    else:
        """ handle dada """
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            form.save()
            return redirect('learning_logs:topics')


    """ show empty form or show form is invalid """
    context = {'form':form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """ add a new entry for specific topic """
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        """ not submit dada create a new form """
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.owner = request.user
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)


    """ show empty form or show form is invalid """
    context = {'topic':topic, 'form':form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """ edit exist entry """
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        """ first request, use present form """
        form = EntryForm(instance=entry)
    else:
        """ handle data """
        form = EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)


    """ show empty form or show form is invalid """
    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)


