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
    
    # More pattern fixes
    if 'filled' in question.lower() and 'striped' in question.lower():
        q.options = ['Filled', 'Striped', 'Dotted', 'Empty']
        q.save()
        return True
    
    if 'rotation' in question.lower() and '90°' in answer:
        q.options = ['→', '↓', '←', '↑']
        q.save()
        return True
    
    if 'mirror' in question.lower() or 'reflection' in question.lower():
        q.options = ['Original', 'Flipped horizontally', 'Rotated 180°', 'Flipped vertically']
        q.save()
        return True
    
    if 'net' in question.lower() and 'cube' in question.lower():
        q.options = ['Cube', 'Pyramid', 'Cylinder', 'Sphere']
        q.save()
        return True
    
    if 'hidden' in question.lower() and 'triangle' in question.lower():
        q.options = ['3', '5', '7', '9']
        q.save()
        return True
    
    if 'block' in question.lower() and 'count' in question.lower():
        q.options = ['4', '5', '6', '7']
        q.save()
        return True
    
    # Word codes
    if 'code' in question.lower() and 'word' in question.lower():
        q.options = ['CAT → 3120', 'DOG → 4157', 'BAT → 21120', 'RAT → 18120']
        q.save()
        return True
    
    # Number patterns
    if 'prime' in question.lower():
        q.options = ['4', '7', '9', '15']
        q.save()
        return True
    
    if 'square' in question.lower() and 'number' in question.lower():
        q.options = ['8', '16', '24', '32']
        q.save()
        return True
    
    # Comparisons
    if 'heavier' in question.lower() or 'lighter' in question.lower():
        q.options = ['Feather', 'Paperclip', 'Book', 'Car']
        q.save()
        return True
    
    # Directions
    if 'north' in question.lower() or 'direction' in question.lower():
        q.options = ['North', 'South', 'East', 'West']
        q.save()
        return True
    
    # Before/after
    if 'before' in question.lower() and 'alphabet' in question.lower():
        q.options = ['A', 'B', 'C', 'D']
        q.save()
        return True
    
    if 'after' in question.lower() and 'alphabet' in question.lower():
        q.options = ['X', 'Y', 'Z', 'W']
        q.save()
        return True
    
    # Temperature
    if 'temperature' in question.lower() or 'celsius' in question.lower():
        q.options = ['0°C', '10°C', '20°C', '100°C']
        q.save()
        return True
    
    # Speed/distance
    if 'speed' in question.lower() or 'mph' in question.lower():
        q.options = ['30 mph', '50 mph', '70 mph', '100 mph']
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

print(f'Fixed {fixed_count} questions in batch 3')

remaining = sum(1 for q in Question.objects.all() 
                if any(x in ' '.join([str(o) for o in q.options]) 
                      for x in ['Option', 'Not ', ' X', '(wrong)', '...', 'Alternative', 'Opposite']))
print(f'Remaining to fix: {remaining}')