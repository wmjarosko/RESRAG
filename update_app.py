import re

with open('/app/app.py', 'r') as f:
    content = f.read()

# Add CSS injection
css_code = """
st.markdown(\"""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    \"""
    </style>
\""", unsafe_allow_html=True)
"""

if '# Initialize backend classes' in content:
    content = content.replace('# Initialize backend classes', css_code + '\n# Initialize backend classes')

with open('/app/app.py', 'w') as f:
    f.write(content)
