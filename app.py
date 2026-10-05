import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Gemini Prompt Generator", layout="centered")

st.title("🤖 Gemini Master Prompt Generator")
st.write("Select the Category, input your data, and copy the prompt to Gemini.")

EXCEL_FILE = "taxonomy for gemini.xlsx" 

@st.cache_data
def load_data():
    if not os.path.exists(EXCEL_FILE):
        return None
    df = pd.read_excel(EXCEL_FILE)
    df = df.dropna(subset=[df.columns[0]])
    return df

df = load_data()

if df is None:
    st.error(f"⚠️ Could not find the Excel file! Make sure a file named `{EXCEL_FILE}` is uploaded to your GitHub repository.")
else:
    fam_col, type_col, sub_col = df.columns[0], df.columns[1], df.columns[2]
    
    families = sorted(df[fam_col].astype(str).unique().tolist())
    selected_family = st.selectbox("1️⃣ Select Target Category (Family):", families)
    
    if selected_family:
        filtered_df = df[df[fam_col] == selected_family]
        grouped = filtered_df.groupby(type_col)[sub_col].apply(
            lambda x: ', '.join(x.dropna().astype(str).unique())
        )
        taxonomy_lines = [f"- {t}: {subtypes}" for t, subtypes in grouped.items()]
        taxonomy_text = "\n".join(taxonomy_lines)

        st.write("### 2️⃣ Select your data type:")
        
        tab1, tab2 = st.tabs(["📝 Text / Titles", "🖼️ Uploaded Images"])

        # ==========================================
        # TAB 1: TEXT / TITLES
        # ==========================================
        with tab1:
            st.write("Use this tab if you only have text data (Titles/SKUs).")
            titles_input = st.text_area("Paste your Titles or SKUs here (one per line):", height=150, key="titles")
            titles_data = titles_input if titles_input.strip() else "[PASTE YOUR LIST OF SKUS/TITLES HERE]"
            
            text_prompt = f"""**Role:**
Act as an expert e-commerce inventory categorizer.

**Task:**
I will provide you with a target Product Family, a strict Taxonomy (Types and Subtypes), and a list of SKUs/Product Titles. You must organize the SKUs and generate a downloadable Excel file (.xlsx) containing the results.

**Rules:**
1. Strictly use ONLY the Types and Subtypes listed in the provided Taxonomy. Do not invent, guess, or modify the spelling of any categories.
2. Ensure the Subtype you select falls exactly under its designated Type.
3. If an item does not logically fit into the Target Family, leave the Type and Subtype columns with the exact phrase: "Not {selected_family}".
4. **Output Requirement:** You MUST use Python to generate and provide a downloadable Excel file (.xlsx) with the categorized data.

**Excel Columns Required:**
1. Original Title
2. Polished Title (Short & clean for e-commerce)
3. Type
4. Subtype

---

**Target Family:** 
{selected_family}

**Taxonomy (Allowed Types and Subtypes):**
{taxonomy_text}

**SKUs to Categorize:**
{titles_data}"""

            st.info("💡 Click the Copy icon in the top-right corner of the code block below, and paste it into Gemini.")
            st.code(text_prompt, language="markdown")

        # ==========================================
        # TAB 2: UPLOADED IMAGES
        # ==========================================
        with tab2:
            st.write("Use this tab if you are uploading images directly into the Gemini chat.")
            st.success("This prompt is designed to automatically read the filenames of the uploaded images.")
            
            image_prompt = f"""**Role:**
Act as an expert e-commerce visual inventory categorizer and listing generator.

**Task:**
I will provide you with a target Product Family, a strict Taxonomy (Types and Subtypes), and attached product images. You must deeply analyze each product image to categorize it perfectly, generate a complete bilingual e-commerce profile, and provide the final output as a downloadable Excel sheet.

**Rules:**
1. **Strict Categorization:** You must categorize the product using ONLY the Types and Subtypes listed in the provided Taxonomy. Ensure the Subtype strictly falls under the chosen Type. Do not invent new categories. 
2. **Out of Scope:** If the image clearly shows an item that does not belong to the Target Family at all, output "Not {selected_family}" for both Type and Subtype.
3. **Visual Extraction:** Carefully examine the image to extract the Brand, Color, and Size/Dimensions. If an attribute cannot be determined from the image, output "N/A".
4. **Content Generation:** Write a catchy e-commerce title and a powerful description in English.
5. **Translation:** Provide a natural, highly engaging Arabic translation for the title, description, and features.
6. **Image Identification:** You MUST use the exact original filename of each uploaded image as the "Original Filename" column. Do not skip this.
7. **Output Requirement:** You MUST use Python to generate and provide a downloadable Excel file (.xlsx) containing all the extracted and generated data. Do not just print the output; you must generate the file.

**Excel Columns Required:**
1. Original Filename
2. Family ({selected_family})
3. Type
4. Subtype
5. Brand
6. Color
7. Size/Dimensions
8. Polished Title (EN)
9. Description (EN)
10. Feature 1 (EN)
11. Feature 2 (EN)
12. Feature 3 (EN)
13. Polished Title (AR)
14. Description (AR)
15. Feature 1 (AR)
16. Feature 2 (AR)
17. Feature 3 (AR)

---
### 📥 Input Data:

**Target Family:** 
{selected_family}

**Taxonomy (Allowed Types and Subtypes):**
{taxonomy_text}

**Images to Process:**
[PLEASE SEE THE ATTACHED IMAGES IN THIS CHAT]"""

            st.info("💡 Copy this prompt and paste it into Gemini along with your uploaded images.")
            st.code(image_prompt, language="markdown")
