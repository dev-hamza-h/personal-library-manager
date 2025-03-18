import streamlit as st
import json
import os
from PIL import Image
import base64
import pandas as pd
import plotly.express as px


# Function to convert image to Base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
 


# Define folders
DATA_FOLDER = "data"
IMAGE_FOLDER = "book_images"
LIBRARY_FILE = os.path.join(DATA_FOLDER, "library.json")

# Create folders if they don't exist
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Load library from file
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# Save library to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Load existing books
library = load_library()

# Set Page Config
st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")

# Sidebar Menu
menu = ["Home", "Add a Book", "Display All Books" , "Edit a Book", "Search for a Book", "Statistics", "Remove a Book"]
choice = st.sidebar.radio("📌 Select an option", menu)



# Home Page
if choice == "Home":
    st.title("📚 Welcome to Personal Library Manager")
    st.write(
        """
        This application allows you to manage your personal book collection efficiently. 
        You can add, remove, edit, search, and organize your books with ease.
        """
    )
    st.markdown(
    """
    <style>
        @media (max-width: 600px) {
            img {
                width: 350px !important;
            }
        }
        @media (min-width: 601px) {
            img {
                width: 1000px !important;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
    )

    # Displaying the image
    st.image("rb_39405.png", caption="Manage Your Books Easily", use_container_width=False) 
    

 
# Add a Book      
elif choice == "Add a Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Enter Book Title:")
    author = st.text_input("Enter Author:")
    year = st.text_input("Enter Publication Year (YYYY):") 
    genre = st.text_input("Enter Genre:")
    read_status = st.radio("Have you read this book?", ("Yes", "No"))
    uploaded_image = st.file_uploader("Upload Book Cover (Required)", type=["jpg", "png", "jpeg"])
    
    if st.button("Add Book"):
        if title and author and year.isdigit() and uploaded_image:
            from PIL import Image
            image = Image.open(uploaded_image)  
            image = image.resize((200, 200))  
            image_path = os.path.join(IMAGE_FOLDER, f"{title.replace(' ', '_')}.png")
            image.save(image_path)  
            
            new_book = {
                "title": title,
                "author": author,
                "year": int(year),  # Convert to integer
                "genre": genre,
                "read": read_status == "Yes",
                "image": image_path
            }
            library.append(new_book)
            save_library(library)
            st.success(f"📖 '{title}' added to your library!")
        else:
            st.warning("⚠️ Please enter all required fields correctly!")




# Display All Books
elif choice == "Display All Books":
    st.subheader("📚 Your Library")

    if library:
        sort_option = st.selectbox("Sort Books By:", ["Title", "Author", "Year"])
        sorted_books = sorted(library, key=lambda x: x[sort_option.lower()])

        cols = st.columns(3)

        for index, book in enumerate(sorted_books):
            with cols[index % 3]:
                image_path = book["image"] if book["image"] and os.path.exists(book["image"]) else "placeholder.png"
                
                # Convert Image to Base64
                img_base64 = image_to_base64(image_path)

                st.markdown(
                    f"""
                    <div style="
                    border: 2px solid #4185ce;
                    border-radius: 10px;
                    padding: 15px;
                    margin-bottom: 10px;
                    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                    background-color: #f9f9f9;">
                    <img src="data:image/png;base64,{img_base64}" width="300px" height="200px" style="border-radius: 5px; object-fit: contain;" />
                    <h4 style="color: #333;">{book['title']}</h4>
                    <p><strong>Author:</strong> {book['author']}</p>
                    <p><strong>Genre:</strong> {book['genre']}</p>
                    <p><strong>Year:</strong> {book['year']}</p>
                    <p><strong>Status:</strong> {'Read' if book['read'] else 'To Read'}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Download Section Below the Books
        st.subheader("📥 Download Library")

        # Convert Library Data to DataFrame
        df = pd.DataFrame(library)

        # Convert DataFrame to CSV
        csv = df.to_csv(index=False).encode("utf-8")

        # Convert Library Data to JSON
        json_data = json.dumps(library, indent=4).encode("utf-8")

      
        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="library.csv",
                mime="text/csv",
                help="Download your library as a CSV file."
            )

        with col2:
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name="library.json",
                mime="application/json",
                help="Download your library as a JSON file."
            )

    else:
        st.warning("No books in your library!")



