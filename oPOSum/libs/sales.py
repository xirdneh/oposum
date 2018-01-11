import json
import logging, traceback

logger = logging.getLogger(__name__)

def ticket_text(sale, folio):
    date = sale.date_time.strftime('%d/%m/%Y')
    sales_det_str = u' {{CR}} {{LF}} Fecha: ' + date + ' {{TAB}} Folio: ' + str(folio) + ' {{CR}} {{LF}} '
    sales_det_str += u' {{CR}} {{LF}} #  CODIGO/DESCRIPCION  PRECIO  CANTIDAD {{CR}} {{LF}} '.encode('latin-1')
    cnt = 1
    for sd in sale.saledetails_set.all():
        sales_det_str += str(cnt) + ' {{TAB}} '
        slug = sd.product.slug.encode('latin-1')
        if len(slug) < 18:
            slug += ' {{TAB}} ' * int( (18 - len(slug))/8 )
        else:
            slug = slug[:18]

        sales_det_str += slug + ' {{TAB}} '
        price = str(sd.over_price)
        if len(price) < 8:
            price += '{{TAB}}' * int( (8 - len(price))/8 )
                        
        sales_det_str += str(sd.over_price) + ' {{TAB}} '
        sales_det_str += str(sd.quantity) 
        sales_det_str += '  {{CR}} {{LF}} '
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
        sales_det_str += sd.product.description[:40] + ' {{TAB}}  {{CR}} {{LF}} '
        cnt += 1

    sales_det_str += ' {{BOLDON}} {{TAB}}  {{TAB}}  {{TAB}}  TOTAL:   ' + str(sale.total_amount) + ' {{CR}} {{LF}} {{BOLDOFF}}'
    sales_det_str += ' {{BOLDON}} {{TAB}}  {{TAB}}  {{TAB}}  SU PAGO:  ' + str(sale.payment_amount) + ' {{CR}} {{LF}} {{BOLDOFF}}'
    sales_det_str += ' {{BOLDON}} {{TAB}}  {{TAB}}  {{TAB}}  {{TAB}} (' + sale.payment_method + ') {{CR}} {{LF}} {{BOLDOFF}}'
    sales_det_str += ' {{BOLDON}} {{TAB}}  {{TAB}}  {{TAB}}  SU CAMBIO: ' + str(sale.payment_amount - sale.total_amount) + ' {{CR}} {{LF}} {{BOLDOFF}}'

    sales_det_str = sale.branch.ticket_pre + ' {{CR}} {{LF}} ' + sales_det_str + ' {{CR}} {{LF}} '
    sales_det_str += ' {{BOLDON}} SUCURSAL  {{TAB}}  ' + sale.branch.name + ' {{CR}} {{LF}} {{BOLDOFF}} '
    sales_det_str += '-------------------------------------------- {{CR}} {{LF}} '
    sales_det_str += sale.branch.ticket_post
    logger.debug(sales_det_str)
    return sales_det_str
