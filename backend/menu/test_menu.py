import pytest
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from menu.models import Product, ProductCategory, CookBook, InventoryProduct
from menu.serializers import ProductSerializer, ProductCategorySerializer, CookBookSerializer


@pytest.mark.django_db
class TestProductCategory:
    """Tests for ProductCategory CRUD operations"""
    
    def test_create_category(self):
        """Test creating a product category"""
        category = ProductCategory.objects.create(name="Bebidas")
        assert category.id is not None
        assert category.name == "Bebidas"
    
    def test_update_category(self):
        """Test updating a product category"""
        category = ProductCategory.objects.create(name="Comida")
        category.name = "Comida Rápida"
        category.save()
        
        updated_category = ProductCategory.objects.get(id=category.id)
        assert updated_category.name == "Comida Rápida"
    
    def test_delete_category(self):
        """Test deleting a product category"""
        category = ProductCategory.objects.create(name="Postres")
        category_id = category.id
        category.delete()
        
        assert not ProductCategory.objects.filter(id=category_id).exists()


@pytest.mark.django_db
class TestCookBook:
    """Tests for CookBook CRUD operations"""
    
    def test_create_cookbook(self):
        """Test creating a cookbook entry"""
        cookbook = CookBook.objects.create(
            name="Pizza Margherita",
            note="Receta clásica italiana"
        )
        assert cookbook.id is not None
        assert cookbook.name == "Pizza Margherita"
        assert cookbook.note == "Receta clásica italiana"
    
    def test_update_cookbook(self):
        """Test updating a cookbook entry"""
        cookbook = CookBook.objects.create(name="Hamburguesa", note="")
        cookbook.note = "Con queso cheddar"
        cookbook.save()
        
        updated_cookbook = CookBook.objects.get(id=cookbook.id)
        assert updated_cookbook.note == "Con queso cheddar"
    
    def test_delete_cookbook(self):
        """Test deleting a cookbook entry"""
        cookbook = CookBook.objects.create(name="Ensalada", note="")
        cookbook_id = cookbook.id
        cookbook.delete()
        
        assert not CookBook.objects.filter(id=cookbook_id).exists()


@pytest.mark.django_db
class TestProduct:
    """Tests for Product CRUD operations with inventory tracking"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures"""
        self.category = ProductCategory.objects.create(name="Pizzas")
        self.cookbook = CookBook.objects.create(name="Pizza Napolitana", note="Receta tradicional")
    
    def test_create_product(self):
        """Test creating a product also creates InventoryProduct"""
        # Create product using serializer
        serializer = ProductSerializer(data={
            'name': 'Pizza Napolitana',
            'price': 150,
            'cookbookId': self.cookbook.id,
            'categoryId': self.category.id
        })
        
        assert serializer.is_valid(), serializer.errors
        product = serializer.save()
        
        # Verify product was created
        assert product.id is not None
        assert product.name == 'Pizza Napolitana'
        assert product.price == 150
        
        # Verify InventoryProduct was auto-created
        inventory_product = InventoryProduct.objects.filter(productId=product).first()
        assert inventory_product is not None
        assert inventory_product.quantity == 0
        assert inventory_product.lastUpdated is not None
    
    def test_update_product(self):
        """Test updating a product updates InventoryProduct timestamp"""
        # Create product first
        serializer = ProductSerializer(data={
            'name': 'Pizza Original',
            'price': 100,
            'cookbookId': self.cookbook.id,
            'categoryId': self.category.id
        })
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        
        # Get initial timestamp
        inventory_product = InventoryProduct.objects.get(productId=product)
        initial_timestamp = inventory_product.lastUpdated
        
        # Wait a moment to ensure timestamp changes
        import time
        time.sleep(0.1)
        
        # Update product
        update_serializer = ProductSerializer(
            product,
            data={'name': 'Pizza Actualizada', 'price': 120},
            partial=True,
            context={'request_data': {'quantity': 10}}
        )
        update_serializer.is_valid(raise_exception=True)
        updated_product = update_serializer.save()
        
        # Verify product was updated
        assert updated_product.name == 'Pizza Actualizada'
        assert updated_product.price == 120
        
        # Verify InventoryProduct timestamp was updated
        inventory_product.refresh_from_db()
        assert inventory_product.lastUpdated > initial_timestamp
        assert inventory_product.quantity == 10
    
    def test_delete_product(self):
        """Test deleting a product cascades to InventoryProduct"""
        # Create product
        serializer = ProductSerializer(data={
            'name': 'Pizza Temporal',
            'price': 80,
            'cookbookId': self.cookbook.id,
            'categoryId': self.category.id
        })
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        product_id = product.id
        
        # Verify InventoryProduct exists
        assert InventoryProduct.objects.filter(productId=product).exists()
        
        # Delete product
        product.delete()
        
        # Verify both Product and InventoryProduct are deleted
        assert not Product.objects.filter(id=product_id).exists()
        assert not InventoryProduct.objects.filter(productId=product_id).exists()
    
    def test_get_products_by_category(self):
        """Test filtering products by category"""
        # Create products in different categories
        category2 = ProductCategory.objects.create(name="Bebidas")
        
        serializer1 = ProductSerializer(data={
            'name': 'Pizza 1',
            'price': 100,
            'cookbookId': self.cookbook.id,
            'categoryId': self.category.id
        })
        serializer1.is_valid(raise_exception=True)
        product1 = serializer1.save()
        
        serializer2 = ProductSerializer(data={
            'name': 'Coca Cola',
            'price': 30,
            'cookbookId': self.cookbook.id,
            'categoryId': category2.id
        })
        serializer2.is_valid(raise_exception=True)
        product2 = serializer2.save()
        
        # Filter by category
        pizza_products = Product.objects.filter(categoryId=self.category)
        bebida_products = Product.objects.filter(categoryId=category2)
        
        assert pizza_products.count() == 1
        assert bebida_products.count() == 1
        assert pizza_products.first().name == 'Pizza 1'
        assert bebida_products.first().name == 'Coca Cola'


