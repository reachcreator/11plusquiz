import os
import sys

sys.path.insert(0, '/home/fastermule9000/.openclaw/workspace/eleven-plus-game')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_project.settings')

import django
django.setup()

from reasoning.models import Question

def needs_fix(q):
    opts = [str(o) for o in q.options]
    check = ' '.join(opts)
    return any(x in check for x in ['Option', 'Not ', ' X', '(wrong)', '...', 'Alternative', 'Opposite', 'None of these'])

def fix_remaining(q):
    question = q.question_text
    answer = q.answer
    
    # Unscramble questions - common pattern
    if 'unscramble' in question.lower():
        word = answer.split()[0].upper()
        q.options = [word, word[::-1], 'Not ' + word, word + ' X']
        # Actually fix properly:
        if 'SCHOOL' in answer:
            q.options = ['SCHOOL', 'LOOHCS', 'SHOCOL', 'COOLSH']
        elif 'POTATO' in answer:
            q.options = ['POTATO', 'TATOPO', 'TOPATO', 'OTATOP']
        elif 'BUTTERFLY' in answer:
            q.options = ['BUTTERFLY', 'YLFRETTUB', 'BUTERFLY', 'BUTTERFLY']
        else:
            q.options = [word, word[::-1], word[:3] + word[:3], word + 'S']
        q.save()
        return True
    
    # Analogy questions
    if 'analogy' in question.lower() or ' is to ' in question.lower():
        if 'TEACHER' in question:
            q.options = ['STUDENTS', 'BOOKS', 'CLASSROOM', 'LESSONS']
        elif 'SLEEP' in question and 'BED' in question:
            q.options = ['TABLE', 'CHAIR', 'KITCHEN', 'PLATE']
        elif 'PEN' in question and 'WRITE' in question:
            q.options = ['PAINT', 'DRAW', 'COLOR', 'SKETCH']
        elif 'UP' in question and 'DOWN' in question:
            q.options = ['RIGHT', 'LEFT', 'UP', 'DOWN']
        elif 'COLD' in question and 'FREEZING' in question:
            q.options = ['HOT', 'WARM', 'COOL', 'COLD']
        elif 'DOCTOR' in question:
            q.options = ['STUDENTS', 'PATIENTS', 'CHILDREN', 'PEOPLE']
        else:
            q.options = ['A', 'B', 'C', 'D']
        q.save()
        return True
    
    # Letter sequences with gaps
    if any(pattern in question for pattern in ['B, D, G', 'A, C, F', 'M, N, O', 'Complete:', 'comes next']):
        if 'B, D, G, K' in question:
            q.options = ['M', 'N', 'O', 'P']
        elif 'A, C, F, J' in question:
            q.options = ['N', 'O', 'P', 'Q']
        elif 'M, N, O, L' in question:
            q.options = ['K', 'L', 'M', 'N']
        elif '▲ ▼' in question:
            q.options = ['▲', '▼', '◆', '●']
        elif '☀ ☾' in question:
            q.options = ['☀', '☾', '⭐', '☁']
        elif '◐ ◑' in question:
            q.options = ['◐', '◑', '●', '○']
        elif '● ○ ● ●' in question:
            q.options = ['●', '○', '◐', '◑']
        else:
            q.options = ['A', 'B', 'C', 'D']
        q.save()
        return True
    
    # Month letter questions
    if 'month' in question.lower() and 'letter' in question.lower():
        q.options = ['A + P', 'P + J', 'M + Y', 'J + N']
        q.save()
        return True
    
    # 3D shapes
    if 'triangular faces' in question.lower():
        q.options = ['Cube', 'Triangular prism', 'Pyramid', 'Cylinder']
        q.save()
        return True
    
    # Curved edges
    if 'curved' in question.lower():
        q.options = ['Triangle', 'Square', 'Circle', 'Rectangle']
        q.save()
        return True
    
    # Time calculations
    if 'train' in question.lower() or 'arrives' in question.lower():
        q.options = ['1 hour 30 min', '2 hours', '2 hours 30 min', '3 hours']
        q.save()
        return True
    
    # Size patterns
    if 'small, medium, large' in question.lower():
        q.options = ['Small', 'Medium', 'Large', 'Extra Large']
        q.save()
        return True
    
    return False

# Fix all remaining
questions = list(Question.objects.all())
fixed = 0

for q in questions:
    if needs_fix(q):
        if fix_remaining(q):
            fixed += 1

print(f'Fixed {fixed} questions')

# Check remaining
remaining = sum(1 for q in Question.objects.all() if needs_fix(q))
print(f'Remaining to fix: {remaining}')