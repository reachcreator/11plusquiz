import os
import sys
import random

sys.path.insert(0, '/home/fastermule9000/.openclaw/workspace/eleven-plus-game')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_project.settings')

import django
django.setup()

from reasoning.models import Question

# Manual fixes for specific question patterns
def fix_question(q):
    question = q.question_text
    answer = q.answer
    
    # 1. Analogy questions: X is to Y as A is to B
    if 'is to' in question.lower() and 'as' in question.lower():
        if 'FISH' in question and 'WATER' in question:
            q.options = ['SKY', 'TREE', 'AIR', 'GROUND']
            q.save()
            return True
        elif 'HAND' in question and 'FINGER' in question:
            q.options = ['LEG', 'TOE', 'ARM', 'HEEL']
            q.save()
            return True
        elif 'KNIFE' in question and 'CUT' in question:
            q.options = ['BUILD', 'PAINT', 'NAIL', 'HIT']
            q.save()
            return True
        elif '2 is to 4' in question or '3 is to' in question:
            q.options = ['SIXTH', 'SEVENTH', 'THIRD', 'FIFTH']
            q.save()
            return True
    
    # 2. Unscramble questions
    if 'unscramble' in question.lower():
        if 'TCA' in question:
            q.options = ['TAC', 'CTA', 'CAT or ACT', 'ATC']
            q.save()
            return True
    
    # 3. Letter/number code questions
    if 'A=26' in question or 'A=1' in question:
        if 'ZA' in question or 'Z+A' in question:
            q.options = ['26+1 = 27', '1-26', '26-1 = 25', '1+26']
            q.save()
            return True
        elif 'Z-A' in question:
            q.options = ['26-1 = 25', '1-26', '26+1 = 27', '1+26']
            q.save()
            return True
    
    # 4. Month questions
    if 'month' in question.lower():
        if 'March' in question or 'M + Y' in answer:
            q.options = ['J + E', 'M + H', 'A + R', 'M + Y']
            q.save()
            return True
        elif 'longest month' in question.lower():
            q.options = ['February', 'April', 'June', 'All equal']
            q.save()
            return True
    
    # 5. Which is longest/biggest
    if 'longest' in question.lower() or 'biggest' in question.lower():
        if 'Ant' in question:
            q.options = ['A) Ant', 'B) Elephant', 'C) Mouse', 'D) Whale']
            q.save()
            return True
    
    # 6. Math questions
    if any(x in question for x in ['0.1', '0.2', '0.3']):
        q.options = ['0.5', '0.6', '0.9', '1.0']
        q.save()
        return True
    if 'sphere' in question.lower() and 'cut' in question.lower():
        q.options = ['Square', 'Triangle', 'Circle', 'Oval']
        q.save()
        return True
    
    # 7. Pattern/sequence with shapes
    if '☆ ★' in question or 'star' in question.lower():
        q.options = ['☆', '★', '◆', '○']
        q.save()
        return True
    
    # 8. Fill in missing word
    if 'missing word' in question.lower() or 'complete the sentence' in question.lower():
        if 'hot' in question.lower() or 'sun' in question.lower():
            q.options = ['COLD', 'WET', 'DARK', 'HOT']
            q.save()
            return True
    
    # 9. Antonym questions
    if 'opposite' in question.lower() or 'antonym' in question.lower():
        if 'happy' in question.lower():
            q.options = ['JOYFUL', 'EXCITED', 'SAD', 'ANGRY']
            q.save()
            return True
    
    # 10. Rotation/mirror
    if 'mirror' in question.lower():
        q.options = ['Same', 'Flipped left-right', 'Rotated 90°', 'Inverted colors']
        q.save()
        return True
    if 'rotation' in question.lower() or 'rotates' in question.lower():
        q.options = ['45° clockwise', '90° clockwise', '180° flip', '45° counter-clockwise']
        q.save()
        return True
    
    return False

# Get questions that still need fixing
questions_to_check = list(Question.objects.all())
fixed_count = 0

for q in questions_to_check:
    opts = [str(o) for o in q.options]
    needs_fix = any(x in ' '.join(opts) for x in ['Option', 'Not ', ' X', '(wrong)', '...', 'Alternative', 'Opposite'])
    
    if needs_fix:
        if fix_question(q):
            fixed_count += 1

print(f'Fixed {fixed_count} questions in this batch')

# Count remaining
remaining = 0
for q in Question.objects.all():
    opts = [str(o) for o in q.options]
    if any(x in ' '.join(opts) for x in ['Option', 'Not ', ' X', '(wrong)', '...', 'Alternative', 'Opposite']):
        remaining += 1

print(f'Remaining to fix: {remaining}')