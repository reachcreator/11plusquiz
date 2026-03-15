from django.db import models

class Question(models.Model):
    QUESTION_TYPES = [
        ('non_verbal', 'Non-Verbal Reasoning'),
        ('verbal', 'Verbal Reasoning'),
        ('spatial', 'Spatial Reasoning'),
        ('mixed', 'Mixed'),
    ]
    
    SUBTYPES = [
        ('sequence', 'Sequence'),
        ('rotation', 'Rotation'),
        ('odd_one_out', 'Odd One Out'),
        ('mirror', 'Mirror/Reflection'),
        ('hidden_shapes', 'Hidden Shapes'),
        ('letter_series', 'Letter Series'),
        ('word_code', 'Word Code'),
        ('number_pattern', 'Number Pattern'),
        ('letter_number', 'Letter-Number Code'),
        ('cube_faces', 'Cube Faces'),
        ('nets', 'Nets'),
        ('rotation_3d', '3D Rotation'),
        ('block_counting', 'Block Counting'),
    ]
    
    DIFFICULTIES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    id = models.CharField(max_length=50, primary_key=True)
    type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    subtype = models.CharField(max_length=30, choices=SUBTYPES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTIES)
    question_text = models.TextField()
    options = models.JSONField(default=list)
    answer = models.CharField(max_length=200)
    explanation = models.TextField()
    technique = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id}: {self.question_text[:50]}"
    
    class Meta:
        ordering = ['type', 'difficulty', 'id']