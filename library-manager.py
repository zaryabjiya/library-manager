import streamlit as st
import json
import os

# --- File setup ---
FILE_PATH = os.path.join(os.getcwd(), "library.json")

# --- Load library data ---
def load_library():
    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# --- Save library data ---
def save_library(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)

# --- Initialize library in session state ---
if "library" not in st.session_state:
    st.session_state.library = load_library()

# --- Functions for managing books ---
def add_book(title, author, year, genre, read):
    book = {"title": title, "author": author, "year": year, "genre": genre, "read": read}
    st.session_state.library.append(book)
    save_library(st.session_state.library)
    st.success("✅ Book added successfully!")

def remove_book(title):
    st.session_state.library = [book for book in st.session_state.library if book['title'].lower() != title.lower()]
    save_library(st.session_state.library)
    st.success("🗑️ Book removed successfully!")

def search_books(keyword, by='title'):
    return [book for book in st.session_state.library if keyword.lower() in book[by].lower()]

def display_statistics():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book['read'])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    return total_books, percentage_read

# --- Custom Styling ---
st.markdown("""
    <style>
        body { background: linear-gradient(to right, #ff7e5f, #feb47b); color: white; }
        .sidebar .sidebar-content { background-color: #2c3e50; }
        .stButton>button { background-color: #3498db; color: #ffffff; border-radius: 8px; padding: 10px 18px; }
        .stButton>button:hover { background-color: #2980b9; }
        .book-card { border: 2px solid #ddd; padding: 12px; border-radius: 12px; background-color: #ffffff; color: black; margin: 12px 0; box-shadow: 3px 3px 10px rgba(0,0,0,0.2); }
        .stProgress>div>div>div { background-color: #27ae60; }
    </style>
""", unsafe_allow_html=True)

# --- Streamlit UI setup ---
st.title("📚 Personal Library Manager")
menu = ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics"]
choice = st.sidebar.selectbox("📌 Menu", menu)

# --- Add Book ---
if choice == "Add a Book":
    st.subheader("📘 Add a New Book")
    title = st.text_input("📖 Title")
    author = st.text_input("✍️ Author")
    year = st.number_input("📅 Publication Year", min_value=0, max_value=2100, value=2024)
    genre = st.text_input("📂 Genre")
    read = st.checkbox("✅ Have you read this book?")
    if st.button("➕ Add Book"):
        if title and author:
            add_book(title, author, year, genre, read)
        else:
            st.error("❌ Title and Author are required!")

# --- Remove Book ---
elif choice == "Remove a Book":
    st.subheader("🗑️ Remove a Book")
    title = st.text_input("Enter the title of the book to remove")
    if st.button("❌ Remove Book"):
        if title:
            remove_book(title)
        else:
            st.warning("⚠️ Please enter a book title.")

# --- Search Books ---
elif choice == "Search for a Book":
    st.subheader("🔍 Search for a Book")
    search_by = st.radio("Search by", ["title", "author"])
    keyword = st.text_input("Enter your search keyword")
    if st.button("🔎 Search"):
        results = search_books(keyword, search_by)
        if results:
            for book in results:
                st.markdown(f"""
                <div class='book-card'>
                    <strong>📖 {book['title']}</strong> <br>
                    ✍️ {book['author']} ({book['year']})<br>
                    📂 {book['genre']} - {'✅ Read' if book['read'] else '📌 Unread'}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No matching books found.")

# --- Display All Books ---
elif choice == "Display All Books":
    st.subheader("📚 Your Library")
    if st.session_state.library:
        for book in st.session_state.library:
            st.markdown(f"""
            <div class='book-card'>
                <strong>📖 {book['title']}</strong> <br>
                ✍️ {book['author']} ({book['year']})<br>
                📂 {book['genre']} - {'✅ Read' if book['read'] else '📌 Unread'}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 Your library is empty!")

# --- Display Statistics ---
elif choice == "Display Statistics":
    st.subheader("📊 Library Statistics")
    total_books, percentage_read = display_statistics()
    st.write(f"📚 *Total Books:* {total_books}")
    st.progress(percentage_read / 100)
    st.write(f"✅ *Percentage Read:* {percentage_read:.2f}%")

# --- Reset Button ---
if st.sidebar.button("🔄 Reset Library Data"):
    st.session_state.library = []
    save_library([])
    st.warning("⚠️ Library data reset!")

# Footer
st.markdown("---")
st.markdown("🚀 Developed by **Zaryab Irfan**")
