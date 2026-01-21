import streamlit as st

st.set_page_config(page_title="Best Value Calculator", layout="centered")

st.title("🛒 Best Value Calculator")
st.caption("Compare total cost and price per unit")

# ---------- STATE ----------
if "products" not in st.session_state:
    st.session_state.products = []

# ---------- SETTINGS ----------
currency = st.selectbox("Currency", ["Baht", "USD", "EUR"])
unit = st.selectbox("Unit", ["g", "ml", "pcs"])

st.divider()

# ---------- INPUTS ----------
st.subheader("➕ Add Product")

name = st.text_input("📦 Product name")

# ---- PRICE ----
price = st.number_input(f"💰 Price ({currency})", min_value=0.0, step=1.0)

p1, p2, p3, p4 = st.columns(4)
if p1.button("+10"): price += 10
if p2.button("+50"): price += 50
if p3.button("+100"): price += 100
if p4.button("+500"): price += 500

st.write(f"Current price: **{price:.2f} {currency}**")

# ---- AMOUNT ----
amount = st.number_input(f"📏 Amount per product ({unit})", min_value=0.0, step=1.0)

a1, a2, a3, a4 = st.columns(4)
if a1.button("+10"): amount += 10
if a2.button("+50"): amount += 50
if a3.button("+100"): amount += 100
if a4.button("+1000"): amount += 1000

st.write(f"Current amount: **{amount} {unit}**")

# ---- QUANTITY ----
quantity = st.number_input("🧮 Quantity", min_value=1, step=1)

# ---- DISCOUNT ----
discount = st.number_input("🏷️ Discount (%)", min_value=0.0, max_value=100.0, step=1.0)

st.divider()

# ---------- ADD PRODUCT ----------
if st.button("✅ Add Product", use_container_width=True):

    total_price = price * quantity * (1 - discount / 100)
    total_amount = amount * quantity

    if not name.strip():
        st.warning("Enter a product name")
    elif total_price <= 0 or total_amount <= 0:
        st.warning("Price and amount must be greater than zero")
    else:
        st.session_state.products.append({
            "name": name,
            "total_price": round(total_price, 2),
            "total_amount": total_amount,
            "unit_price": round(total_price / total_amount, 4),
            "quantity": quantity
        })

        st.success("Product added")

# ---------- COMPARISON ----------
st.divider()
st.subheader("📊 Comparison")

if st.session_state.products:
    best = min(st.session_state.products, key=lambda x: x["unit_price"])

    for p in st.session_state.products:
        tag = "🏆 BEST VALUE" if p == best else ""
        st.markdown(
            f"""
            **{p['name']}** {tag}  
            Quantity: {p['quantity']}  
            Total price: {p['total_price']} {currency}  
            Total amount: {p['total_amount']} {unit}  
            **Unit price: {p['unit_price']} {currency}/{unit}**
            ---
            """
        )

    if st.button("🗑️ Clear all products"):
        st.session_state.products.clear()
else:
    st.info("No products added yet")















