from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
sentiment_analyzer = SentimentIntensityAnalyzer()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

class SentimentAnalysisForm(FlaskForm):
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Analyze')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SentimentAnalysisForm()
    messages = []

    if form.validate_on_submit():
        user_input = form.message.data
        messages.append(('user', user_input))

        sentiment_scores = sentiment_analyzer.polarity_scores(user_input)
        compound_score = sentiment_scores['compound']

        if compound_score >= 0.05:
            sentiment = 'Positive'
        elif compound_score <= -0.05:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'

        bot_response = f'Sentiment: {sentiment}'
        messages.append(('bot', bot_response))

    return render_template('index.html', form=form, messages=messages)

if __name__ == '__main__':
    app.run()
