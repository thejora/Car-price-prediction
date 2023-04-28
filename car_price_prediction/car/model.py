import pandas as pd
from lightgbm import LGBMRegressor
import psycopg2
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings("ignore")

# Создаем коннект с бд
conn_string = "host='localhost' dbname='postgres' user='postgres' password='example'"
conn = psycopg2.connect(conn_string)
engine = create_engine('postgresql://postgres:example@localhost:5432/postgres')
# Выгружаем таблицу
cars = pd.read_sql_query('select * from car_car', con=engine, index_col='index')
target = cars['price']
features = cars.drop(['price','id',], axis=1, errors='ignore')

cat_features = ['brand', 'model','transmission','gearbox','fuel']
features[cat_features] = features[cat_features].astype('category')

# Обучаем модель по определенным в тетрадке параметрам
lgb = LGBMRegressor(n_estimators= 940, 
                           learning_rate=0.038, 
                           max_depth=150,
                           random_state=42)
lgb.fit(features, target)