from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,HttpResponse, redirect
from datetime import datetime
from app1.models import Contact, ICDetail
from django.contrib import messages
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ICDetailSerializer



# create your views here
def index(request):
#    return HttpResponse("THis is index Page from app1")
    query_set = ICDetail.objects.all()[:9]
    first = ICDetail.objects.filter(id__range=(6,9))
    context = {'name': None, 'dtls':query_set,'first':first}
    if request.user.is_authenticated:
        context['name'] = request.user.username

#    messages.success(request, "Welcome to Our Website!")
    return render(request, 'index.html', context)

def about(request):

    return render(request,'about.html')

def services(request):
    query_set = ICDetail.objects.all()[9:13]
    context = {'dtls': query_set}
    return render(request,'services.html', context)
#    return HttpResponse("THis is services Page from app1")

def contact(request):
    try:
        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            desc = request.POST['desc']
            contact = Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
            contact.save()
            messages.success(request, "Data Submitted Successfully!")

        return render(request,'contact.html')
    except:
        pass



def iceCreamDetails(request,slugID):
    try:
        product = ICDetail.objects.get(icecream_slug=slugID)
        if product:
            context = {'product':product}
            d=request.COOKIES.setdefault('recent_items ','')
            if product.name not in d.split('\n'):
                d=d+'\n'+product.name
                d=d.strip('\n')
            response = render(request, "iceCreamDetails.html", context)
            response.set_cookie('recent_items',d)
            return response
        else:
            return HttpResponse("ID Not found")
    except:
        pass       

#  function based views for REST API

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_IceCreams(request):
    if request.method == 'GET':
        dtls = ICDetail.objects.all()
        serializer = ICDetailSerializer(dtls, many=True)
        return Response(serializer.data)
    
    # elif request.method == 'POST' & request.user.is_staff:
    #     serializer = ICDetailSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)


# Method 1 for POST Api
# Class based views for REST API
class PostView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def post(self, request):
        serializer = ICDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Method 2 for POST Api

# @api_view(['POST'])
# @permission_classes([IsAdminUser])
# # @parser_classes([MultiPartParser, FormParser])
# def post_new_IceCreams(request):
#     serializer = ICDetailSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)