# main.py — User interface using the new library_core

from library_core import create_library

def safe_input(prompt, required=True):
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("This field is required.")

def safe_int(prompt, min_val=0):
    while True:
        try:
            val = int(input(prompt))
            if val >= min_val:
                return val
            print(f"Value must be ≥ {min_val}.")
        except ValueError:
            print("Please enter a number.")

def display_books(books, members):
    if not books:
        print("\n📚 No books.")
        return
    print("\n📚 Books:")
    for isbn, info in books.items():
        borrowed = sum(1 for m in members for b in m["borrowed_books"] if b == isbn)
        print(f"  ISBN: {isbn}")
        print(f"    Title: {info['title']}")
        print(f"    Author: {info['author']}")
        print(f"    Genre: {info['genre']}")
        print(f"    Copies: {info['total_copies']} (Available: {info['total_copies'] - borrowed})")
        print()

def display_members(members):
    if not members:
        print("\n👥 No members.")
        return
    print("\n👥 Members:")
    for m in members:
        print(f"  ID: {m['member_id']} | {m['name']} ({m['email']})")
        books = ', '.join(m['borrowed_books']) if m['borrowed_books'] else "None"
        print(f"    Borrowed: [{books}]")
        print()

def main():
    lib = create_library()
    print("🏛️  Mini Library Management System (Alternative Design)")
    
    while True:
        print("\n" + "="*50)
        print("1. Add Book")
        print("2. Add Member")
        print("3. Search Books")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. Update Book")
        print("7. Delete Book")
        print("8. View All Books")
        print("9. View All Members")
        print("0. Exit")
        print("="*50)

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                isbn = safe_input("ISBN: ")
                title = safe_input("Title: ")
                author = safe_input("Author: ")
                print("Genres:", ", ".join(lib["VALID_GENRES"]))
                genre = safe_input("Genre: ")
                copies = safe_int("Total copies: ", min_val=0)
                lib["add_book"](isbn, title, author, genre, copies)
                print("✅ Book added!")

            elif choice == "2":
                mid = safe_input("Member ID: ")
                name = safe_input("Name: ")
                email = safe_input("Email: ")
                lib["add_member"](mid, name, email)
                print("✅ Member added!")

            elif choice == "3":
                q = safe_input("Search (title/author): ")
                results = lib["search_books"](q)
                if results:
                    for r in results:
                        print(f"  - {r['title']} by {r['author']} (ISBN: {r['isbn']})")
                else:
                    print("❌ No results.")

            elif choice == "4":
                mid = safe_input("Member ID: ")
                isbn = safe_input("Book ISBN: ")
                lib["borrow_book"](mid, isbn)
                print("📥 Borrowed!")

            elif choice == "5":
                mid = safe_input("Member ID: ")
                isbn = safe_input("Book ISBN: ")
                lib["return_book"](mid, isbn)
                print("📤 Returned!")

            elif choice == "6":
                isbn = safe_input("ISBN to update: ")
                if isbn not in lib["get_books"]():
                    print("❌ Book not found.")
                    continue
                title = input(f"New title (leave blank): ").strip() or None
                author = input(f"New author (leave blank): ").strip() or None
                genre = input(f"New genre (leave blank): ").strip() or None
                copies_str = input(f"New copies (leave blank): ").strip()
                copies = int(copies_str) if copies_str.isdigit() else None
                lib["update_book"](isbn, title=title, author=author, genre=genre, total_copies=copies)
                print("✏️ Updated!")

            elif choice == "7":
                isbn = safe_input("ISBN to delete: ")
                lib["delete_book"](isbn)
                print("🗑️ Deleted!")

            elif choice == "8":
                display_books(lib["get_books"](), lib["get_members"]())

            elif choice == "9":
                display_members(lib["get_members"]())

            elif choice == "0":
                print("👋 Goodbye!")
                break

            else:
                print("❌ Invalid option.")

        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    main()