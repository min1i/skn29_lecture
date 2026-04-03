import pandas as pd
import numpy as np
import os


def run_preprocessing_pipeline(file_path):
    '''file_path : csv 파일명'''
    
    # 1. 데이터 로드
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeEncodeError as e:
        df = pd.read_csv(file_path, encoding='cp949')

    # 2. 결측치 처리 (대치)
    # name, salary : 중앙값으로 대치
    df['age'] = df['age'].fillna(df['age'].median())
    df['salary'] = df['salary'].fillna(df['salary'].median())
    
    # score : 선형보간 하고 양끝에 남은 nan은 얖뒤 값으로 대치
    df['score'] = df['score'].interpolate(method='linear')
    df['score'] = df['score'].bfill().ffill()

    # 3. 이상치 처리 (경계값으로 이상치를 대치)
    numeric_cols = ['age','salary','score']
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - IQR*1.5
        upper = Q3 + IQR*1.5
        df[col] = df[col].clip(lower=lower, upper=upper)

    # 중복 데이터 제거
    df = df.drop_duplicates(keep='first')

    # 종료
    print(f'파이프 라인 종료')
    print(f'shape = {df.shape}')

if __name__ == '__main__':
    file_path = r'C:\SKN_29th\git_src\데이터분석\Pandas\NaN_Outlier\data\messy_data.csv'
    clean_df = run_preprocessing_pipeline(file_path)
    clean_df.to_csv('data/clean_data.csv', encoding='utf-8', index=False)
    print('데이터 저장완료')