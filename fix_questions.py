import os
import sys
import re
import random

sys.path.insert(0, '/home/fastermule9000/.openclaw/workspace/eleven-plus-game')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_project.settings')

import django
django.setup()

from reasoning.models import Question

def generate_distractors(question_text, answer, q_type):
    """Generate 3 plausible wrong answers based on question type."""
    
    # Number sequence questions
    if any(x in question_text.lower() for x in ['complete:', 'comes next', 'pattern', 'sequence']):
        if re.search(r'\d+', answer):
            num = int(re.search(r'\d+', answer).group())
            # Generate nearby numbers as distractors
            distractors = [str(num + random.choice([2, 4, 8, -2, -4])) for _ in range(3)]
            return distractors
    
    # Letter sequence
    if any(x in question_text.lower() for x in ['letter', 'alphabet']):
        if len(answer) == 1 and answer.isalpha():
            # Nearby letters
            val = ord(answer.upper())
            distractors = [chr(val + random.choice([1, 2, -1, -2])) for _ in range(3)]
            return distractors
    
    # Shape/rotation questions
    if any(x in question_text.lower() for x in ['shape', 'rotation', 'mirror', 'triangle', 'square']):
        shapes = ['△', '□', '○', '◇', '⬠', '⬡', '▲', '●']
        if answer in shapes:
            remaining = [s for s in shapes if s != answer]
            return random.sample(remaining, 3)
    
    # Odd one out
    if 'odd one out' in question_text.lower():
        return ['A', 'B', 'C']  # Generic for odd one out
    
    # Default: generate variations of the answer
    if len(answer) < 20:
        # For short answers, modify slightly
        distractors = [
            answer + ' (wrong)',
            'Not ' + answer,
            answer[::-1] if len(answer) > 2 else 'X' + answer
        ]
        return distractors
    
    return ['Option A', 'Option B', 'Option C']

# Fix questions with bad options
questions_to_fix = Question.objects.filter(options=['A', 'B', 'C', 'D'])
total = questions_to_fix.count()
print(f'Fixing {total} questions...')

fixed_count = 0
for q in questions_to_fix:
    try:
        distractors = generate_distractors(q.question_text, q.answer, q.type)
        
        # Create options list with answer in random position
        all_options = distractors + [q.answer]
        random.shuffle(all_options)
        
        q.options = all_options
        q.save()
        fixed_count += 1
        
        if fixed_count % 10 == 0:
            print(f'Fixed {fixed_count}/{total}...')
            
    except Exception as e:
        print(f'Error fixing {q.id}: {e}')

print(f'Fixed {fixed_count} questions!')

# Show sample
sample = Question.objects.exclude(options=['A', 'B', 'C', 'D']).first()
if sample:
    print(f'\\nSample fixed:')
    print(f'Q: {sample.question_text[:50]}...')
    print(f'Options: {sample.options}')
    print(f'Answer: {sample.answer}')