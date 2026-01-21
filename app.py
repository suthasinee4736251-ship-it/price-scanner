import streamlit as st

st.set_page_config(page_title="Best Value Calculator", layout="centered")

# ---------- TRANSLATIONS ----------
TEXT = {
    "en": {
        "title": "🛒 Best Value Calculator",
        "subtitle": "Compare products by total cost and unit price",
        "settings": "⚙️ Settings",
        "language": "Language",
        "currency": "Currency",
        "unit": "Unit",
        "add_product": "➕ Add Product",
        "name": "📦 Product name",
        "price": "💰 Price",
        "amount": "📏 Amount per product",
        "quantity": "🧮 Quantity",
        "discount": "🏷️ Discount (%)",
        "add": "✅ Add Product",
        "comparison": "📊 Comparison",
        "best": "🏆 BEST VALUE",
        "clear": "🗑️ Clear all products",
        "empty": "No products added yet",
        "warning_name": "Please enter a product name",
        "warning_values": "Price and amount must be greater than zero",
        "success": "Product added"
    },
    "th": {
        "title": "🛒 เครื่องคำนวณความคุ้มค่า",
        "subtitle": "เปรียบเทียบสินค้าตามราคาและปริมาณ",
        "settings": "⚙️ การตั้งค่า",
        "language": "ภาษา",
        "currency": "สกุลเงิน",
        "unit": "หน่วย",
        "add_product": "➕ เพิ่มสินค้า",
        "name": "📦 ชื่อสินค้า",
        "price": "💰 ราคา",
        "amount": "📏 ปริมาณต่อชิ้น",
        "quantity": "🧮 จำนวน",
        "discount": "🏷️ ส่วนลด (%)",
        "add": "✅ เพิ่มสินค้า",
        "comparison": "📊 การเปรียบเทียบ",
        "best": "🏆 คุ้มค่าที่สุด",
        "clear": "🗑️ ล้างทั้งหมด",
        "empty": "ยังไม่มีสินค้า",
        "warning_name": "กรุณาใส่ชื่อสินค้า",
        "warning_values": "ราคาและปริมาณต้องมากกว่า 0",
        "success": "เพิ่มสินค้าแล้ว"
    }
}

# ---------- STATE ----------
if "products" not in st.session_state:
    st.session_state.products = []

if "lang" not in st.session_state:
    st.session_state.lang = "en"

t = TEXT[st.session_state.lang]

# ---------- SETTINGS ----------
st.sidebar.header(t["settings"])

lang = st.sidebar.radio(
    t["language"],
    ["English", "ไทย"],
    index=0 if st.session_state.lang == "en" else 1
)
st.session_state.lang = "en" if lang == "English" else "th"
t = TEXT[st.session_state.lang]

currency = st.sidebar.selectbox(t["currency"], ["Baht", "USD", "EUR"])
unit = st.sidebar.selectbox(t["unit"], ["g", "ml", "pcs"])

# ---------- UI ----------
st.title(t["title"])
st.caption(t["subtitle"])
st.divider()

# ---------- INPUT ----------
st.subheader(t["add_product"])

name = st.text_input(t["name"])
price = st.number_input(f"{t['price']} ({currency})", min_value=0.0, step=1.0)
amount = st.number_input(f"{t['amount']} ({unit})", min_value=0.0, step=1.0)
quantity = st.number_input(t["quantity"], min_value=1, step=1)
discount = st.number_input(t["discount"], min_value=0.0, max_value=100.0, step=1.0)

# ---------- ADD ----------
if st.button(t["add"], use_container_width=True):

    total_price = price * quantity * (1 - discount / 100)
    total_amount = amount * quantity

    if not name.strip():
        st.warning(t["warning_name"])
    elif total_price <= 0 or total_amount <= 0:
        st.warning(t["warning_values"])
    else:
        st.session_state.products.append({
            "name": name,
            "total_price": round(total_price, 2),
            "total_amount": total_amount,
            "unit_price": round(total_price / total_amount, 4),
            "quantity": quantity
        })
        st.success(t["success"])

# ---------- COMPARISON ----------
st.divider()
st.subheader(t["comparison"])

if st.session_state.products:
    best = min(st.session_state.products, key=lambda x: x["unit_price"])

    for p in st.session_state.products:
        badge = t["best"] if p == best else ""
        st.markdown(
            f"""
            **{p['name']}** {badge}  
            {t["quantity"]}: {p["quantity"]}  
            {t["price"]}: {p["total_price"]} {currency}  
            {t["amount"]}: {p["total_amount"]} {unit}  
            **{p["unit_price"]} {currency}/{unit}**
            ---
            """
        )

    if st.button(t["clear"]):
        st.session_state.products.clear()
else:
    st.info(t["empty"])















