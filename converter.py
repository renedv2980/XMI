from BianBom import BianBom
import sys
import time

def main(arg):
    print('Converting Excel to CSV...')
    diagrams = BianBom()

    diagrams.getExcel(arg)
    print('Completed')
    time.sleep(0.5)
    print('Converting Global Model to XMI...')
    diagrams.converttoxmiBIANBOMSubSuperTypeRelations()
    print('Completed')
    time.sleep(0.5)
    print('Converting Helper Diagrams with refrences to Xmi Files...')
    diagrams.converttoxmiwithDiagrams("XMI BIAN files\HELPER DIAGRAMS_and_REFERENCES",'Helper diagram','R','HOL')
    print('Completed')
    time.sleep(0.5)
    print('Converting Overview Diagrams with references to Xmi Files...')
    diagrams.converttoxmiwithDiagrams("XMI BIAN files\OVERVIEW DIAGRAMS_and_REFERENCES",'Overview diagram','R','HOL')
    print('Completed')
    time.sleep(0.5)
    print('Converting Landscape Diagrams with references to Xmi Files...')
    diagrams.converttoxmiwithDiagrams("XMI BIAN files\LANDSCAPE DIAGRAMS_and_REFERENCES",'Landscape diagram','R','HOL')
    print('Completed')
    time.sleep(0.5)
    print('Converting Helper Diagrams to Xmi Files...')
    diagrams.converttoxmiwithDiagrams('XMI BIAN files/HELPER DIAGRAM','Helper diagram','NR','HOL')
    print('Completed')
    time.sleep(0.5)
    print('Converting Overview Diagrams to Xmi Files...')
    diagrams.converttoxmiwithDiagrams('XMI BIAN files/OVERVIEW DIAGRAMS','Overview diagram','NR','HOL')
    print('Completed')
    time.sleep(0.5)
    print('Converting Landscape Diagrams to Xmi Files...')
    diagrams.converttoxmiwithDiagrams('XMI BIAN files/LANDSCAPE DIAGRAMS','Landscape diagram','NR','HOL')
    print('Completed')
    time.sleep(0.5)
    print('Converting Class Diagram with references to XMI...')
    diagrams.converttoxmiwithDiagrams("XMI BIAN files\CLASS DIAGRAMS_and_REFERENCES",'servicedomain','NR','Domains')
    print('Completed')
    time.sleep(0.5)
    print('Converting Bussiness Domains with references to XMI Files...')
    diagrams.converttoxmiwithDiagrams("XMI BIAN files\BUSINESS DOMAINS_AND_CLASS_DIAGRAMS_and_REFERENCES",'bussinessdomain','R','Domains')
    print('Completed')
    time.sleep(0.5)
    print('Converting Bussiness Area with references to XMI Files...')
    diagrams.converttoxmiwithDiagrams("XMI BIAN files\BUSINESS AREAS_AND_CLASS_DIAGRAMS_and_REFERENCES",'bussinessarea','R','Domains')
    print('Completed')
    time.sleep(0.5)
    print('Converting Bussiness Domains to XMI Files...')
    diagrams.converttoxmiwithDiagrams("XMI BIAN files\BUSINESS DOMAINS_AND_CLASS_DIAGRAMS",'bussinessdomain','NR','Domains')
    print('Completed')
    time.sleep(0.5)
    print('Converting Bussiness Area to XMI Files...')
    diagrams.converttoxmiwithDiagrams("XMI BIAN files\BUSINESS AREAS_AND_CLASS_DIAGRAMS",'bussinessarea','NR','Domains')
    print('Completed')
    time.sleep(0.5)
    print('Converting Class Diagram to XMI Files...')
    diagrams.converttoxmiwithDiagrams("XMI BIAN files\CLASS DIAGRAMS",'servicedomain','NR','Domains')
    print('Completed')
    
if __name__ == "__main__":

    myarg1= sys.argv[1]

    main(myarg1)