from app import app
import os
from flask import jsonify, request, send_file
from werkzeug.utils import secure_filename
import pdfplumber
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import glob
from datetime import datetime
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import red
from reportlab.lib.colors import Color, red

dictroute = {
  "000113": "3",
  "000114": "1",
  "000118": "2",
  "000120": "3",
  "000123": "1",
  "000127": "2",
  "000130": "3",
  "000134": "1",
  "000136": "1",
  "000138": "3",
  "000142": "2",
  "000144": "1",
  "000146": "1",
  "000148": "2",
  "000149": "2",
  "000151": "4",
  "000153": "3",
  "000154": "1",
  "000156": "3",
  "000401": "4",
  "000402": "4",
  "000403": "4",
  "003002": "3",
  "003003": "1",
  "003004": "1",
  "003005": "1",
  "003006": "3",
  "003007": "2",
  "003008": "3",
  "003009": "2",
  "003010": "2",
  "003011": "3",
  "003013": "3"
}

dictCustomer = {
  "000113": "SOHO  ",
  "000114": "MADISON",
  "000118": "FIRST AVE",
  "000120": "  8TH ",
  "000123": "LINCOLN",
  "000127": "BRYANT ",
  "000130": "TRIBECA",
  "000134": "MINERAL",
  "000136": "   88 ",
  "000138": "BLEECKER",
  "000142": " GCW  ",
  "000144": "  E97 ",
  "000146": "  E83 ",
  "000148": "  E65 ",
  "000149": "  W55 ",
  "000151": "ROOSEVELT",
  "000153": "85 BROAD",
  "000154": "SAILBOAT",
  "000156": "SOUTH END",
  "000401": "N.CANAAN",
  "000402": "  RYE ",
  "000403": "GREENWICH",
  "003002": "921 BWAY",
  "003003": "   58 ",
  "003004": "   87 ",
  "003005": "   76 ",
  "003006": "JORALEMON",
  "003007": "   56 ",
  "003008": "   36 ",
  "003009": "   38 ",
  "003010": "   43 ",
  "003011": "   41 ",
  "003013": "   29 "
}


UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + '/Downloads/'
ALLOWED_EXTENSIONS = set(['pdf'])
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif',
#                           'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'csv', 'zip', 'rar', 'mp4',
#                           'mp3', 'wav', 'avi', 'mkv', 'flv', 'mov', 'wmv'])


def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST', 'GET'])
# API to upload file
def fileUpload():
    if request.method == 'POST':
        file = request.files.getlist('file')
        for f in file:
            filename = secure_filename(f.filename)
            print("The dir is: %s"%os.listdir(os.getcwd()))
            if allowedFile(filename):
                f.save(os.path.join(UPLOAD_FOLDER, filename))
                os.chdir(UPLOAD_FOLDER)
                print("The new dir is: %s"%os.listdir(os.getcwd()))

                orderType = str(filename) # user input filename and saves to orderType variable
                os.rename(orderType,"input.pdf") # rename file to input.pdf
                with open('input.pdf', "rb") as f:
                    lastPage = PyPDF2.PdfFileReader(f).numPages
                page_id = 1 # fix for overwriting orders >1 page long
                outputName = ""

                with pdfplumber.open('input.pdf') as pdf: # opens inputted pdf
                    for i in range(lastPage): # iterate to lastPage
                        curr_page = pdf.pages[i] # assign curr_page variable
                        customerId = curr_page.extract_text()[10:16] # extract customer ID
                        route = dictroute.get(f"{customerId}") # get route from dictionary
                        customer = dictCustomer.get(f"{customerId}") # get customer from dictionary
                        path = ('input.pdf') # set path variable
                        pdf_reader = PdfFileReader(path)
                        pdf_writer = PdfFileWriter()
                        pdf_writer.addPage(pdf_reader.getPage(i)) # creates the page
                        output_filename = 'input_{}_{}_{}.pdf'.format( # file name convention
                            route, customerId, page_id)
                        with open(output_filename, 'wb') as out: # writes file name
                            pdf_writer.write(out)
                        print('Created: {}'.format(output_filename)) # logs the pages as renaming finishes

                        # draw with canvas
                        redtransparent = Color( 255, 0, 0, alpha=0.4)
                        packet = io.BytesIO()
                        can = canvas.Canvas(packet, pagesize=letter)
                        can.setFillColor(redtransparent)

                        # draw bottom text
                        can.setFont("Helvetica-Bold", 110)
                        if (len(customer) == 6):
                            can.setFont("Helvetica-Bold", 185)
                        if (len(customer) >= 9):
                            can.setFont("Helvetica-Bold", 95)
                        can.drawString(12, 18, f'{customer}')
                        # can.drawString(12, 18, f'ROUTE {route} - {customer}') # draw text on bottom

                        # draw top text
                        can.setFont("Helvetica-Bold", 40)
                        can.drawString(12, 685, f'ROUTE {route} - {customer}')

                        can.save()
                        #move to the beginning of the StringIO buffer
                        packet.seek(0)
                        # create a new PDF with Reportlab
                        new_pdf = PdfFileReader(packet)
                        # read your existing PDF

                        existing_pdf = open(output_filename, "rb")
                        PdfFileReader(existing_pdf)
                        output = PdfFileWriter()
                        # add the "watermark" (which is the new pdf) on the existing page
                        page2 = PdfFileReader(existing_pdf).getPage(0)
                        page2.mergePage(new_pdf.getPage(0))
                        output.addPage(page2)
                        outputStream = open(f'canvas_{route}_{customerId}_{page_id}.pdf', "wb")
                        output.write(outputStream)
                        print(f'Created: canvas_{route}_{customerId}_{page_id}.pdf')
                        existing_pdf.close()
                        outputStream.close()
                        page_id += 1

                def merger(output_path, input_paths):
                    pdf_merger = PdfFileMerger()
                    for path in input_paths:
                        pdf_merger.append(path)
                    with open(output_path, 'wb') as fileobj:
                        pdf_merger.write(fileobj)
                    pdf_merger.close()

                paths = glob.glob('canvas_*.pdf')
                paths.sort()
                now = datetime.now()
                current_time = now.strftime("%Y%m%d_%H%M%S")
                merger((f'_{orderType[:-4]}_output_{current_time}.pdf'), paths)
                outputName = (f'_{orderType[:-4]}_output_{current_time}.pdf')
                print (f'Created: {outputName}')

            # remove input files
            for f in glob.glob("input*.pdf"):
                os.remove(f)

            # remove canvas files
            for f in glob.glob("canvas*.pdf"):
                os.remove(f)

            else:
                return jsonify({'message': 'File type not allowed'}), 400
        return jsonify({"name": filename, "status": "success"})
    else:
        return jsonify({"status": "failed"})
