from django.shortcuts import render

def index(request):
    if request.user.is_authenticated:
        return render(request, 'VisionSnap/logged_in.html', {'username': request.user.username})
    else:
        return render(request, 'VisionSnap/logged_out.html')

def controls(request):
    return render(request, 'VisionSnap/controls.html')

def records(request):
    return render(request, 'VisionSnap/records.html')

def logout(request):
    return render(request, 'VisionSnap/logout.html')