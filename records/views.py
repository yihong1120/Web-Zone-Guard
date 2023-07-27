from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.
def history(request):
    if request.user.is_authenticated:
        return render(request, 'records/history.html')
    else:
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})