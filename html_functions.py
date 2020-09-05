'''
create html pages
'''
def create_html(body, title = 'default'):
    html = '''<!DOCTYPE html>\n<html>\n<head>\n<title>''' + title + '''</title>\n</head>\n<body>'''
    html += body +  '''\n</body>\n</html> '''
    return html


def create_html_body(title, text = '', dated = [], url = []):
    html = '<div>\n'
    if url != []:
        html += '<h2><a href="' + url + '">' + title +'</a></h2>\n'
    else:
        html += '<h2>' + title +'</h2>\n'
    if dated != []:
        html += '<h4>' + dated.strftime("%d.%m.%Y") +'</h4>\n'
    html += text +  '\n</div>\n'
    return html