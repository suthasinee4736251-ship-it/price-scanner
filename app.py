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
    "name": "",
    "price_value": 0.0,
    "amount_value": 0.0,
    "quantity": 1,
    "discount": 0.0,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- CALLBACKS ----------------
def add_price(v):
    st.session_state.price_value += v

def add_amount(v):
    st.session_state.amount_value += v

def add_product():
    total_price = st.session_state.price_value * st.session_state.quantity
    total_price *= (1 - st.session_state.discount / 100)

    total_amount = st.session_state.amount_value * st.session_state.quantity

    if st.session_state.name.strip() and total_price > 0 and total_amount > 0:
        st.session_state.products.append({
            "name": st.session_state.name,
            "quantity": st.session_state.quantity,
            "total_price": round(total_price, 2),
            "total_amount": total_amount,
            "unit_price": round(total_price / total_amount, 4),
        })

        # reset
        st.session_state.name = ""
        st.session_state.price_value = 0.0
        st.session_state.amount_value = 0.0
        st.session_state.quantity = 1
        st.session_state.discount = 0.0

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

# ---------------- INPUTS ----------------
st.subheader("➕ Add Product")

st.text_input("📦 Product name", key="name")

col1, col2 = st.columns(2)

# -------- PRICE --------
with col1:
    st.number_input(
        f"💰 Price ({currency})",
        min_value=0.0,
        step=1.0,
        value=st.session_state.price_value,
        key="price_display"
    )
    st.session_state.price_value = st.session_state.price_display

    st.caption("Price presets")
    p1, p2, p3, p4 = st.columns(4)
    p1.button("+10", on_click=add_price, args=(10.0,))
    p2.button("+50", on_click=add_price, args=(50.0,))
    p3.button("+100", on_click=add_price, args=(100.0,))
    p4.button("+500", on_click=add_price, args=(500.0,))

# -------- AMOUNT --------
with col2:
    st.number_input(
        f"📏 Amount per product ({unit})",
        min_value=0.0,
        step=1.0,
        value=st.session_state.amount_value,
        key="amount_display"
    )
    st.session_state.amount_value = st.session_state.amount_display

    st.caption("Amount presets")
    a1, a2, a3, a4 = st.columns(4)
    a1.button("+10", on_click=add_amount, args=(10.0,))
    a2.button("+50", on_click=add_amount, args=(50.0,))
    a3.button("+100", on_click=add_amount, args=(100.0,))
    a4.button("+1000", on_click=add_amount, args=(1000.0,))

# ---------------- QUANTITY ----------------
st.markdown("---")
st.number_input("🧮 Quantity", min_value=1, step=1, key="quantity")

# ---------------- DISCOUNT ----------------
st.markdown("---")
st.number_input("🏷️ Discount (%)", min_value=0.0, max_value=100.0, step=1.0, key="discount")

# ---------------- ADD BUTTON ----------------
st.markdown("---")
st.button("✅ Add Product", use_container_width=True, on_click=add_product)

# ---------------- COMPARISON ----------------
st.markdown("---")
st.subheader("📊 Comparison")

if st.session_state.products:
    best = min(st.session_state.products, key=lambda x: x["unit_price"])

    for p in st.session_state.products:
        is_best = p == best
        st.markdown(
            f"""
            <div style="
                padding:16px;
                border-radius:14px;
                margin-bottom:12px;
                background:{'#E8F5E9' if is_best else '#F6F6F6'};
                border:2px solid {'#4CAF50' if is_best else '#DDD'};
            ">
                <h4>{p['name']} {'🏆 Best Value' if is_best else ''}</h4>
                🧮 Quantity: {p['quantity']}<br>
                💰 Total price: {p['total_price']} {currency}<br>
                📏 Total amount: {p['total_amount']} {unit}<br>
                <b>📐 Unit price: {p['unit_price']} {currency}/{unit}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    if st.button("🗑️ Clear all products"):
        st.session_state.products.clear()
else:
    st.info("➕ Add products to compare")












