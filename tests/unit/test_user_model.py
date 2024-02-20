from application.auth.models import User

def test_new_user():
    user = User(name='Test', email='test@test.com', password='jkljkl')
    
    assert user.name == 'Test'
    assert user.email == 'test@test.com'
    assert user.password == 'jkljkl'