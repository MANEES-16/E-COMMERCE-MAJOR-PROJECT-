# backend/base/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Product, Order, OrderItem, ShippingAddress
from .serializers import (
    ProductSerializer,
    UserSerializer,
    UserSerializerWithToken,
    OrderSerializer,
)

# ---------- JWT Login ----------

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  def validate(self, attrs):
      data = super().validate(attrs)
      serializer = UserSerializerWithToken(self.user).data
      for k, v in serializer.items():
          data[k] = v
      return data

class MyTokenObtainPairView(TokenObtainPairView):
  serializer_class = MyTokenObtainPairSerializer


# ---------- User / Auth Views ----------

@api_view(['POST'])
def registerUser(request):
  data = request.data
  try:
      user = User.objects.create(
          first_name=data['name'],
          username=data['email'],
          email=data['email'],
          password=make_password(data['password']),
      )
      serializer = UserSerializerWithToken(user, many=False)
      return Response(serializer.data)
  except:
      message = {'detail': 'User with this email already exists'}
      return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
  user = request.user
  serializer = UserSerializer(user, many=False)
  return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
  user = request.user
  data = request.data

  user.first_name = data.get('name', user.first_name)
  user.username = data.get('email', user.username)
  user.email = data.get('email', user.email)

  if data.get('password'):
      user.password = make_password(data['password'])

  user.save()
  serializer = UserSerializerWithToken(user, many=False)
  return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
  users = User.objects.all()
  serializer = UserSerializer(users, many=True)
  return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
  user = User.objects.get(id=pk)
  serializer = UserSerializer(user, many=False)
  return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateUser(request, pk):
  user = User.objects.get(id=pk)
  data = request.data

  user.first_name = data['name']
  user.username = data['email']
  user.email = data['email']
  user.is_staff = data['isAdmin']

  user.save()
  serializer = UserSerializer(user, many=False)
  return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
  user = User.objects.get(id=pk)
  user.delete()
  return Response({'detail': 'User deleted'})


# ---------- Product Views ----------

@api_view(['GET'])
def getProducts(request):
  products = Product.objects.all()
  serializer = ProductSerializer(products, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def getProduct(request, pk):
  product = Product.objects.get(_id=pk)
  serializer = ProductSerializer(product, many=False)
  return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
  user = request.user
  data = request.data

  product = Product.objects.create(
      user=user,
      name=data.get('name', 'Sample Name'),
      price=data.get('price', 0),
      brand=data.get('brand', ''),
      category=data.get('category', ''),
      description=data.get('description', ''),
      countInStock=data.get('countInStock', 0),
      image=data.get('image', ''),
  )
  serializer = ProductSerializer(product, many=False)
  return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
  data = request.data
  product = Product.objects.get(_id=pk)

  product.name = data['name']
  product.price = data['price']
  product.brand = data['brand']
  product.category = data['category']
  product.description = data['description']
  product.countInStock = data['countInStock']
  product.image = data['image']

  product.save()
  serializer = ProductSerializer(product, many=False)
  return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
  product = Product.objects.get(_id=pk)
  product.delete()
  return Response({'detail': 'Product Deleted'})


# ---------- Order Views ----------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
  user = request.user
  data = request.data

  orderItems = data['orderItems']

  if not orderItems or len(orderItems) == 0:
      return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)

  # 1. Create order
  order = Order.objects.create(
      user=user,
      paymentMethod=data['paymentMethod'],
      taxPrice=data['taxPrice'],
      shippingPrice=data['shippingPrice'],
      totalPrice=data['totalPrice'],
  )

  # 2. Shipping address
  ShippingAddress.objects.create(
      order=order,
      address=data['shippingAddress']['address'],
      city=data['shippingAddress']['city'],
      postalCode=data['shippingAddress']['postalCode'],
      country=data['shippingAddress']['country'],
      shippingPrice=data['shippingPrice'],
  )

  # 3. Create order items & update stock
  for i in orderItems:
      product = Product.objects.get(_id=i['product'])

      item = OrderItem.objects.create(
          product=product,
          order=order,
          name=product.name,
          qty=i['qty'],
          price=i['price'],
          image=product.image,
      )

      product.countInStock -= item.qty
      product.save()

  serializer = OrderSerializer(order, many=False)
  return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
  user = request.user
  orders = user.order_set.all()
  serializer = OrderSerializer(orders, many=True)
  return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
  user = request.user
  order = Order.objects.get(_id=pk)

  if user.is_staff or order.user == user:
      serializer = OrderSerializer(order, many=False)
      return Response(serializer.data)
  else:
      return Response(
          {'detail': 'Not authorized to view this order'},
          status=status.HTTP_400_BAD_REQUEST,
      )

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
  orders = Order.objects.all()
  serializer = OrderSerializer(orders, many=True)
  return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
  order = Order.objects.get(_id=pk)
  order.isPaid = True
  order.paidAt = timezone.now()
  order.save()
  serializer = OrderSerializer(order, many=False)
  return Response(serializer.data)