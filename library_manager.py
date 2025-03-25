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

# Custom CSS for specific menu items
st.markdown("""
    <style>
    .sidebar {
        color: white;
        background-color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

menu = ["Home", "Add a Book", "Display All Books", "Edit a Book", "Search for a Book", "Statistics", "Remove a Book"]

# Initialize session state for choice if not already set
if 'choice' not in st.session_state:
    st.session_state.choice = "Home"

# Display menu items as buttons
for item in menu:
    if st.sidebar.button(item, key=item):
        st.session_state.choice = item

choice = st.session_state.choice


# Custom CSS for the entire app
st.markdown(
    """
    <style>
    body {
        background-color: #ffffff;    
    }
    
    .stApp {
        background-color: #ffffff;
    }
      
    div[data-baseweb="select"] > div {
        background-color:rgb(255, 214, 193) !important;
    }
    input {
        background-color: rgb(255, 234, 223) !important;
        border: 1px solid #d14b11 !important;
    }
    
    /* Sidebar bg */
   .stSidebar {
     background: linear-gradient(135deg, #d48a56, #ed8830); 
     border-radius: 0px 15px 15px 0px;
     box-shadow: 2px 0 15px rgba(0, 0, 0, 0.5); 
     border-left: 3px solid #f4a261; 
    }
    
   h2, label, span {
        text-align: start;
        font-weight: bold;
        background-color: #d14b11; 
        -webkit-background-clip: text;
        -webkit-text-fill-color: #d14b11;
        transition: 0.3s;       
    }
    
    /* tabs styling for download button*/
    div.stTabs button[data-baseweb="tab"] {
        background-color: #ff9455;    
        color: white;     
        border: none;
        border-radius: 20px;
        padding: 12px 22px;
        margin-right: 8px;
        font-weight: bold !important;    
        cursor: pointer;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
    }

    div.stTabs button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #ffc300;   
        color: #023e8a;         
        border-bottom: 4px solid #9eb5d3;
    }

    /* custom styling for button */
   .stButton > button {
        color: #fff;
        padding: 14px 40px;
        background-color: #d14b11 ; 
        border: none;
        border-radius: 10px;
        width: 100%;
        cursor: pointer;
        text-transform: uppercase;
        transition: 0.3s;
        position: relative;
        overflow: hidden;
        outline: none;
        z-index: 1;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.2);
    }

    .stButton > button::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(120deg, #cb5421, #e1710f); 
        z-index: -1;
        transition: 0.4s;
        transform: scaleX(0);
        transform-origin: left;
    }

    .stButton > button:hover::before {
        transform: scaleX(1);
    }

   .stButton > button:hover {
        color: #fff;
        transform: translateY(-2px);
    }
    .stButton > button:active,
    .stButton > button:focus {
      color: white !important; 
    }
  
  
   /* Custom styling for success message */
    .stSuccess {
        background-color: #edd4de; 
        color: #b2236f;  
        padding: 6px;
        border-radius: 5px;
        font-size: 1.2em;
    }
    @media (max-width: 480px) {
    .stSuccess {
        font-size: 1em;  
        padding: 1px;
        border-radius: 2px;
        }
    }
    /* Blinking animation for error message */
    @keyframes fastBlink {
        0% { opacity: 0; }
        25% { opacity: 1; }
        50% { opacity: 0; }
        75% { opacity: 1; }
        100% { opacity: 0; }
    }
        
        
    /* Custom styling for error message */
    .stError {
        background-color: #ffd0d0; 
        color: #ff0f0f;  
        padding: 10px;
        border-radius: 5px;
        animation: fastBlink 0.6s ease-in-out 1; 
    }
    @media (max-width: 480px) {
    .stError {
        font-size: 1em; 
        padding: 4px; 
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Home Page
if choice == "Home":
    
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&display=swap');
            .heading-1 {
                text-align: center;
                font-size: 45px !important; 
                text-transform: uppercase;
                background-size: 300% 300%;
                font-family: 'Oswald', sans-serif !important;
                color: #d14b11 !important;  
            }

            @media screen and (max-width: 600px) {
                .heading-1 {
                    font-size: 19px !important;
                }
            }

            .heading-1::before {
                content: "📚";;
            }
        </style>
        
        <h1 class="heading-1">Welcome to Personal Library Manager</h1>
    """, unsafe_allow_html=True)
    
    # Little paragraph Custom text for password strength
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Delish+Swash+Caps&display=swap');
            
            .custom-text {
                font-family: 'Delish Swash Caps', cursive;
                text-align: center;
                color: #000000;
                font-size: 18px !important; 
            }

            @media screen and (max-width: 768px) {
                .custom-text {
                    font-size: 16px !important;
                }
            }

            /* Mobile View */
            @media screen and (max-width: 480px) {
                .custom-text {
                    font-size: 14px !important;
                }
            }  
        </style>
        
        <p class="custom-text">This application allows you to manage your personal book collection efficiently. 
        You can add, remove, edit, search, and organize your books with ease.</p>
    """, unsafe_allow_html=True)
    
    # for image
    st.image("rb_39405.png", caption="Manage Your Books Easily", use_container_width=True)
    
    
    # Library Section
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&display=swap');
            .heading-5 {
                font-size: 45px !important; 
                text-transform: uppercase;
                background-size: 300% 300%;
                font-family: 'Oswald', sans-serif !important;
                color: #d14b11 !important;  
            }

            @media screen and (max-width: 600px) {
                .heading-5 {
                    font-size: 19px !important;
                }
            }

            .heading-5::before {
                content: "📚";
            }
        </style>
        
        <h1 class="heading-5">Your Library</h1>
    """, unsafe_allow_html=True)

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
                    border-radius: 10px;
                    padding: 20px;
                    margin-bottom: 15px;
                    box-shadow: 4px 4px 12px rgba(215, 176, 139, 0.96);
                    background-color: rgb(255, 234, 223);
                    width: 300px;
                    ">
                    <img src="data:image/png;base64,{img_base64}" width="300px" height="200px" style="border-radius: 5px; object-fit: contain;" />
                    <h5 style="color: #000000; margin-top:10px">{book['title']}</h4>
                    <p><strong>Author:</strong> {book['author']}</p>
                    <p><strong>Genre:</strong> {book['genre']}</p>
                    <p><strong>Year:</strong> {book['year']}</p>
                    <p><strong>Status:</strong> {'Read' if book['read'] else 'To Read'}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Download Section Below the Books
        st.markdown("""
          <style>
              @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&display=swap');
               .heading-2 {
                  font-size: 45px !important; 
                  text-transform: uppercase;
                  background-size: 300% 300%;
                  font-family: 'Oswald', sans-serif !important;
                  color: #d14b11 !important;
                  margin-top: 30px !important;
                  margin-bottom: 20px !important;  
                }

               @media screen and (max-width: 600px) {
                .heading-2 {
                    font-size: 19px !important;
                }
             }

               .heading-2::before {
                 content: "📥";
                }
          </style>
        
           <h1 class="heading-2">Download Library</h1>
        """, unsafe_allow_html=True)

        # Convert Library Data to DataFrame
        df = pd.DataFrame(library)

        # Convert DataFrame to CSV
        csv = df.to_csv(index=False).encode("utf-8")

        # Convert Library Data to JSON
        json_data = json.dumps(library, indent=4).encode("utf-8")

        # tabs for CSV and JSON download
        tab1, tab2 = st.tabs(["CSV Download", "JSON Download"])

        with tab1:
            st.markdown(
                f"""
                <a href="data:text/csv;base64,{base64.b64encode(csv).decode()}" download="library.csv">
                    <button style="
                    color: white !important;
                    padding: 12px 60px;
                    background: #d14b11;
                    width: 100%;
                    border: none;
                    border-radius: 10px;
                    cursor: pointer;
                    transition: transform 0.3s ease-in-out;
                    box-shadow: 0px 2px 12px rgba(245, 117, 42, 0.60);">
                    Download CSV
                    </button>
                </a>
                <style>
                a:hover button {{
                    transform: scale(1.02);
                    background: #d85116 !important;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

        with tab2:
            st.markdown(
                f"""
                <a href="data:application/json;base64,{base64.b64encode(json_data).decode()}" download="library.json">
                    <button style="
                    color: white !important;
                    padding: 12px 60px;
                    background: #d14b11;
                    width: 100%;
                    margin-top: 20px;
                    border: none;
                    border-radius: 10px; 
                    cursor: pointer;
                    transition: transform 0.3s ease-in-out;
                    box-shadow: 0px 2px 12px rgba(245, 117, 42, 0.60);">
                    Download JSON
                    </button>
                </a>
                <style>
                a:hover button {{
                    transform: scale(1.02);
                    background: #d85116 !important;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

    else:
        st.markdown('<div class="stError">⚠️ No books in your library. </div>', unsafe_allow_html=True)
      
 
# Add a Book      
elif choice == "Add a Book":
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&display=swap');
            .heading-1 {
                font-size: 45px !important; 
                text-transform: uppercase;
                background-size: 300% 300%;
                font-family: 'Oswald', sans-serif !important;
                color: #d14b11 !important;  
            }

            @media screen and (max-width: 600px) {
                .heading-1 {
                    font-size: 19px !important;
                }
            }

            .heading-1::before {
                content: "➕";
            }
        </style>
        
        <h1 class="heading-1">Add a New Book</h1>
    """, unsafe_allow_html=True)
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
                "year": int(year),  
                "genre": genre,
                "read": read_status == "Yes",
                "image": image_path
            }
            library.append(new_book)
            save_library(library)
            st.markdown(f"<div class='stSuccess'>✔ Your '{title}' book added to your library. </div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="stError">⚠️ Please enter all required fields correctly. </div>', unsafe_allow_html=True)


# Display All Books
elif choice == "Display All Books":
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&display=swap');
            .heading-1 {
                font-size: 45px !important; 
                text-transform: uppercase;
                background-size: 300% 300%;
                font-family: 'Oswald', sans-serif !important;
                color: #d14b11 !important;  
            }

            @media screen and (max-width: 600px) {
                .heading-1 {
                    font-size: 19px !important;
                }
            }

            .heading-1::before {
                content: "📚";
            }
        </style>
        
        <h1 class="heading-1">Your Library</h1>
    """, unsafe_allow_html=True)

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
                    border-radius: 10px;
                    padding: 20px;
                    margin-bottom: 15px;
                    box-shadow: 4px 4px 12px rgba(215, 176, 139, 0.96);
                    background-color: rgb(255, 234, 223);
                    width: 300px;
                    ">
                    <img src="data:image/png;base64,{img_base64}" width="300px" height="200px" style="border-radius: 5px; object-fit: contain;" />
                    <h5 style="color: #000000; margin-top:10px">{book['title']}</h4>
                    <p><strong>Author:</strong> {book['author']}</p>
                    <p><strong>Genre:</strong> {book['genre']}</p>
                    <p><strong>Year:</strong> {book['year']}</p>
                    <p><strong>Status:</strong> {'Read' if book['read'] else 'To Read'}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Download Section Below the Books
        st.markdown("""
          <style>
              @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&display=swap');
               .heading-2 {
                  font-size: 45px !important; 
                  text-transform: uppercase;
                  background-size: 300% 300%;
                  font-family: 'Oswald', sans-serif !important;
                  color: #d14b11 !important;
                  margin-top: 30px !important;
                  margin-bottom: 20px !important;  
                }

               @media screen and (max-width: 600px) {
                .heading-2 {
                    font-size: 19px !important;
                }
             }

               .heading-2::before {
                 content: "📥";
                }
          </style>
        
           <h1 class="heading-2">Download Library</h1>
        """, unsafe_allow_html=True)

        # Convert Library Data to DataFrame
        df = pd.DataFrame(library)

        # Convert DataFrame to CSV
        csv = df.to_csv(index=False).encode("utf-8")

        # Convert Library Data to JSON
        json_data = json.dumps(library, indent=4).encode("utf-8")

        # tabs for CSV and JSON download
        tab1, tab2 = st.tabs(["CSV Download", "JSON Download"])

        with tab1:
            st.markdown(
                f"""
                <a href="data:text/csv;base64,{base64.b64encode(csv).decode()}" download="library.csv">
                    <button style="
                    color: white !important;
                    padding: 12px 60px;
                    background: #d14b11;
                    width: 100%;
                    border: none;
                    border-radius: 10px;
                    cursor: pointer;
                    transition: transform 0.3s ease-in-out;
                    box-shadow: 0px 2px 12px rgba(245, 117, 42, 0.60);">
                    Download CSV
                    </button>
                </a>
                <style>
                a:hover button {{
                    transform: scale(1.02);
                    background: #d85116 !important;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

        with tab2:
            st.markdown(
                f"""
                <a href="data:application/json;base64,{base64.b64encode(json_data).decode()}" download="library.json">
                    <button style="
                    color: white !important;
                    padding: 12px 60px;
                    background: #d14b11;
                    width: 100%;
                    margin-top: 20px;
                    border: none;
                    border-radius: 10px; 
                    cursor: pointer;
                    transition: transform 0.3s ease-in-out;
                    box-shadow: 0px 2px 12px rgba(245, 117, 42, 0.60);">
                    Download JSON
                    </button>
                </a>
                <style>
                a:hover button {{
                    transform: scale(1.02);
                    background: #d85116 !important;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

    else:
        st.markdown('<div class="stError">⚠️ No books in your library. </div>', unsafe_allow_html=True)


# Edit a Book
elif choice == "Edit a Book":
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&display=swap');
            .heading-1 {
                font-size: 45px !important; 
                text-transform: uppercase;
                background-size: 300% 300%;
                font-family: 'Oswald', sans-serif !important;
                color: #d14b11 !important;  
            }

            @media screen and (max-width: 600px) {
                .heading-1 {
                    font-size: 19px !important;
                }
            }

            .heading-1::before {
                content: "✏️";
            }
        </style>
        
        <h1 class="heading-1">Edit a Book</h1>
    """, unsafe_allow_html=True)
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
            uploaded_image = st.file_uploader("Upload New Book Cover", type=["jpg", "png", "jpeg"])

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
                st.markdown(f"<div class='stSuccess'>'{title}'✔ Updated Seccessfully</div>", unsafe_allow_html=True)
    else:
        st.markdown('<div class="stError">⚠️ No books to edit. </div>', unsafe_allow_html=True)
        
 
# Search for a Book
elif choice == "Search for a Book":
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&display=swap');
            .heading-1 {
                font-size: 45px !important; 
                text-transform: uppercase;
                background-size: 300% 300%;
                font-family: 'Oswald', sans-serif !important;
                color: #d14b11 !important;  
            }

            @media screen and (max-width: 600px) {
                .heading-1 {
                    font-size: 19px !important;
                }
            }

            .heading-1::before {
                content: "🔎";
            }
        </style>
        
        <h1 class="heading-1">Search for a Book</h1>
    """, unsafe_allow_html=True)
    search_type = st.radio("Search by:", ["Title", "Author"])
    query = st.text_input(f"Enter {search_type}:")

    if st.button("Search"):
        if query.strip() == "":
            st.markdown(f'<div class="stError">⚠️ Please enter a {search_type.lower()} to find your book. </div>', unsafe_allow_html=True)
        else:
            results = [book for book in library if query.lower() in book[search_type.lower()].lower()]
            if results:
                cols = st.columns(3)  
                for index, book in enumerate(results):
                    with cols[index % 3]:  
                        image_path = book["image"] if book["image"] and os.path.exists(book["image"]) else "placeholder.png"
                        
                        # Convert Image to Base64
                        img_base64 = image_to_base64(image_path)

                        st.markdown(
                            f"""
                            <div style="
                                border: 2px solid #d14b11;
                                border-radius: 10px;
                                padding: 15px;
                                margin-bottom: 10px;
                                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                                background-color: rgb(255, 234, 223);">
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
            else:
                st.markdown('<div class="stError">⚠️ No matching books found. </div>', unsafe_allow_html=True)

  
# Books Statistics                
elif choice == "Statistics":
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&display=swap');
            .heading-1 {
                font-size: 45px !important; 
                text-transform: uppercase;
                background-size: 300% 300%;
                font-family: 'Oswald', sans-serif !important;
                color: #d14b11 !important;
                margin-bottom: 20px !important;  
            }

            @media screen and (max-width: 600px) {
                .heading-1 {
                    font-size: 19px !important;
                }
            }

            .heading-1::before {
                content: "📊";
            }
        </style>
        
        <h1 class="heading-1">Library Statistics</h1>
    """, unsafe_allow_html=True)
    st.markdown("""
       <style>
           [data-testid="stHorizontalBlock"] {
             display: flex;
             flex-wrap: wrap;
             justify-content: space-around;
            }

           [data-testid="stHorizontalBlock"] > div {
             flex: 1 1 20%;
             min-width: 120px;
             margin-bottom: 10px;
            }
       </style>
    """, unsafe_allow_html=True)

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
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&display=swap');
            .heading-1 {
                font-size: 45px !important; 
                text-transform: uppercase;
                background-size: 300% 300%;
                font-family: 'Oswald', sans-serif !important;
                color: #d14b11 !important;  
            }

            @media screen and (max-width: 600px) {
                .heading-1 {
                    font-size: 19px !important;
                }
            }

            .heading-1::before {
                content: "🗑️";
            }
        </style>
        
        <h1 class="heading-1">Remove a Book</h1>
    """, unsafe_allow_html=True)
    book_titles = [book["title"] for book in library]

    if book_titles:
        book_to_remove = st.selectbox("Select a book to remove:", book_titles)
        if st.button("Remove Book"):
            library = [book for book in library if book["title"] != book_to_remove]
            save_library(library)
            st.markdown(f"<div class='stSuccess'>✔ Your '{book_to_remove}' book removed from your library. </div>", unsafe_allow_html=True)
    else:
        st.markdown('<div class="stError">⚠️ No books in the library. </div>', unsafe_allow_html=True)

