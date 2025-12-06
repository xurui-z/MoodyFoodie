import os
import pickle
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai 

# ================= Configuration Area =================
# 🔴 Enter your Google Gemini API Key here
MY_GOOGLE_KEY = "AIzaSyBTpupZl8X3QG90AltwUdsKXWQB9a1oxpI" # <--- Paste your 'AIza...' key here

# Path to the data file
DATA_PATH = r"E:\DS\NLP\recipe_data_with_embeddings.pkl"
# ======================================================

# 1. Configure Google Gemini
genai.configure(api_key=MY_GOOGLE_KEY)

def get_best_available_model():
    """
    Automatically finds a working model for your API Key.
    Prioritizes 'flash' models, falls back to 'pro'.
    """
    print("🤖 Connecting to Google to find available models...")
    try:
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        # Priority Logic: Try to find the best model name that actually exists for you
        # 1. Look for a Flash model (Fastest/Free-est)
        for model in available_models:
            if "gemini-1.5-flash" in model:
                print(f"✅ Found preferred model: {model}")
                return model
        
        # 2. Look for Pro model (Stronger)
        for model in available_models:
            if "gemini-1.5-pro" in model:
                print(f"✅ Found robust model: {model}")
                return model
        
        # 3. Fallback to standard Gemini Pro (1.0)
        for model in available_models:
            if "gemini-pro" in model:
                print(f"⚠️ 1.5 Flash not found. Falling back to standard: {model}")
                return model

        # 4. Last resort: Just take the first one available
        if available_models:
            print(f"⚠️ Using first available model: {available_models[0]}")
            return available_models[0]
            
    except Exception as e:
        print(f"⚠️ Could not list models automatically ({e}).")
    
    # If all else fails, try the standard string
    return "gemini-1.5-flash"

# Initialize the best model found
best_model_name = get_best_available_model()
llm_model = genai.GenerativeModel(best_model_name)

# 2. Load data and models
print("Loading data and models... (This might take a moment)")
try:
    with open(DATA_PATH, 'rb') as f:
        data = pickle.load(f)
    df = data['df']
    recipe_embeddings = data['embeddings']
    rag_model = SentenceTransformer('all-MiniLM-L6-v2') 
    print("System Ready!")
except FileNotFoundError:
    print(f"Error: Could not find {DATA_PATH}")
    exit()

# 3. Retrieval Function
def retrieve_recipes(mood_text, top_k=3):
    """
    Search for recipes in the database based on semantic similarity to the mood.
    """
    query_embedding = rag_model.encode([mood_text])
    similarities = cosine_similarity(query_embedding, recipe_embeddings)
    top_indices = similarities[0].argsort()[-top_k:][::-1]
    
    results = []
    for idx in top_indices:
        recipe = df.iloc[idx]
        results.append({
            "name": recipe['name'],
            "description": recipe['description'],
            "ingredients": recipe['ingredients'], 
            "steps": recipe['steps']
        })
    return results

# 4. Generation Function (Using Google Gemini)
def generate_mood_plan(mood_text):
    """
    Generates a full response using Google Gemini.
    """
    # A. Search the database 
    print(f"\n🔍 Searching recipes for mood: '{mood_text}'...")
    retrieved_recipes = retrieve_recipes(mood_text, top_k=2) 
    
    # Context for LLM
    recipes_context = ""
    for i, r in enumerate(retrieved_recipes):
        recipes_context += f"Recipe {i+1}: {r['name']}\nDescription: {r['description']}\nIngredients: {r['ingredients']}\n\n"

    # B. Construct Prompt for Gemini
    full_prompt = f"""
    You are 'MoodBites', an empathetic culinary therapist and chef.
    
    USER MOOD: "{mood_text}"
    
    Here are the recipes found in the database matching this mood:
    {recipes_context}
    
    Please write a response following this format:
    1. A warm, empathetic opening paragraph acknowledging the user's feelings.
    2. Introduce the suggested meals and EXPLAIN WHY they fit this specific mood (connect ingredients/textures to emotions).
    3. A combined 'Grocery List' for the suggested meals.
    4. A short 'Self-Care Tip' related to the meal.
    """

    # C. Call Google Gemini API
    try:
        print(f"🤖 Chef AI ({best_model_name}) is writing your story...")
        
        response = llm_model.generate_content(full_prompt)
        
        # Return the text
        return response.text

    except Exception as e:
        print(f"\n⚠️ API Error: {e}")
        return "Sorry, I encountered an error connecting to the Chef Brain. Please check your API Key."

# ================= Main Execution Entry =================
if __name__ == "__main__":
    user_mood = "I've had a really long, exhausting day at work and I just want to curl up with something warm."
    
    final_output = generate_mood_plan(user_mood)
    
    print("\n" + "="*50)
    print("FINAL OUTPUT FROM MOODBITES (Powered by Gemini)")
    print("="*50)
    print(final_output)