"""Module for the Sentiment Analyzer Flask application."""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Sentiment Analyzer")

@app.route('/emotionDetector')
def emotion_detector_view():
    """Analyze the emotion of the given text input."""
    text_input = request.args.get('textToAnalyze')

    if not text_input:
        empty_emotions = {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
        return str(empty_emotions) + "\nEmpty! Please enter a Text"

    emotions = emotion_detector(text_input)

    if emotions['dominant_emotion'] is None:
        return "Invalid text! Please try again!", 400

    response = (
        f"For the given statement, the system response is "
        f"'anger': {emotions['anger']}, 'disgust': {emotions['disgust']}, "
        f"'fear': {emotions['fear']}, 'joy': {emotions['joy']}, "
        f"'sadness': {emotions['sadness']}. "
        f"The dominant emotion is {emotions['dominant_emotion']}."
    )
    return response, 200

@app.route('/')
def emotion_render():
    """Render the homepage."""
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
