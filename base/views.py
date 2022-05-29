
from wsgiref.util import request_uri
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Lable, Note
from django.contrib.auth.decorators import login_required
from .form import LableForm, NoteForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt

def loginUser(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does note Exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "username or password is wrong")
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

@csrf_exempt

def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occured during registration")
    return render(request, 'base/login_register.html', {'form': form})

@login_required(login_url='login')
@csrf_exempt
def home(request):
    lables = Lable.objects.all()
    note = Note.objects.all().order_by('-updated')
    #  (note)
    q = request.GET.get('q') if request.GET.get('q') != None else ''
   
    note = Note.objects.filter(
        Q(lable__lable__icontains=q) |
        Q(note__icontains=q)
    )

    if request.method == "POST":
        note = Note.objects.create(
            user=request.user,
            note=request.POST.get('note'),
            lable =Lable.objects.get(id=20)
        )
        return redirect('home')
# ---------------------------------------
    # for Create new label


    context = {'lables': lables, 'notes': note}

    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def note(request, pk):
    lable = Lable.objects.get(id=pk)
    #  (lable)
    lable_note = lable.note_set.all().order_by('-created')
    note = Note.objects.all().order_by('-updated')
    # note = Note.objects.get(id=54)


    # print(lable_note)

    l = request.GET.get('l') if request.GET.get('l') != None else ''
   
    lable_note = lable.note_set.filter(
        Q(lable__lable__icontains=l) |
        Q(note__icontains=l)
    ).order_by('-created')

    if request.method == "POST":
        note = Note.objects.create(
            user=request.user,
            lable=lable,
            note=request.POST.get('note')
        )
        return redirect('note', lable.id)
    

    context = {'lable': lable, 'lable_notes': lable_note, "note":note}
    return render(request, 'base/note.html', context)


@login_required(login_url='login')
@csrf_exempt
def createLable(request):

    form = LableForm()

    context = {'form': form}
    if request.method == 'POST':
        form = LableForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/create_lable.html', context)


@login_required(login_url='login')
def noteDetails(request, pk):
    note = Note.objects.get(id=pk)

    context = {'note': note}
    return render(request, 'base/note_details.html', context)


@login_required(login_url='login')
def deleteNote(request, pk):
    note = Note.objects.get(id=pk)

    if request.method == 'POST':
        note.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': note})


@login_required(login_url='login')
def updateNote(request, pk):
    note = Note.objects.get(id=pk)
    form = NoteForm(instance=note)

    # if request.user != note.user:
    #     return HttpResponse('You are not allowed here!!!')

    if request.method == 'POST':

        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form ,'note':note}
    return render(request, 'base/note_form.html', context)
