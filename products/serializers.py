# from rest_framework import serializers
# from .models import Category, Product, Review, Favourite


# class CategorySerializer(serializers.ModelSerializer):
#     product_count = serializers.SerializerMethodField()

#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'description', 'product_count', 'created_at']

#     def get_product_count(self, obj):
#         return obj.products.filter(is_active=True).count()


# class ReviewSerializer(serializers.ModelSerializer):
#     user_name = serializers.CharField(source='user.full_name', read_only=True)
#     user_email = serializers.CharField(source='user.email', read_only=True)

#     class Meta:
#         model = Review
#         fields = ['id', 'user_name', 'user_email', 'rating', 'comment', 'created_at']
#         read_only_fields = ['id', 'created_at']


# class ProductSerializer(serializers.ModelSerializer):
#     category_name = serializers.CharField(source='category.name', read_only=True)

#     # Frontend uses product.rating and product.num_reviews
#     rating = serializers.FloatField(source='avg_rating', read_only=True)
#     num_reviews = serializers.IntegerField(source='review_count', read_only=True)
#     reviews = ReviewSerializer(many=True, read_only=True)

#     # Frontend uses product.is_favourited
#     is_favourited = serializers.SerializerMethodField()

#     # Frontend uses product.is_in_stock (boolean)
#     is_in_stock = serializers.SerializerMethodField()

#     # Admin panel uses product.quantity — alias for the 'stock' db field
#     # write_only=False so it appears in GET responses too
#     quantity = serializers.IntegerField(source='stock', required=False)

#     class Meta:
#         model = Product
#         fields = [
#             'id', 'name', 'description', 'price', 'category', 'category_name',
#             'image', 'stock', 'quantity', 'is_active', 'is_in_stock',
#             'rating', 'num_reviews', 'reviews', 'is_favourited',
#             'created_at', 'updated_at',
#         ]

#     def get_is_favourited(self, obj):
#         request = self.context.get('request')
#         if request and request.user.is_authenticated:
#             return obj.favourited_by.filter(user=request.user).exists()
#         return False

#     def get_is_in_stock(self, obj):
#         return obj.stock > 0


# class ProductListSerializer(serializers.ModelSerializer):
#     """Lighter serializer for list views — no reviews."""
#     category_name = serializers.CharField(source='category.name', read_only=True)

#     # Frontend uses product.rating and product.num_reviews
#     rating = serializers.FloatField(source='avg_rating', read_only=True)
#     num_reviews = serializers.IntegerField(source='review_count', read_only=True)

#     # Frontend uses product.is_favourited
#     is_favourited = serializers.SerializerMethodField()

#     # Frontend uses product.is_in_stock (boolean)
#     is_in_stock = serializers.SerializerMethodField()

#     # Admin panel uses product.quantity — alias for the 'stock' db field
#     quantity = serializers.IntegerField(source='stock', required=False)

#     class Meta:
#         model = Product
#         fields = [
#             'id', 'name', 'price', 'category', 'category_name',
#             'image', 'stock', 'quantity', 'is_active', 'is_in_stock',
#             'rating', 'num_reviews', 'is_favourited', 'created_at',
#         ]

#     def get_is_favourited(self, obj):
#         request = self.context.get('request')
#         if request and request.user.is_authenticated:
#             return obj.favourited_by.filter(user=request.user).exists()
#         return False

#     def get_is_in_stock(self, obj):
#         return obj.stock > 0


# from rest_framework import serializers
# from .models import Category, Product, Review, Favourite


# class CategorySerializer(serializers.ModelSerializer):
#     product_count = serializers.SerializerMethodField()

#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'description', 'product_count', 'created_at']

#     def get_product_count(self, obj):
#         return obj.products.filter(is_active=True).count()


# class ReviewSerializer(serializers.ModelSerializer):
#     user_name = serializers.CharField(source='user.full_name', read_only=True)
#     user_email = serializers.CharField(source='user.email', read_only=True)

#     class Meta:
#         model = Review
#         fields = ['id', 'user_name', 'user_email', 'rating', 'comment', 'created_at']
#         read_only_fields = ['id', 'created_at']


# class ProductSerializer(serializers.ModelSerializer):
#     category_name = serializers.CharField(source='category.name', read_only=True)
#     avg_rating = serializers.FloatField(read_only=True)
#     review_count = serializers.IntegerField(read_only=True)
#     reviews = ReviewSerializer(many=True, read_only=True)
#     is_favourite = serializers.SerializerMethodField()

#     class Meta:
#         model = Product
#         fields = [
#             'id', 'name', 'description', 'price', 'category', 'category_name',
#             'image', 'stock', 'is_active', 'avg_rating', 'review_count',
#             'reviews', 'is_favourite', 'created_at', 'updated_at'
#         ]

