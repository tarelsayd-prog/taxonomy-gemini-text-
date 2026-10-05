import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Gemini Prompt Generator", layout="centered")

st.title("🤖 Gemini Taxonomy Prompt Generator")
st.write("Select the Family, paste your Titles/SKUs, and copy the ready prompt for Gemini.")

# Ensure this matches your file name on GitHub exactly
EXCEL_FILE = "taxonomy for gemini.xlsx" 

@st.cache_data
def load_data():
    if not os.path.exists(EXCEL_FILE):
        return None
    # Read the excel file
    df = pd.read_excel(EXCEL_FILE)
    # Drop rows where the Family column is empty
    df = df.dropna(subset=[df.columns[0]])
    return df

df = load_data()

if df is None:
    st.error(f"⚠️ Could not find the Excel file! Please make sure a file named `{EXCEL_FILE}` is uploaded to your GitHub repository in the same directory.")
else:
    # Assign columns based on position (0=Family, 1=Type, 2=Subtype)
    fam_col, type_col, sub_col = df.columns[0], df.columns[1], df.columns[2]
    
    # 1. Dropdown for Family selection
    families = sorted(df[fam_col].astype(str).unique().tolist())
    selected_family = st.selectbox("1️⃣ Select Target Family:", families)
    
    # 2. Text area for SKUs/Titles input
    skus_input = st.text_area("2️⃣ Enter SKUs or Product Titles here (one per line):", height=150)
    
    if selected_family:
        # Filter dataframe by selected family
        filtered_df = df[df[fam_col] == selected_family]
        
        # Group by Type and join Subtypes with commas
        grouped = filtered_df.groupby(type_col)[sub_col].apply(
            lambda x: ', '.join(x.dropna().astype(str).unique())
        )
        
        taxonomy_lines = []
        for t, subtypes in grouped.items():
            taxonomy_lines.append(f"- {t}: {subtypes}")
        
        taxonomy_text = "\n".join(taxonomy_lines)
        
        # Use placeholder text if no SKUs are entered
        skus_to_categorize = skus_input if skus_input.strip() else "[PASTE YOUR LIST OF SKUS/PRODUCT TITLES HERE]"

        # 3. The final generated Prompt
        master_prompt = f"""Categorization Master Prompt: Please act as an expert inventory categorizer. I will provide you with a list of SKUs. You must organize them into a table with the columns: Title, Type, and Subtype.

Rules:
1. Strictly use only the Types and Subtypes listed below.
2. If an item is not a {selected_family.lower()} (e.g., adult apparel, baby feeding bottles), leave the Type and Subtype columns With keyword like ( Not {selected_family})

Types and Subtypes:
{taxonomy_text}

SKUs to Categorize:
{skus_to_categorize}"""

        st.divider()
        st.subheader("📝 Your Generated Prompt:")
        st.info("💡 Hover over the top-right corner of the text box below and click the 'Copy' icon.")
        
        # Display the prompt with a copy button
        st.code(master_prompt, language="markdown")
