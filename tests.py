# tests_alt.py

from library_core import create_library

def test_full_flow():
    lib = create_library()
    
    # Add book and member
    lib["add_book"]("111", "Python Guide", "Jane Doe", "Non-Fiction", 2)
    lib["add_member"]("M1", "Ali", "ali@test.com")
    
    # Borrow
    lib["borrow_book"]("M1", "111")
    
    # Search
    results = lib["search_books"]("Python")
    assert len(results) == 1
    assert results[0]["isbn"] == "111"
    
    # Return
    lib["return_book"]("M1", "111")
    
    # Delete
    lib["delete_book"]("111")
    
    # Ensure gone
    assert "111" not in lib["get_books"]()
    print("✅ Alternative design test passed!")

if __name__ == "__main__":
    test_full_flow()