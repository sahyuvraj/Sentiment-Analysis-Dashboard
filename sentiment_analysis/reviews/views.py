from django.shortcuts import render, redirect
from .forms import ReviewForm
from textblob import TextBlob
import cv2
from .models import Review

def analyze_sentiment(content):
    blob = TextBlob(content)
    sentiments = {str(sentence): sentence.sentiment.polarity for sentence in blob.sentences}
    return sentiments

def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            sentiments = analyze_sentiment(form.cleaned_data['content'])
            review.sentiment = 'Positive' if all(val > 0 for val in sentiments.values()) else 'Negative'
            review.save()
            return redirect('review_list')
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form})

def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def process_image(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('media/processed_image.jpg', gray_image)