# Edit a Book
elif choice == "Edit a Book":
    st.subheader("✏️ Edit a Book")
    book_titles = [book["title"] for book in library]

    if book_titles:
        book_to_edit = st.selectbox("Select a book to edit:", book_titles)
        book = next((b for b in library if b["title"] == book_to_edit), None)

        if book:
            title = st.text_input("Title:", book["title"])
            author = st.text_input("Author:", book["author"])
            year = st.number_input("Publication Year:", min_value=1000, max_value=3000, step=1, value=book["year"])
            genre = st.text_input("Genre:", book["genre"])
            read_status = st.radio("Read Status:", ("Yes", "No"), index=0 if book["read"] else 1)
            uploaded_image = st.file_uploader("Upload New Book Cover (Optional)", type=["jpg", "png", "jpeg"])

            if st.button("Update Book"):
                if uploaded_image is not None:
                    image = Image.open(uploaded_image)  
                    image = image.resize((200, 200))  
                    image_path = os.path.join(IMAGE_FOLDER, f"{title.replace(' ', '_')}.png")
                    image.save(image_path)  
                    book["image"] = image_path  

                book.update({
                    "title": title,
                    "author": author,
                    "year": year,
                    "genre": genre,
                    "read": True if read_status == "Yes" else False
                })
                save_library(library)
                st.success(f"✅ '{title}' updated successfully!")
    else:
        st.warning("No books to edit!")
        
        
 
# Search for a Book
elif choice == "Search for a Book":
    st.subheader("🔎 Search for a Book")
    search_type = st.radio("Search by:", ["Title", "Author"])
    query = st.text_input(f"Enter {search_type}:")

    if st.button("Search"):
        if query.strip() == "":
            st.warning(f"⚠️ Please enter a {search_type.lower()} to find your book!")
        else:
            results = [book for book in library if query.lower() in book[search_type.lower()].lower()]
            if results:
                cols = st.columns(3)  
                for index, book in enumerate(results):
                    with cols[index % 3]:  # Distribute books in columns
                        image_path = book["image"] if book["image"] and os.path.exists(book["image"]) else "placeholder.png"
                        
                        # Convert Image to Base64
                        img_base64 = image_to_base64(image_path)

                        st.markdown(
                            f"""
                            <div style="
                                border: 2px solid #4CAF50;
                                border-radius: 10px;
                                padding: 15px;
                                margin-bottom: 10px;
                                text-align: center;
                                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                                background-color: #f9f9f9;">
                                <img src="data:image/png;base64,{img_base64}" width="300px" height="200px" style="border-radius: 5px; object-fit: contain;" />
                                <h4 style="color: #333;">📖 {book['title']}</h4>
                                <p>✍️ {book['author']} ({book['year']})</p>
                                <p>📚 {book['genre']}</p>
                                <p style="font-weight: bold; color: {'green' if book['read'] else 'red'};">
                                    {'✅ Read' if book['read'] else '❌ Unread'}
                                </p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            else:
                st.warning("No matching books found!")
  
  
  
                
elif choice == "Statistics":
    st.subheader("📊 Library Statistics")

    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    unread_books = total_books - read_books
    read_percentage = (read_books / total_books) * 100 if total_books > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("<p style='text-align: center;'>Total Books</p>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: #1E73BE; text-align: center;'>{total_books}</h3>", unsafe_allow_html=True)

    with col2:
        st.markdown("<p style='text-align: center;'>Read</p>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: #28A745; text-align: center;'>{read_books}</h3>", unsafe_allow_html=True)

    with col3:
        st.markdown("<p style='text-align: center;'>Unread</p>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: #DC3545; text-align: center;'>{unread_books}</h3>", unsafe_allow_html=True)

    with col4:
        st.markdown("<p style='text-align: center;'>Percentage Read</p>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: #FFC107; text-align: center;'>{read_percentage:.2f}%</h3>", unsafe_allow_html=True)

    data = {
        "Category": ["Total Books", "Read", "Unread", "Percentage Read"],
        "Count": [total_books, read_books, unread_books, read_percentage]
    }

    df = pd.DataFrame(data)

    fig = px.bar(df, x="Category", y="Count", text="Count", color="Category", 
                 color_discrete_map={"Total Books": "#1E73BE", "Read": "#28A745", 
                                     "Unread": "#DC3545", "Percentage Read": "#FFC107"})

    fig.update_traces(textposition="outside") 
    fig.update_layout(xaxis_title="Category", yaxis_title="Value")

    st.plotly_chart(fig)                
                
     
                        
# Remove a Book
elif choice == "Remove a Book":
    st.subheader("🗑️ Remove a Book")
    book_titles = [book["title"] for book in library]

    if book_titles:
        book_to_remove = st.selectbox("Select a book to remove:", book_titles)
        if st.button("Remove Book"):
            library = [book for book in library if book["title"] != book_to_remove]
            save_library(library)
            st.success(f"❌ '{book_to_remove}' removed from your library!")
    else:
        st.warning("No books in the library!")


     
        
        
 
                
 





 
    
    
