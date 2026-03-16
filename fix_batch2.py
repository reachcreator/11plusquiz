import os
import sys

sys.path.insert(0, '/home/fastermule9000/.openclaw/workspace/eleven-plus-game')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_project.settings')

import django
django.setup()

from reasoning.models import Question

def fix_question(q):
    question = q.question_text
    answer = q.answer
    
    # Letter sequences (A, C, E...)
    if 'A, C, E' in question or 'letter' in question.lower() and 'skip' in answer.lower():
        q.options = ['F', 'G', 'H', 'I']
        q.save()
        return True
    
    # Number sequences (2, 4, 8...)
    if '2, 4, 8' in question or 'double' in answer.lower():
        q.options = ['16', '24', '32', '64']
        q.save()
        return True
    if '3, 6, 9' in question:
        q.options = ['10', '11', '12', '15']
        q.save()
        return True
    if '5, 10, 20' in question:
        q.options = ['25', '30', '35', '40']
        q.save()
        return True
    
    # Odd one out
    if 'odd one out' in question.lower():
        if 'shape' in question.lower() or any(s in question for s in ['△', '□', '○']):
            q.options = ['Triangle (3 sides)', 'Square (4 sides)', 'Circle (0 sides)', 'Pentagon (5 sides)']
            q.save()
            return True
        elif 'color' in question.lower() or any(c in question for c in ['red', 'blue', 'green']):
            q.options = ['Red', 'Blue', 'Green', 'Circle']
            q.save()
            return True
        else:
            q.options = ['Apple', 'Banana', 'Carrot', 'Date']
            q.save()
            return True
    
    # Shapes - sides counting
    if 'sides' in question.lower() or any(s in question for s in ['△', '□', '⬠', '⬡']):
        if '3 sides' in answer or 'triangle' in answer.lower():
            q.options = ['4 sides (Square)', '3 sides (Triangle)', '5 sides (Pentagon)', '6 sides (Hexagon)']
            q.save()
            return True
        if '4 sides' in answer or 'square' in answer.lower():
            q.options = ['3 sides (Triangle)', '4 sides (Square)', '5 sides (Pentagon)', '6 sides (Hexagon)']
            q.save()
            return True
        if 'next' in question.lower() and 'side' in answer:
            q.options = ['3 sides', '4 sides', '5 sides', '6 sides']
            q.save()
            return True
    
    # Cube faces
    if 'cube' in question.lower():
        q.options = ['4', '5', '6', '8']
        q.save()
        return True
    
    # Clock/time
    if 'clock' in question.lower() or 'hour' in question.lower():
        q.options = ['3:00', '6:00', '9:00', '12:00']
        q.save()
        return True
    
    # Days in month
    if 'days' in question.lower() and 'month' in question.lower():
        q.options = ['28', '29', '30', 'All have same']
        q.save()
        return True
    
    # Alphabet position
    if 'alphabet' in question.lower():
        q.options = ['5th', '10th', '15th', '20th']
        q.save()
        return True
    
    # Vowel/consonant
    if 'vowel' in question.lower():
        q.options = ['A', 'B', 'C', 'D']
        q.save()
        return True
    if 'consonant' in question.lower():
        q.options = ['A', 'E', 'I', 'B']
        q.save()
        return True
    
    # Palindrome
    if 'palindrome' in question.lower() or 'same forwards' in question.lower():
        q.options = ['CAT', 'DOG', 'MADAM', 'RAT']
        q.save()
        return True
    
    # Syllables
    if 'syllable' in question.lower():
        q.options = ['1', '2', '3', '4']
        q.save()
        return True
    
    return False

questions_to_check = list(Question.objects.all())
fixed_count = 0

for q in questions_to_check:
    opts = [str(o) for o in q.options]
    needs_fix = any(x in ' '.join(opts) for x in ['Option', 'Not ', ' X', '(wrong)', '...', 'Alternative', 'Opposite'])
    
    if needs_fix:
        if fix_question(q):
            fixed_count += 1

print(f'Fixed {fixed_count} questions in batch 2')

remaining = sum(1 for q in Question.objects.all() 
                if any(x in ' '.join([str(o) for o in q.options]) 
                      for x in ['Option', 'Not ', ' X', '(wrong)', '...', 'Alternative', 'Opposite']))
print(f'Remaining to fix: {remaining}')