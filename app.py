from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import json
import random
import os
from dotenv import load_dotenv  # for environment variables

# Load environment variables
load_dotenv()

# Configure Gemini API
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Use environment variable
    model = genai.GenerativeModel('gemini-pro')
    print("Gemini model configured successfully")
except Exception as e:
    print(f"Error configuring Gemini: {e}")
    model = None  # Fallback to mock mode

app = Flask(__name__)

# Mock quotes database (you can expand this)
QUOTES = {
    "happy": [
        "Happiness is not something ready made. It comes from your own actions. - Dalai Lama",
        "The purpose of our lives is to be happy. - Dalai Lama",
        "Happiness is a choice, not a result. Nothing will make you happy until you choose to be happy."
    ],
    "sad": [
        "The wound is the place where the Light enters you. - Rumi",
        "Tears are words that need to be written. - Paulo Coelho",
        "Every storm runs out of rain. - Maya Angelou"
    ],
    "angry": [
        "Anger is an acid that can do more harm to the vessel in which it is stored than to anything on which it is poured. - Mark Twain",
        "For every minute you remain angry, you give up sixty seconds of peace of mind. - Ralph Waldo Emerson",
        "The best fighter is never angry. - Lao Tzu"
    ],
    "anxious": [
        "You have been assigned this mountain to show others it can be moved. - Mel Robbins",
        "Anxiety is the dizziness of freedom. - Søren Kierkegaard",
        "Nothing can bring you peace but yourself. - Ralph Waldo Emerson"
    ],
    "excited": [
        "The way to get started is to quit talking and begin doing. - Walt Disney",
        "Life is what happens to you while you're busy making other plans. - John Lennon",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt"
    ],
    "calm": [
        "Peace comes from within. Do not seek it without. - Buddha",
        "In the midst of movement and chaos, keep stillness inside of you. - Deepak Chopra",
        "Calm mind brings inner strength and self-confidence. - Dalai Lama"
    ]
}

# Mock playlists (you can replace with real Spotify/YouTube embed codes)
PLAYLISTS = {
    "happy": "https://open.spotify.com/embed/playlist/37i9dQZF1DX0XUsuxWHRQd",
    "sad": "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry": "https://open.spotify.com/embed/playlist/37i9dQZF1DWXIcbzpLauPS",
    "anxious": "https://open.spotify.com/embed/playlist/37i9dQZF1DWZqd5JICZI0u",
    "excited": "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",
    "calm": "https://open.spotify.com/embed/playlist/37i9dQZF1DWU0ScTcjJBdj"
}

def analyze_mood_mock(text):
    """Mock function to simulate Gemini API response"""
    # Simple keyword-based mood detection for demo
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['happy', 'joy', 'excited', 'great', 'amazing', 'wonderful']):
        return 'happy'
    elif any(word in text_lower for word in ['sad', 'down', 'depressed', 'upset', 'hurt']):
        return 'sad'
    elif any(word in text_lower for word in ['angry', 'mad', 'furious', 'annoyed', 'irritated']):
        return 'angry'
    elif any(word in text_lower for word in ['anxious', 'worried', 'nervous', 'stressed', 'panic']):
        return 'anxious'
    elif any(word in text_lower for word in ['excited', 'thrilled', 'pumped', 'energetic']):
        return 'excited'
    elif any(word in text_lower for word in ['calm', 'peaceful', 'relaxed', 'serene']):
        return 'calm'
    else:
        return 'calm'  # default mood

def analyze_mood_gemini(text):
    """Function to analyze mood using Gemini API"""
    if model is None:
        return analyze_mood_mock(text)  # Fallback to mock if Gemini not available
        
    try:
        prompt = f"""
        Analyze the emotional tone of this text and return only one word from these options:
        happy, sad, angry, anxious, excited, calm
        
        Text: "{text}"
        
        Return only the mood word, nothing else.
        """
        
        response = model.generate_content(prompt)
        mood = response.text.strip().lower()
        
        # Validate the response
        valid_moods = ['happy', 'sad', 'angry', 'anxious', 'excited', 'calm']
        if mood not in valid_moods:
            print(f"Gemini returned invalid mood: {mood}")
            return analyze_mood_mock(text)
        
        return mood
            
    except Exception as e:
        print(f"Error analyzing mood with Gemini: {e}")
        return analyze_mood_mock(text)
            
    except Exception as e:
        print(f"Error analyzing mood with Gemini: {e}")
        return analyze_mood_mock(text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        user_text = data.get('text', '').strip()
        
        if not user_text:
            return jsonify({'error': 'Please enter some text'}), 400
        
        # Analyze mood
        mood = analyze_mood_gemini(user_text)
        
        # Get random quote for the mood
        quote = random.choice(QUOTES.get(mood, QUOTES['calm']))
        
        # Get playlist for the mood
        playlist_url = PLAYLISTS.get(mood, PLAYLISTS['calm'])
        
        return jsonify({
            'mood': mood,
            'quote': quote,
            'playlist_url': playlist_url
        })
        
    except Exception as e:
        return jsonify({'error': 'Something went wrong. Please try again.'}), 500

if __name__ == '__main__':
    app.run(debug=True)