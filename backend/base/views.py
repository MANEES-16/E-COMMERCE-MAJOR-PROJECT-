# backend/base/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
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


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for key, value in serializer.items():
            data[key] = value
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerUser(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')
    name = data.get('name', '')

    if not email or not password:
        return Response(
            {'detail': 'Email and password are required'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {'detail': 'User with this email already exists'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.create(
        first_name=name,
        username=email,
        email=email,
        password=make_password(password),
    )

    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)


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
    user = get_object_or_404(User, id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateUser(request, pk):
    user = get_object_or_404(User, id=pk)
    data = request.data

    user.first_name = data.get('name', user.first_name)
    user.username = data.get('email', user.username)
    user.email = data.get('email', user.email)
    user.is_staff = data.get('isAdmin', user.is_staff)

    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    user = get_object_or_404(User, id=pk)
    user.delete()
    return Response({'detail': 'User deleted'})


@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all().order_by('-createdAt')
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
    product = get_object_or_404(Product, _id=pk)
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
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    data = request.data
    product = get_object_or_404(Product, _id=pk)

    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.brand = data.get('brand', product.brand)
    product.category = data.get('category', product.category)
    product.description = data.get('description', product.description)
    product.countInStock = data.get('countInStock', product.countInStock)
    product.image = data.get('image', product.image)

    product.save()
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    product = get_object_or_404(Product, _id=pk)
    product.delete()
    return Response({'detail': 'Product Deleted'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data

    order_items = data.get('orderItems')

    if not order_items:
        return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)

    validated_items = []
    for incoming in order_items:
        product = get_object_or_404(Product, _id=incoming.get('product'))

        qty = int(incoming.get('qty', 0))
        if qty <= 0:
            return Response(
                {'detail': 'Quantity must be greater than zero'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if product.countInStock < qty:
            return Response(
                {'detail': f"{product.name} does not have enough stock"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated_items.append(
            {
                'product': product,
                'qty': qty,
                'price': incoming.get('price', product.price),
            }
        )

    order = Order.objects.create(
        user=user,
        paymentMethod=data.get('paymentMethod', ''),
        taxPrice=data.get('taxPrice', 0),
        shippingPrice=data.get('shippingPrice', 0),
        totalPrice=data.get('totalPrice', 0),
    )

    shipping_address = data.get('shippingAddress', {})
    ShippingAddress.objects.create(
        order=order,
        address=shipping_address.get('address', ''),
        city=shipping_address.get('city', ''),
        postalCode=shipping_address.get('postalCode', ''),
        country=shipping_address.get('country', ''),
        shippingPrice=data.get('shippingPrice', 0),
    )

    for item in validated_items:
        OrderItem.objects.create(
            product=item['product'],
            order=order,
            name=item['product'].name,
            qty=item['qty'],
            price=item['price'],
            image=item['product'].image,
        )

        product = item['product']
        product.countInStock -= item['qty']
        product.save(update_fields=['countInStock'])

    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


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
    order = get_object_or_404(Order, _id=pk)

    if user.is_staff or order.user == user:
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)

    return Response(
        {'detail': 'Not authorized to view this order'},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
    orders = Order.objects.all().order_by('-createdAt')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
    order = get_object_or_404(Order, _id=pk)

    if not (request.user.is_staff or order.user == request.user):
        return Response(
            {'detail': 'Not authorized to update this order'},
            status=status.HTTP_403_FORBIDDEN,
        )

    order.isPaid = True
    order.paidAt = timezone.now()
    order.save()
    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)
