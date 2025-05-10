
import streamlit as st
import pandas as pd
import numpy as np
import pickle

model = pickle.load(open("nutrition_model_ext.pkl", "rb"))

fto_map = {"TT": 0, "CT": 1, "CC": 2}
lct_map = {"AA": 0, "AG": 1, "GG": 2}
sex_map = {"여": 0, "남": 1}
activity_map = {"낮음": 0, "보통": 1, "높음": 2}

def food_list_mapping(carb, protein, fat):
    foods = []
    if carb >= 150:
        foods.append("현미밥 1공기")
    else:
        foods.append("고구마 100g")
    if protein >= 100:
        foods.append("닭가슴살 150g")
    else:
        foods.append("두부 1모")
    if fat >= 40:
        foods.append("아보카도 1개")
    else:
        foods.append("올리브오일 1스푼")
    return foods

st.title("개인 맞춤형 영양 식단 추천 시스템")

st.markdown("유전자, 신체 정보, 수면 및 활동량을 바탕으로 AI가 식단을 추천합니다.")

fto = st.radio("FTO 유전자형", ["TT", "CT", "CC"])
lct = st.radio("LCT 유전자형", ["AA", "AG", "GG"])
sex = st.radio("성별", ["남", "여"])
bmi = st.slider("BMI", 16.0, 32.0, 22.0)
age = st.slider("나이", 15, 25, 18)
sleep = st.slider("수면 시간 (시간)", 4, 10, 7)
activity = st.radio("활동량 수준", ["낮음", "보통", "높음"])

if st.button("식단 추천 받기"):
    input_data = pd.DataFrame([[fto_map[fto], lct_map[lct], bmi, age, sex_map[sex], sleep, activity_map[activity]]],
                              columns=['FTO', 'LCT', 'BMI', 'Age', 'Sex', 'SleepHours', 'ActivityLevel'])
    prediction = model.predict(input_data)[0]
    st.success("AI 분석 결과")
    st.write(f"1일 열량 권장량: {round(prediction[0])} kcal")
    st.write(f"탄수화물: {round(prediction[1])} g")
    st.write(f"단백질: {round(prediction[2])} g")
    st.write(f"지방: {round(prediction[3])} g")
    st.write(f"예상 체중 변화: {round(prediction[4], 1)} kg")
    st.write(f"예상 달성 기간: {int(prediction[5])}일")
    foods = food_list_mapping(prediction[1], prediction[2], prediction[3])
    st.markdown("**추천 식품 리스트:**")
    for food in foods:
        st.write(f"- {food}")
