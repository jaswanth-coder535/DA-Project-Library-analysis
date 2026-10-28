"""
Library Book Analysis and Data Visualization System
---------------------------------------------------
A simple, beginner-friendly Streamlit web application for analyzing
and visualizing library book data using Pandas, Matplotlib, and Seaborn.

Author: Academic Project
Technology: Python, Streamlit, Pandas, Matplotlib, Seaborn
"""

import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Library Book Analysis System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Styling (CSS) for Modern and Clean Look
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Metric Card Styling */
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 1px solid #dee2e6;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
    }
    .metric-title {
        font-size: 0.85rem;
        color: #6c757d;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #2b3a42;
        margin-top: 5px;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #495057;
        margin-top: 3px;
    }
    /* Section headers */
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1e3d59;
        border-left: 5px solid #ff6e40;
        padding-left: 10px;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    /* Info badge */
    .badge-sample {
        display: inline-block;
        background-color: #e3f2fd;
        color: #0d47a1;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Sample Data Generator (Fallback if CSV is missing)
# ---------------------------------------------------------
def create_default_csv(filepath):
    """Creates the library_books.csv file if it does not already exist."""
    data = """Book_ID,Book_Title,Author,Genre,Publication_Year,Copies_Available,Times_Borrowed,Rating
1001,To Kill a Mockingbird,Harper Lee,Fiction,1960,8,142,4.8
1002,1984,George Orwell,Fiction,1949,10,175,4.7
1003,The Great Gatsby,F. Scott Fitzgerald,Fiction,1925,6,110,4.4
1004,Pride and Prejudice,Jane Austen,Fiction,1813,7,125,4.6
1005,The Catcher in the Rye,J.D. Salinger,Fiction,1951,5,98,4.1
1006,Brave New World,Aldous Huxley,Fiction,1932,6,105,4.3
1007,The Alchemist,Paulo Coelho,Fiction,1988,12,188,4.7
1008,The Kite Runner,Khaled Hosseini,Fiction,2003,9,134,4.6
1009,A Brief History of Time,Stephen Hawking,Science,1988,7,145,4.7
1010,Cosmos,Carl Sagan,Science,1980,8,138,4.8
1011,The Selfish Gene,Richard Dawkins,Science,1976,5,82,4.4
1012,Sapiens: A Brief History of Humankind,Yuval Noah Harari,History,2011,11,195,4.8
1013,The Origin of Species,Charles Darwin,Science,1859,4,64,4.3
1014,Astrophysics for People in a Hurry,Neil deGrasse Tyson,Science,2017,9,122,4.5
1015,The Gene: An Intimate History,Siddhartha Mukherjee,Science,2016,6,79,4.6
1016,Clean Code: A Handbook of Agile Software,Robert C. Martin,Technology,2008,10,165,4.7
1017,Introduction to Algorithms,Thomas H. Cormen,Technology,2009,8,130,4.6
1018,Design Patterns: Elements of Reusable Object-Oriented Software,Erich Gamma,Technology,1994,5,92,4.5
1019,Artificial Intelligence: A Modern Approach,Stuart Russell,Technology,2020,7,140,4.8
1020,Python Crash Course,Eric Matthes,Technology,2015,12,180,4.7
1021,The Pragmatic Programmer,Andrew Hunt,Technology,1999,9,152,4.8
1022,Guns Germs and Steel,Jared Diamond,History,1997,6,108,4.4
1023,The Silk Roads: A New History of the World,Peter Frankopan,History,2015,7,95,4.5
1024,SPQR: A History of Ancient Rome,Mary Beard,History,2015,5,84,4.3
1025,The Wright Brothers,David McCullough,History,2015,6,76,4.5
1026,Churchill: A Life,Martin Gilbert,Biography,1991,4,58,4.4
1027,Steve Jobs,Walter Isaacson,Biography,2011,10,172,4.7
1028,Einstein: His Life and Universe,Walter Isaacson,Biography,2007,7,115,4.6
1029,Long Walk to Freedom,Nelson Mandela,Biography,1994,8,128,4.8
1030,Becoming,Michelle Obama,Biography,2018,11,164,4.7
1031,The Diary of a Young Girl,Anne Frank,Biography,1947,9,150,4.8
1032,Elon Musk,Ashlee Vance,Biography,2015,8,135,4.4
1033,The Hound of the Baskervilles,Arthur Conan Doyle,Mystery,1902,8,148,4.6
1034,And Then There Were None,Agatha Christie,Mystery,1939,11,185,4.8
1035,The Girl with the Dragon Tattoo,Stieg Larsson,Mystery,2005,9,139,4.5
1036,Gone Girl,Gillian Flynn,Mystery,2012,8,126,4.3
1037,The Da Vinci Code,Dan Brown,Mystery,2003,10,168,4.2
1038,Big Little Lies,Liane Moriarty,Mystery,2014,7,104,4.4
1039,The Silent Patient,Alex Michaelides,Mystery,2019,10,158,4.5
1040,The Hobbit,J.R.R. Tolkien,Fantasy,1937,12,192,4.8
1041,The Fellowship of the Ring,J.R.R. Tolkien,Fantasy,1954,10,178,4.9
1042,Harry Potter and the Sorcerer's Stone,J.K. Rowling,Fantasy,1997,14,210,4.9
1043,A Game of Thrones,George R.R. Martin,Fantasy,1996,8,144,4.6
1044,The Name of the Wind,Patrick Rothfuss,Fantasy,2007,7,118,4.7
1045,Mistborn: The Final Empire,Brandon Sanderson,Fantasy,2006,9,132,4.8
1046,The Way of Kings,Brandon Sanderson,Fantasy,2010,8,129,4.9
1047,Dune,Frank Herbert,Science,1965,11,170,4.7
1048,Deep Learning,Ian Goodfellow,Technology,2016,6,98,4.6
1049,Atomic Habits,James Clear,Technology,2018,15,205,4.9
1050,Educated,Tara Westover,Biography,2018,9,141,4.7
1051,A Promised Land,Barack Obama,Biography,2020,7,112,4.5
1052,The Code Breaker,Walter Isaacson,Biography,2021,6,88,4.6
1053,The Midnight Library,Matt Haig,Fiction,2020,9,137,4.4
1054,Project Hail Mary,Andy Weir,Science,2021,10,162,4.8
1055,Klara and the Sun,Kazuo Ishiguro,Fiction,2021,6,90,4.2
1056,Chip War: The Fight for the World's Most Critical Technology,Chris Miller,Technology,2022,8,119,4.7
1057,The Anarchy,William Dalrymple,History,2019,5,78,4.5
1058,Thinking Fast and Slow,Daniel Kahneman,Science,2011,8,136,4.6
1059,The Thursday Murder Club,Richard Osman,Mystery,2020,7,109,4.3
1060,The Priory of the Orange Tree,Samantha Shannon,Fantasy,2019,6,85,4.4"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(data)


# ---------------------------------------------------------
# Load and Clean Dataset
# ---------------------------------------------------------
@st.cache_data
def load_data():
    """Loads and cleans the library book dataset from CSV."""
    # Look for CSV in same directory or current working directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "library_books.csv")

    if not os.path.exists(csv_path):
        # Fallback check in current working directory
        if os.path.exists("library_books.csv"):
            csv_path = "library_books.csv"
        else:
            # Auto-generate if missing
            create_default_csv(csv_path)

    # Read CSV
    df = pd.read_csv(csv_path)

    # Clean and validate types
    df = df.dropna()
    df["Book_ID"] = df["Book_ID"].astype(int)
    df["Publication_Year"] = df["Publication_Year"].astype(int)
    df["Copies_Available"] = df["Copies_Available"].astype(int)
    df["Times_Borrowed"] = df["Times_Borrowed"].astype(int)
    df["Rating"] = df["Rating"].astype(float)
    df["Genre"] = df["Genre"].astype(str).str.strip()
    df["Book_Title"] = df["Book_Title"].astype(str).str.strip()
    df["Author"] = df["Author"].astype(str).str.strip()

    return df


# Load dataset
df_raw = load_data()

# ---------------------------------------------------------
# Sidebar: Controls and Filters
# ---------------------------------------------------------
st.sidebar.image("https://img.icons8.com/fluency/96/books.png", width=70)
st.sidebar.title("Library Filter Panel")
st.sidebar.caption("Filter and refine records for analytics")

# Genre filter
all_genres = sorted(df_raw["Genre"].unique().tolist())
selected_genres = st.sidebar.multiselect(
    "Select Genre(s):",
    options=all_genres,
    default=all_genres,
    help="Choose one or more book genres to analyze."
)

# Publication Year filter
min_year = int(df_raw["Publication_Year"].min())
max_year = int(df_raw["Publication_Year"].max())

year_range = st.sidebar.slider(
    "Select Publication Year Range:",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=1,
    help="Filter books published within this year range."
)

# Text Search Filter
search_query = st.sidebar.text_input(
    "🔍 Search Title or Author:",
    "",
    help="Type a keyword to filter by Book Title or Author name."
)

# Quick reset button
if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info(
    "**Student Presentation Note:**\n"
    "This dashboard is built with **Streamlit**, **Pandas**, **Matplotlib**, and **Seaborn** "
    "to analyze library circulation and inventory patterns."
)

# ---------------------------------------------------------
# Filter Dataset Based on User Selections
# ---------------------------------------------------------
filtered_df = df_raw.copy()

# Apply genre filter
if selected_genres:
    filtered_df = filtered_df[filtered_df["Genre"].isin(selected_genres)]
else:
    filtered_df = filtered_df.iloc[0:0]  # empty dataframe

# Apply year range filter
filtered_df = filtered_df[
    (filtered_df["Publication_Year"] >= year_range[0]) &
    (filtered_df["Publication_Year"] <= year_range[1])
]

# Apply text search filter
if search_query:
    q = search_query.lower()
    filtered_df = filtered_df[
        filtered_df["Book_Title"].str.lower().str.contains(q) |
        filtered_df["Author"].str.lower().str.contains(q)
    ]

# ---------------------------------------------------------
# Dashboard Header
# ---------------------------------------------------------
st.title("📚 Library Book Analysis & Data Visualization System")
st.markdown(
    '<span class="badge-sample">📌 ACADEMIC PROJECT &bull; SAMPLE DATASET (60 RECORDS)</span>',
    unsafe_allow_html=True
)
st.markdown(
    "Welcome to the **Library Book Analytics Dashboard**. This application provides an interactive "
    "overview of library inventory, borrowing frequency, genre popularity, and book ratings."
)

st.markdown("---")

# ---------------------------------------------------------
# Section 1: Key Summary Metrics Cards
# ---------------------------------------------------------
st.markdown('<div class="section-title">📊 Key Performance Metrics</div>', unsafe_allow_html=True)

if not filtered_df.empty:
    total_books = len(filtered_df)
    total_copies = int(filtered_df["Copies_Available"].sum())
    total_borrowed = int(filtered_df["Times_Borrowed"].sum())
    avg_rating = round(filtered_df["Rating"].mean(), 2)

    # Most popular book (highest times borrowed)
    most_popular_idx = filtered_df["Times_Borrowed"].idxmax()
    most_popular_book = filtered_df.loc[most_popular_idx, "Book_Title"]
    most_popular_borrows = filtered_df.loc[most_popular_idx, "Times_Borrowed"]

    # Most popular genre (by total borrowings in filtered set)
    genre_borrowings = filtered_df.groupby("Genre")["Times_Borrowed"].sum()
    top_genre = genre_borrowings.idxmax() if not genre_borrowings.empty else "N/A"

    # Year span
    earliest_year = int(filtered_df["Publication_Year"].min())
    latest_year = int(filtered_df["Publication_Year"].max())

    # Display Metrics in Columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📖 Total Books</div>
            <div class="metric-value">{total_books}</div>
            <div class="metric-sub">Unique book titles</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📦 Total Copies</div>
            <div class="metric-value">{total_copies:,}</div>
            <div class="metric-sub">In circulation/shelves</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🔄 Total Borrowings</div>
            <div class="metric-value">{total_borrowed:,}</div>
            <div class="metric-sub">Cumulative checkout count</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">⭐ Average Rating</div>
            <div class="metric-value">{avg_rating} / 5.0</div>
            <div class="metric-sub">Across filtered titles</div>
        </div>
        """, unsafe_allow_html=True)

    col5, col6, col7 = st.columns(3)
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🏆 Most Borrowed Book</div>
            <div class="metric-value" style="font-size: 1.2rem;">{most_popular_book}</div>
            <div class="metric-sub">{most_popular_borrows} times borrowed</div>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🔥 Leading Genre</div>
            <div class="metric-value" style="font-size: 1.3rem;">{top_genre}</div>
            <div class="metric-sub">Highest reader engagement</div>
        </div>
        """, unsafe_allow_html=True)

    with col7:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">⏳ Publication Span</div>
            <div class="metric-value" style="font-size: 1.3rem;">{earliest_year} &ndash; {latest_year}</div>
            <div class="metric-sub">Oldest to newest title</div>
        </div>
        """, unsafe_allow_html=True)

