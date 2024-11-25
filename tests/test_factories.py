def test_sqla_factory() -> None:
    from app.models import User
    from tests.factories import UserFactory

    user = UserFactory.build()
    assert isinstance(user, User)
    assert user.id is not None
