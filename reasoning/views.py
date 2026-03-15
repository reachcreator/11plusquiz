from django.shortcuts import render
from django.http import JsonResponse
from .models import Question
import random

def home(request):
    """Home page with game selection."""
    return render(request, 'reasoning/home.html')

def game(request, mode='cem_simulator'):
    """Main game view."""
    # Get random questions based on mode
    if mode == 'cem_simulator':
        # Mixed questions like real CEM
        questions = list(Question.objects.all().order_by('?')[:10])
    elif mode == 'non_verbal':
        questions = list(Question.objects.filter(type='non_verbal').order_by('?')[:10])
    elif mode == 'verbal':
        questions = list(Question.objects.filter(type='verbal').order_by('?')[:10])
    elif mode == 'spatial':
        questions = list(Question.objects.filter(type='spatial').order_by('?')[:10])
    else:
        questions = list(Question.objects.all().order_by('?')[:10])
    
    return render(request, 'reasoning/game.html', {
        'questions': questions,
        'mode': mode,
    })

def check_answer(request):
    """AJAX endpoint to check answer."""
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        user_answer = request.POST.get('answer')
        
        try:
            question = Question.objects.get(id=question_id)
            correct = user_answer == question.answer
            
            return JsonResponse({
                'correct': correct,
                'correct_answer': question.answer,
                'explanation': question.explanation,
                'technique': question.technique,
            })
        except Question.DoesNotExist:
            return JsonResponse({'error': 'Question not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)