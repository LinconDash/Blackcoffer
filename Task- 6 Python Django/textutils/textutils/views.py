from django.http import HttpResponse
from django.shortcuts import render
import re

def index(request):
    return render(request, "index.html")
    # return HttpResponse("Home")

def clean(request):
    text = request.GET["text"]
    text = re.sub(r'[^\w\s]', '', text)
    # print(text)
    params = {"cleaned_text":text}
    return render(request, "cleaned.html", params)
