from PIL import Image
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import TemplateView
from django.views import View
from rest_framework.response import Response
from .forms import ImageForm
from .models import Characters, Images
from .serializers import CharacterSerializer
from rest_framework import views, status
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

#default_model = 모델 코드!!! representative

def change(id_ch, image):
    image = Image.open(image).convert("RGB")
    result = setIdImage(id_ch, image)
    return result

@csrf_exempt
def characterize(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES) # ImageForm(id_ch, image)

        if form.is_valid():
            file = form.cleaned_data.get('image')
            #file = change(id_ch, file)
            return HttpResponse(file, content_type="image/jpeg")

    else:
        form = ImageForm()
    return render(request, 'core/create-view.html', {'form': form})


    # image =  request.data("image")
    # load_model = model.load("DualSytleGan/charmodel.h1")
    # convert = load_model.convert(image)
    # return response(convert)


