def recommend_alternatives(cart_items, df):
    df = df.copy()
    df['product_name_clean'] = df['product_name'].str.strip().str.lower().str.replace("_", " ")

    recommendations = []

    for item in cart_items:
        item_clean = item.strip().lower().replace("_", " ")
        print(f"🔍 Looking for alternative for: {item_clean}")
        
        original = df[df['product_name_clean'] == item_clean]
        if original.empty:
            print(f"❌ No match in dataset for: {item}")
            continue

        original_row = original.iloc[0]
        category = original_row['category']
        original_score = (
            original_row['carbon'] +
            original_row['water'] +
            original_row['packaging']
        )

        same_category = df[(df['category'] == category) & (df['product_name_clean'] != item_clean)]

        best_alt = None
        best_score = original_score

        for _, row in same_category.iterrows():
            score = row['carbon'] + row['water'] + row['packaging']
            if score < best_score:
                best_score = score
                best_alt = row

        if best_alt is not None:
            print(f"✅ Found alternative: {best_alt['product_name']} for {item}")
            recommendations.append({
                "original": original_row["product_name"],
                "alternative": best_alt["product_name"],
                "impact": f"Lower total impact: {round(best_score, 2)} vs {round(original_score, 2)}",
                "value": int(original_score - best_score),
                "type": "Total"
            })
        else:
            print(f"❌ No better alternative found for: {item}")

    return recommendations
