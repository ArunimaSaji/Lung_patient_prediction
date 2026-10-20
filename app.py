import streamlit as st
import pickle
from PIL import Image
import pymysql
conn=pymysql.connect(host='localhost',user='root',password='db_password',db='lung')
cursor=conn.cursor()
def main():
    st.title('Lung Patient Prediction')
    img=Image.open('lung.jpeg')
    st.image(img,width=700)
    age=st.number_input('enter the age')
    smoke=st.number_input('smoke')
    area=st.number_input('area')
    alcohol=st.number_input('alcohol')
    feature=[age,smoke,area,alcohol]
    knn=pickle.load(open('knn_lung.sav','rb'))
    scaler=pickle.load(open('scaler_lknn.sav','rb'))
    pred=st.button('predict')
    if pred:
        result=knn.predict(scaler.transform([feature]))
        result=int(result[0])
        if result==0:
            st.write('Not a lung cancer patient')
        else:
            st.write('Lung Patient')
        q1='''insert into lung_hist(age,smoke,area,alcohol,result)
            values (%s,%s,%s,%s,%s)'''
        values=[age,smoke,area,alcohol,result]
        cursor.execute(q1,values)
        conn.commit()
        st.success("Data saved successfully")


main()
