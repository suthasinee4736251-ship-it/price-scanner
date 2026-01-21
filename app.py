import streamlit as st

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Best Value Calculator",
    page_icon="🛒",
    layout="centered"
)

# ---------------- STATE ----------------
defaults = {
    "products": [],
    "price": 0.0,
    "amount": 0.0,
    "quantity": 1,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

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

# ---------------- ADD PRODUCT ----------------
st.subheader("➕ Add Product")

name = st.text_input("📦 Product name")

col1, col2 = st.columns(2)

with col1:
    st.session_state.price = st.number_input(
        f"💰 Price ({currency})",
        min_value=0.0,
        step=1.0,
        value=st.session_state.price,
        key="price_input"
    )

    b1, b2 = st.columns(2)
    if b1.button("+10", key="price_plus_10"):
        st.session_state.price += 10
    if b2.button("+50", key="price_plus_50"):
        st.session_state.price += 50

with col2:
    st.session_state.amount = st.number_input(
        f"📏 Amount per product ({unit})",
        min_value=0.0,
        step=1.0,
        value=st.session_state.amount,
        key="amount_input"
    )

    b3, b4 = st.columns(2)
    if b3.button("+10", key="amount_plus_10"):
        st.session_state.amount += 10
    if b4.button("+100", key="amount_plus_100"):
        st.session_state.amount += 100

# ---------------- PRESETS ----------------
st.caption("Quick amount presets")
preset_cols = st.columns(4)
for value, key, col in zip(
    [250, 500, 1000, 1],
    ["preset_250", "preset_500", "preset_1000", "preset_1"],
    preset_cols
):
    if col.button(str(value), key=key):
        st.session_state.amount = value

# ---------------- QUANTITY ----------------
st.markdown("---")
st.subheader("🧮 Quantity")

st.session_state.quantity = st.number_input(
    "Number of products bought",
    min_value=1,
    step=1,
    value=st.session_state.quantity,
    key="quantity_input"
)

# ---------------- DISCOUNT ----------------
st.markdown("---")
st.subheader("🏷️ Discount (optional)")

discount = st.slider("Discount (%)", 0, 100, 0, key="discount_slider")

total_price = st.session_state.price * st.session_state.quantity
total_price *= (1 - discount / 100)

total_amount = st.session_state.amount * st.session_state.quantity

# ---------------- ADD BUTTON ----------------
st.markdown("---")
if st.button("✅ Add Product", use_container_width=True, key="add_product"):
    if name.strip() and total_price > 0 and total_amount > 0:
        st.session_state.products.append({
            "name": name,
            "quantity": st.session_state.quantity,
            "total_price": round(total_price, 2),
            "total_amount": total_amount,
            "unit_price": round(total_price / total_amount, 4)
        })

        st.session_state.price = 0.0
        st.session_state.amount = 0.0
        st.session_state.quantity = 1
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

    if st.button("🗑️ Clear all products", use_container_width=True, key="clear_all"):
        st.session_state.products.clear()
else:
    st.info("➕ Add products to compare")








