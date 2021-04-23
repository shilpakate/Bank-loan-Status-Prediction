

import pickle
import streamlit as st
import pandas as pd
 
# loading the trained model
pickle_in = open('E:/Project/c1.pkl', 'rb') 
st.cache(suppress_st_warning=True) 
classifier = pickle.load(pickle_in)

st.title('Bank Loan Prediction')

st.sidebar.header('User Input Parameters')

@st.cache()


# defining the function which will make the prediction using the data which the user inputs 
def prediction(Gender, Married,  Education, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount,Loan_Amount_Term, Credit_History):   
 
    # Pre-processing user input    
    if Gender == "Male":
        Gender = 0
    else:
        Gender = 1
 
    if Married == "Unmarried":
        Married = 0
    else:
        Married = 1
      
    if Credit_History == "Unsatisfactory":
        Credit_History = 0
    else:
        Credit_History = 1  
    
    if Education == 'Graduate':
        Education = 0
    else:
        Education = 1
    
    if Self_Employed == 'No':
       Self_Employed = 0
    else:
       Self_Employed = 1
        
    ApplicantIncome=ApplicantIncome
    CoapplicantIncome=CoapplicantIncome
    Total =(ApplicantIncome+CoapplicantIncome)*100
    LoanAmount = LoanAmount / 1000

    # Making predictions 
    prediction = classifier.predict([[Gender, Married, Education, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount,Loan_Amount_Term, Credit_History]])
    prediction_proba = classifier.predict_proba([[Gender, Married, Education, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount,Loan_Amount_Term, Credit_History]])
    
    if  prediction_proba[0][1]<=0.01:
   
        pred = 'Rejected'
    else:
    
        pred =  'Approved'
                 
       
    return pred
       
  
# this is the main function in which we define our webpage  
def main():       
   
    # following lines create boxes in which user can enter data required to make prediction 
    Name = st.sidebar.text_input('Enter your name')
    Gender = st.sidebar.radio('Gender',("Male","Female"))  
    Married = st.sidebar.selectbox('Marital Status',("Unmarried","Married")) 
   # Dependents =st.sidebar.selectbox('Dependents',('1','2','3+'))
    Education = st.sidebar.selectbox('Education',('Graduate','Non Graduate'))
    Self_Employed = st.sidebar.selectbox('Employment Status',('Self Employed','Not Self Employed'))
    
    ApplicantIncome = st.sidebar.number_input("Applicants monthly income",1000)
    CoapplicantIncome =st.sidebar.number_input(" CoapplicantIncome monthly income",1000)
    LoanAmount = st.sidebar.number_input("Total loan amount",1)
    Loan_Amount_Term =st.sidebar.number_input("Loan_Amount_Term",360)
    Credit_History = st.sidebar.selectbox('Credit_History',("Satisfactory","Unsatisfactory"))
   # Property_Area = st.sidebar.selectbox(' Property_Area',("Urban","Rural","Semiurban"))
    result =""
        
    def user_input_features():
        data={'Name': Name,
              'Gender' : Gender,
              'Marital Status': Married,
             # 'Dependents': Dependents,
              'Education': Education,
              'Employment Status' : Self_Employed,
              'Applicant Income' : ApplicantIncome,
              'CoapplicantIncome':CoapplicantIncome,
              'Loan_Amount_Term':Loan_Amount_Term,
              'Credit History': Credit_History,
             # 'Property_Area': Property_Area}
             }
        features = pd.DataFrame(data,index = [1])
        return features
    
    df = user_input_features()
    st.subheader('Customer Details')
    st.write(df,width=500,height=2000)

 
    
    
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        result = prediction(Gender, Married, Education, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount,Loan_Amount_Term, Credit_History) 
        
        #st.success('Your loan is {} '.format(result))
        if result == 'Approved':
            if Gender== 'Male':
                st.success('Congratulations Mr. {}, your loan is {} '.format(Name,result))
                st.info('Loan Amount is(EMI): {}'.format(LoanAmount))
            else:
                st.success('Congratulations Mrs. {}, your loan is {} '.format(Name,result))
                st.info('Loan Amount is: {}'.format(LoanAmount))
        else:
            #st.success('Loan Amount is: Nil')
            st.info('Sorry, you are not eligible for loan')
            

                       
     
if __name__=='__main__': 
    main()
 
