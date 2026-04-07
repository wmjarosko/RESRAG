with open('/app/app.py', 'r') as f:
    content = f.read()

content = content.replace('"""\n    </style>\n"""', '</style>\n"""')

with open('/app/app.py', 'w') as f:
    f.write(content)
