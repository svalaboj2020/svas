from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

# from weasyprint import HTML, CSS
# from django.template.loader import get_template
# from django.http import HttpResponse

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



#
# def pdf_generation(request,param):
#     print('entertered pdf_generation')
#     html_template = get_template(param)
#     pdf_file = HTML(string=html_template).write_pdf()
#     print('entertered pdf_generation2')
#     response = HttpResponse(pdf_file, content_type='application/pdf')
#     response['Content-Disposition'] = 'filename="home_page.pdf"'
#     return response
