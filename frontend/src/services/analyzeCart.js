import api from "./api";

export async function analyzeCart(cart) {
  const itemIds = cart.map(item => item.name.toLowerCase().replace(/ /g, "_"));

  try {
    const response = await api.post("/analyze-cart", {
      cart: itemIds,
    });
    return response.data;
  } catch (error) {
    console.error("Cart analysis failed:", error);
    return null;
  }
}
