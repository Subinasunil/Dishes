from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from disheitem.models import Dishes
from disheitem.serializer import DishSerializer,DishModelSerializer
from rest_framework import status
from rest_framework.viewsets import ViewSet
class DishesView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Dishes.objects.all()
        serializer=DishSerializer(qs,many=True)
        return Response(data=serializer.data)
    def post(self,request,*args,**kwargs):
        serializer=DishSerializer(data=request.data)
        if serializer.is_valid():
            Dishes.objects.create(**serializer.validated_data)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
class DishDetailView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Dishes.objects.get(id=id)
        serializer=DishSerializer(qs)
        return Response(data=serializer.data)
    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        instance=Dishes.objects.filter(id=id)
        serializers=DishSerializer (data=request.data)
        if serializers.is_valid():
            # instance.name=serializers.validated_data.get("name")
            # instance.category=serializers.validated_data.get("category")
            # instance.price=serializers.validated_data.get("price")
            # instance.rating = serializers.validated_data.get("rating")
            # instance.save()
            instance.update(**serializers.validated_data)
            return Response(data=serializers.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializers.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        instance=Dishes.objects.get(id=id)
        serializers=DishSerializer(instance)
        instance.delete()
        return Response({"msg:deleted"},status=status.HTTP_204_NO_CONTENT)


class DishModelView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Dishes.objects.all()
        if "category" in request.query_params:
            qs=qs.filter(category__contains=request.query_params.get("category"))
        if "price_gt" in request.query_params:
            qs=qs.filter(price__gte=request.query_params.get("price_gt"))
        serializer=DishModelSerializer(qs,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    def post(self,request,*args,**kwargs):
        serializer=DishModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.data,status=status.HTTP_400_BAD_REQUEST)


class DishDetailModelView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Dishes.objects.get(id=id)
        serializer=DishModelSerializer(qs)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        object=Dishes.objects.get(id=id)
        serializer=DishModelSerializer(data=request.data,instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        instance=Dishes.objects.get(id=id)
        instance.delete()
        return Response({"msg":"deleted"},status=status.HTTP_204_NO_CONTENT)


class DishViewsetView(ViewSet):
    def list(self,request,*args,**kwargs):
        qs=Dishes.objects.all()
        serializer=DishModelSerializer(qs,many=True)
        return Response(data=serializer.data)
    def create(self,request,*args,**kwargs):
        serializer=DishModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Dishes.objects.get(id=id)
        serialzer=DishModelSerializer(qs)
        return Response(data=serialzer.data)

    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Dishes.objects.get(id=id)
        serializer=DishModelSerializer(instance=object,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Dishes.objects.get(id=id)
        object.delete()
        return Response({"msg":"deleted"},status=status.HTTP_204_NO_CONTENT)