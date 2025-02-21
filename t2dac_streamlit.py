pip install -r requirements.txt
import streamlit as st
import os
import subprocess
#import glob
#import uuid
import warnings
#import shutil
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
warnings.filterwarnings('ignore') 

st.set_page_config(layout="wide")
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;} /* Hides the three dots menu */
    header {visibility: hidden;}
    footer {visibility: hidden;}   /* Hides the footer if needed */
    .block-container {
        padding-top: 0rem; /* Removes extra space at the top */
    }
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)
#def icon(icon_name):
    #st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)
    
banner_text = "T2DAC - Type 2 Diabetes Associated Cancer"
banner_color = "#800080"  # Dodger blue background
text_color = "#FFFFFF"  # White text
font_size = "40px"  # Font size

# Create the banner using Markdown
st.markdown(
    f"""
    <div style="
        background-color: {banner_color}; 
        padding: 20px; 
        text-align: center; 
        border-radius: 10px;">
        <span style="
            color: {text_color}; 
            font-size: {font_size}; 
            font-weight: bold;">
            {banner_text}
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

def display_aggrid_table(df, italic_column=None):
    custom_css = {
        ".ag-header-cell-label": {
            "white-space": "normal !important",  # Allow text wrapping
            "line-height": "1.2 !important",     # Adjust line height for wrapped text
        }
    }
    # Build grid options
    grid_options_builder = GridOptionsBuilder.from_dataframe(df)
    grid_options_builder.configure_default_column(
        resizable=True,
        editable=False,
        sortable=True,
        #filter=True,
        wrapText=True,
        autoHeight=True  
    )
    if italic_column:
            grid_options_builder.configure_column(
            italic_column,
            cellStyle={"fontStyle": "italic"},
            )
    grid_options_builder.configure_grid_options(
        domLayout="normal",
        suppressHorizontalScroll=False,  # Remove horizontal scrolling
        headerHeight=40,        # Adjusts layout to allow scrollbars
    )
    #grid_options_builder.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20)
    #grid_options_builder.configure_grid_options(suppressHorizontalScroll=True)

    # Ensure scrollbars for row and column navigation
    grid_options = grid_options_builder.build()
    

    # Display the grid
    return AgGrid(
        df,
        gridOptions=grid_options,
        height=400,  # Set appropriate height for the grid
        fit_columns_on_grid_load=True,
        enable_enterprise_modules=False,
        reload_data=True,
        custom_css=custom_css
    )

def search_combined_dataframe(df, search_term):
        search_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
        return search_df
    
def main():
    #st.set_page_config(layout="wide")
    #st.title("T2DAC")
    #st.set_page_config(layout="wide")
    #st.image("Picture1_name.jpg", width=700)
    
    df= pd.read_csv("cancer_surabhi_data2.csv",  encoding="utf-8")
    col1, col2,col3,col4 = st.columns([2,2,1,0.5])  # Adjust ratio for search bar and button alignment

    with col3:
    # Compact search bar and button
        search_query = st.text_input(
        "Search",
        key="search_query",
        label_visibility="collapsed",
        placeholder="Search here"
        )
        #search_button = st.button("Search", key="search_button")
    with col4:
        search_button = st.button("Go")

# --- Handle Search ---
    if search_button and search_query.strip():
    # Filter rows in the DataFrame based on the search query
        search_df = df[
        df.apply(lambda row: search_query.lower() in row.to_string().lower(), axis=1)
    ]
        
    # Display results as a popup
        if not search_df.empty:
            with st.expander("", expanded=True):
                st.write(f"Results for: **{search_query}**")
                display_aggrid_table(search_df)
        else:
            st.warning(f"No results found for: **{search_query}**")
    #else:
    # Display full combined data initially
        #st.subheader("Full Data")
        #display_aggrid_table(df, italic_column="Gene", title="Full Data")
    # Create tabs
    #tabs = df["label"].unique()
    #selected_tab = st.sidebar.selectbox("Select a topic", ["All"] + list(tabs))
    #text_search = st.text_input("Search ", value="")
    #icon("search")
    #selected = st.text_input("", "Search...")
    #button_clicked = st.button("OK")
    #search_keyword = st.sidebar.text_input("Search by keyword")
    filtered_df = df[df['Cancer Type'] == 'Liver cancer']
    filtered_df2 = df[df['Cancer Type'] == 'Pancreatic cancer']
    filtered_df3 = df[df['Cancer Type'] == 'Kindey cancer']
    filtered_df4 = df[df['Cancer Type'] == 'Endometrial cancer']
    #filtered_df2 = df[df['label'] == 'WT']
    css = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.2rem;
    }
</style>
'''

    st.markdown(css, unsafe_allow_html=True)
    #tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Home", "Pancreatic Cancer","Liver Cancer",  "Kidney Cancer", "Endometrial Cancer", "Contact us"])
    tabs = st.tabs(["Home", "Pancreatic Cancer","Liver Cancer",  "Kidney Cancer", "Endometrial Cancer", "Contact us"])
    #tabs = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
    with tabs[0]:
        #st.markdown("<h2 style='color: black;'>This is Home Tab</h2>", unsafe_allow_html=True)
        #st.markdown("<h2 style='color: red;'>This is Tab 1 with Red Text!</h2>", unsafe_allow_html=True)
        #st.header("**Welcome to T2DAC**")
        col1, col2,col3= st.columns([1.5, 2, 1.2])  # Adjust column width proportions as needed
        #image1= Image.open("Picture2.jpg")
        #image2= Image.open("word_cloud_9.png")
        #new_size = (300, 150)  # You can change this size as needed
        #new_size2 = (300, 250)
        #image1_resized = image1.resize(new_size)
        #image2_resized = image2.resize(new_size)
# Add image to the left column
        with col1:
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.image(
                ["Picture2.jpg"],  # Replace with your image path or URL
                #caption="Shared risk factors between T2D and Cancer",
                use_container_width=True
            )
            #st.markdown('''
            #:violet[Shared risk factors between T2D and Cancer]
            #''')
            st.markdown('<div style="text-align: center;">Shared risk factors between T2D and Cancer</div>', unsafe_allow_html=True)
            #st.write("<h1 style='color:#002244;font-size: 12px'>Shared risk factors between T2D and Cancer</h1>", unsafe_allow_html=True)
        with col2:
            main_text="A comprehensive overview of genes implicated in Type 2 Diabetes Mellitus (T2DM) associated Cancer. This database provides curated and integrated information on genes implicated in the development and progression of T2DM associated Cancers. These Cancer includes Pancreatic Cancer, Liver Cancer, Kidney Cancer and Endometrial Cancer, which are commonly observed and higher have higher risk of manifestation when presented with T2DM. The database offers up-to-date information on population-specific genetic studies, experimentally validated SNPs, tissue-specific gene expression patterns from microarray data. It serves as a valuable resource for understanding the genetic and molecular basis of T2DM associated Cancer."
            banner_color = "#ebe5f7"
            text_color = "#000000"  # White text
            font_size = "16px" 
            st.markdown(
    f"""
    <div style="
        background-color: {banner_color}; 
        padding: 20px; 
        text-align: justify; 
        border-radius: 1px;">
        <span style="
            color: {text_color}; 
            font-size: {font_size}; 
            #font-weight: bold;">
            {main_text}
        </span>
    </div>
    """,
    unsafe_allow_html=True
        )
 
        # Add text to the right column
        with col3:
            st.write("")
            st.write("")
            st.image(
                "word_cloud_9.png",  # Replace with your image path or URL
                #caption="Shared risk factors between T2D and Cancer",
                #use_container_width=True
            )
            #st.write("<h1 style='color:#002244;font-size: 12px'>Most frequent words in T2DM-Cancer abstracts</h1>", unsafe_allow_html=True)
            #st.markdown('''
            #:violet[  Top words in T2DM-Cancer abstracts]
            #''')
            st.markdown('<div style="text-align: center;">Top words in T2DM-Cancer abstracts</div>', unsafe_allow_html=True)
        
         
    #st.write("""
    #Welcome to PAMIR-ERLs.
    #This tool is used for prediction of antimicrobial resistance genes, especially focusing of ESKAPE pathogenes. 
    #""")
        #st.write("Antimicrobial resistance (AMR) is a global health concern as it limits our ability to treat infections. The major cause for AMR is misuse and overuse of antimicrobial drugs in humans and animals. These factors contribute to the evolution of bacteria using different genetic mechanisms. ESKAPE pathogens fall into World health Organisation’s (WHO) critical and high priority group, necessitating consideration. There is an urgent need for rapid and precise diagnosis. Howbeit, traditional antimicrobial susceptibility testing is time-consuming and low throughput. On the other hand, machine learning methods using bacteria's genomic information can enable accurate and rapid AMR detection. Hence, we intend to develop a machine learning-based prediction model focusing on ESKAPE pathogens based on AMR functional classes.")
        
    with tabs[1]:
        st.header("Pancreatic cancer")
        #filtered_df = df[df['label'] == 'MT']
        #filtered_df= df["label"=="MT"]
        display_aggrid_table(filtered_df2, italic_column="Gene")
        #st.dataframe(filtered_df)
        #m1 = filtered_df["Whitelisted.taxa"].str.contains(text_search)
        #m2 = filtered_df["Product.name"].str.contains(text_search)
        #df_search = df[m1, m2]   
        #if text_search:
            #st.write(df_search)
        if not filtered_df2.empty:
            csv_data = filtered_df2.to_csv(index=False).encode("utf-8")
            st.download_button(
            label="Download Pancreatic cancer data",
            data=csv_data,
            file_name="pancreatic_cancer.csv",
            mime="text/csv"
            )
    #images = "comb_liver.png"
    #st.image(images,  caption="some generic text")
        banner_text = "Gene analysis overview"
        banner_color = "#DDA0DD"  # Dodger blue background
        text_color = "#800080"  # White text
        font_size = "25px"  # Font size

# Create the banner using Markdown
        st.markdown(
    f"""
    <div style="
        background-color: {banner_color}; 
        padding: 1px; 
        text-align: center; 
        border-radius: 10px;">
        <span style="
            color: {text_color}; 
            font-size: {font_size}; 
            font-weight: bold;">
            {banner_text}
        </span>
    </div>
    """,
    unsafe_allow_html=True
        )
        #st.write("Enrichment and trends insights")
        image1= "bubble_plot_Panc_new2.png"
        image2= "bwi_pac_new.tif"
        col1, col2 = st.columns(2)

# Display the images in their respective columns
        with col1:
            st.markdown('<div style="text-align: left;font-size: 20px;">Enriched Biological processes</div>', unsafe_allow_html=True)
            st.image(image1,  use_container_width=True)
            st.markdown('<div style="text-align: center;font-size: 12px;">Enriched Biological processes of T2DM-Pancreatic Cancer genes [done using DAVID].</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div style="text-align: left;font-size: 20px;">Trend analysis</div>', unsafe_allow_html=True)
            #st.write("Trend analysis")
            st.image(image2,  use_container_width=True)  
            st.markdown('<div style="text-align: center;font-size: 12px;">The pattern analysis of Genes’ trend in T2DM-Pancreatic Cancer dataset, Buzz Word Index:BWI.</div>', unsafe_allow_html=True)
    with tabs[2]:
        st.header("Liver cancer")
        display_aggrid_table(filtered_df, italic_column="Gene")
        #st.set_page_config(layout="wide")
        if not filtered_df.empty:
            csv_data = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button(
            label="Download liver cancer data",
            data=csv_data,
            file_name="liver_cancer.csv",
            mime="text/csv"
            )
        images = "liver_comb.tif"
        
        banner_text = "Gene analysis overview"
        banner_color = "#DDA0DD"  # Dodger blue background
        text_color = "#800080"  # White text
        font_size = "25px"  # Font size

# Create the banner using Markdown
        st.markdown(
    f"""
    <div style="
        background-color: {banner_color}; 
        padding: 1px; 
        text-align: center; 
        border-radius: 10px;">
        <span style="
            color: {text_color}; 
            font-size: {font_size}; 
            font-weight: bold;">
            {banner_text}
        </span>
    </div>
    """,
    unsafe_allow_html=True
        )
        
        col3, col4=st.columns([0.5, 0.5])
        with col3:
            st.markdown('<div style="text-align: left;font-size: 20px;">Enriched Biological processes</div>', unsafe_allow_html=True)
            #st.write("Enriched Biological pathway ")
            #st.image(image1,  use_container_width=True)
            #st.markdown('<div style="text-align: center;font-size: 12px;">Enriched Biological processes of T2DM-Liver Cancer genes [done using DAVID].</div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div style="text-align: left;font-size: 20px;">Trend analysis</div>', unsafe_allow_html=True)
            #st.markdown('<div style="text-align: center;font-size: 12px;">The pattern analysis of Genes’ trend in T2DM-Liver Cancer dataset, Buzz Word Index:BWI.</div>', unsafe_allow_html=True)

        #st.write("Enrichment and trends insights")
        st.image(images)
        col1, col2=st.columns([0.5, 0.5])
        with col1:
            #st.write("Enriched Biological pathway ")
            #st.image(image1,  use_container_width=True)
            st.markdown('<div style="text-align: center;font-size: 12px;">Enriched Biological processes of T2DM-Liver Cancer genes [done using DAVID].</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div style="text-align: center;font-size: 12px;">The pattern analysis of Genes’ trend in T2DM-Liver Cancer dataset, Buzz Word Index:BWI.</div>', unsafe_allow_html=True)

        #st.markdown('<div style="text-align: center;">Top words in T2DM-Cancer abstracts</div>', unsafe_allow_html=True)
        #st.write("write something")
        #image3= "bubble_plot_liver_new2.png"
        #image4= "bwi_liv_new2.tif"
        #col1, col2 = st.columns(2)
        
# Display the images in their respective columns
        #with col1:
            #st.image(image3, caption="bubble plot", width=300, use_container_width='auto')

        #with col2:
            #st.image(image4, caption="bwi", use_container_width='auto', width=300)            
    with tabs[3]:
        st.header("Kidney cancer")
        display_aggrid_table(filtered_df3, italic_column="Gene")
        if not filtered_df3.empty:
            csv_data = filtered_df3.to_csv(index=False).encode("utf-8")
            st.download_button(
            label="Download kidney cancer data",
            data=csv_data,
            file_name="kidney_cancer.csv",
            mime="text/csv"
            )
        banner_text = "Gene analysis overview"
        banner_color = "#DDA0DD"  # Dodger blue background
        text_color = "#800080"  # White text
        font_size = "25px"  # Font size

# Create the banner using Markdown
        st.markdown(
    f"""
    <div style="
        background-color: {banner_color}; 
        padding: 1px; 
        text-align: center; 
        border-radius: 10px;">
        <span style="
            color: {text_color}; 
            font-size: {font_size}; 
            font-weight: bold;">
            {banner_text}
        </span>
    </div>
    """,
    unsafe_allow_html=True
        )
        #st.write("write something")
        #st.write("Enrichment and trends insights")
        image5= "bubble_plot_kidney_new2.png"
        image6= "bwi_kid_new.tif"
        col1, col2 = st.columns(2)

# Display the images in their respective columns
        with col1:
            st.markdown('<div style="text-align: left;font-size: 20px;">Enriched Biological processes</div>', unsafe_allow_html=True)
            #st.write("Enriched Biological pathway")
            st.image(image5, width=300, use_container_width='auto')
            st.markdown('<div style="text-align: center;font-size: 12px;">Enriched Biological processes of T2DM-Kidney Cancer genes [done using DAVID].</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div style="text-align: left;font-size: 20px;">Trend analysis</div>', unsafe_allow_html=True)
            #st.write("Trend analysis")
            st.image(image6,use_container_width='auto', width=300) 
            st.markdown('<div style="text-align: center;font-size: 12px;">The pattern analysis of Genes’ trend in T2DM-Kidney Cancer dataset, Buzz Word Index:BWI.</div>', unsafe_allow_html=True)
    with tabs[4]:
        st.header("Endometrial cancer")
        #st.dataframe(filtered_df4)
        display_aggrid_table(filtered_df4, italic_column="Gene")
        if not filtered_df4.empty:
            csv_data = filtered_df4.to_csv(index=False).encode("utf-8")
            st.download_button(
            label="Download Endometrial cancer data",
            data=csv_data,
            file_name="endometrial_cancer.csv",
            mime="text/csv"
            )
        images2 = "endo_comb.tif"
        
        #st.markdown('<div style="text-align: center;">Top words in T2DM-Cancer abstracts</div>', unsafe_allow_html=True)
        #st.write("Enrichment and trends insights")
        banner_text = "Gene analysis overview"
        banner_color = "#DDA0DD"  # Dodger blue background
        text_color = "#800080"  # White text
        font_size = "25px"  # Font size
       
# Create the banner using Markdown
        st.markdown(
    f"""
    <div style="
        background-color: {banner_color}; 
        padding: 1px; 
        text-align: center; 
        border-radius: 10px;">
        <span style="
            color: {text_color}; 
            font-size: {font_size}; 
            font-weight: bold;">
            {banner_text}
        </span>
    </div>
    """,
    unsafe_allow_html=True
        )
        col3, col4=st.columns([0.5, 0.5])
        with col3:
            st.markdown('<div style="text-align: left;font-size: 20px;">Enriched Biological processes</div>', unsafe_allow_html=True)
            #st.write("Enriched Biological pathway ")
            #st.image(image1,  use_container_width=True)
            #st.markdown('<div style="text-align: center;font-size: 12px;">Enriched Biological processes of T2DM-Liver Cancer genes [done using DAVID].</div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div style="text-align: left;font-size: 20px;">Trend analysis</div>', unsafe_allow_html=True)

        st.image(images2)
        col1, col2=st.columns([0.5, 0.5])
        with col1:
            #st.write("Enriched Biological pathway ")
            #st.image(image1,  use_container_width=True)
            st.markdown('<div style="text-align: center;font-size: 12px;">Enriched Biological processes of T2DM-Endometrial Cancer genes [done using DAVID].</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div style="text-align: center;font-size: 12px;">The pattern analysis of Genes’ trend in T2DM-Endometrial Cancer dataset, Buzz Word Index:BWI.</div>', unsafe_allow_html=True)

        #image7= "bubble_plot_endo_new.png"
        #image8= "bwi_endo_new.tif"
        #col1, col2 = st.columns(2)

# Display the images in their respective columns
        #with col1:
            #st.image(image7, caption="bubble plot", width=300, use_container_width='auto')

        #with col2:
            #st.image(image8, caption="bwi", use_container_width='auto', width=300)
    with tabs[5]:
        st.header("CSIR-IGIB")
 
if __name__ == "__main__":
    main()
