from rest_framework import serializers

from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'password',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']
        
class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only = True)
    category_id = serializers.IntegerField(write_only = True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']
        
class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only = True)
    menuitem_id = serializers.IntegerField(write_only=True)
    unit_price = serializers.IntegerField()
    # price = serializers.SerializerMethodField(method_name='total_price')
    user = UserSerializer(read_only = True)
    user_id = serializers.IntegerField(write_only = True)
    class Meta:
        model = Cart
        fields = ['user','user_id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']
        
    # def total_price(self, product:Cart):
    #     return product.quantity * product.unit_price
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only = True)
    menuitem = MenuItemSerializer(read_only = True)
    price = serializers.SerializerMethodField(method_name='total_price')
    class Meta:
        model = OrderItem
        fields = ['order', 'menuitem', 'quantity', 'unit_price', 'price']
        
    def total_price(self, product:OrderItem):
        return product.quantity * product.unit_price   

