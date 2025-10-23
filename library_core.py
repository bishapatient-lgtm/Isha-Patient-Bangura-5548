# library_core.py — Alternative implementation using functional encapsulation

# Immutable valid genres
VALID_GENRES = ("Fiction", "Non-Fiction", "Sci-Fi", "Fantasy", "Mystery", "Biography")

def create_library():
    """
    Returns a dictionary containing the library's data and operations.
    This simulates a "library object" using only allowed data structures.
    """
    books = {}   # ISBN → {title, author, genre, total_copies}
    members = [] # list of {member_id, name, email, borrowed_books: [isbn]}

    # --- Helper functions (private to this library instance) ---
    def _find_member(member_id):
        return next((m for m in members if m["member_id"] == member_id), None)

    def _get_borrowed_count(isbn):
        return sum(1 for m in members for b in m["borrowed_books"] if b == isbn)

    def _is_genre_valid(genre):
        return genre in VALID_GENRES

    # --- Public operations ---
    def add_book(isbn, title, author, genre, total_copies):
        if not _is_genre_valid(genre):
            raise ValueError(f"Invalid genre: {genre}. Allowed: {VALID_GENRES}")
        if isbn in books:
            raise ValueError(f"Book with ISBN {isbn} already exists.")
        if total_copies < 0:
            raise ValueError("Total copies cannot be negative.")
        books[isbn] = {
            "title": title,
            "author": author,
            "genre": genre,
            "total_copies": total_copies
        }

    def add_member(member_id, name, email):
        if _find_member(member_id):
            raise ValueError(f"Member ID {member_id} already exists.")
        members.append({
            "member_id": member_id,
            "name": name,
            "email": email,
            "borrowed_books": []
        })

    def search_books(query):
        query = query.lower()
        return [
            {**info, "isbn": isbn}

                      for isbn, info in books.items()
            if query in info["title"].lower() or query in info["author"].lower()
        ]

    def update_book(isbn, **kwargs):
        if isbn not in books:
            raise KeyError(f"Book {isbn} not found.")
        book = books[isbn]
        if "genre" in kwargs and not _is_genre_valid(kwargs["genre"]):
            raise ValueError(f"Invalid genre: {kwargs['genre']}")
        if "total_copies" in kwargs:
            new_copies = kwargs["total_copies"]
            if new_copies < 0:
                raise ValueError("Copies cannot be negative.")
            borrowed = _get_borrowed_count(isbn)
            if new_copies < borrowed:
                raise ValueError(f"Cannot set copies below {borrowed} (currently borrowed).")
        for key, value in kwargs.items():
            if value is not None:
                book[key] = value

    def update_member(member_id, **kwargs):
        member = _find_member(member_id)
        if not member:
            raise KeyError(f"Member {member_id} not found.")
        for key, value in kwargs.items():
            if value is not None:
                member[key] = value

    def delete_book(isbn):
        if isbn not in books:
            raise KeyError(f"Book {isbn} not found.")
        if _get_borrowed_count(isbn) > 0:
            raise ValueError(f"Cannot delete {isbn} — it is borrowed.")
        del books[isbn]

    def delete_member(member_id):
        member = _find_member(member_id)
        if not member:
            raise KeyError(f"Member {member_id} not found.")
        if member["borrowed_books"]:
            raise ValueError(f"Cannot delete {member_id} — has borrowed books.")
        members[:] = [m for m in members if m["member_id"] != member_id]

    def borrow_book(member_id, isbn):
        member = _find_member(member_id)
        if not member:
            raise KeyError(f"Member {member_id} not found.")
        if isbn not in books:
            raise KeyError(f"Book {isbn} not found.")
        if len(member["borrowed_books"]) >= 3:
            raise ValueError(f"{member_id} has reached the 3-book limit.")
        available = books[isbn]["total_copies"] - _get_borrowed_count(isbn)
        if available <= 0:
            raise ValueError(f"No copies of {isbn} available.")
        member["borrowed_books"].append(isbn)

    def return_book(member_id, isbn):
        member = _find_member(member_id)
        if not member:
            raise KeyError(f"Member {member_id} not found.")
        if isbn not in member["borrowed_books"]:
            raise ValueError(f"{member_id} has not borrowed {isbn}.")
        member["borrowed_books"].remove(isbn)

    def get_books():
        return books

    def get_members():
        return members

    # Return public interface
    return {
        "add_book": add_book,
        "add_member": add_member,
        "search_books": search_books,
        "update_book": update_book,
        "update_member": update_member,
        "delete_book": delete_book,
        "delete_member": delete_member,
        "borrow_book": borrow_book,
        "return_book": return_book,
        "get_books": get_books,
        "get_members": get_members,
        "VALID_GENRES": VALID_GENRES
    }
