import google.generativeai as genai
from config import GEMINI_API_KEY  # Import the key from config.py

# Configure the API key
genai.configure(api_key=GEMINI_API_KEY)

def ask_diet_bot(question):
    """Ask the diet bot a question and get a response."""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def generate_diet_plan(user_data):
    """Generate a personalized diet plan based on user data."""
    try:
        prompt = f"""
        As a nutrition expert, create a detailed diet plan for someone with these characteristics:
        
        {user_data}
        
        Please provide:
        1. Daily calorie target
        2. Macronutrient breakdown (carbs, proteins, fats)
        3. Sample meals for breakfast, lunch, dinner, and snacks
        4. Food recommendations and portions
        5. Any special considerations
        
        Format the response clearly with headers and bullet points.
        """
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating diet plan: {str(e)}"