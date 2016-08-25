import json
import logging, traceback

logger = logging.getLogger(__name__)

def ticket_text(sale):
    date = sale.date_time.strftime('%d/%m/%Y')
    sales_det_str = u'#  CODIGO/DESCRIPCION  PRECIO  CANTIDAD \n\n'.encode('latin-1')
    cnt = 1
    for sd in sale.saledetails_set.all():
        sales_det_str += str(cnt) + '\t'
        slug = sd.product.slug.encode('latin-1')
        if len(slug) < 18:
            slug += '{{TAB}} ' * int( (18 - len(slug))/8 )
        else:
            slug = slug[:18]

        sales_det_str += slug + '\t'
        price = str(sd.over_price)
        if len(price) < 8:
            price += '{{TAB}}' * int( (8 - len(price))/8 )
                        
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
        sales_det_str += sd.product.description[:40] + '\t\n'
        cnt += 1

    sales_det_str += '{{BOLDON}}\t\t\t TOTAL:   ' + str(sale.total_amount) + '\n{{BOLDOFF}}'
    sales_det_str += '{{BOLDON}}\t\t\t SU PAGO:  ' + str(sale.payment_amount) + '\n{{BOLDOFF}}'
    sales_det_str += '{{BOLDON}}\t\t\t      (' + sale.payment_method + ')\n{{BOLDOFF}}'
    sales_det_str += '{{BOLDON}}\t\t\t SU CAMBIO: ' + str(sale.total_amount - sale.payment_amount) + '\n{{BOLDOFF}}'

    sales_det_str = sale.branch.ticket_pre + '\n' + sales_det_str + '\n'
    sales_det_str += 'SUCURSAL \t ' + sale.branch.name + '\n'
    sales_det_str += '--------------------------------------------\n'
    sales_det_str += sale.branch.ticket_post
    logger.debug(sales_det_str)
    return sales_det_str
