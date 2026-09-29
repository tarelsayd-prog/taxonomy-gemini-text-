import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gemini Prompt Generator", layout="centered")

st.title("🤖 Gemini Taxonomy Prompt Generator")
st.write("Upload your Excel taxonomy, select a family, and copy your prompt.")

# File Uploader
uploaded_file = st.file_uploader("Upload Taxonomy Excel File (Columns: Family, Type, Subtype)", type=['xlsx', 'xls', 'csv'])

if uploaded_file:
    # Read the data
    try:
        if uploaded_file.name.endswith('csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        # Bind to columns based on position (A=0, B=1, C=2)
        fam_col, type_col, sub_col = df.columns[0], df.columns[1], df.columns[2]
        
        # Clean data: drop empty rows in the Family column
        df = df.dropna(subset=[fam_col])
        
        # Create Dropdown for Family
        families = sorted(df[fam_col].unique().tolist())
        selected_family = st.selectbox("Select Target Family:", families)
        
        if selected_family:
            # Filter dataframe by the chosen family
            filtered_df = df[df[fam_col] == selected_family]
            
            # Group by Type (Column B) and join Subtypes (Column C) with commas
            grouped = filtered_df.groupby(type_col)[sub_col].apply(
                lambda x: ', '.join(x.dropna().astype(str).unique())
            )
            
            # Format the taxonomy text
            taxonomy_lines = []
            for t, subtypes in grouped.items():
                taxonomy_lines.append(f"- {t}: {subtypes}")
            
            taxonomy_text = "\n".join(taxonomy_lines)
            
            # Construct the final prompt
            master_prompt = f"""**Categorization Master Prompt:** 
Please act as an expert inventory categorizer. I will provide you with a list of SKUs/Product Titles. You must organize them into a Markdown table with the columns: Title, Type, and Subtype.

**Target Family:** {selected_family}

**Rules:**
1. Strictly use only the Types and Subtypes listed below. Do not invent new categories or modify the spelling.
2. Ensure the Subtype you select falls exactly under its designated Type in the list provided.
3. If an item does not logically fit into the Target Family, leave the Type and Subtype columns with the exact keyword: (Not {selected_family}).

**Types and Subtypes:**
{taxonomy_text}

**SKUs to Categorize:**
[PASTE YOUR LIST OF SKUS/PRODUCT TITLES HERE]"""

            st.divider()
            st.subheader("📝 Your Generated Prompt")
            st.info("Hover over the top right corner of the text box below and click the 'Copy' icon.")
            
            # st.code automatically provides a copy-to-clipboard button
            st.code(master_prompt, language="markdown")

    except Exception as e:
        st.error(f"Error processing file. Please ensure it has at least 3 columns (Family, Type, Subtype). Details: {e}")