"""
Tests for the restocking order creation endpoint (POST /api/orders)
and the unit_cost field added to demand forecasts.
"""
from datetime import datetime

import pytest


def _payload(items, total_value=None):
    """Build a create-restocking-order request body from a list of item dicts."""
    if total_value is None:
        total_value = sum(i["quantity"] * i["unit_price"] for i in items)
    return {"items": items, "total_value": total_value}


class TestDemandUnitCost:
    """The Restocking feature relies on a unit_cost on each demand forecast."""

    def test_demand_forecasts_include_unit_cost(self, client):
        """Every demand forecast should expose a non-negative numeric unit_cost."""
        response = client.get("/api/demand")
        assert response.status_code == 200

        data = response.json()
        assert len(data) > 0
        for forecast in data:
            assert "unit_cost" in forecast
            assert isinstance(forecast["unit_cost"], (int, float))
            assert forecast["unit_cost"] >= 0


class TestCreateRestockingOrder:
    """Test suite for POST /api/orders (submitted restocking orders)."""

    def test_create_restocking_order_success(self, client):
        """A valid payload creates a Submitted order and returns it (201)."""
        items = [
            {"sku": "WDG-001", "name": "Industrial Widget Type A",
             "quantity": 150, "unit_price": 12.50, "trend": "increasing"},
        ]
        response = client.post("/api/orders", json=_payload(items))
        assert response.status_code == 201

        order = response.json()
        assert order["status"] == "Submitted"
        assert order["customer"] == "Internal Restocking"
        assert order["order_number"].startswith("RST-")
        assert order["warehouse"] is None
        assert order["category"] is None
        assert len(order["items"]) == 1
        # The trend field is used only for lead time and must NOT be persisted on items.
        assert "trend" not in order["items"][0]
        assert order["items"][0]["sku"] == "WDG-001"

    def test_create_restocking_order_lead_time_increasing(self, client):
        """An order of only 'increasing' items gets a 7-day lead time."""
        items = [
            {"sku": "WDG-001", "name": "Industrial Widget Type A",
             "quantity": 150, "unit_price": 12.50, "trend": "increasing"},
            {"sku": "GSK-203", "name": "High-Temperature Gasket",
             "quantity": 100, "unit_price": 8.75, "trend": "increasing"},
        ]
        response = client.post("/api/orders", json=_payload(items))
        assert response.status_code == 201

        order = response.json()
        order_date = datetime.fromisoformat(order["order_date"])
        expected_delivery = datetime.fromisoformat(order["expected_delivery"])
        assert (expected_delivery - order_date).days == 7

    def test_create_restocking_order_lead_time_uses_slowest_item(self, client):
        """Lead time is the MAX across items: a stable item (14d) dominates increasing (7d)."""
        items = [
            {"sku": "WDG-001", "name": "Industrial Widget Type A",
             "quantity": 150, "unit_price": 12.50, "trend": "increasing"},
            {"sku": "PSU-501", "name": "5V 10A Switching Power Supply",
             "quantity": 50, "unit_price": 18.99, "trend": "stable"},
        ]
        response = client.post("/api/orders", json=_payload(items))
        assert response.status_code == 201

        order = response.json()
        order_date = datetime.fromisoformat(order["order_date"])
        expected_delivery = datetime.fromisoformat(order["expected_delivery"])
        assert (expected_delivery - order_date).days == 14

    def test_submitted_order_appears_in_orders_list(self, client):
        """A submitted order is retrievable via GET /api/orders?status=Submitted."""
        items = [
            {"sku": "FLT-405", "name": "Oil Filter Cartridge",
             "quantity": 150, "unit_price": 6.25, "trend": "increasing"},
        ]
        create_response = client.post("/api/orders", json=_payload(items))
        assert create_response.status_code == 201
        new_id = create_response.json()["id"]

        list_response = client.get("/api/orders?status=Submitted")
        assert list_response.status_code == 200
        submitted = list_response.json()
        assert all(o["status"] == "Submitted" for o in submitted)
        assert any(o["id"] == new_id for o in submitted)

    def test_create_restocking_order_total_value_preserved(self, client):
        """The submitted total_value matches the requested total."""
        items = [
            {"sku": "GSK-203", "name": "High-Temperature Gasket",
             "quantity": 100, "unit_price": 8.75, "trend": "increasing"},
        ]
        payload = _payload(items, total_value=875.0)
        response = client.post("/api/orders", json=payload)
        assert response.status_code == 201
        assert abs(response.json()["total_value"] - 875.0) < 0.01

    def test_create_restocking_order_empty_items_rejected(self, client):
        """An order with no items returns 400."""
        response = client.post("/api/orders", json={"items": [], "total_value": 0})
        assert response.status_code == 400
        assert "detail" in response.json()

    def test_create_restocking_order_missing_fields_rejected(self, client):
        """A malformed item (missing required fields) returns a 422 validation error."""
        bad_payload = {"items": [{"sku": "X-1"}], "total_value": 0}
        response = client.post("/api/orders", json=bad_payload)
        assert response.status_code == 422
