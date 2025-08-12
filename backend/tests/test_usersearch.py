import pytest

@pytest.mark.parametrize(
        ('search_term', 'messages'), (
            ('TEs', [b'test', b'test2', b'test3']),
            ('xx', [b'error', b'no results found']))
        )
def test_usersearch(client, auth, search_term, messages):
    response = client.get('/users/search')
    # Check for a redirect response (302)
    assert response.status_code == 302
    # Check that client is redirected to login page
    assert 'auth/login' in response.location
    
    auth.login()
    response = client.get(f'/users/search?user={search_term}')
    assert response.status_code == 200
    for m in messages:
        assert m in response.data