import os
import sys
import random

sys.path.insert(0, '/home/fastermule9000/.openclaw/workspace/eleven-plus-game')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_project.settings')

import django
django.setup()

from reasoning.models import Question

def generate_better_distractors(q):
    """Generate proper distractors based on question type and answer."""
    question = q.question_text
    answer = q.answer
    
    # Pattern: A, AA, AAA... (letter sequences)
    if 'A, AA, AAA' in question or 'letter' in question.lower():
        if 'AAAAA' in answer or 'increasing count' in answer:
            return ['AAAA (stays at 4)', 'AAAAAA (jumps to 6)', 'A (back to 1)']
        if len(answer) == 1 and answer.isalpha():
            next_letter = chr(ord(answer.upper()) + 1) if ord(answer.upper()) < 90 else 'A'
            prev_letter = chr(ord(answer.upper()) - 1) if ord(answer.upper()) > 65 else 'Z'
            return [next_letter, prev_letter, answer + answer]
    
    # Pattern: filled, striped, dotted
    if 'filled' in question.lower() and 'striped' in question.lower():
        return ['Filled (repeats)', 'Striped (repeats)', 'Solid (new pattern)']
    
    # Number sequences
    if any(x in question.lower() for x in ['complete', 'comes next', 'pattern']) and any(c.isdigit() for c in answer):
        nums = [int(n) for n in answer.split() if n.isdigit()]
        if nums:
            num = nums[0]
            return [str(num + 2), str(num - 2), str(num * 2)]
    
    # Odd one out
    if 'odd one out' in question.lower():
        return ['A (similar to B)', 'B (matches pattern)', 'C (alternative fit)']
    
    # Mirror/reflection
    if 'mirror' in question.lower():
        return ['Same direction', 'Rotated 90°', 'Flipped vertically']
    
    # Rotation
    if 'rotation' in question.lower() or 'rotates' in question.lower():
        return ['45° clockwise', '90° counter-clockwise', '180° flip']
    
    # Shapes
    shapes = ['△', '□', '○', '◇', '⬠', '⬡', '▲', '●', '⭐', '♦']
    if any(s in answer for s in shapes):
        remaining = [s for s in shapes if s not in answer]
        return random.sample(remaining, min(3, len(remaining)))
    
    # Word patterns
    if 'word' in question.lower() or 'missing word' in question.lower():
        return ['Synonym', 'Antonym', 'Related word']
    
    # Generic but better than "Option X"
    return [
        f'Alternative: {answer[:3]}...' if len(answer) > 5 else f'Not {answer}',
        f'Opposite of {answer[:5]}' if len(answer) > 5 else 'Different pattern',
        'None of these'
    ]

# Fix all questions with generic options
fixed_count = 0
for q in Question.objects.all():
    needs_fix = any('Option' in str(opt) for opt in q.options)
    
    if needs_fix:
        distractors = generate_better_distractors(q)
        
        # Ensure answer is included
        all_options = distractors[:3] + [q.answer]
        random.shuffle(all_options)
        
        q.options = all_options
        q.save()
        fixed_count += 1
        
        if fixed_count % 20 == 0:
            print(f'Fixed {fixed_count}...')

print(f'Fixed {fixed_count} questions!')

# Verify
remaining_bad = sum(1 for q in Question.objects.all() if any('Option' in str(opt) for opt in q.options))
print(f'Remaining bad questions: {remaining_bad}')