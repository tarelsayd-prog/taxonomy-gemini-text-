import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Gemini Prompt Generator", layout="centered")

st.title("🤖 Gemini Master Prompt Generator")
st.write("اختار الـ Category، حط الداتا بتاعتك، وانسخ الأسطمبة لـ Gemini.")

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
    st.error(f"⚠️ مش قادر ألاقي ملف الإكسيل! اتأكد إنك رافع ملف اسمه `{EXCEL_FILE}` على GitHub.")
else:
    fam_col, type_col, sub_col = df.columns[0], df.columns[1], df.columns[2]
    
    families = sorted(df[fam_col].astype(str).unique().tolist())
    selected_family = st.selectbox("1️⃣ اختار الـ Category (Family):", families)
    
    if selected_family:
        filtered_df = df[df[fam_col] == selected_family]
        grouped = filtered_df.groupby(type_col)[sub_col].apply(
            lambda x: ', '.join(x.dropna().astype(str).unique())
        )
        taxonomy_lines = [f"- {t}: {subtypes}" for t, subtypes in grouped.items()]
        taxonomy_text = "\n".join(taxonomy_lines)

        st.write("### 2️⃣ اختار نوع الداتا بتاعتك:")
        
        tab1, tab2 = st.tabs(["📝 Text / Titles", "🖼️ Uploaded Images"])

        # ==========================================
        # TAB 1: TEXT / TITLES
        # ==========================================
        with tab1:
            st.write("استخدم التاب دي لو معاك نصوص (Titles/SKUs) بس.")
            titles_input = st.text_area("حط الـ Titles أو الـ SKUs هنا (كل واحد في سطر):", height=150, key="titles")
            titles_data = titles_input if titles_input.strip() else "[PASTE YOUR LIST OF SKUS/TITLES HERE]"
            
            text_prompt = f"""**Role:**
Act as an expert e-commerce inventory categorizer.

**Task:**
I will provide you with a target Product Family, a strict Taxonomy (Types and Subtypes), and a list of SKUs/Product Titles. You must organize the SKUs into a clean Markdown table with the following columns: 
1. Original Title
2. Polished Title (Short & clean for e-commerce)
3. Type
4. Subtype

**Rules:**
1. Strictly use ONLY the Types and Subtypes listed in the provided Taxonomy. Do not invent, guess, or modify the spelling of any categories.
2. Ensure the Subtype you select falls exactly under its designated Type.
3. If an item does not logically fit into the Target Family, leave the Type and Subtype columns with the exact phrase: "Not {selected_family}".

---

**Target Family:** 
{selected_family}

**Taxonomy (Allowed Types and Subtypes):**
{taxonomy_text}

**SKUs to Categorize:**
{titles_data}"""

            st.info("💡 اضغط على علامة النسخ (Copy) في المربع الأسود تحت، وروح حطها في Gemini.")
            st.code(text_prompt, language="markdown")

        # ==========================================
        # TAB 2: UPLOADED IMAGES
        # ==========================================
        with tab2:
            st.write("استخدم التاب دي لو هترفع الصور بإيدك جوا شات Gemini.")
            images_input = st.text_area("حط أسماء أو أرقام الصور هنا (اختياري - عشان ينظمهم):", height=150, key="images")
            images_data = images_input if images_input.strip() else "[PLEASE SEE THE ATTACHED IMAGES IN THIS CHAT]"
            
            image_prompt = f"""**Role:**
Act as an expert e-commerce visual inventory categorizer and listing generator.

**Task:**
I will provide you with a target Product Family, a strict Taxonomy (Types and Subtypes), and attached product images. You must deeply analyze each product image to categorize it perfectly and generate a complete bilingual e-commerce profile.

**Rules:**
1. **Strict Categorization:** You must categorize the product using ONLY the Types and Subtypes listed in the provided Taxonomy. Ensure the Subtype strictly falls under the chosen Type. Do not invent new categories. 
2. **Out of Scope:** If the image clearly shows an item that does not belong to the Target Family at all, output "Not {selected_family}" for both Type and Subtype.
3. **Visual Extraction:** Carefully examine the image to extract the Brand, Color, and Size/Dimensions. If an attribute cannot be determined from the image, output "N/A".
4. **Content Generation:** Write a catchy e-commerce title and a powerful description in English.
5. **Translation:** Provide a natural, highly engaging Arabic translation for the title, description, and features (do not use literal/robotic translation).

---
### 📥 Input Data:

**Target Family:** 
{selected_family}

**Taxonomy (Allowed Types and Subtypes):**
{taxonomy_text}

**Images to Process:**
{images_data}

---
### 📤 Output Format:
*Please analyze each attached image and output the results using the EXACT following structure:*

**Original Input:** [Insert Image Name/Number here]
* **Categorization:**
  * **Family:** {selected_family}
  * **Type:** [Strictly from taxonomy]
  * **Subtype:** [Strictly from taxonomy]
* **Visual Attributes Extracted:**
  * **Brand:** [Extracted Brand or N/A]
  * **Color:** [Extracted Color or N/A]
  * **Size/Dimensions:** [Extracted Size or N/A]
* **English Content:**
  * **Polished Title:** [Short, catchy e-commerce title based on the image]
  * **Description:** [One powerful paragraph describing the item]
  * **Key Features:** 
    - [Feature 1]
    - [Feature 2]
    - [Feature 3]
* **Arabic Content (المحتوى العربي):**
  * **Polished Title:** [Arabic translation of the title]
  * **Description:** [Engaging Arabic translation of the description]
  * **Key Features:**
    - [Arabic Feature 1]
    - [Arabic Feature 2]
    - [Arabic Feature 3]

***[Add a horizontal line `---` between each product]***"""

            st.info("💡 انسخ الأسطمبة دي، وارفع معاها الصور بتاعتك في شات Gemini.")
            st.code(image_prompt, language="markdown")
