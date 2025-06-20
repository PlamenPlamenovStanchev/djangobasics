from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from departament.models import Departament


def index(request):
    return HttpResponse("<h1>Hello, world. You're at the polls index.</h1>")


def int_param_view(request, pk):
    response = HttpResponse(f"<h1>Departament index: {pk}</h1>")
    return response


def string_param_view(request, name):
    return HttpResponse(f"<h1>Departament name: {name}</h1>")


def slug_param_view(request, slug):
    # department = Department.objects.filter(slug=slug).first()
    #
    # if not department:
    #     raise Http404

    # Option 2:
    departament = get_object_or_404(Departament, slug=slug)
    return render(request, "slug_template.html", {"departament": departament})


def path_to_file_param_view(request, path_to_file):
    return HttpResponse(f"<h1>This file is located at: {path_to_file}</h1>")


def uuid_param_view(request, id):
    return HttpResponse(f"<h1>The department id is: {id}</h1>")


def regex_view(request, archive_year: int):
    return HttpResponse(f"<h1>The year is: {archive_year}</h1>")

def contacts_view(request):
    return HttpResponse("We are departments")


def about_view(request):
    return redirect('int-view', pk=2, permanent=True)
