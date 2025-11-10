from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from smart_scraper import scrape_amazon_product
from nlp_processor import nlp_processor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"], 
    allow_headers=["*"],
)

def rating_to_stars(rating):
    """Convert 0-5 rating to star emojis"""
    try:
        full_stars = int(rating)
        half_star = 1 if rating - full_stars >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star
        return "⭐" * full_stars + "🌗" * half_star + "☆" * empty_stars
    except:
        return "⭐⭐⭐☆☆"

@app.post("/analyze")
def analyze_product(request: dict):
    url = request.get("product_url", "")
    
    print(f"🔍 Starting Full Analysis: {url}")
    
    #Scraping data including reviews
    print("🔄 STEP 2: Scraping product data and reviews...")
    scrape_result = scrape_amazon_product(url)
    
    if not scrape_result["success"]:
        return {"status": "error", "message": scrape_result["error"]}
    
    product_data = scrape_result["product_data"]
    reviews = product_data.get("reviews", [])
    total_reviews_count = product_data.get("total_reviews_count", len(reviews))
    
    print(f"✅ STEP 2 Complete: {len(reviews)} reviews scraped")
    
    #Processing data with NLP
    print("🔄 STEP 3: Analyzing reviews with AI...")
    website_rating = product_data.get("rating", 3.0)
    
    #Sending the scraped reviews to NLP processor
    ai_result = nlp_processor.analyze_product_reviews(
        reviews=reviews,
        total_reviews_count=total_reviews_count,
        website_rating=website_rating
    )
    
    print(f"✅ STEP 3 Complete: Buy Score {ai_result['buy_score']}/100")
    
    #Returning the final analysis
    print("🎉 Final Analysis Ready!")
    
    return {
        "status": "success",
        "productTitle": product_data.get("title", "Amazon Product"),
        "productImage": product_data.get("image", "https://placehold.co/150x150/0a0a0a/ffffff?text=Product"),
        "price": product_data.get("price", "Not available"),
        "websiteRating": website_rating,
        "score": ai_result["ai_rating"],  # Our AI's rating from sentiment analysis
        "stars": rating_to_stars(ai_result["ai_rating"]),
        "buyScore": ai_result["buy_score"],
        "recommendation": ai_result["recommendation"],
        "verdict": ai_result["summary"],
        "pros": ai_result["pros"],
        "cons": ai_result["cons"],
        "totalReviews": total_reviews_count,
        "analyzedReviews": len(reviews),  # How many reviews we actually analyzed
        "features": product_data.get("features", [])[:5],
        "breakdown": ai_result.get("breakdown", {})
    }

if _name_ == "_main_":
    print("🚀 Full Pipeline: Scraping → NLP → Analysis")
    print("   Step 1: Scrape product data ✓")
    print("   Step 2: Scrape 20+ reviews ✓") 
    print("   Step 3: NLP sentiment analysis ✓")
    print("   Step 4: Generate buy score & summary ✓")
    uvicorn.run(app, host="0.0.0.0", port=8000)