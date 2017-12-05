from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect, render
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer

from .forms import SignUpForm

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('registration-complete')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration_form.html', {'form': form})