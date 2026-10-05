import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Gemini Prompt Generator", layout="centered")

st.title("🤖 Gemini Taxonomy Prompt Generator")
st.write("اختار الفاميلي، حط الـ Titles، وانسخ البرومت لـ Gemini.")

# اسم ملف الإكسيل اللي موجود معاك في نفس الفولدر على GitHub
EXCEL_FILE = "taxonomy.xlsx" 

@st.cache_data
def load_data():
    if not os.path.exists(EXCEL_FILE):
        return None
    # قراءة الملف
    df = pd.read_excel(EXCEL_FILE)
    # مسح الصفوف الفاضية
    df = df.dropna(subset=[df.columns[0]])
    return df

df = load_data()

if df is None:
    st.error(f"⚠️ مش قادر ألاقي ملف الإكسيل! اتأكد إنك رافع ملف اسمه `{EXCEL_FILE}` على GitHub في نفس المكان.")
else:
    # تحديد العواميد (العمود الأول Family, التاني Type, التالت Subtype)
    fam_col, type_col, sub_col = df.columns[0], df.columns[1], df.columns[2]
    
    # 1. قائمة اختيار الفاميلي
    families = sorted(df[fam_col].astype(str).unique().tolist())
    selected_family = st.selectbox("1️⃣ اختار الـ Family:", families)
    
    # 2. مكان تحط فيه الـ Titles (SKUs)
    skus_input = st.text_area("2️⃣ حط الـ Titles أو الـ SKUs هنا (كل واحد في سطر):", height=150)
    
    if selected_family:
        # فلترة الداتا بناءً على الفاميلي
        filtered_df = df[df[fam_col] == selected_family]
        
        # تجميع الـ Subtypes تحت كل Type
        grouped = filtered_df.groupby(type_col)[sub_col].apply(
            lambda x: ', '.join(x.dropna().astype(str).unique())
        )
        
        taxonomy_lines = []
        for t, subtypes in grouped.items():
            taxonomy_lines.append(f"- {t}: {subtypes}")
        
        taxonomy_text = "\n".join(taxonomy_lines)
        
        # لو مكتبتش تايتلز، هيحط رسالة بديلة
        skus_to_categorize = skus_input if skus_input.strip() else "[PASTE YOUR LIST OF SKUS/PRODUCT TITLES HERE]"

        # 3. الأسطمبة النهائية زي ما طلبتها بالظبط
        master_prompt = f"""Categorization Master Prompt: Please act as an expert inventory categorizer. I will provide you with a list of SKUs. You must organize them into a table with the columns: Title, Type, and Subtype.

Rules:
1. Strictly use only the Types and Subtypes listed below.
2. If an item is not a {selected_family.lower()} (e.g., adult apparel, baby feeding bottles), leave the Type and Subtype columns With keyword like ( Not {selected_family})

Types and Subtypes:
{taxonomy_text}

SKUs to Categorize:
{skus_to_categorize}"""

        st.divider()
        st.subheader("📝 البرومت جاهز:")
        st.info("💡 اضغط على علامة النسخ (Copy) اللي هتظهر في المربع الأسود فوق على اليمين.")
        
        # عرض البرومت بطريقة سهلة للنسخ
        st.code(master_prompt, language="markdown")
