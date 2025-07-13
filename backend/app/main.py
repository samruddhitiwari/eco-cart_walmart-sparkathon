from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from app.data_loader import load_data
from app.score_engine import calculate_score
from app.recommender import recommend_alternatives
from fastapi.middleware.cors import CORSMiddleware
origins = [
  "https://eco-cart-walmart-sparkathon.vercel.app"
]


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://eco-cart-walmart-sparkathon.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data
df = load_data()

# Request model
class CartRequest(BaseModel):
    cart: List[str]

@app.get("/")
def root():
    return {"message": "EchoCart API is running 🚀"}

@app.post("/analyze-cart")
async def analyze_cart(cart_request: CartRequest):
    try:
        cart = cart_request.cart
        print("Cart received:", cart)
        result = calculate_score(cart, df)
        return result
    except Exception as e:
        return {"error": str(e)}
@app.post("/recommendations")
async def get_recommendations(cart_request: CartRequest):
    cart = cart_request.cart
    suggestions = recommend_alternatives(cart, df)
    return {"recommendations": suggestions}
@app.get("/products")
def get_products():
    def map_row(row):
        return {
            "id": row.name,
            "name": row["product_name"].replace("_", " ").title(),
            "category": row["category"],
            "carbon": row["carbon"],
            "water": row["water"],
            "packaging": row["packaging"],
            "ethics": row["ethics_score"],
            "ecoScore": (
                "A" if row["carbon"] < 500
                else "B" if row["carbon"] < 1000
                else "C" if row["carbon"] < 2000
                else "D"
            )
        }

    return [map_row(row) for _, row in sustainability_data.iterrows()]



@app.get("/dashboard-stats")
def dashboard_stats():
    df = load_data()

    # Calculate averages
    avg_carbon = round(df["carbon"].mean(), 2)
    avg_water = round(df["water"].mean(), 2)
    avg_packaging = round(df["packaging"].mean(), 2)

    # Top 2 categories by average carbon
    top_categories = (
        df.groupby("category")["carbon"]
        .mean()
        .sort_values(ascending=False)
        .head(2)
        .reset_index()
        .to_dict(orient="records")
    )

    # Mock recommendations (optional: collect from usage later)
    most_recommended = ["metal_flask", "veggie_burger"]

    return {
        "average_carbon": avg_carbon,
        "average_water": avg_water,
        "average_packaging": avg_packaging,
        "top_categories_by_impact": top_categories,
        "most_recommended_items": most_recommended
    }

