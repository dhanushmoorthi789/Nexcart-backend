from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Category, Product, Review, Favourite
from .serializers import CategorySerializer, ProductSerializer, ProductListSerializer, ReviewSerializer
from users.views import IsAdminUser


class CategoryListView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        cats = Category.objects.all()
        return Response(CategorySerializer(cats, many=True).data)

    def post(self, request):
        if not request.user.is_admin:
            return Response({'detail': 'Admin only.'}, status=403)
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CategoryDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def patch(self, request, pk):
        cat = self.get_object(pk)
        if not cat:
            return Response({'detail': 'Not found.'}, status=404)
        serializer = CategorySerializer(cat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        cat = self.get_object(pk)
        if not cat:
            return Response({'detail': 'Not found.'}, status=404)
        cat.delete()
        return Response(status=204)


class ProductListView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        from django.db.models import Avg, Count
        qs = Product.objects.filter(is_active=True).annotate(
            _avg_rating=Avg('reviews__rating'),
            _review_count=Count('reviews'),
        )
        # Filters
        category = request.query_params.get('category')
        search = request.query_params.get('search')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        in_stock = request.query_params.get('in_stock')
        # Frontend sends 'ordering'; support legacy 'sort' too
        sort = request.query_params.get('ordering') or request.query_params.get('sort', '-created_at')

        if category:
            qs = qs.filter(category__id=category)
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(description__icontains=search))
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)
        if in_stock == 'true':
            qs = qs.filter(stock__gt=0)

        sort_map = {
            'price': 'price', '-price': '-price',
            '-created_at': '-created_at', 'name': 'name',
            '-rating': '-_avg_rating', 'rating': '_avg_rating',
        }
        if sort in sort_map:
            qs = qs.order_by(sort_map[sort])

        serializer = ProductListSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_admin:
            return Response({'detail': 'Admin only.'}, status=403)
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Category, Product, Review, Favourite
from .serializers import CategorySerializer, ProductSerializer, ProductListSerializer, ReviewSerializer
from users.views import IsAdminUser


class CategoryListView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        cats = Category.objects.all()
        return Response(CategorySerializer(cats, many=True).data)

    def post(self, request):
        if not request.user.is_admin:
            return Response({'detail': 'Admin only.'}, status=403)
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CategoryDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def patch(self, request, pk):
        cat = self.get_object(pk)
        if not cat:
            return Response({'detail': 'Not found.'}, status=404)
        serializer = CategorySerializer(cat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        cat = self.get_object(pk)
        if not cat:
            return Response({'detail': 'Not found.'}, status=404)
        cat.delete()
        return Response(status=204)


class ProductListView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        qs = Product.objects.filter(is_active=True)
        # Filters
        category = request.query_params.get('category')
        search = request.query_params.get('search')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        sort = request.query_params.get('sort', '-created_at')

        if category:
            qs = qs.filter(category__id=category)
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(description__icontains=search))
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)
        if sort in ['price', '-price', '-created_at', 'name']:
            qs = qs.order_by(sort)

        serializer = ProductListSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_admin:
            return Response({'detail': 'Admin only.'}, status=403)
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ProductDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({'detail': 'Not found.'}, status=404)
        return Response(ProductSerializer(product, context={'request': request}).data)

    def patch(self, request, pk):
        if not request.user.is_admin:
            return Response({'detail': 'Admin only.'}, status=403)
        product = self.get_object(pk)
        if not product:
            return Response({'detail': 'Not found.'}, status=404)
        serializer = ProductSerializer(product, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        if not request.user.is_admin:
            return Response({'detail': 'Admin only.'}, status=403)
        product = self.get_object(pk)
        if not product:
            return Response({'detail': 'Not found.'}, status=404)
        product.delete()
        return Response(status=204)


class AddReviewView(APIView):
    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)
        if Review.objects.filter(product=product, user=request.user).exists():
            return Response({'error': 'You have already reviewed this product.'}, status=400)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product, user=request.user)
            return Response(ProductSerializer(product, context={'request': request}).data, status=201)
        return Response(serializer.errors, status=400)


class DeleteReviewView(APIView):
    def delete(self, request, pk):
        try:
            review = Review.objects.get(product_id=pk, user=request.user)
            review.delete()
            product = Product.objects.get(pk=pk)
            return Response(ProductSerializer(product, context={'request': request}).data)
        except Review.DoesNotExist:
            return Response({'detail': 'Review not found.'}, status=404)


class ToggleFavouriteView(APIView):
    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)
        fav, created = Favourite.objects.get_or_create(user=request.user, product=product)
        if not created:
            fav.delete()
            return Response({'is_favourite': False})
        return Response({'is_favourite': True})


class FavouritesListView(APIView):
    def get(self, request):
        favs = Favourite.objects.filter(user=request.user).select_related('product')
        products = [f.product for f in favs]
        return Response(ProductListSerializer(products, many=True, context={'request': request}).data)
