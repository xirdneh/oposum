import json
import logging, traceback

logger = logging.getLogger(__name__)

def ticket_text(sale):
    date = sale.date_time.strftime('%d/%m/%Y')
    sales_det_str = u'# \t CODIGO/DESCRIPCION \t PRECIO \t CANTIDAD \n\n'.encode('latin-1')
    cnt = 1
    for sd in sale.saledetails_set.all():
        sales_det_str += str(cnt) + '\t'
        sales_det_str += sd.product.description.encode('latin-1') + '\t'
        sales_det_str += str(sd.over_price) + '\t'
        sales_det_str += str(sd.quantity) 
        sales_det_str += '\n'
        if len(sd.product.description) > 40:
            desc = sd.product.description[:40]
        else:
            desc = sd.product.description
        
        cat = '' 
        for c in sd.product.category.all():
            if c.type.lower() == 'bodega':
                cat = c.name
                break

    sales_det_str += cat + ' '
    sales_det_str += sale.product.description[:40] + '\t'
    sales_det_str += '\t\t\t TOTAL:   ' + str(sale.total_amount)
    sales_det_str += '\t\t\t SU PAGO:  ' + str(sale.payment_amount)
    sales_det_str += '\t\t\t      (' + sale.payment_method + ')'
    sales_det_str += '\t\t\t SU CAMBIO: ' + str(sale.total_amount - sale.payment_amount)

    sales_det_str = branch.ticket_pre + sales_det_str
    sales_det_str += 'SUCURSAL \t ' + sale.branch.name
    sales_det_str += branc.ticket_post
    logger.debug(sales_det_str)
    return sales_det_str
