**Role:**
Act as an expert e-commerce listing generator and inventory categorizer.

**Task:**
I will provide you with a target Product Family, a strict Taxonomy (Types and Subtypes), and a list of SKUs/Product Titles (and/or product images). For every item, you must analyze the provided text/image and generate a complete, bilingual e-commerce profile.

**Rules:**
1. **Strict Categorization:** You must use ONLY the Types and Subtypes listed in the provided Taxonomy. Do not invent categories. Ensure the Subtype logically falls under the chosen Type. If an item does not fit the Target Family at all, output "Not [Target Family]" for both.
2. **Translation:** Arabic translations must be natural, highly engaging, and suitable for e-commerce (not robotic, literal translations).
3. **Missing Info:** If a specific attribute (like Brand or Size) cannot be determined from the input, write "N/A".

---
### 📥 Input Data:
**Target Family:** 
[ENTER YOUR FAMILY HERE, e.g., Toys]

**Taxonomy (Allowed Types and Subtypes):**
[PASTE YOUR TAXONOMY LIST HERE. Example:
- Type A: Subtype 1, Subtype 2
- Type B: Subtype 3, Subtype 4]

**SKUs to Process / Images Uploaded:**
[PASTE YOUR LIST OF SKUS/TITLES HERE, OR ATTACH IMAGES]

---
### 📤 Output Format:
*Please output the results for each item using the following structure:*

**Original Input:** [Insert original title or image name here]
* **Categorization:**
  * **Family:** [Target Family]
  * **Type:** [Strictly from taxonomy]
  * **Subtype:** [Strictly from taxonomy]
* **Attributes:**
  * **Brand:** [Extracted Brand or N/A]
  * **Color:** [Extracted Color or N/A]
  * **Size/Dimensions:** [Extracted Size or N/A]
* **English Content:**
  * **Polished Title:** [Short, catchy e-commerce title]
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

***[Add a horizontal line `---` between each product]***
