from django.core.management.base import BaseCommand
from reasoning.models import Question
import re

class Command(BaseCommand):
    help = 'Import 11+ questions from research file'

    def handle(self, *args, **options):
        # I'll create a simpler seed with some sample questions first
        # Then we can expand
        
        sample_questions = [
            {
                'id': 'nvr_seq_1',
                'type': 'non_verbal',
                'subtype': 'sequence',
                'difficulty': 'easy',
                'question': 'What comes next: △ □ ⬠ ?',
                'options': ['⬡', '○', '△', '□'],
                'answer': '⬡',
                'explanation': 'Sides increase by 1: 3, 4, 5, so next is 6 (hexagon)',
                'technique': 'Count sides and look for progression',
            },
            {
                'id': 'vr_letter_1',
                'type': 'verbal',
                'subtype': 'letter_series',
                'difficulty': 'easy',
                'question': 'Complete: A, C, E, G, ?',
                'options': ['H', 'I', 'J', 'K'],
                'answer': 'I',
                'explanation': 'Skip 1 letter: A_C_E_G_I',
                'technique': 'Write alphabet and mark positions',
            },
            {
                'id': 'vr_number_1',
                'type': 'verbal',
                'subtype': 'number_pattern',
                'difficulty': 'easy',
                'question': 'Complete: 2, 4, 8, 16, ?',
                'options': ['24', '32', '30', '20'],
                'answer': '32',
                'explanation': 'Multiply by 2 each time',
                'technique': 'Check multiplication patterns',
            },
        ]
        
        for q_data in sample_questions:
            Question.objects.get_or_create(
                id=q_data['id'],
                defaults=q_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'Imported {len(sample_questions)} sample questions'))