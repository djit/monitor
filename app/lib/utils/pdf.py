from weasyprint import HTML


def render_pdf(html, filename):
    return HTML(html).write_pdf(filename)