import re
import sys
import random
from pathlib import Path

sys.path.insert(0, '/home/fastermule9000/.openclaw/workspace/eleven-plus-game')
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_project.settings')

import django
django.setup()

from reasoning.models import Question

def generate_options(question_text, answer):
    """Generate 3 distractors + correct answer in random order."""
    distractors = []
    
    # Number patterns
    nums = re.findall(r'\d+', answer)
    if nums:
        num = int(nums[0])
        distractors = [str(num + i) for i in [2, 4, -2] if num + i > 0]
    
    # Single letters
    if len(answer) == 1 and answer.isalpha():
        val = ord(answer.upper())
        distractors = [chr(val + i) for i in [1, 2, -1] if 65 <= val + i <= 90]
    
    # Shapes
    shapes = ['△', '□', '○', '◇', '⬠', '⬡', '▲', '●', '⭐']
    if answer in shapes:
        remaining = [s for s in shapes if s != answer]
        distractors = random.sample(remaining, min(3, len(remaining)))
    
    # Words/phrases - create variations
    if len(distractors) < 3:
        if 'odd one out' in question_text.lower():
            distractors = ['B', 'C', 'D']
        elif 'mirror' in question_text.lower() or 'rotation' in question_text.lower():
            directions = ['→', '←', '↑', '↓', '↗', '↘', '↙', '↖']
            if answer in directions:
                remaining = [d for d in directions if d != answer]
                distractors = random.sample(remaining, 3)
            else:
                distractors = ['Flipped left', 'Flipped right', 'Rotated 90°']
        else:
            # Generic distractors based on answer
            if len(answer) < 20:
                distractors = [
                    answer + ' X',
                    'Not ' + answer,
                    answer[::-1] if len(answer) > 2 else 'Option X'
                ]
    
    # Ensure we have exactly 3 distractors
    while len(distractors) < 3:
        distractors.append(f'Option {chr(65 + len(distractors))}')
    
    # Combine and shuffle
    all_options = distractors[:3] + [answer]
    random.shuffle(all_options)
    
    return all_options

# Parse and import all questions from markdown
md_file = Path('/home/fastermule9000/.openclaw/workspace/memory/11-plus-question-bank.md')
content = md_file.read_text()

lines = content.split('\n')
questions = []
current_type = 'mixed'
current_subtype = 'general'

i = 0
while i < len(lines):
    line = lines[i].strip()
    
    # Detect sections
    if line.startswith('## '):
        if 'NON-VERBAL' in line:
            current_type = 'non_verbal'
        elif 'VERBAL' in line:
            current_type = 'verbal'
        elif 'SPATIAL' in line:
            current_type = 'spatial'
        elif 'MATH' in line or 'MIXED' in line:
            current_type = 'mixed'
    
    # Detect subtypes
    if line.startswith('### Type'):
        match = re.search(r'Type \d+: (.+)', line)
        if match:
            current_subtype = match.group(1).lower().replace(' ', '_').replace('(', '').replace(')', '')
    
    # Find questions
    if line.startswith('**Q') and ':' in line:
        match = re.search(r'\*\*Q(\d+):\*\*\s*(.+)', line)
        if match:
            q_num = match.group(1)
            q_text = match.group(2).strip()
            
            # Look for answer
            answer = ''
            explanation = ''
            j = i + 1
            while j < len(lines) and j < i + 15:
                next_line = lines[j].strip()
                if next_line.startswith('**Answer:**'):
                    answer = next_line.replace('**Answer:**', '').strip()
                elif next_line.startswith('**Explanation:**'):
                    explanation = next_line.replace('**Explanation:**', '').strip()
                elif next_line.startswith('**Q') or next_line.startswith('###'):
                    break
                j += 1
            
            if q_text and answer and len(answer) < 200:
                q_id = f'{current_type}_{q_num}'
                
                # Skip if already exists
                if not Question.objects.filter(id=q_id).exists():
                    options = generate_options(q_text, answer)
                    
                    questions.append({
                        'id': q_id,
                        'type': current_type,
                        'subtype': current_subtype,
                        'difficulty': random.choice(['easy', 'medium', 'hard']),
                        'question_text': q_text,
                        'options': options,
                        'answer': answer,
                        'explanation': explanation or answer,
                        'technique': f'Practice {current_subtype} patterns',
                    })
    
    i += 1

# Bulk create
print(f'Found {len(questions)} new questions to import')

imported = 0
for q_data in questions:
    try:
        Question.objects.create(**q_data)
        imported += 1
        if imported % 50 == 0:
            print(f'Imported {imported}...')
    except Exception as e:
        print(f'Error importing {q_data["id"]}: {e}')

print(f'Imported {imported} new questions!')
print(f'Total in database: {Question.objects.count()}')