from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, OrderSerializer, CreateOrderSerializer
from products.models import Product
from users.views import IsAdminUser


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def cart_response(cart, request=None):
    return CartSerializer(cart, context={'request': request}).data


# ── Cart ─────────────────────────────────────────────────────────────────────

class CartView(APIView):
    def get(self, request):
        cart = get_or_create_cart(request.user)
        return Response(cart_response(cart, request))


class CartItemView(APIView):
    def post(self, request):
        """Add item to cart."""
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        try:
            product = Product.objects.get(pk=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=404)
        if product.stock < quantity:
            return Response({'error': f'Only {product.stock} in stock.'}, status=400)

        cart = get_or_create_cart(request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            new_qty = item.quantity + quantity
            if product.stock < new_qty:
                return Response({'error': f'Only {product.stock} in stock.'}, status=400)
            item.quantity = new_qty
        else:
            item.quantity = quantity
        item.save()
        return Response(cart_response(cart, request))

    def patch(self, request):
        """Update item quantity."""
        item_id = request.data.get('item_id')
        quantity = int(request.data.get('quantity', 1))
        try:
            cart = get_or_create_cart(request.user)
            item = CartItem.objects.get(pk=item_id, cart=cart)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found.'}, status=404)
        if quantity <= 0:
            item.delete()
        else:
            if item.product.stock < quantity:
                return Response({'error': f'Only {item.product.stock} in stock.'}, status=400)
            item.quantity = quantity
            item.save()
        return Response(cart_response(cart, request))

    def delete(self, request):
        """Remove item from cart."""
        item_id = request.query_params.get('item_id')
        try:
            cart = get_or_create_cart(request.user)
            item = CartItem.objects.get(pk=item_id, cart=cart)
            item.delete()
        except CartItem.DoesNotExist:
            pass
        cart.refresh_from_db()
        return Response(cart_response(cart, request))


class CartClearView(APIView):
    def delete(self, request):
        cart = get_or_create_cart(request.user)
        cart.items.all().delete()
        return Response(cart_response(cart, request))


# ── Orders ───────────────────────────────────────────────────────────────────

class OrderListView(APIView):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return Response(OrderSerializer(orders, many=True).data)

    @transaction.atomic
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        cart = get_or_create_cart(request.user)
        if not cart.items.exists():
            return Response({'error': 'Cart is empty.'}, status=400)

        # Validate stock
        for item in cart.items.select_related('product'):
            if item.product.stock < item.quantity:
                return Response({'error': f'Not enough stock for {item.product.name}.'}, status=400)

        total = cart.total
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            **serializer.validated_data
        )

        for item in cart.items.select_related('product'):
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                product_price=item.product.price,
                quantity=item.quantity,
            )
            item.product.stock -= item.quantity
            item.product.save()

        cart.items.all().delete()
        return Response(OrderSerializer(order).data, status=201)


class OrderDetailView(APIView):
    def get_object(self, pk, user):
        try:
            return Order.objects.get(pk=pk, user=user)
        except Order.DoesNotExist:
            return None

    def get(self, request, pk):
        order = self.get_object(pk, request.user)
        if not order:
            return Response({'detail': 'Not found.'}, status=404)
        return Response(OrderSerializer(order).data)


class CancelOrderView(APIView):
    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)
        if order.status not in ('pending', 'confirmed'):
            return Response({'error': 'Cannot cancel this order.'}, status=400)
        order.status = 'cancelled'
        order.save()
        # Restore stock
        for item in order.items.select_related('product'):
            if item.product:
                item.product.stock += item.quantity
                item.product.save()
        return Response(OrderSerializer(order).data)


# ── Admin Order views ─────────────────────────────────────────────────────────

class AdminOrderListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        orders = Order.objects.all().select_related('user')
        return Response(OrderSerializer(orders, many=True).data)


class AdminOrderDetailView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)
        allowed_fields = {'status', 'notes'}
        data = {k: v for k, v in request.data.items() if k in allowed_fields}
        for attr, value in data.items():
            setattr(order, attr, value)
        order.save()
        return Response(OrderSerializer(order).data)