@pytest.mark.django_db
class TestInventoryTracking:
    """Tests specifically for inventory movement tracking"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures"""
        self.category = ProductCategory.objects.create(name="Test Category")
        self.cookbook = CookBook.objects.create(name="Test Recipe", note="")
    
    def test_inventory_product_created_with_product(self):
        """Verify InventoryProduct is automatically created when Product is created"""
        serializer = ProductSerializer(data={
            'name': 'Test Product',
            'price': 50,
            'cookbookId': self.cookbook.id,
            'categoryId': self.category.id
        })
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        
        # Check InventoryProduct exists
        inventory_count = InventoryProduct.objects.filter(productId=product).count()
        assert inventory_count == 1
        
        inventory_product = InventoryProduct.objects.get(productId=product)
        assert inventory_product.quantity == 0
    
    def test_inventory_product_updated_timestamp(self):
        """Verify lastUpdated changes when InventoryProduct is modified"""
        # Create product
        serializer = ProductSerializer(data={
            'name': 'Test Product',
            'price': 50,
            'cookbookId': self.cookbook.id,
            'categoryId': self.category.id
        })
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        
        inventory_product = InventoryProduct.objects.get(productId=product)
        old_timestamp = inventory_product.lastUpdated
        
        # Wait and update
        import time
        time.sleep(0.1)
        
        inventory_product.quantity = 100
        inventory_product.save()
        
        # Verify timestamp changed
        inventory_product.refresh_from_db()
        assert inventory_product.lastUpdated > old_timestamp
        assert inventory_product.quantity == 100


@pytest.mark.django_db
class TestProductAPI:
    """Integration tests for Product API endpoints"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up API client and fixtures"""
        self.client = APIClient()
        self.category = ProductCategory.objects.create(name="API Test Category")
        self.cookbook = CookBook.objects.create(name="API Test Recipe", note="")
    
    def test_create_product_via_api(self):
        """Test creating a product via API endpoint"""
        data = {
            'name': 'API Pizza',
            'price': 200,
            'cookbookId': self.cookbook.id,
            'categoryId': self.category.id
        }
        
        response = self.client.post('/product/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'API Pizza'
        
        # Verify InventoryProduct was created
        product_id = response.data['id']
        product = Product.objects.get(id=product_id)
        assert InventoryProduct.objects.filter(productId=product).exists()
    
    def test_update_product_via_api(self):
        """Test updating a product via API endpoint"""
        # Create product first
        serializer = ProductSerializer(data={
            'name': 'Original Name',
            'price': 100,
            'cookbookId': self.cookbook.id,
            'categoryId': self.category.id
        })
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        
        # Update via API
        update_data = {
            'name': 'Updated Name',
            'price': 150,
            'cookbookId': self.cookbook.id,
            'categoryId': self.category.id,
            'quantity': 25
        }
        
        response = self.client.put(f'/product/{product.id}/', update_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated Name'
        assert response.data['price'] == 150
