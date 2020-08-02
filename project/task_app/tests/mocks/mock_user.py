from django.contrib.auth import get_user_model


def mock_user_profile(
        email='test@gmail.com',
        first_name='test_name',
        last_name='test_last_name',
):
    password = '123.#'
    user = get_user_model().objects.create_user(
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password
    )

    return user