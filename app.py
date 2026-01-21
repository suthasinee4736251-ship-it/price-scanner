import streamlit as st

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Best Value Calculator",
    page_icon="🛒",
    layout="centered"
)

# ---------------- STATE ----------------
for key, default in {
    "products": [],
    "price": 0.0,
    "amount": 0.0,
    "quantity": 1,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ---------------- SETTINGS ----------------
st.sidebar.header("⚙️ Settings")

currency = st.sidebar.selectbox("Currency", ["Baht", "USD", "EUR"])
dark_mode = st.sidebar.toggle("🌙 Dark mode")

unit = st.sidebar.selectbox("Unit", ["g", "ml", "pcs"])

bg = "#1E1E1E" if dark_mode else "#FFFFFF"
card = "#2A2A2A" if dark_mode else "#F6F6F6"
text = "#FFFFFF" if dark_mode else "#000000"
best_bg = "#1B5E20" if dark_mode else "#E8F5E9"

# ---------------- STYLE ----------------
st.markdown(
    f"""
    <style>
    body {{ background-color: {bg}; color: {text}; }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- HEADER ----------------
st.markdown(
    f"""
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
        value=st.session_state.price
    )

    p1, p2 = st.columns(2)
    if p1.button("+10"):
        st.session_state.price += 10
    if p2.button("+50"):
        st.session_state.price += 50

with col2:
    st.session_state.amount = st.number_input(
        f"📏 Amount per product ({unit})",
        min_value=0.0,
        step=1.0,
        value=st.session_state.amount
    )

    a1, a2 = st.columns(2)
    if a1.button("+10"):
        st.session_state.amount += 10
    if a2.button("+100"):
        st.session_state.amount += 100

# ---------------- PRESETS ----------------
st.caption("Quick amount presets")
preset_cols = st.columns(4)
for value, col in zip([250, 500, 1000, 1], preset_cols):
    if col.button(str(value)):
        st.session_state.amount = value

# ---------------- QUANTITY ----------------
st.markdown("---")
st.subheader("🧮 Quantity")

st.session_state.quantity = st.number_input(
    "Number of products bought",
    min_value=1,
    step=1,
    value=st.session_state.quantity
)

# ---------------- DISCOUNT ----------------
st.markdown("---")
st.subheader("🏷️ Discount (optional)")

discount = st.slider("Discount (%)", 0, 100, 0)

final_price = st.session_state.price * st.session_state.quantity
final_price *= (1 - discount / 100)

total_amount = st.session_state.amount * st.session_state.quantity

# ---------------- ADD BUTTON ----------------
st.markdown("---")
if st.button("✅ Add Product", use_container_width=True):
    if name.strip() and total_amount > 0 and final_price > 0:
        st.session_state.products.append({
            "name": name,
            "total_price": round(final_price, 2),
            "total_amount": total_amount,
            "unit_price": round(final_price / total_amount, 4),
            "quantity": st.session_state.quantity
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
        is_best = p == best

        st.markdown(
            f"""
            <div style="
                padding:16px;
                border-radius:14px;
                margin-bottom:12px;
                background:{best_bg if is_best else card};
                border:2px solid {'#4CAF50' if is_best else '#CCC'};
                color:{text};
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

    if st.button("🗑️ Clear all products", use_container_width=True):
        st.session_state.products.clear()

else:
    st.info("➕ Add products to compare")





