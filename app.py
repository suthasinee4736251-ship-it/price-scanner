import streamlit as st

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Best Value Calculator",
    page_icon="🛒",
    layout="centered"
)

# ---------------- STATE ----------------
if "products" not in st.session_state:
    st.session_state.products = []

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Settings")
currency = st.sidebar.selectbox("Currency", ["Baht", "USD", "EUR"])
unit = st.sidebar.selectbox("Unit", ["g", "ml", "pcs"])

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align:center;'>🛒 Best Value Calculator</h1>
    <p style='text-align:center;color:gray'>
    Compare total cost and price per unit
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ================= FORM =================
with st.form("add_product_form"):

    st.subheader("➕ Add Product")

    name = st.text_input("📦 Product name")

    col1, col2 = st.columns(2)

    with col1:
        price = st.number_input(
            f"💰 Price ({currency})",
            min_value=0.0,
            step=1.0
        )

    with col2:
        amount = st.number_input(
            f"📏 Amount per product ({unit})",
            min_value=0.0,
            step=1.0
        )

    st.markdown("**Quick amount presets**")
    preset_cols = st.columns(4)
    preset_value = None

    for value, col in zip([250, 500, 1000, 1], preset_cols):
        if col.form_submit_button(f"+{value}"):
            preset_value = float(value)

    if preset_value is not None:
        amount = preset_value

    st.subheader("🧮 Quantity")
    quantity = st.number_input("Number of products bought", min_value=1, step=1)

    st.subheader("🏷️ Discount")
    discount = st.number_input(
        "Discount (%)",
        min_value=0.0,
        max_value=100.0,
        step=1.0
    )

    submitted = st.form_submit_button("✅ Add Product")

# ================= LOGIC =================
if submitted:
    total_price = price * quantity * (1 - discount / 100)
    total_amount = amount * quantity

    if name.strip() and total_price > 0 and total_amount > 0:
        st.session_state.products.append({
            "name": name,
            "quantity": quantity,
            "total_price": round(total_price, 2),
            "total_amount": total_amount,
            "unit_price": round(total_price / total_amount, 4)
        })
    else:
        st.warning("⚠️ Please enter valid product details")

# ---------------- COMPARISON ----------------
st.markdown("---")
st.subheader("📊 Comparison")

if st.session_state.products:
    best = min(st.session_state.products, key=lambda x: x["unit_price"])

    for p in st.session_state.products:
        highlight = p == best
        st.markdown(
            f"""
            <div style="
                padding:16px;
                border-radius:14px;
                margin-bottom:12px;
                background:{'#E8F5E9' if highlight else '#F6F6F6'};
                border:2px solid {'#4CAF50' if highlight else '#DDD'};
            ">
                <h4>{p['name']} {'🏆 Best Value' if highlight else ''}</h4>
                🧮 Quantity: {p['quantity']}<br>
                💰 Total price: {p['total_price']} {currency}<br>
                📏 Total amount: {p['total_amount']} {unit}<br>
                <b>📐 Unit price: {p['unit_price']} {currency}/{unit}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    if st.button("🗑️ Clear all products", use_container_width=True):
        st.session_state.products.clear()
else:
    st.info("➕ Add products to compare")











