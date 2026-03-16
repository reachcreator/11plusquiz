import json
import re
import sys
from pathlib import Path
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_project.settings')
sys.path.insert(0, '/home/fastermule9000/.openclaw/workspace/eleven-plus-game')
django.setup()

from reasoning.models import Question

# Read the question bank
md_file = Path('/home/fastermule9000/.openclaw/workspace/memory/11-plus-question-bank.md')
content = md_file.read_text()

questions = []
current_type = ''
current_subtype = ''
question_counter = 0

# Parse line by line
lines = content.split('\n')
i = 0
while i < len(lines):
    line = lines[i].strip()
    
    # Detect question type sections
    if line.startswith('## ') and 'REASONING' in line:
        if 'NON-VERBAL' in line:
            current_type = 'non_verbal'
        elif 'VERBAL' in line:
            current_type = 'verbal'
        elif 'SPATIAL' in line:
            current_type = 'spatial'
        elif 'MATH' in line or 'MIXED' in line:
            current_type = 'mixed'
    
    # Detect subtypes
    elif line.startswith('### Type'):
        subtype_match = re.search(r'Type \d+: (.+)', line)
        if subtype_match:
            subtype_name = subtype_match.group(1).lower().replace(' ', '_').replace('(', '').replace(')', '')
            current_subtype = subtype_name
    
    # Detect questions
    elif line.startswith('**Q') and ':' in line:
        question_counter += 1
        q_match = re.search(r'\*\*Q(\d+):\*\*\s*(.+)', line)
        if q_match:
            q_num = q_match.group(1)
            question_text = q_match.group(2).strip()
            
            # Look for answer in next few lines
            answer = ''
            explanation = ''
            j = i + 1
            while j < len(lines) and j < i + 10:
                next_line = lines[j].strip()
                if next_line.startswith('**Answer:**'):
                    answer = next_line.replace('**Answer:**', '').strip()
                elif next_line.startswith('**Explanation:**'):
                    explanation = next_line.replace('**Explanation:**', '').strip()
                elif next_line.startswith('**Q') or next_line.startswith('###'):
                    break
                j += 1
            
            # Create question object
            if question_text and answer:
                questions.append({
                    'id': f'{current_type}_{q_num}',
                    'type': current_type,
                    'subtype': current_subtype or 'general',
                    'difficulty': 'medium',
                    'question_text': question_text,
                    'options': ['A', 'B', 'C', 'D'],  # Default options
                    'answer': answer,
                    'explanation': explanation or answer,
                    'technique': f'Practice {current_subtype or current_type} patterns',
                })
    
    i += 1

# Save to database
print(f"Found {len(questions)} questions")
for q in questions[:50]:  # Import first 50 for now
    try:
        Question.objects.get_or_create(
            id=q['id'],
            defaults=q
        )
    except Exception as e:
        print(f"Error importing {q['id']}: {e}")

print(f"Imported successfully!")