from django import forms
from django.db import models
from car.models import Car

FUEL_CHOICES = [
    ('бензин', 'Бензин'),    
    ('дизель', 'Дизель'),    
    ('гибрид', 'Гибрид'),    
    ('electric', 'Электро'),
    ]

TRANSMISSION_CHOICES = [
    ('передний', 'Передний'),
    ('задний', 'Задний'),
    ('полный', 'Полный'),
    ]

GEARBOX_CHOICES = [
    ('механика', 'Механическая'),
    ('автомат', 'Автоматическая'),
    ('вариатор', 'Вариатор'),
    ('робот', 'Роботизированная'),
    ]

brand_choices = Car.objects.order_by('brand').values_list('brand', flat=True).distinct()
brand_choices = [choice for choice in brand_choices if not choice.lower().startswith('car')]

class CarForm(forms.ModelForm):
    brand = forms.ChoiceField(choices=[(brand, brand) for brand in brand_choices], label='Марка авто')
    model = forms.ChoiceField(choices=[], label='Модель авто' )
    year = forms.IntegerField(label='Год выпуска', max_value=2023)
    engine_capacity = forms.DecimalField(label='Объем двигателя, л.')
    horses = forms.IntegerField(label='Мощность, л.с.')
    fuel = forms.ChoiceField(choices=FUEL_CHOICES, label='Тип топлива')
    transmission = forms.ChoiceField(choices=TRANSMISSION_CHOICES, label='Привод')
    gearbox = forms.ChoiceField(choices=GEARBOX_CHOICES, label='Коробка передач')
    distance = forms.DecimalField(label='Пробег, км')
    repair = forms.BooleanField(required=False, label='Не на ходу или требует ремонта')
    docs_problems = forms.BooleanField(required=False, label='Нет документов')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].choices = [(model, model) for model in Car.objects.order_by('model').values_list('model', flat=True).distinct()]

    class Meta:
        model = Car
        fields = [
            'brand',
            'model',
            'year',
            'engine_capacity',
            'horses',
            'fuel',
            'transmission',
            'gearbox',
            'distance',
            'repair',
            'docs_problems',
        ]

