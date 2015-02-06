import MySQLdb as mdb
import sys
from oPOSum.apps.products.models import *
import re
from django.core.exceptions import ObjectDoesNotExist
import re
import logging
from decimal import Decimal
logger = logging.getLogger("oPOSum.mysql")
def get_con( ):
    try:
        con = mdb.connect('joyeriasbalco.com', 'root', 'tsmbat', 'balco', port=25273)
    except mdb.Error, e:
        logger.error("Error %d: %s" % (e.args[0], e.args[1]))
    return con

def get_lines( ):
    con = get_con()
    cur  = con.cursor()
    cur.execute("SELECT * FROM tabla")
    res = cur.fetchall()
    if con:
        con.close()
    return res

def get_providers( ):
    con = get_con()
    cur  = con.cursor()
    cur.execute("SELECT * FROM proveedor")
    res = cur.fetchall()
    if con:
        con.close()
    return res

def get_arts( ):
    con = get_con()
    cur = con.cursor()
    cur.execute("select * from articulos")
    res = cur.fetchall()
    if con:
        con.close()
    return res

def get_art( code ):
    con = get_con()
    cur = con.cursor()
    cur.execute("select * from articulos where cbarras = %s", 
                    (
                        code.replace("-", ""),
                    )
                )
    logger.debug("Statement:{0}".format(code))
    res = cur.fetchall()
    if con:
        con.close()
    logger.debug("Mysql Response:{0}".format(res))
    return res

def get_det( art ):
    con = get_con()
    cur = con.cursor()
    for n in range(1, 17):
        cur.execute("SELECT bodega, linea, area FROM almacen" + str(n) + " where clave = '" + art + "' order by idnum asc")
        r = cur.fetchone()
        if r: 
            break
    if con:
        con.close()
    return r

def get_art_objs( objs ):
    f = open('migrate-log', 'w')
    print "starting..."
    for obj in objs:
        parts = obj[15].split("-")
        linea = parts[0][:2]
        prov = parts[0][2:]
        if prov == "":
            prov = "00"
        if len(prov) == 1:
            prov = "0" + prov
        else:
            if len(prov) > 3:
                #prov = prov[:2]
                prov = "00"
        s = "{0} \n".format(parts)
        #print parts
        #f.write(s)
        det = get_det(obj[15])
        if det:
            pcb = ProductCategory.objects.filter(slug = det[0]).filter(type='bodega')
            if pcb:
                pcb_s = pcb[0].name
            else:
                pcb_s = "-"
            lpl = []
            if len(obj[4]) == 1:
                lpl.append("0" + obj[4])
            else:
                if len(obj[4]) != 2:
                    lpl.append("00")
                else:
                    lpl.append(obj[4])
            lpl.append(pcb_s[:3])
            lp = obj[4] + "/" + pcb_s[:3]
            precios = str(obj[13]) + "/" + str(obj[14])
            try:
                provider = Provider.objects.get(sku = unicode(prov.decode('latin-1')))
            except ObjectDoesNotExist:
                provider = Provider(sku = prov, name = prov, type = 'N/A')
                s = "!!! Provider Created {0} !!! 'n".format(prov)
                #f.write(s)
                try:
                    provider.save()
                except:
                    provider = Provider.objects.get(sku = "00")
            category = []
            try:
                c = ProductCategory.objects.filter(type='bodega').filter(slug=det[0])[0]
                category.append(c)
                c = ProductCategory.objects.filter(type='area').filter(name=det[2])[0]
                category.append(c)
                c = ProductCategory.objects.filter(type='linea').filter(name=det[1])[0]
                category.append(c)
            except: 
                s = "!!!Error: {0}!!! \n".format("No Category Found") 
                #f.write(s)
            if obj[2] != "NINGUNO" and obj[2] != "" and obj is not None and len(obj) > 2:
                try:
                    c = ProductCategory.objects.filter(type='marca').filter(name=obj[2])[0]
                except:
                    c = ProductCategory(name = unicode(obj[2].decode('latin-1')), slug = u'N/A', type='marca')
                    c.save()
                category.append(c)
            price_line = None
            if lpl[0] != "00":
                s = "!!! lpl: {0} - {1} !!! \n".format(lpl[1].lower(), lpl[0])
                #f.write(s)
                price_line = ProductLine.objects.filter(type=lpl[1].lower()).filter(name=lpl[0])
                if not price_line:
                    price_l = ProductLine(name = lpl[0], price=Decimal("111.11"), type=lpl[1].lower())
                    s = "!!! creating price line !!! \n"
                    #f.write(s)
                    price_l.save()
                    price_line = []
                    price_line.append(price_l)
            regular_price = obj[13]
            equivalency = Decimal(obj[10])
            description = unicode(obj[1].decode('latin-1'))
            slug = obj[15].replace("-", "")
            name = obj[15]
            try:
                s = "Slug: {0} | ".format(slug)
            except:
                pass
            #f.write(s)
            try:
                s = "Name: {0} | ".format(name)
            except:
                pass
            #f.write(s)
            try:
                s = "Provider: {0} | ".format(provider.name)
            except:
                pass
            #f.write(s)
            s = "Category: "
            #f.write(s)
            for c in category:
                try:
                    s = "{0} - {1}, ".format(c.name, c.type)
                except:
                    pass
                #f.write(s)
            #f.write(" | ")
            if price_line:
                s = "Price Line: {0} - {1} | ".format(price_line[0].name, price_line[0].type)
                #f.write(s)
            s = "Regular Price: {0} | ".format(str(regular_price))
            #f.write(s)
            s = "Equivalency: {0} | ".format(str(equivalency))
            #f.write(s)
            s = "Description:"
            #f.write(s)
            #f.write('\n')
            product = Product.objects.filter(slug = slug)
            try:
                if not product:
                    product = Product(slug = slug, 
                        name = name,
                        provider = provider,
                        regular_price = regular_price,
                        equivalency = equivalency,
                        description = description)
                    product.save()
                    for c in category:
                        product.category.add(c)
                    if price_line:
                        product.line = price_line[0]
                    product.save()
                else:
                    #f.write("\t Item already in the DB\n")
                    #print "\033[91m Item already in the DB \033[0m"
                    pass
            except:
                #print "couldn't work with %s" % (parts)
                #f.write("couldn't work with {0} \n".format(parts))
                pass
            s = "========================================================================= \n"
            #f.write(s)
            #print "linea: %s - prov: %s - bodega: %s - area: %s - linea_precio: %s - precios: %s - equivalency: %s - description: %s" % (det[1], prov, det[0], det[2], lp, precios, obj[10], unicode(obj[1].decode('latin-1'))) 
        else:
            test = "tst"
            s = "!!! Non existent  !!! \n"
            #f.write(s)
            s = "========================================================================= \n"
            #f.write(s)

