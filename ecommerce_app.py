import json
from pathlib import Path
import streamlit as st

st.title("Oat & Smoothie Shop")

# Load menu data
menu_path = Path(__file__).parent / "data" / "menu.json"
menu = json.loads(menu_path.read_text())

st.header("Menu")
for item in menu:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"**{item['name']}** - ${item['price']:.2f}")
        st.caption(item["description"])
    with col2:
        qty = st.number_input(
            f"qty_{item['name']}", min_value=0, max_value=10, value=0, key=f"qty_{item['name']}"
        )
    item["quantity"] = qty

if st.button("Add to cart"):
    selected = [
        {k: v for k, v in i.items() if k != "description"}
        for i in menu
        if i["quantity"] > 0
    ]
    if not selected:
        st.warning("No items selected")
    else:
        st.session_state.setdefault("cart", [])
        for s in selected:
            st.session_state["cart"].append(s)
        st.success("Added to cart!")

st.header("Cart")
cart = st.session_state.get("cart", [])
if cart:
    total = 0
    for item in cart:
        subtotal = item["quantity"] * item["price"]
        st.write(f"{item['quantity']} x {item['name']} - ${subtotal:.2f}")
        total += subtotal
    st.write(f"**Total: ${total:.2f}**")
    if st.button("Place order"):
        st.success("Order placed! We'll reach out soon.")
        st.session_state["cart"] = []
else:
    st.write("Cart is empty.")
