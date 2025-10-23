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
            for isbn, info in