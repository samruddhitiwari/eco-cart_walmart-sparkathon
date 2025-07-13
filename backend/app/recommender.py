def recommend_alternatives(cart_items, df):
    df = df.copy()
    df['product_name_lower'] = df['product_name'].str.strip().str.lower()

    recommendations = []

    for item in cart_items:
        print(f"\n🔍 Checking item: {item}")
        item_clean = item.strip().lower()

        # Match item
        original = df[df['product_name_lower'] == item_clean]
        if original.empty:
            print(f"❌ No match found for: {item}")
            continue
        print(f"✅ Found match for: {item}")

        original_row = original.iloc[0]
        category = original_row['category']
        original_score = (
            original_row['carbon'] +
            original_row['water'] +
            original_row['packaging']
        )
        print(f"📦 Original item: {original_row['product_name']} | Score: {original_score}")

        # Get alternatives in the same category
        same_category = df[(df['category'] == category) & (df['product_name_lower'] != item_clean)]
        print(f"📊 Found {len(same_category)} alternatives in category '{category}'")

        best_alt = None
        best_score = original_score

        for _, row in same_category.iterrows():
            score = row['carbon'] + row['water'] + row['packaging']
            print(f"🔸 {row['product_name']} | Score: {score}")
            if score < best_score:
                print(f"✅ New better alternative: {row['product_name']} (Score: {score})")
                best_score = score
                best_alt = row

        if best_alt is not None:
            print(f"🟢 Selected alternative: {best_alt['product_name']} (Reduced Score: {best_score})")
            recommendations.append({
                "original": original_row["product_name"],
                "alternative": best_alt["product_name"],
                "impact": f"Lower total impact: {round(best_score, 2)} vs {round(original_score, 2)}",
                "value": int(original_score - best_score),
                "type": "Total"
            })
        else:
            print("⚠️ No better alternative found.")

    print(f"\n✅ Total recommendations made: {len(recommendations)}")
    return recommendations
