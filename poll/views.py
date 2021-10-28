from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from .models import Poll,Vote

def home(request):
    voted_id=[]
    voted=[]
    if request.user.is_authenticated:
        voted = Vote.objects.filter(name=request.user,status=True)
        for each in voted:
            voted_id.append(each.poll.id)

    if len(voted)>0:
        polls = Poll.objects.filter().exclude(id__in=voted_id)
    else:
        polls = Poll.objects.all()

    context = {'polls': polls,'voted':voted}
    return render(request, 'home.html', context)

@login_required(login_url="/accounts/Login/")
def create(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body)
        question = jsondata['question']
        options = jsondata['options']
        options_count = [0]*len(options)
        poll = Poll()
        poll.question=question
        poll.options=options
        poll.options_count=options_count
        poll.save()
        return redirect('poll:home')

    return render(request, 'create.html')

@login_required(login_url="/accounts/Login/")
def edit(request,poll_id):
    poll = Poll.objects.get(pk=poll_id)
    if request.method == 'POST':
        jsondata = json.loads(request.body)
        question = jsondata['question']
        options = jsondata['options']
        options_count = [0]*len(options)

        Vote.objects.filter(poll=poll).delete()

        poll.question=question
        poll.options=options
        poll.options_count=options_count
        poll.save()

        return redirect('poll:home')

    context = {'poll': poll}
    return render(request, 'edit.html', context)

@login_required(login_url="/accounts/Login/")
def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':
        selected_option = request.POST['poll']
        if selected_option:
            poll.options_count[int(selected_option)-1] += 1
            poll.save()
            voted = Vote()
            voted.name=request.user
            voted.poll=poll
            voted.status=True
            voted.chosen=poll.options[int(selected_option)-1]
            voted.save()
        else:
            return HttpResponse(400, 'Invalid form')

        return redirect('poll:results', poll.id)

    context = {'poll' : poll}
    return render(request, 'vote.html', context)

@login_required(login_url="/accounts/Login/")
def delete(request, poll_id):
    Poll.objects.get(pk=poll_id).delete()
    return redirect('poll:home')

def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    options = zip(poll.options,poll.options_count)
    total = sum(poll.options_count)
    percent = []
    for count in poll.options_count:
        if count>0:
            percent.append(int((count / total) * 100))
        else:
            percent.append(0)

    option_percent = zip(poll.options,percent)
    maxpoll="no votings...!"
    if total>0:
        maxpoll = poll.options[poll.options_count.index(max(poll.options_count))]
    context = {'poll' : poll,'options' : options,'total':total,'percent':percent,'option_percent':option_percent,'maxpoll':maxpoll}
    return render(request, 'results.html', context)