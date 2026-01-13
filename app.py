import streamlit as st
from PIL import Image
from pyzbar.pyzbar import decode
import re

st.set_page_config(page_title="Price Compare", page_icon="🛒")
st.title("🛒 Price Comparison App")

PRODUCTS = {
    "012345678905": {"name": "Milk", "amount": "1L"},
    "036000291452": {"name": "Eggs", "amount": "12 pcs"},
    "123456789012": {"name": "Chocolate", "amount": "100g"},
}

# ✅ Use a SAFE name
if "products" not in st.session_state:
    st.session_state.products = []

def parse_amount(text):
    match = re.match(r"([\d\.]+)\s*(\w+)", text)
    if match:
        return float(match.group(1)), match.group(2)
    return None, None

st.subheader("Manual Entry")

name = st.text_input("Product name", key="name")
amount = st.text_input("Amount (e.g. 100g, 1L)", key="amount")
price = st.number_input("Price", min_value=0.01, format="%.2f", key="price")

if st.button("📷 Scan Barcode"):
    image = st.camera_input("Scan barcode", key="camera")

    if image:
        img = Image.open(image).convert("L")
        img = img.resize((img.width * 2, img.height * 2))
        codes = decode(img)

        if codes:
            code = codes[0].data.decode("utf-8")
            if code in PRODUCTS:
                st.session_state.name = PRODUCTS[code]["name"]
                st.session_state.amount = PRODUCTS[code]["amount"]
                st.success("Product found!")
        else:
            st.error("Barcode not detected")

if st.button("➕ Add product"):
    num, unit = parse_amount(st.session_state.amount)

    if not st.session_state.name or not num:
        st.error("Invalid input")
    else:
        value = num / st.session_state.price
        st.session_state.products.append({
            "name": st.session_state.name,
            "value": value,
            "unit": unit
        })
        st.success("Product added!")

if st.session_state.products:
    st.subheader("📊 Comparison")

    best = max(st.session_state.products, key=lambda x: x["value"])

    for p in st.session_state.products:
        st.write(
            f"**{p['name']}** → {p['value']:.2f} {p['unit']} per 1 baht"
        )

    st.success(f"🏆 Best value: {best['name']}")

if st.button("🗑 Clear all"):
    st.session_state.products = []
    st.experimental_rerun()

