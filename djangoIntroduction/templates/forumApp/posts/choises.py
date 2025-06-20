from django.db import models

class LanguageChoices(models.TextChoices):
    PYTHON = 'py', 'Python'
    PHP = 'php', 'PHP'
    JAVA = 'Java', 'Java'
    JAVA_SCRYPT = 'js', 'JavaScript'
    C_SHARP = 'C#', 'C#'
    C_PLUS_PLUS = 'C++', 'C++'
    RUBY = 'R', 'Ruby'
    OTHER = 'other', 'Other'
