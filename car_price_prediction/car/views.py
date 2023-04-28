from django.shortcuts import render
from .forms import CarForm
from .models import Car
from car.model import lgb
import pandas as pd
from django.http import JsonResponse
from django.db.models import Q

def get_brands(request):
    term = request.GET.get('term')
    brands = Car.objects.filter(Q(brand__istartswith=term)).values_list('brand', flat=True).distinct()
    response = [{'label': brand, 'value': brand} for brand in brands]
    return JsonResponse(response, safe=False)

def predict_price(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = Car()
            car.brand = form.cleaned_data['brand']
            car.model = form.cleaned_data['model']
            car.year = form.cleaned_data['year']
            car.engine_capacity = form.cleaned_data['engine_capacity']
            car.horses = form.cleaned_data['horses']
            car.fuel = form.cleaned_data['fuel']
            car.transmission = form.cleaned_data['transmission']
            car.gearbox = form.cleaned_data['gearbox']
            car.distance = form.cleaned_data['distance']
            car.repair = int(form.cleaned_data.get('repair', 0))  # если не выбрано, будет 0
            car.docs_problems = int(form.cleaned_data.get('docs_problems', 0))  # если не выбрано, будет 0
            #car.save()    # если потребуется вносить предсказания в базу, раскомментить

        
            features = (
                pd.DataFrame([[str(car.brand), str(car.model), int(car.year),  
                               float(car.engine_capacity), int(car.horses), str(car.fuel),
                               str(car.gearbox), str(car.transmission), int(car.distance),
                               int(car.repair), int(car.docs_problems)]], 
                             columns=[['brand', 'model', 'year', 'engine_capacity', 
                                        'horses','fuel', 'gearbox', 'transmission', 
                                        'distance', 'repair', 'docs_problems']])
            )

            cat_features = ['brand', 'model','fuel', 'gearbox', 'transmission']

            features[cat_features] = features[cat_features].astype('category')

            car.price = '{0:,}'.format(round(int(lgb.predict(features)))).replace(',', ' ')
            car.save()

            return render(request, 'car/result.html', {'price': car.price})
    else:
        form = CarForm()
        
    return render(request, 'car/predict.html', {'form': form})



def get_models(request):
    brand_id = request.GET.get('brand')
    print('Brand ID:', brand_id)  # отладочная информация
    models = Car.objects.filter(brand=brand_id).order_by('model').distinct('model').values_list('model', flat=True)
    print('Models:', models)  # отладочная информация
    data = {'models': list(models)}
    return JsonResponse(data)
