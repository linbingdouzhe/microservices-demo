import pytest
from grpc_health.v1 import health_pb2

import demo_pb2
import email_server


class FakeContext:
  """Minimal stand-in for grpc.ServicerContext, just enough for these handlers."""

  def __init__(self):
    self.code = None
    self.details = None

  def set_code(self, code):
    self.code = code

  def set_details(self, details):
    self.details = details


def test_dummy_send_order_confirmation_returns_empty():
  service = email_server.DummyEmailService()
  request = demo_pb2.SendOrderConfirmationRequest(
    email="buyer@example.com",
    order=demo_pb2.OrderResult(order_id="12345"),
  )

  response = service.SendOrderConfirmation(request, FakeContext())

  assert response == demo_pb2.Empty()


def test_check_reports_serving():
  service = email_server.DummyEmailService()

  response = service.Check(health_pb2.HealthCheckRequest(), FakeContext())

  assert response.status == health_pb2.HealthCheckResponse.SERVING


def test_watch_crashes_on_missing_unimplemented_status():
  # BaseEmailService.Watch references health_pb2.HealthCheckResponse.UNIMPLEMENTED,
  # which does not exist in the currently pinned grpcio-health-checking version
  # (only UNKNOWN/SERVING/NOT_SERVING/SERVICE_UNKNOWN are defined). This test
  # documents that calling Watch() currently raises instead of returning a response.
  service = email_server.DummyEmailService()

  with pytest.raises(AttributeError):
    service.Watch(health_pb2.HealthCheckRequest(), FakeContext())
