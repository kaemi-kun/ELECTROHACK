from transformers import pipeline
import re

class SmartBuyNLP:
    def _init_(self):
        print("🧠 Loading NLP models...")
        
        # Sentiment analysis model
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment",
            tokenizer="nlptown/bert-base-multilingual-uncased-sentiment"
        )
        
        # Summarization model  
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            tokenizer="facebook/bart-large-cnn"
        )
        
        print("✅ NLP models loaded successfully!")
    
    def analyze_sentiment(self, reviews):
        """Analyze sentiment of reviews and return average score"""
        if not reviews:
            return 3.0  # Neutral if no reviews
        
        sentiment_scores = []
        
        for review in reviews[:15]:  # Analyze first 15 reviews for performance
            try:
                # TruncatING long reviews
                truncated_review = review[:512]
                result = self.sentiment_pipeline(truncated_review)[0]
                
                # Convert "1 star", "2 stars" etc. to 1-5 scale
                stars = int(result['label'].split()[0])
                sentiment_scores.append(stars)
                
            except Exception as e:
                print(f"⚠ Sentiment analysis error: {e}")
                continue
        
        # Calculateing average rating
        if sentiment_scores:
            avg_rating = sum(sentiment_scores) / len(sentiment_scores)
            return round(avg_rating, 1)
        else:
            return 3.0
    
    def generate_summary(self, reviews):
        """Generate overall summary from reviews"""
        if not reviews:
            return "No reviews available for analysis."
        
        try:
            # Combineing sample reviews for summary
            sample_reviews = reviews[:8]
            combined_text = " ".join(sample_reviews)
            
            # Truncating to model limits
            if len(combined_text) > 4000:
                combined_text = combined_text[:4000]
            
            summary = self.summarizer(
                combined_text,
                max_length=150,
                min_length=50,
                do_sample=False
            )[0]['summary_text']
            
            return summary
            
        except Exception as e:
            print(f"⚠ Summarization error: {e}")
            return "Our AI is analyzing reviews to generate insights."
    
    def extract_pros_cons(self, reviews, sentiment_scores):
        """Extract pros and cons based on sentiment"""
        pros = []
        cons = []
        
        for i, review in enumerate(reviews[:10]):  # First 10 reviews
            if i < len(sentiment_scores):
                score = sentiment_scores[i]
                
                # Simple rules: 4-5 stars = pro, 1-2 stars = con
                if score >= 4:
                    # Extract key phrase (first 15 words)
                    snippet = ' '.join(review.split()[:15])
                    if len(snippet) > 20:
                        pros.append(snippet + '...')
                elif score <= 2:
                    snippet = ' '.join(review.split()[:15])
                    if len(snippet) > 20:
                        cons.append(snippet + '...')
        
        return {
            'pros': pros[:5],  # Return top 5 each
            'cons': cons[:5]
        }
    
    def calculate_buy_score(self, avg_sentiment, total_reviews_count, website_rating, price_trend="stable"):
        """
        Calculate comprehensive buy score (0-100)
        Factors:
        - Sentiment from our AI (40%)
        - Website rating (20%) 
        - Review volume/confidence (20%)
        - Price trend (20%)
        """
        
        # 1. Sentiment score (0-100) from our AI analysis
        sentiment_score = (avg_sentiment / 5.0) * 100 * 0.4
        
        # 2. Website rating score (0-100)
        website_score = (website_rating / 5.0) * 100 * 0.2
        
        # 3. Review volume score - more reviews = more confidence
        if total_reviews_count >= 100:
            volume_score = 100 * 0.2
        elif total_reviews_count >= 50:
            volume_score = 80 * 0.2
        elif total_reviews_count >= 20:
            volume_score = 60 * 0.2
        else:
            volume_score = 40 * 0.2
        
        # 4. Price trend score (simplified for now)
        price_scores = {
            "decreasing": 100 * 0.2,
            "stable": 80 * 0.2, 
            "increasing": 60 * 0.2
        }
        price_score = price_scores.get(price_trend, 80 * 0.2)
        
        # Calculate final score
        final_score = sentiment_score + website_score + volume_score + price_score
        
        return {
            'buy_score': int(final_score),
            'sentiment_breakdown': {
                'ai_sentiment': int(sentiment_score / 0.4),
                'website_rating': int(website_score / 0.2),
                'review_volume': int(volume_score / 0.2),
                'price_trend': int(price_score / 0.2)
            }
        }

    def get_recommendation(self, buy_score):
        """Get recommendation based on buy score"""
        if buy_score >= 90:
            return "STRONG BUY 🟢"
        elif buy_score >= 75:
            return "BUY 🟡" 
        elif buy_score >= 40:
            return "HOLD ⚪"
        else:
            return "AVOID 🔴"

    def analyze_product_reviews(self, reviews, total_reviews_count, website_rating):
        """Complete analysis pipeline"""
        print("🤖 Starting AI analysis of reviews...")
        
        # 1. Sentiment Analysis
        avg_sentiment = self.analyze_sentiment(reviews)
        print(f"   ✅ Average Sentiment: {avg_sentiment}/5")
        
        # 2. Generate Summary
        summary = self.generate_summary(reviews)
        print(f"   ✅ Summary Generated")
        
        # 3. Calculate Buy Score
        buy_score_data = self.calculate_buy_score(avg_sentiment, total_reviews_count, website_rating)
        print(f"   ✅ Buy Score: {buy_score_data['buy_score']}/100")
        
        # 4. Get individual sentiment scores for pros/cons
        sentiment_scores = []
        for review in reviews[:15]:
            try:
                result = self.sentiment_pipeline(review[:512])[0]
                stars = int(result['label'].split()[0])
                sentiment_scores.append(stars)
            except:
                sentiment_scores.append(3)  # Neutral if error
        
        # 5. Extract Pros/Cons
        pros_cons = self.extract_pros_cons(reviews, sentiment_scores)
        
        # 6. Get Recommendation
        recommendation = self.get_recommendation(buy_score_data['buy_score'])
        
        return {
            'summary': summary,
            'buy_score': buy_score_data['buy_score'],
            'recommendation': recommendation,
            'ai_rating': avg_sentiment,
            'pros': pros_cons['pros'],
            'cons': pros_cons['cons'],
            'breakdown': buy_score_data['sentiment_breakdown']
        }

# Create global instance
nlp_processor = SmartBuyNLP()