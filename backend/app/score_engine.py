def calculate_score(cart, df):
    selected = df[df["product_name"].isin(cart)]

    co2 = selected["carbon"].sum()
    water = selected["water"].sum()
    packaging = selected["packaging"].sum()

    # Normalize for greenScore (you can adjust this logic)
    green_score = max(0, 100 - (co2 / 50 + water / 200 + packaging))

    # Simple eco badges
    is_plastic_free = all("plastic" not in name.lower() and "disposable" not in name.lower() for name in cart)
    has_local_items = any("bamboo" in name.lower() or "beeswax" in name.lower() for name in cart)

    return {
        "greenScore": round(green_score),
        "co2Impact": round(co2),
        "waterUsage": round(water, 2),
        "packagingWaste": round(packaging),
        "isPlasticFree": is_plastic_free,
        "hasLocalItems": has_local_items
    }
