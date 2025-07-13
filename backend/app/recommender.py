def recommend_alternatives(cart_items, df):
    df = df.copy()
    df['product_name_lower'] = df['product_name'].str.strip().str.lower()

    recommendations = []

    for item in cart_items:
        item_clean = item.strip().lower()
        original = df[df['product_name_lower'] == item_clean]
        if original.empty:
            print(f"No match for item: {item}")
            continue

        original_row = original.iloc[0]
        category = original_row['category']
        original_score = (
            original_row['carbon'] +
            original_row['water'] +
            original_row['packaging']
        )

        same_category = df[(df['category'] == category) & (df['product_name_lower'] != item_clean)]

        best_alt = None
        best_score = original_score

        for _, row in same_category.iterrows():
            score = row['carbon'] + row['water'] + row['packaging']
            if score < best_score:
                best_score = score
                best_alt = row

        if best_alt is not None:
            recommendations.append({
                "original": original_row["product_name"],
                "alternative": best_alt["product_name"],
                "impact": f"Lower total impact: {round(best_score, 2)} vs {round(original_score, 2)}",
                "value": int(original_score - best_score),
                "type": "Total"
            })

    return recommendations
