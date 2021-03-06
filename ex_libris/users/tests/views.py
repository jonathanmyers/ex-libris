import pytest

from ..views import (
    UserRedirectView,
    UserUpdateView,
)


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.get_or_create(username='testuser')[0]


def generate_view(view_class, rf, user):
    # Instantiate the view directly. Never do this outside a test!
    view = view_class()
    # Generate a fake request
    request = rf.get('/fake-url')
    # Attach the user to the request
    request.user = user
    # Attach the request to the view
    view.request = request
    return view


@pytest.fixture
def user_redirect_view(rf, user):
    return generate_view(UserRedirectView, rf, user)


@pytest.fixture
def user_update_view(rf, user):
    return generate_view(UserUpdateView, rf, user)


@pytest.mark.django_db
def test_get_redirect_url(user_redirect_view):
    # Expect: '/users/testuser/', as that is the default username for
    #   the `user` fixture.
    assert user_redirect_view.get_redirect_url() == '/users/testuser/'


@pytest.mark.django_db
def test_get_success_url(user_update_view):
    # Expect: '/users/testuser/', as that is the default username for
    #   the `user` fixture.
    assert user_update_view.get_success_url() == '/users/testuser/'


def test_get_object(user_update_view, user):
    # Expect: user, as that is the request's user object
    assert user_update_view.get_object() == user
