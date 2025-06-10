def load_template(f_path):
    with open(f_path) as f:
        subject = text = html = None
        content = f.read()
        try:
            subject = content.split('---subject---')[1].split('---text---')[0].strip()
            text = content.split('---text---')[1].split('---html---')[0].strip()
            html = content.split('---html---')[1].strip()
        except:
            raise ValueError('invalid template')
        
    return subject,text,html

if __name__ == '__main__':
    print(load_template(r'template/template.txt'))
