import os
import sys

sys.path.insert(0, '/home/fastermule9000/.openclaw/workspace/eleven-plus-game')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_project.settings')

import django
django.setup()

from reasoning.models import Question

def has_issues(q):
    """Check if question has problematic options."""
    opts = [str(o) for o in q.options]
    
    # Check for duplicates
    if len(set(opts)) != len(opts):
        return True, "duplicates"
    
    # Check for mismatched types (letters vs numbers)
    letters = sum(1 for o in opts if o.isalpha() and len(o) == 1)
    numbers = sum(1 for o in opts if o.isdigit())
    if letters > 0 and numbers > 0 and letters + numbers == 4:
        return True, "mixed types"
    
    # Check for empty or very short
    if any(len(o) < 1 for o in opts):
        return True, "empty"
    
    return False, "ok"

def fix_question(q, issue_type):
    """Fix a question based on its issue type."""
    question = q.question_text
    answer = q.answer.split()[0] if ' ' in q.answer else q.answer
    answer = answer.strip()
    
    if 'letter' in question.lower() or (',' in question and all(c.isalpha() or c in ', ?' for c in question.replace('Complete:', '').strip())):
        # Letter sequence - generate proper letter options
        if answer.isalpha() and len(answer) == 1:
            val = ord(answer.upper())
            opts = []
            for offset in [-2, -1, 1, 2]:
                new_val = val + offset
                if 65 <= new_val <= 90:
                    opts.append(chr(new_val))
            if answer not in opts:
                opts = opts[:3] + [answer]
            q.options = opts
            q.save()
            return True
    
    if any(x in question for x in ['cube', 'stack', 'faces']):
        # Number answer for geometry
        q.options = ['4', '6', '8', '10']
        q.save()
        return True
    
    if 'many' in question.lower() or 'count' in question.lower():
        # Counting questions
        q.options = ['3', '4', '5', '6']
        q.save()
        return True
    
    # Default: just ensure 4 unique options
    if issue_type == "duplicates":
        unique = list(dict.fromkeys([str(o) for o in q.options]))  # Remove duplicates
        while len(unique) < 4:
            unique.append(f'Option {len(unique) + 1}')
        q.options = unique[:4]
        q.save()
        return True
    
    return False

# Find and fix all problematic questions
issues_found = 0
fixed_count = 0

for q in Question.objects.all():
    has_issue, issue_type = has_issues(q)
    if has_issue:
        issues_found += 1
        if fix_question(q, issue_type):
            fixed_count += 1

print(f'Found {issues_found} questions with issues')
print(f'Fixed {fixed_count} questions')

# Verify
remaining_issues = 0
for q in Question.objects.all():
    has_issue, _ = has_issues(q)
    if has_issue:
        remaining_issues += 1
        print(f'Still bad: {q.question_text[:40]}... Options: {q.options}')

print(f'Remaining issues: {remaining_issues}')