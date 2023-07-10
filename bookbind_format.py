from PyPDF2 import PdfFileReader, PdfFileWriter
import argparse

def format_pdf(input_path,output_path,initial_page=1,final_page=None,sheets_per_signature=4):
    writer = PdfFileWriter()
    reader = PdfFileReader(input_path)


    if not final_page:
        final_page = reader.getNumPages()

    #account for pages being 1-indexed
    #and for 4 book pages fitting on each sheet of paper
    signature_starts = [i-1 for i in range(initial_page,final_page,sheets_per_signature*4)]

    for i in range(len(signature_starts)):
        this_start = signature_starts[i]
        this_end = this_start + sheets_per_signature*4-1

        def add_formatted_page(page_index):
            if page_index < final_page:
                writer.addPage(reader.getPage(page_index))
            else:
                writer.addBlankPage()

        for j in range(0,sheets_per_signature*2,2):
            #outer side of the sheet
            add_formatted_page(this_end-j)
            add_formatted_page(this_start+j)
            # #inner side of the sheet
            add_formatted_page(this_start+j+1)
            add_formatted_page(this_end-j-1)

    with open(output_path,'wb') as out:
        writer.write(out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path')
    parser.add_argument('output_path')
    parser.add_argument('--initial_page',type=int,default=1)
    parser.add_argument('--final_page',type=int,default=None)
    parser.add_argument('--sheets_per_signature',type=int,default=4)

    args=parser.parse_args()

    format_pdf(args.input_path,args.output_path,args.initial_page,args.final_page,args.sheets_per_signature)