def get_migration_details( code, description ):
    prod = {}
    code_arr = code.split('-')
    linea = code_arr[0][:2]
    prov = code_arr[0][2:]
    string = code_arr[1]
    try:
        bodega = string[:2]
        bodega = int(bodega)
    except:
        try:
            bodega = string[:1]
            bodega = int(bodega)
        except:
            if string[0] == 'T':
                bodega = 14
                area = 'TLL'
            elif string[0] == 'B':
                bodega = 16
                area = 'B'
            elif string[0] == 'C':
                bodega = 6
                area = 'C'
            elif string[0] == 'A':
                bodega = 16
                area = 'A'
            elif code_arr[1][0] == 'P':
                bodega = 16
                area = 'P'
            elif string[0] == 'V':
                bodega = 20
                area = 'RC' 

    if linea == 19 or bodega == 17:
        area = 'EST'
    elif string[2:] == 'LAMI':
        area = 'LAM'
    elif linea == 17 or linea == 25 or linea == 13:
        area = 'R'
    elif not linea:
        area = 'J'
    if(len(code_arr) > 2):
        m = re.search(r'^(0?[A-Za-z]{1,2})([0-9]{1,4}\.[0-9]{1,4})', code_arr[2])
        if m:
            line = m.group(1)
            prod['line'] = line
            weight = m.group(2)
            prod['equivalency'] = weight
            prod['price'] = '0.0'
        elif re.search(r'[0-9]{1,4}\.[0-9]{1,4}', code_arr[2]):
            prod['line'] = ''
            prod['equivalency'] = code_arr[2]
            prod['price'] = '0.0'
        else:
            try: 
                price = int(code_arr[2])
                prod['price'] = price
                prod['line'] = ''
                prod['equivalency']=''
            except:
                prod['line'] = ''
                prod['equivalency'] = code_arr[2]
                prod['price'] = '0.0'
    prod['code'] = code.replace("-", "")
    prod['name'] = code
    prod['description'] = unicode(description, errors='ignore')
    if(linea[:1] == '0'):
        prod['linea'] = linea[1]
    else:
        prod['linea'] = linea
    prod['prov'] = prov
    prod['bodega'] = bodega
    prod['area'] = area
    logger.debug("Product: {0}".format(prod));
    return prod   

def arts():
    objs = get_arts()
    get_art_objs(objs)

def get_lines_objects( lines ):
    ret = []
    for line in lines:
        l = ProductLine(name = line[2], price  = Decimal(line[1]), type = line[3].lower())
        ret.append(l)
    return ret

def get_cat_objects( cats, type ):
    ret = []
    for cat in cats:
        p = ProductCategory(name = cat[1], slug = cat[2], type = type)
        ret.append(p)
    return ret

def save_lines(lines):
    for line in lines:
        l = ProductLine.objects.all().filter(name=line.name).filter(type=line.type)
        if not l:
            try:
                print "saving cat: %s - %s" % (line.name, line.type)
                line.save()
            except:
                print "couldn't save: %s - %s" % (line.name, line.type)
                print "Error:" , sys.exc_info()[0]

def save_cats(cats):
    for cat in cats:
        p = ProductCategory.objects.all().filter(slug=cat.slug)
        if not p:
            try:
                print "saving cat: %s" % (cat.name)
                cat.save()
            except:
                print "couldn't save: %s" % (cat.name)
                print "Error:" , sys.exc_info()[0]

def get_prov_objects(provs):
    ret = []
    for prov in provs:
        if prov[6] is None:
            type = "None"
        else:
            type = prov[6]
        p = Provider(sku = prov[2], name = unicode(prov[1].decode('latin-1')), type=type)
        ret.append(p)
    return ret

def save_provs(provs):
    for prov in provs:
        p = Provider.objects.all().filter(name=prov.name)
        if not p:
            try:
                print "saving prov: %s" % (prov.name)
                prov.save()
            except:
                print "couldn't svae: %s" % (prov.name)
                prov.type="None"
                prov.save()
                print "Error:", sys.exc_info()[0]
