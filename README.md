🎧 MoodBites — A Mood-Based Recipe Recommendation System

A Retrieval-Augmented, Emotion-Aware Meal Planner powered by SentenceTransformers & Google Gemini.

🌟 Overview

MoodBites is an NLP-powered system that recommends recipes based on how the user feels, not just what they want to eat.
By combining Semantic Search with LLM-driven storytelling, MoodBites delivers emotionally aligned meals grounded in real recipes.

✨ Key Features

Mood Understanding: Interprets natural-language emotions (e.g., “exhausted,” “overwhelmed,” “energized”).

RAG Retrieval: Pulls real recipes from a 5,000-recipe vector database instead of hallucinating.

Empathetic Narrative Generation: Uses Gemini 1.5 Flash to craft warm, supportive explanations.

One-Click Grocery List: Automatically generates a combined shopping list.

Fast & Lightweight: Semantic retrieval takes <0.5 seconds.

🧠 System Architecture
User Mood Input
        ↓
Text Embedding (all-MiniLM-L6-v2)
        ↓
Semantic Retrieval (Cosine Similarity, Top-K)
        ↓
LLM Generation (Gemini 1.5 Flash + RAG)
        ↓
Final Output: Recipe + Story + Grocery List + Self-Care Tip


To include the image version:

![Architecture](moodbites_architecture.png)

🏗️ Pipeline Components
1. Data & Embeddings

Source: Food.com Dataset

Processed ~5,000 high-quality recipes

Combined text: name + description + tags

Embedded using SentenceTransformers (MiniLM)

2. Semantic Retrieval

Compute cosine similarity between mood embedding and recipe embeddings

Return Top-3 semantically closest recipes

Ensures mood-consistent results (e.g., “warm” → soups, stews)

3. LLM Generation

Model: Gemini 1.5 Flash

Persona: “Empathetic culinary therapist”

Output:

Emotional reflection

Recipe explanations

Grocery list

Self-care suggestion

4. Interface

Streamlit app with a simple text box

Returns narrative + recipes in Markdown

🧪 Demo Inputs
🌧 Comfort Mood

I’ve had a really exhausting day and want something warm.
→ Potato soup, chicken stew, warm desserts.

🌞 Energetic Mood

I’m feeling energized and want something fresh and healthy.
→ Citrus salad, cucumber bowls.

📦 Installation
1. Clone
git clone https://github.com/yourusername/MoodBites.git
cd MoodBites

2. Install Requirements
pip install -r requirements.txt

3. Add Gemini API Key

In agent_logic_google.py:

MY_GOOGLE_KEY = "YOUR_GEMINI_KEY"

4. Run App
streamlit run app.py

📁 Project Structure
MoodBites/
├── app.py
├── agent_logic_google.py
├── recipe_data_with_embeddings.pkl
└── readme

🚧 Limitations

Western-biased recipe dataset

No long-term user preference memory

Minor LLM embellishments possible

Embeddings capture semantics, not flavor/texture

🔮 Future Work

Multi-modal input: fridge photos → recipe matching

Persistent taste profiles

Thumbs-up/down feedback loop (RLHF)

Larger, more diverse recipe datasets