import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from inventory.models import inventorySupply, inventorySupplyType, inventoryMovementType, inventoryMovement
from inventory.serializers import inventorySupplySerializer

pytestmark = pytest.mark.django_db

def test_create_inventory_supply():
	supply_type = inventorySupplyType.objects.create(name="Materia Prima")
	supply = inventorySupply.objects.create(
		name="Harina",
		quantity=10,
		type=supply_type
	)
	assert supply.name == "Harina"
	assert supply.quantity == 10
	assert supply.type == supply_type

def test_inventory_product_serializer_create():
	supply_type = inventorySupplyType.objects.create(name="Materia Prima")
	data = {
		"name": "Azúcar",
		"quantity": 5,
		"type": supply_type.id # type: ignore
	}
	serializer = inventorySupplySerializer(data=data, context={"userId": 1})
	assert serializer.is_valid(), serializer.errors
	product = serializer.save()
	assert product.name == "Azúcar" # type: ignore
	assert product.quantity == 5 # type: ignore
	assert product.type == supply_type # type: ignore

def test_inventory_movement_created_on_product_create():
	supply_type = inventorySupplyType.objects.create(name="Materia Prima")
	movement_type, _ = inventoryMovementType.objects.get_or_create(name="add")
	data = {
		"name": "Sal",
		"quantity": 3,
		"type": supply_type.id  # type: ignore
	}
	serializer = inventorySupplySerializer(data=data, context={"userId": 2})
	assert serializer.is_valid(), serializer.errors
	product = serializer.save()
	movement = inventoryMovement.objects.filter(itemId=product, movementType=movement_type, userId=2).first()
	assert movement is not None

def test_inventory_supply_api_create():
	supply_type = inventorySupplyType.objects.create(name="Materia Prima")
	client = APIClient()
	url = reverse("inventorysupply-add-product")
	data = {
		"name": "Aceite",
		"quantity": 7,
		"type": supply_type.id # type: ignore
	}
	response = client.post(url, data, format="json")
	assert response.status_code == 201 # type: ignore
	assert inventorySupply.objects.filter(name="Aceite").exists()
from django.test import TestCase

