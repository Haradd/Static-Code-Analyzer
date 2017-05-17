import pdfkit, subprocess


def analyze(path, options):
    cmd = 'flake8 {} {} >>media/report.txt'.format(' '.join(options), path)
    subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)
    subprocess.call('echo "\n" >>media/report.txt', stdout=subprocess.PIPE, shell=True)

def make_pdf(txt_path, pdf_path, media_path, project_name):
    with open(txt_path, 'r') as file:
        data = file.readlines()

    html = '<h3>{}</h3>'.format(project_name)
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
    }
    for line in data:
        html += line.replace('\n', '<br>').replace(media_path, '')

    pdfkit.from_string(html, pdf_path, options)
