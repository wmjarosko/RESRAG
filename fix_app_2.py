with open('/app/app.py', 'r') as f:
    content = f.read()

# Make some visual enhancements to the sidebar
content = content.replace('st.sidebar.header("Silo A: Technical Docs")', 'st.sidebar.header("📚 Silo A: Technical Docs")\nst.sidebar.markdown("Upload architecture diagrams, standard operating procedures, and other technical documentation your candidate should be familiar with.")')

# Make visual enhancements to the main area
content = content.replace('st.header("Evaluation Pipeline")', 'st.header("⚙️ Evaluation Pipeline")\nst.markdown("Provide the candidate\'s resume and the job description to run a multi-agent evaluation against the technical documentation in Silo A.")')

content = content.replace('st.subheader("Silo B: Candidate Resume")', 'st.subheader("📄 Silo B: Candidate Resume")')
content = content.replace('st.subheader("Silo C: Job Description")', 'st.subheader("💼 Silo C: Job Description")')

content = content.replace('st.subheader("1. HR Agent Extraction")', 'st.subheader("🕵️‍♀️ 1. HR Agent Extraction")\nst.markdown("*Extracting core technical skills, software experience, and infrastructure knowledge.*")')
content = content.replace('st.subheader("2. Retrieval Agent Context (From Silo A)")', 'st.subheader("🔍 2. Retrieval Agent Context (From Silo A)")\nst.markdown("*Retrieving specific, relevant technical context from the uploaded documentation.*")')
content = content.replace('st.subheader("3. Evaluator Agent Final Verdict")', 'st.subheader("⚖️ 3. Evaluator Agent Final Verdict")\nst.markdown("*Determining if the candidate is capable of operating in the specific environment.*")')

# Wrap the evaluation button in a column to center it or make it look better
button_code = """
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        run_eval = st.button("🚀 Run Multi-Agent Evaluation", type="primary", use_container_width=True)
"""
content = content.replace('if st.button("Run Multi-Agent Evaluation", type="primary"):', button_code + '\n    if run_eval:')

with open('/app/app.py', 'w') as f:
    f.write(content)
