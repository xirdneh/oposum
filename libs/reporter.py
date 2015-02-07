from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

import logging

logger = logging.getLogger(__name__)


class PDFReporter:
    def __init__(self, buffer, pagesize, header, footer):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize
        self.header = header
        self.footer = footer


    def _header_footer(self, canvas, doc):
        canvas.saveState()
        styles = getSampleStyleSheet()
        logging.debug("class {0}".format(self))
        header = Paragraph(self.header, styles['Normal'])
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin )
        footer = Paragraph(self.footer, styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h - 10 * mm)
        canvas.restoreState()

    def print_entries(self, eh, ehds):
        buffer = self.buffer
        styles = getSampleStyleSheet()
        data = []
        ts = TableStyle()
        d = []
        hs = styles['Heading1']
        hs.alignment = TA_CENTER
        d.append(Paragraph('<b>Producto</b>', hs))
        d.append(Paragraph('<b>Descripcion</b>', hs))
        d.append(Paragraph('<b>Cantidad</b>', hs))
        title = Paragraph('<b> Entrada de Mercancia </b>', hs)
        data.append(d)
        for ehd in ehds:
            d = []
            d.append(ehd.product.name)
            sp = styles['BodyText']
            sp.alignment = TA_CENTER
            p = Paragraph(ehd.product.description, sp)
            d.append(p)
            sq = styles['BodyText']
            sq.alignment = TA_RIGHT
            pq = Paragraph(str(ehd.quantity), sq)
            d.append(pq)
            data.append(d)
        t = Table(data, colWidths = [(letter[0] * .20), (letter[0] * .50), (letter[0] * .20)])
        ts.add('LINEBELOW', (0,1), (-1,-1), 0.25, colors.black)
        t.setStyle(ts)
        elements = []
        elements.append(title)
        elements.append(t)
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer, canvasmaker = NumberedCanvas)
        return buffer



class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
 
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
 
    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
 
    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.drawRightString(211 * mm, 10 * mm + (0.22 * inch),
                             "Pagina %d de %d" % (self._pageNumber, page_count))
