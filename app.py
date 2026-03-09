import streamlit as st
from ingest import extract_text_from_pdf
from rag_engine import create_rag
from dotenv import load_dotenv
import os
from llm_config import get_llm
import json
from risk_engine import calculate_risk_score, risk_category
import pandas as pd
import matplotlib.pyplot as plt
from decision_engine import loan_decision
from report_generator import generate_cam_report
from explainability_engine import explain_decision
from news_agent import fetch_company_news, analyze_news_risk
import plotly.graph_objects as go
import re





load_dotenv()

llm = get_llm()



st.title("IntelliCredit AI")
st.caption("AI-Powered Credit Risk Analysis Platform")



st.sidebar.title("AI Credit Intelligence")


st.sidebar.markdown("### Workflow")

st.sidebar.markdown("""
1️⃣ Upload Financial Document  
2️⃣ Extract Financial Data  
3️⃣ Risk Scoring Engine  
4️⃣ Credit Decision Engine  
5️⃣ External Risk Signals  
6️⃣ CAM Report Generation  
7️⃣ AI Credit Assistant  
""")


st.sidebar.markdown("### System Status")

st.sidebar.success("RAG Engine Ready")
st.sidebar.success("Risk Engine Active")
st.sidebar.success("Decision Engine Active")




def extract_number(value):

    if isinstance(value, str):
        nums = re.findall(r'\d+', value)
        return float(nums[0]) if nums else 0

    if isinstance(value, dict):
        return extract_number(list(value.values())[0])

    return value




uploaded_file = st.file_uploader("Upload company document", type="pdf")



if uploaded_file:

    with st.spinner("Analyzing financial document..."):

      text = extract_text_from_pdf(uploaded_file)

    
      

      summary_prompt = f"""
Analyze the financial document and extract structured data.

Return ONLY valid JSON.
Do not include explanations, markdown, or text outside JSON.

Format:

{{
  "company": "",
  "revenue_by_year": {{}},
  "profit_by_year": {{}},
  "debt_by_year": {{}},
  "risks": [],
  "financial_health": ""
}}

Document:
{text}
""" 
    
    

      response = llm.invoke(summary_prompt)

      content = response.content.strip()
      content = content.replace("```json", "").replace("```", "")
    
      data = json.loads(content)


      # normalize numbers
      if "revenue_by_year" in data:
        for k,v in data["revenue_by_year"].items():
          data["revenue_by_year"][k] = extract_number(v)

      if "profit_by_year" in data:
        for k,v in data["profit_by_year"].items():
          data["profit_by_year"][k] = extract_number(v)

      if "debt_by_year" in data:
        for k,v in data["debt_by_year"].items():
          data["debt_by_year"][k] = extract_number(v)


      progress = st.progress(0)

      progress.progress(10)
      text = extract_text_from_pdf(uploaded_file)

      progress.progress(30)
      response = llm.invoke(summary_prompt)

      progress.progress(60)
      data = json.loads(content)

      progress.progress(80)
      score = calculate_risk_score(data)

      progress.progress(100)

    

    tab1, tab2, tab3, tab4 = st.tabs([
    "Financial Analysis",
    "Risk Dashboard",
    "Credit Decision",
    "AI Assistant"  ])

    
    score = calculate_risk_score(data)
    category = risk_category(score)

    with tab1:
      st.subheader("Financial Summary")
      st.json(data)
 


    with tab2:
      st.subheader("Credit Risk Analysis")
      st.write(f"Risk Score: {score}/100")
      st.write(f"Risk Category: {category}")


      fig = go.Figure(go.Indicator(
      mode="gauge+number",
      value=score,
      title={'text': "Credit Risk Score"},
      gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "darkblue"},
        'steps': [
            {'range': [0, 45], 'color': "red"},
            {'range': [45, 75], 'color': "yellow"},
            {'range': [75, 100], 'color': "green"}
        ]
       }    ))

      st.plotly_chart(fig)




    




    


    with tab3:
      decision = loan_decision(data, score)
      st.subheader("Credit Decision")


      if decision:
       st.write("Decision:", decision["decision"])
       st.write("Suggested Loan Amount:", decision["loan_amount"], "crore")
       st.write("Interest Rate:", decision["interest_rate"], "%")




      explanations = explain_decision(data, score)

      st.subheader("Decision Explanation")

      for e in explanations:
        st.write(e)





      report_path = generate_cam_report(data, score, category, decision)

      company = data.get("company","")

      news = fetch_company_news(company)

      risk_news = analyze_news_risk(company, news)

      st.subheader("External Risk Signals")
      for r in risk_news.split("\n"):
        st.write(r)



      st.success("CAM Report generated successfully!")



      with open(report_path, "rb") as f:
       st.download_button(
        label="⬇ Download CAM Report",
        data=f,
        file_name="credit_appraisal_report.pdf",
        mime="application/pdf"
       )




      if "revenue_by_year" in data:

         rev_df = pd.DataFrame(
         list(data["revenue_by_year"].items()),
         columns=["Year","Revenue"]
     )

         fig = plt.figure()
         plt.plot(rev_df["Year"], rev_df["Revenue"], marker="o")
         plt.title("Revenue Trend")
         plt.xlabel("Year")
         plt.ylabel("Revenue")
         st.pyplot(fig)



      if "profit_by_year" in data:

         profit_df = pd.DataFrame(
         list(data["profit_by_year"].items()),
         columns=["Year","Profit"]
        )

         fig = plt.figure()
         plt.bar(profit_df["Year"], profit_df["Profit"])
         plt.title("Profit Trend")
         plt.xlabel("Year")
         plt.ylabel("Profit")
         st.pyplot(fig)



      if "debt_by_year" in data:

         debt_df = pd.DataFrame(
         list(data["debt_by_year"].items()),
         columns=["Year","Debt"]
     )

         fig = plt.figure()
         plt.plot(debt_df["Year"], debt_df["Debt"], marker="o")
         plt.title("Debt Exposure")
         plt.xlabel("Year")
         plt.ylabel("Debt")
         st.pyplot(fig)




    
    with tab4:
      st.subheader("AI Credit Officer Assistant")

      user_question = st.text_input("Ask about the company or credit decision:")

      if user_question:

        context = f"""
      Company Financial Data:
       {data}

      Risk Score: {score}
      Risk Category: {category}

      Loan Decision:
       {decision}

      Decision Explanation:
       {explanations}

      External Risk Signals:
       {risk_news}
      """

        prompt = f"""
          You are an AI credit analyst.

       Answer the user's question based only on the following analysis.

       {context}

       Question: {user_question}
       """

        answer = llm.invoke(prompt)

        st.write(answer.content)
    




      st.subheader("Document Q&A")

      qa = create_rag(text)

      question = st.text_input("Ask about the company")

      if question:
        answer = qa.run(question)
        st.write(answer)