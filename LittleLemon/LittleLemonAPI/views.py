from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import MenuItem, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, UserSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token


# Create your views here.
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])

def menu_items_view(request):
    if request.user.groups.filter(name="Manager").exists():
        if request.method == 'GET': 
            items = MenuItem.objects.select_related("category").all()
            serialized_item = MenuItemSerializer(items, many=True)    
            return Response(serialized_item.data)
        
        if request.method == 'POST': 
            serialized_item = MenuItemSerializer(data = request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status = 201)
        
    else:
        if request.method == 'GET':
            items = MenuItem.objects.select_related("category").all()
            serialized_item = MenuItemSerializer(items, many=True)    
            return Response(serialized_item.data, status = 200)
        else:
            content = {'403' : 'Unauthorized'}
            return Response(content, status = 403) 

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])

def single_item_view(request, id):
    if request.user.groups.filter(name="Manager").exists():
        if request.method == 'GET': 
            item = get_object_or_404(MenuItem, pk=id)
            serialized_item = MenuItemSerializer(item)    
            return Response(serialized_item.data)
        
        if  request.method == 'PUT':
            item = get_object_or_404(MenuItem, pk=id)
            serialized_item = MenuItemSerializer(item, data = request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data)
        
        if  request.method == 'PATCH':
            item = get_object_or_404(MenuItem, pk=id)
            serialized_item = MenuItemSerializer(item, data = request.data, partial = True)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data)
        
        if request.method == 'DELETE':
            item = get_object_or_404(MenuItem, pk=id)
            item.delete()
            return Response(status.HTTP_204_NO_CONTENT)
    else:
        if request.method == 'GET': 
            item = get_object_or_404(MenuItem, pk=id)
            serialized_item = MenuItemSerializer(item)    
            return Response(serialized_item.data)  
        else:
            content = {'403' : 'Unauthorized'}
            return Response(content, status = 403)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])        
def manager_view(request):
    if request.user.groups.filter(name="Manager").exists():
        if request.method == 'GET':
            users = User.objects.filter(groups=1)
            serialized_user = UserSerializer(users, many=True)
            return Response(serialized_user.data)
       
        if request.method == 'POST':
            serialized_user = UserSerializer(data=request.data)
            serialized_user.is_valid(raise_exception=True)
            serialized_user.save()
            username = request.data['username']
            if username:
                user = get_object_or_404(User, username=username)
                managers = Group.objects.get(name="Manager")
                managers.user_set.add(user)
            return Response(serialized_user.data, status = 201)
    else:
        return Response(status = 403)       

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])      
def single_manager_delete_view(request, id):
    if request.user.groups.filter(name="Manager").exists():
        if request.method == 'DELETE':
            user = get_object_or_404(User, pk=id)
            managers = Group.objects.get(name="Manager")
            managers.user_set.remove(user)
            return Response({'200' : 'Success'}, status=200)  
            
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])        
def delivery_view(request):
    if request.user.groups.filter(name="Manager").exists():
        if request.method == 'GET':
            users = User.objects.filter(groups=2)
            serialized_user = UserSerializer(users, many=True)
            return Response(serialized_user.data)
        
        if request.method == 'POST':
            serialized_user = UserSerializer(data=request.data)
            serialized_user.is_valid(raise_exception=True)
            serialized_user.save()
            username = request.data['username']
            if username:
                user = get_object_or_404(User, username=username)
                managers = Group.objects.get(name="Delivery Crew")
                managers.user_set.add(user)
            return Response(serialized_user.data, status = 201)
    else:
        return Response(status = 403)     
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])        
def single_delivery_delete_view(request, id):
    if request.user.groups.filter(name="Manager").exists():
        if request.method == 'DELETE':
            user = get_object_or_404(User, pk=id)
            managers = Group.objects.get(name="Delivery Crew")
            managers.user_set.remove(user)
            return Response({'200' : 'Success'}, status=200)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart_view(request):
    if request.user.groups.filter(name="Manager").exists():
        pass
    
    elif request.user.groups.filter(name="Delivery Crew").exists():
        pass
    
    else:
        if request.method == "GET":
            items = Cart.objects.filter(user=request.user)
            serialized_item = CartSerializer(items, many=True)    
            return Response(serialized_item.data)
    
        if request.method == "POST":
            serialized_item = CartSerializer(data = request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status = 201)
    
        if request.method == "DELETE":
            item = Cart.objects.filter(user=request.user)
            item.delete()
            return Response(status.HTTP_204_NO_CONTENT)
    return Response(status = 403) 
    
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])    

def order_view(request):
    if request.user.groups.filter(name="Manager").exists():
        if request.method == 'GET':
            order = Order.objects.all()
            serialized_order = OrderSerializer(order, many=True)    
            return Response(serialized_order.data)
        
    if request.user.groups.filter(name="Delivery Crew").exists():
        pass
    else:
        if request.method == 'GET':
            pass
        if request.method == 'POST':
            serialized_order = OrderItemSerializer(data = request.data)
            serialized_order.is_valid(raise_exception=True)
            serialized_order.save()
            return Response(serialized_order.data, status = 201)
            
    return Response(status = 403)     

def single_order_view(request, id):
    if request.user.groups.filter(name="Manager").exists():
        if request.method == 'GET':
            order = get_object_or_404(Order, pk=id)
            serialized_order = OrderSerializer(order)    
            return Response(serialized_order.data)
    return Response(status = 403)  
    
    
        
    