#     def get_is_favourite(self, obj):
#         request = self.context.get('request')
#         if request and request.user.is_authenticated:
#             return obj.favourited_by.filter(user=request.user).exists()
#         return False


# class ProductListSerializer(serializers.ModelSerializer):
#     """Lighter serializer for list views (no reviews)."""
#     category_name = serializers.CharField(source='category.name', read_only=True)
#     avg_rating = serializers.FloatField(read_only=True)
#     review_count = serializers.IntegerField(read_only=True)
#     is_favourite = serializers.SerializerMethodField()

#     class Meta:
#         model = Product
#         fields = [
#             'id', 'name', 'price', 'category', 'category_name',
#             'image', 'stock', 'is_active', 'avg_rating', 'review_count',
#             'is_favourite', 'created_at'
#         ]

#     def get_is_favourite(self, obj):
#         request = self.context.get('request')
#         if request and request.user.is_authenticated:
#             return obj.favourited_by.filter(user=request.user).exists()
#         return False



from rest_framework import serializers
from .models import Category, Product, Review, Favourite


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count', 'created_at']

    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user_name', 'user_email', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    # Rating helpers
    rating = serializers.FloatField(source='avg_rating', read_only=True)
    num_reviews = serializers.IntegerField(source='review_count', read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    # Computed booleans
    is_favourited = serializers.SerializerMethodField()
    is_in_stock = serializers.SerializerMethodField()

    # Admin alias: 'quantity' → 'stock'
    quantity = serializers.IntegerField(source='stock', required=False)

    # ── NEW FIELDS ────────────────────────────────────────────────────────────
    discount_price = serializers.DecimalField(
        max_digits=10, decimal_places=2,
        required=False, allow_null=True,
    )
    brand = serializers.CharField(required=False, allow_blank=True)
    sku = serializers.CharField(required=False, allow_blank=True)
    # Computed discount percentage (read-only, handy for frontend)
    discount_percent = serializers.SerializerMethodField()
    # ─────────────────────────────────────────────────────────────────────────

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description',
            'price', 'discount_price', 'discount_percent',
            'brand', 'sku',
            'category', 'category_name',
            'image', 'stock', 'quantity', 'is_active', 'is_in_stock',
            'rating', 'num_reviews', 'reviews', 'is_favourited',
            'created_at', 'updated_at',
        ]

    def get_is_favourited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favourited_by.filter(user=request.user).exists()
        return False

    def get_is_in_stock(self, obj):
        return obj.stock > 0

    def get_discount_percent(self, obj):
        if obj.discount_price and obj.price:
            return round((1 - float(obj.discount_price) / float(obj.price)) * 100)
        return 0

    def validate(self, data):
        price = data.get('price') or (self.instance.price if self.instance else None)
        discount_price = data.get('discount_price')
        if discount_price is not None and price is not None:
            if discount_price >= price:
                raise serializers.ValidationError(
                    {'discount_price': 'Discount price must be less than the regular price.'}
                )
        return data


class ProductListSerializer(serializers.ModelSerializer):
    """Lighter serializer for list views — no reviews."""
    category_name = serializers.CharField(source='category.name', read_only=True)

    rating = serializers.FloatField(source='avg_rating', read_only=True)
    num_reviews = serializers.IntegerField(source='review_count', read_only=True)

    is_favourited = serializers.SerializerMethodField()
    is_in_stock = serializers.SerializerMethodField()

    quantity = serializers.IntegerField(source='stock', required=False)

    # ── NEW FIELDS ────────────────────────────────────────────────────────────
    discount_price = serializers.DecimalField(
        max_digits=10, decimal_places=2,
        read_only=True, allow_null=True,
    )
    brand = serializers.CharField(read_only=True)
    sku = serializers.CharField(read_only=True)
    discount_percent = serializers.SerializerMethodField()
    # ─────────────────────────────────────────────────────────────────────────

    class Meta:
        model = Product
        fields = [
            'id', 'name',
            'price', 'discount_price', 'discount_percent',
            'brand', 'sku',
            'category', 'category_name',
            'image', 'stock', 'quantity', 'is_active', 'is_in_stock',
            'rating', 'num_reviews', 'is_favourited', 'created_at',
        ]

    def get_is_favourited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favourited_by.filter(user=request.user).exists()
        return False

    def get_is_in_stock(self, obj):
        return obj.stock > 0

    def get_discount_percent(self, obj):
        if obj.discount_price and obj.price:
            return round((1 - float(obj.discount_price) / float(obj.price)) * 100)
        return 0