with open('/app/app.py', 'r') as f:
    content = f.read()

content = content.replace("""
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        run_eval = st.button("🚀 Run Multi-Agent Evaluation", type="primary", use_container_width=True)

    if run_eval:
    if not resume_text or not jd_text:""", """col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    run_eval = st.button("🚀 Run Multi-Agent Evaluation", type="primary", use_container_width=True)

if run_eval:
    if not resume_text or not jd_text:""")

content = content.replace("""            st.subheader("🕵️‍♀️ 1. HR Agent Extraction")
st.markdown("*Extracting core technical skills, software experience, and infrastructure knowledge.*")""", """            st.subheader("🕵️‍♀️ 1. HR Agent Extraction")
            st.markdown("*Extracting core technical skills, software experience, and infrastructure knowledge.*")""")

content = content.replace("""            st.subheader("🔍 2. Retrieval Agent Context (From Silo A)")
st.markdown("*Retrieving specific, relevant technical context from the uploaded documentation.*")""", """            st.subheader("🔍 2. Retrieval Agent Context (From Silo A)")
            st.markdown("*Retrieving specific, relevant technical context from the uploaded documentation.*")""")

content = content.replace("""            st.subheader("⚖️ 3. Evaluator Agent Final Verdict")
st.markdown("*Determining if the candidate is capable of operating in the specific environment.*")""", """            st.subheader("⚖️ 3. Evaluator Agent Final Verdict")
            st.markdown("*Determining if the candidate is capable of operating in the specific environment.*")""")


with open('/app/app.py', 'w') as f:
    f.write(content)
