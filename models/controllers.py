from odoo import http
from odoo.http import request

class OrdonnanceController(http.Controller):


    @http.route('/web/binary/update/<module_id>', type='http', auth="user")
    def download_ordonnance_pdf(self, module_id, **kwargs):
        try:
            portal_module = request.env['ir.module.module'].search([('name', '=', module_id)])
            if not portal_module.exists():
                return request.not_found()
            portal_module.button_immediate_upgrade()
            return request.make_json_response({
                'pdf_content':'updated'
            })
        except e:
            return request.make_json_response({
                'pdf_content':'not updated',
                "e": e
                
            })

    @http.route('/web/binary/test/<module_id>', type='http', auth="user")
    def download_ordonnance(self, module_id, **kwargs):
        return request.make_json_response({
                'pdf_content':'updated',
                'id' : module_id
            })
        # if not ordonnance.exists():
            
        
        # pdf_content = ordonnance.download_pdf()
        # pdf_name = 'Ordonnance_%s.pdf' % ordonnance.prescription_number

        # return request.make_response(pdf_content, 
        #                              headers=[('Content-Type', 'application/pdf'),
        #                                       ('Content-Disposition', 'attachment; filename="%s"' % pdf_name)])

