from app.core.hash_helper import get_password_hash, verify_password

def test__check_password_hash_is_correct():
    password: str = "abc"
    hashed_password: str = get_password_hash(password)
    assert verify_password(password, hashed_password)
    
def test__check_salted_password_hash_is_correct():
    password: str = "same password should give different hashed password"
    assert get_password_hash(password) != get_password_hash(password)
    
    
    