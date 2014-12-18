from django.shortcuts import render, render_to_response

# Create your views here.
def select_branch(request):
    return render_to_response('branches/select_branch.html')