else:
    st.warning("⚠️ No books match your selected filters. Please expand your filter criteria on the left sidebar.")

# ---------------------------------------------------------
# Section 2: Data Visualizations (5 Charts)
# ---------------------------------------------------------
st.markdown('<div class="section-title">📈 Visual Data Analytics</div>', unsafe_allow_html=True)

if not filtered_df.empty:
    # Set Seaborn theme aesthetics
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 11})

    # Row 1 of charts: Chart 1 (Genre Count Bar) & Chart 3 (Genre Distribution Pie)
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("1. Number of Books by Genre")
        st.caption("Distribution of distinct book titles across genres.")

        genre_counts = filtered_df["Genre"].value_counts().reset_index()
        genre_counts.columns = ["Genre", "Count"]

        fig1, ax1 = plt.subplots(figsize=(6, 4))
        palette1 = sns.color_palette("deep", len(genre_counts))
        bars1 = ax1.bar(genre_counts["Genre"], genre_counts["Count"], color=palette1, edgecolor="#333", alpha=0.85)

        # Label counts on bars
        for bar in bars1:
            height = bar.get_height()
            ax1.annotate(f"{int(height)}",
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha="center", va="bottom", fontweight="bold")

        ax1.set_xlabel("Genre", fontweight="bold")
        ax1.set_ylabel("Book Count", fontweight="bold")
        ax1.set_title("Total Book Titles per Genre", pad=12, fontweight="bold")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        st.pyplot(fig1)
        plt.close(fig1)

    with row1_col2:
        st.subheader("2. Genre Distribution Proportion")
        st.caption("Percentage breakdown of books by genre.")

        fig2, ax2 = plt.subplots(figsize=(6, 4))
        pie_colors = sns.color_palette("pastel", len(genre_counts))
        wedges, texts, autotexts = ax2.pie(
            genre_counts["Count"],
            labels=genre_counts["Genre"],
            autopct="%1.1f%%",
            startangle=140,
            colors=pie_colors,
            wedgeprops={"edgecolor": "white", "linewidth": 1.5}
        )
        for autotext in autotexts:
            autotext.set_fontweight("bold")
            autotext.set_fontsize(9)

        ax2.set_title("Proportion of Books by Genre", pad=12, fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)

    # Row 2 of charts: Chart 2 (Top 10 Most Borrowed) & Chart 5 (Average Rating by Genre)
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.subheader("3. Top 10 Most Borrowed Books")
        st.caption("Books with the highest checkout frequency.")

        top10_df = filtered_df.sort_values(by="Times_Borrowed", ascending=True).tail(10)

        fig3, ax3 = plt.subplots(figsize=(6, 4.5))
        bars3 = ax3.barh(top10_df["Book_Title"], top10_df["Times_Borrowed"], color="#4C72B0", edgecolor="#2B4268")

        for bar in bars3:
            width = bar.get_width()
            ax3.annotate(f" {int(width)}",
                         xy=(width, bar.get_y() + bar.get_height() / 2),
                         va="center", ha="left", fontweight="bold", fontsize=9)

        ax3.set_xlabel("Times Borrowed", fontweight="bold")
        ax3.set_ylabel("Book Title", fontweight="bold")
        ax3.set_title("Top 10 Most Frequently Borrowed Books", pad=12, fontweight="bold")
        ax3.set_xlim(0, top10_df["Times_Borrowed"].max() * 1.15)
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close(fig3)

    with row2_col2:
        st.subheader("4. Average Rating by Genre")
        st.caption("Comparison of average reader ratings across genres.")

        genre_rating = filtered_df.groupby("Genre")["Rating"].mean().reset_index()
        genre_rating = genre_rating.sort_values(by="Rating", ascending=False)

        fig4, ax4 = plt.subplots(figsize=(6, 4.5))
        palette4 = sns.color_palette("Spectral", len(genre_rating))
        bars4 = ax4.bar(genre_rating["Genre"], genre_rating["Rating"], color=palette4, edgecolor="#333", alpha=0.9)

        for bar in bars4:
            height = bar.get_height()
            ax4.annotate(f"{height:.2f}★",
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha="center", va="bottom", fontweight="bold", fontsize=9)

        ax4.set_xlabel("Genre", fontweight="bold")
        ax4.set_ylabel("Average Rating (out of 5.0)", fontweight="bold")
        ax4.set_title("Average Book Rating by Genre", pad=12, fontweight="bold")
        ax4.set_ylim(0, 5.5)
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        st.pyplot(fig4)
        plt.close(fig4)

    # Row 3: Chart 4 (Line Chart - Publication Year Trend)
    st.subheader("5. Publication Trend Over Time")
    st.caption("Number of books published across different years in the dataset.")

    yearly_counts = filtered_df.groupby("Publication_Year")["Book_ID"].count().reset_index()
    yearly_counts.columns = ["Year", "Books_Published"]
    yearly_counts = yearly_counts.sort_values("Year")

    fig5, ax5 = plt.subplots(figsize=(10, 3.8))
    ax5.plot(
        yearly_counts["Year"],
        yearly_counts["Books_Published"],
        marker="o",
        color="#D95F02",
        linewidth=2.5,
        markersize=6,
        label="Books Published"
    )
    ax5.fill_between(yearly_counts["Year"], yearly_counts["Books_Published"], color="#D95F02", alpha=0.15)

    ax5.set_xlabel("Publication Year", fontweight="bold")
    ax5.set_ylabel("Number of Books", fontweight="bold")
    ax5.set_title("Historical Timeline of Published Books", pad=12, fontweight="bold")
    ax5.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    st.pyplot(fig5)
    plt.close(fig5)

