import pytest
from unittest.mock import Mock
from grpc_health.v1 import health_pb2

import demo_pb2
import recommendation_server


class FakeContext:
  """Minimal stand-in for grpc.ServicerContext, just enough for these handlers."""

  def __init__(self):
    self.code = None
    self.details = None

  def set_code(self, code):
    self.code = code

  def set_details(self, details):
    self.details = details


def test_list_recommendations_excludes_requested_products(monkeypatch):
  catalog = demo_pb2.ListProductsResponse(products=[
    demo_pb2.Product(id="A"),
    demo_pb2.Product(id="B"),
    demo_pb2.Product(id="C"),
  ])
  fake_stub = Mock()
  fake_stub.ListProducts.return_value = catalog
  monkeypatch.setattr(recommendation_server, "product_catalog_stub", fake_stub, raising=False)

  service = recommendation_server.RecommendationService()
  request = demo_pb2.ListRecommendationsRequest(product_ids=["A"])

  response = service.ListRecommendations(request, FakeContext())

  assert "A" not in response.product_ids
  assert set(response.product_ids) <= {"B", "C"}


def test_check_reports_serving():
  service = recommendation_server.RecommendationService()

  response = service.Check(health_pb2.HealthCheckRequest(), FakeContext())

  assert response.status == health_pb2.HealthCheckResponse.SERVING


def test_watch_crashes_on_missing_unimplemented_status():
  # Watch() references health_pb2.HealthCheckResponse.UNIMPLEMENTED, which does
  # not exist in the currently pinned grpcio-health-checking version (only
  # UNKNOWN/SERVING/NOT_SERVING/SERVICE_UNKNOWN are defined). This test
  # documents that calling Watch() currently raises instead of returning a response.
  service = recommendation_server.RecommendationService()

  with pytest.raises(AttributeError):
    service.Watch(health_pb2.HealthCheckRequest(), FakeContext())
