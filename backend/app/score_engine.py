def calculate_score(cart, df):
    # Normalize cart item names to match DataFrame format (snake_case)
    normalized_cart = [name.lower().replace(" ", "_") for name in cart]

    selected = df[df["product_name"].isin(normalized_cart)]

    co2 = selected["carbon"].sum()
    water = selected["water"].sum()
    packaging = selected["packaging"].sum()

    green_score = max(0, 100 - (co2 / 50 + water / 200 + packaging))

    is_plastic_free = all("plastic" not in name.lower() and "disposable" not in name.lower() for name in normalized_cart)
    has_local_items = any("bamboo" in name.lower() or "beeswax" in name.lower() for name in normalized_cart)

    return {
    "greenScore": round(green_score),
    "co2Impact": round(co2),
    "waterUsage": round(water, 2),
    "packagingWaste": round(packaging),
    "isPlasticFree": is_plastic_free,
    "hasLocalItems": has_local_items,
    "details": [
        {
            "product_name": str(row["product_name"]),
            "category": str(row["category"]),
            "carbon": int(row["carbon"]),
            "water": float(row["water"]),
            "packaging": int(row["packaging"]),
            "ethics_score": int(row["ethics_score"])
        }
        for _, row in selected.iterrows()
    ]
}

