from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template import loader

from .models import *
from crawler.crawled_info import majors_list
from crawler.crawled_info import majors_dictionary


def main(request):
    template = loader.get_template("main.html")
    context = {
        "majors": majors_list.majors,
    }
    return HttpResponse(template.render(context, request))


def search_course(request):
    major_value = request.GET.get('major_value')
    if major_value:
        return get_all_course_by_major(request, major_value)
    
    course_name = request.GET.get('course_name')
    if course_name:
        return get_all_course_by_name(request, course_name)
    
    course_code = request.GET.get('course_code')
    if course_code:
        return get_all_course_by_code(request, course_code)

    raise Http404("페이지를 찾을 수 없습니다.")

def get_all_course_by_major(request, major_value):
    search_parameter_validator(major_value)
    
    major_name = majors_dictionary.majors_dictionary[major_value]
    course_queryset = Course.objects.filter(major_name = major_name)
    template = loader.get_template("main.html")
    context = {
        "majors": majors_list.majors, 
        "course_list": course_queryset,
        "major_name":major_name
    }
    return HttpResponse(template.render(context, request))

def get_all_course_by_name(request, course_name):
    search_parameter_validator(course_name)
    
    course_queryset =  Course.objects.filter(name__contains = course_name)
    template = loader.get_template("main.html")
    context = {
        "majors": majors_list.majors,
        "course_list": course_queryset,
        "course_name":course_name
    }
    return HttpResponse(template.render(context, request))

def get_all_course_by_code(request, course_code):
    search_parameter_validator(course_code)
    
    course_queryset =  Course.objects.filter(code__contains = course_code)
    template = loader.get_template("main.html")
    context = {
        "majors": majors_list.majors,
        "course_list": course_queryset,
        "course_code":course_code
    }
    return HttpResponse(template.render(context, request))

def search_parameter_validator(param):
    if param == "" or param == None:
        raise Http404("search parameter does not null or empty")
    if len(param) < 3:
        raise Http404("search parameter must greater than 3")

# def get_all_course(request):
#     return Course.objects.all()