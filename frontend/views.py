from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url="/accounts/login/")
def index(request, *args, **kwargs):
    return render(request, "index.html")


def public_index(request, *args, **kwargs):
    return render(request, "index.html")