# ---------------------------------------------------------
# Section 3: Interactive Data Table
# ---------------------------------------------------------
st.markdown('<div class="section-title">📋 Explore Filtered Book Dataset</div>', unsafe_allow_html=True)

if not filtered_df.empty:
    st.write(f"Showing **{len(filtered_df)}** book records matching your current filter criteria:")

    # Sortable interactive dataframe
    st.dataframe(
        filtered_df.sort_values("Book_ID"),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Book_ID": st.column_config.NumberColumn("ID", format="%d"),
            "Book_Title": st.column_config.TextColumn("Title"),
            "Author": st.column_config.TextColumn("Author"),
            "Genre": st.column_config.TextColumn("Genre"),
            "Publication_Year": st.column_config.NumberColumn("Year", format="%d"),
            "Copies_Available": st.column_config.NumberColumn("Copies"),
            "Times_Borrowed": st.column_config.NumberColumn("Borrows"),
            "Rating": st.column_config.NumberColumn("Rating ⭐", format="%.1f"),
        }
    )

    # Download CSV button
    csv_export = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_export,
        file_name="filtered_library_books.csv",
        mime="text/csv",
    )
else:
    st.info("No records to display. Adjust filter settings on the sidebar.")

# ---------------------------------------------------------
# Section 4: Analytical Insights & Findings (Viva Section)
# ---------------------------------------------------------
st.markdown('<div class="section-title">💡 Key Project Insights & Observations</div>', unsafe_allow_html=True)

st.markdown("""
Here are the primary analytical conclusions derived from the library dataset:

1. **High Reader Engagement in Fantasy & Fiction**:
   - Classic and popular series like *Harry Potter*, *The Hobbit*, and *Atomic Habits* exhibit the highest circulation and borrow frequencies.
2. **Consistent Quality Across Genres**:
   - The average ratings across all genres range between **4.4 and 4.8**, reflecting a curated collection of well-regarded titles.
3. **Inventory Balance**:
   - Technology and Science collections show steady growth in publication years from **1990 to 2022**, indicating modern updates to the library catalogue.
4. **Actionable Recommendations for Librarians**:
   - High-demand books with low copies available should be prioritized for additional acquisitions.
""")

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888; font-size: 0.85rem;'>"
    "Library Book Analysis and Data Visualization System &bull; College Mini Project &bull; Built with Streamlit & Python"
    "</div>",
    unsafe_allow_html=True
)
