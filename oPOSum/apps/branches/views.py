from django.shortcuts import render

# Create your views here.
def select_branch(request):
    return render(request, 'branches/select_branch.html')
