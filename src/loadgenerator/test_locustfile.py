from unittest.mock import Mock

import locustfile


def test_index_calls_get_root():
  l = Mock()

  locustfile.index(l)

  l.client.get.assert_called_once_with("/")


def test_set_currency_posts_known_currency():
  l = Mock()

  locustfile.setCurrency(l)

  args, _ = l.client.post.call_args
  assert args[0] == "/setCurrency"
  assert args[1]["currency_code"] in ['EUR', 'USD', 'JPY', 'CAD', 'GBP', 'TRY']


def test_browse_product_uses_known_product():
  l = Mock()

  locustfile.browseProduct(l)

  args, _ = l.client.get.call_args
  product_id = args[0].split("/product/")[1]
  assert product_id in locustfile.products


def test_view_cart_calls_get_cart():
  l = Mock()

  locustfile.viewCart(l)

  l.client.get.assert_called_once_with("/cart")


def test_add_to_cart_gets_product_then_posts_it():
  l = Mock()

  locustfile.addToCart(l)

  get_args, _ = l.client.get.call_args
  post_args, _ = l.client.post.call_args
  assert post_args[0] == "/cart"
  assert get_args[0] == "/product/" + post_args[1]["product_id"]
  assert 1 <= post_args[1]["quantity"] <= 10


def test_empty_cart_posts_empty_endpoint():
  l = Mock()

  locustfile.empty_cart(l)

  l.client.post.assert_called_once_with('/cart/empty')


def test_checkout_posts_required_fields():
  l = Mock()

  locustfile.checkout(l)

  checkout_args, _ = l.client.post.call_args_list[-1]
  assert checkout_args[0] == "/cart/checkout"
  payload = checkout_args[1]
  for field in [
    'email', 'street_address', 'zip_code', 'city', 'state', 'country',
    'credit_card_number', 'credit_card_expiration_month',
    'credit_card_expiration_year', 'credit_card_cvv',
  ]:
    assert field in payload


def test_logout_calls_get_logout():
  l = Mock()

  locustfile.logout(l)

  l.client.get.assert_called_once_with('/logout')


def test_user_behavior_starts_with_index():
  assert locustfile.UserBehavior.on_start is not None
  assert locustfile.index in locustfile.UserBehavior.tasks
