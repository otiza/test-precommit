from odoo import http
from odoo.http import request

class OrdonnanceController(http.Controller):


    @http.route('/web/binary/download_ordonnance_pdf/<int:ordonnance_id>', type='http', auth="user")
    def download_ordonnance_pdf(self, ordonnance_id, **kwargs):
        ordonnance = request.env['gestion.clinique.ordonnance'].browse(ordonnance_id)
        if not ordonnance.exists():
            return request.not_found()
        
        pdf_content = ordonnance.download_pdf()
        pdf_name = 'Ordonnance_%s.pdf' % ordonnance.prescription_number

        return request.make_response(pdf_content, 
                                     headers=[('Content-Type', 'application/pdf'),
                                              ('Content-Disposition', 'attachment; filename="%s"' % pdf_name)])

