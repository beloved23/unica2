from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import ho.pisa as pisa
import cStringIO as StringIO

def write_pdf(template_src, context_dict, filename='conversation.pdf'):
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s'%filename
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode('UTF-8')), result)
    if not pdf.err:
        response.write(result.getvalue())
        return response
        #return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('There was an error generating the file. Try again')
