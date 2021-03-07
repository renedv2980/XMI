from tkinter import IntVar,filedialog,messagebox,Listbox,Scrollbar,Tk,Button,OptionMenu,Frame,Checkbutton,Text,Radiobutton
import pandas as pd
from tkinter import StringVar
# from lxml import etree
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import csv
import os
import sys
import time
from progress.bar import IncrementalBar

def getExcel(arg):
    global read_file
    excel_file = arg
    read_file = pd.read_excel(excel_file, sheet_name=None)
    if not os.path.exists("All CSV Files"):
        folder = os.path.join(os.getcwd(), 'All CSV Files')
        os.makedirs(folder)
    if not os.path.exists("XMI Files For Each Tab"):
        folder = os.path.join(os.getcwd(), 'XMI Files For Each Tab')
        os.makedirs(folder)
    if not os.path.exists("Separate XMI files For Each Diagram"):
        folder = os.path.join(os.getcwd(), 'Separate XMI files For Each Diagram')
        os.makedirs(folder)
    for sheet_name in read_file:
        read_file[sheet_name].to_csv('All CSV Files\%s.csv' % sheet_name,index =None ,header=None)

def converttoxmiBIANBOMSubSuperTypeRelations():
    # create the file structure
    comntcounter =0
    uml = ET.Element('uml:Model')
    uml.set('xmi:version','2.1')
    uml.set('xmlns:xmi','http://schema.omg.org/spec/XMI/2.1')
    uml.set('xmlns:uml','http://www.eclipse.org/uml2/3.0.0/UML')
    uml.set('xmi:id','BianID')
    uml.set('name','Bian')
    eAnnotations = ET.SubElement(uml, 'eAnnotations')
    eAnnotations.set('xmi:id','AnnotationID')
    eAnnotations.set('source','Objing')
    contents = ET.SubElement(eAnnotations, 'contents')
    contents.set('xmi:type','uml:Property')
    contents.set('xmi:id','contentID')
    contents.set('name','exporterVersion')
    defaultValue=ET.SubElement(contents,'defaultValue')
    defaultValue.set('xmi:type','uml:LiteralString')
    defaultValue.set('xmi:id','stringID')
    defaultValue.set('value','3.0.0')
    # open file in read mode
    with open('All CSV Files\BIAN BOM.csv', 'r',encoding="utf-8") as read_obj:
        # pass the file object to reader() to get the reader object
        indexvalue =0
        data=[]
        data2=[]
        data3 = []
        convertedstring = str(comntcounter)
        csv_reader = csv.reader(read_obj)
        #csv_reader.replace(" ",np.nan, inplace=True)
        with open('All CSV Files\BIAN BOM SubSuperType.csv','r',encoding="utf-8") as read2_obj:
            csv_reader2 = csv.reader(read2_obj)    
        # Iterate over each row in the csv using reader object
            for row2 in csv_reader2:
                data2.append(row2[2])
                data3.append(row2[1])
            for row in csv_reader:
                data.append(row[0])
                data = list(dict.fromkeys(data))
                if not (row[2] and row[3]):
                    packageElement=ET.SubElement(uml,'packagedElement')
                    packageElement.set('xmi:type','uml:Class')
                    packageElement.set('xmi:id',row[0])
                    packageElement.set('name',row[1])
                    for y in range(2,len(data2)):
                        if row[0] == data2[y]:
                            indexvalue = data3[y]
                            genrealization = ET.SubElement(packageElement,'generalization')
                            genrealization.set('xmi:id','gen'+convertedstring)
                            genrealization.set('general',indexvalue)
                    ownedcomment=ET.SubElement(packageElement,'ownedComment')
                    ownedcomment.set('xmi:type','uml:Comment')
                    ownedcomment.set('xmi:id',convertedstring)
                    comntcounter = comntcounter +1
                    convertedstring = str(comntcounter)
                    body=ET.SubElement(ownedcomment,'body')
                    body.text=row[4]
                elif row[0] != 'UID BO' :
                    ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                    ownedAttribute.set('xmi:id',row[2])
                    ownedAttribute.set('name',row[3])
                    ownedcomment=ET.SubElement(ownedAttribute,'ownedComment')
                    ownedcomment.set('xmi:type','uml:Comment')
                    ownedcomment.set('xmi:id',convertedstring)
                    comntcounter = comntcounter +1
                    convertedstring = str(comntcounter)
                    body=ET.SubElement(ownedcomment,'body')
                    body.text=row[4]
                    types=ET.SubElement(ownedAttribute,'type')
                    types.set('xmi:type','uml:PrimitiveType')
                    types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')
    namecounter = 5555
    #relations
    with open('All CSV Files\BIAN BOM Relations.csv','r',encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            my_string = row[3]
            my_list = my_string.split(",")
            #Association
            if(my_list[0] == 'aggregation:shared'):
                packageElement=ET.SubElement(uml,'packagedElement')
                packageElement.set('xmi:type','uml:Association')
                packageElement.set('xmi:id',row[0])
                packageElement.set('name',row[1])
                con=row[2]+"a"+" "+row[4]+"b"
                packageElement.set('memberEnd',con)
                packageElement.set('navigableOwnedEnd',row[4]+"b")
                ownedEnd=ET.SubElement(packageElement,'ownedEnd')
                ownedEnd.set('xmi:id',row[2]+"a")
                namecounter = namecounter+1
                namestr=str(namecounter)
                ownedEnd.set('name',namestr)
                if(my_list[8]==' visibility:public'):
                    ownedEnd.set('visibility','public')
                elif(my_list[8]==' visibility:package'):
                    ownedEnd.set('visibility','package')
                elif(my_list[8]==' visibility:protected'):
                    ownedEnd.set('visibility','protected')
                elif(my_list[8]==' visibility:private'):
                    ownedEnd.set('visibility','private')
                if(my_list[4]==' isUnique:true'):
                    ownedEnd.set('isUnique','true')
                elif(my_list[4]==' isUnique:false'):
                    ownedEnd.set('isUnique','false')
                ownedEnd.set('type',row[2])
                ownedEnd.set('association',row[0])
                upperValue=ET.SubElement(ownedEnd,'upperValue')
                upperValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                upperValue.set('xmi:id','')
                if(my_list[7]==' upper:1'):
                    upperValue.set('value','1')
                elif(my_list[7]==' upper:0'):
                    upperValue.set('value','0')
                elif(my_list[7]==' upper:*'):
                    upperValue.set('value','*')
                lowerValue=ET.SubElement(ownedEnd,'lowerValue')
                lowerValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                lowerValue.set('xmi:id','')
                if(my_list[5]==' lower:1'):
                    lowerValue.set('value','1')
                elif(my_list[5]==' lower:0'):
                    lowerValue.set('value','0')
                elif(my_list[5]==' lower:*'):
                    lowerValue.set('value','*')
                lowerValue.set('xmi:type','uml:LiteralInteger')
                lowerValue.set('xmi:id','')

                my_string = row[5]
                my_list = my_string.split(",")
                ownedEnd2=ET.SubElement(packageElement,'ownedEnd')
                ownedEnd2.set('xmi:id',row[4]+"b")
                namecounter = namecounter+1
                namestr=str(namecounter)
                ownedEnd2.set('name',namestr)
                if(my_list[8]==' visibility:public'):
                    ownedEnd2.set('visibility','public')
                elif(my_list[8]==' visibility:package'):
                    ownedEnd2.set('visibility','package')
                elif(my_list[8]==' visibility:protected'):
                    ownedEnd2.set('visibility','protected')
                elif(my_list[8]==' visibility:private'):
                    ownedEnd2.set('visibility','private')
                if(my_list[4]==' isUnique:true'):
                    ownedEnd2.set('isUnique','true')
                elif(my_list[4]==' isUnique:false'):
                    ownedEnd2.set('isUnique','false')
                ownedEnd2.set('type',row[4])
                ownedEnd2.set('association',row[0])
                upperValue2=ET.SubElement(ownedEnd2,'upperValue')
                upperValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                upperValue2.set('xmi:id','')
                if(my_list[7]==' upper:1'):
                    upperValue2.set('value','1')
                elif(my_list[7]==' upper:0'):
                    upperValue2.set('value','0')
                elif(my_list[7]==' upper:*'):
                    upperValue2.set('value','*')
                lowerValue2=ET.SubElement(ownedEnd2,'lowerValue')
                lowerValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                lowerValue2.set('xmi:id','')
                if(my_list[5]==' lower:1'):
                    lowerValue2.set('value','1')
                elif(my_list[5]==' lower:0'):
                    lowerValue2.set('value','0')
                elif(my_list[5]==' lower:*'):
                    lowerValue2.set('value','*')
                lowerValue2.set('xmi:type','uml:LiteralInteger')
                lowerValue2.set('xmi:id','')
            #NONE
            elif(my_list[0] == 'aggregation:none'):
                packageElement=ET.SubElement(uml,'packagedElement')
                packageElement.set('xmi:type','uml:Association')
                packageElement.set('xmi:id',row[0])
                packageElement.set('name',row[1])
                ownedEnd=ET.SubElement(packageElement,'ownedEnd')
                ownedEnd.set('xmi:id',row[2]+"a")
                namecounter = namecounter+1
                namestr=str(namecounter)
                ownedEnd.set('name',namestr)
                if(my_list[8]==' visibility:public'):
                    ownedEnd.set('visibility','public')
                elif(my_list[8]==' visibility:package'):
                    ownedEnd.set('visibility','package')
                elif(my_list[8]==' visibility:protected'):
                    ownedEnd.set('visibility','protected')
                elif(my_list[8]==' visibility:private'):
                    ownedEnd.set('visibility','private')
                if(my_list[4]==' isUnique:true'):
                    ownedEnd.set('isUnique','true')
                elif(my_list[4]==' isUnique:false'):
                    ownedEnd.set('isUnique','false')
                ownedEnd.set('type',row[2])
                ownedEnd.set('association',row[0])
                upperValue=ET.SubElement(ownedEnd,'upperValue')
                upperValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                upperValue.set('xmi:id','')
                if(my_list[7]==' upper:1'):
                    upperValue.set('value','1')
                elif(my_list[7]==' upper:0'):
                    upperValue.set('value','0')
                elif(my_list[7]==' upper:*'):
                    upperValue.set('value','*')
                lowerValue=ET.SubElement(ownedEnd,'lowerValue')
                lowerValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                lowerValue.set('xmi:id','')
                if(my_list[5]==' lower:1'):
                    lowerValue.set('value','1')
                elif(my_list[5]==' lower:0'):
                    lowerValue.set('value','0')
                elif(my_list[5]==' lower:*'):
                    lowerValue.set('value','*')
                lowerValue.set('xmi:type','uml:LiteralInteger')
                lowerValue.set('xmi:id','')

                my_string = row[5]
                my_list = my_string.split(",")
                ownedEnd2=ET.SubElement(packageElement,'ownedEnd')
                ownedEnd2.set('xmi:id',row[4]+"b")
                namecounter = namecounter+1
                namestr=str(namecounter)
                ownedEnd2.set('name',namestr)
                if(my_list[8]==' visibility:public'):
                    ownedEnd2.set('visibility','public')
                elif(my_list[8]==' visibility:package'):
                    ownedEnd2.set('visibility','package')
                elif(my_list[8]==' visibility:protected'):
                    ownedEnd2.set('visibility','protected')
                elif(my_list[8]==' visibility:private'):
                    ownedEnd2.set('visibility','private')
                if(my_list[4]==' isUnique:true'):
                    ownedEnd2.set('isUnique','true')
                elif(my_list[4]==' isUnique:false'):
                    ownedEnd2.set('isUnique','false')
                ownedEnd2.set('type',row[4])
                ownedEnd2.set('association',row[0])
                upperValue2=ET.SubElement(ownedEnd2,'upperValue')
                upperValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                upperValue2.set('xmi:id','')
                if(my_list[7]==' upper:1'):
                    upperValue2.set('value','1')
                elif(my_list[7]==' upper:0'):
                    upperValue2.set('value','0')
                elif(my_list[7]==' upper:*'):
                    upperValue2.set('value','*')
                lowerValue2=ET.SubElement(ownedEnd2,'lowerValue')
                lowerValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                lowerValue2.set('xmi:id','')
                if(my_list[5]==' lower:1'):
                    lowerValue2.set('value','1')
                elif(my_list[5]==' lower:0'):
                    lowerValue2.set('value','0')
                elif(my_list[5]==' lower:*'):
                    lowerValue2.set('value','*')
                lowerValue2.set('xmi:type','uml:LiteralInteger')
                lowerValue2.set('xmi:id','')
            #Composition
            elif(my_list[0] == 'aggregation:composite'):
                packageElement=ET.SubElement(uml,'packagedElement')
                packageElement.set('xmi:type','uml:Association')
                packageElement.set('xmi:id',row[0])
                packageElement.set('name',row[1])
                con=row[2]+"a"+" "+row[4]+"b"
                packageElement.set('memberEnd',con)
                packageElement.set('navigableOwnedEnd',row[4]+"b")
                ownedEnd=ET.SubElement(packageElement,'ownedEnd')
                ownedEnd.set('xmi:id',row[2]+"a")
                namecounter = namecounter+1
                namestr=str(namecounter)
                ownedEnd.set('name',namestr)
                if(my_list[8]==' visibility:public'):
                    ownedEnd.set('visibility','public')
                elif(my_list[8]==' visibility:package'):
                    ownedEnd.set('visibility','package')
                elif(my_list[8]==' visibility:protected'):
                    ownedEnd.set('visibility','protected')
                elif(my_list[8]==' visibility:private'):
                    ownedEnd.set('visibility','private')
                if(my_list[4]==' isUnique:true'):
                    ownedEnd.set('isUnique','true')
                elif(my_list[4]==' isUnique:false'):
                    ownedEnd.set('isUnique','false')
                ownedEnd.set('type',row[2])
                ownedEnd.set('association',row[0])
                upperValue=ET.SubElement(ownedEnd,'upperValue')
                upperValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                upperValue.set('xmi:id','')
                if(my_list[7]==' upper:1'):
                    upperValue.set('value','1')
                elif(my_list[7]==' upper:0'):
                    upperValue.set('value','0')
                elif(my_list[7]==' upper:*'):
                    upperValue.set('value','*')
                lowerValue=ET.SubElement(ownedEnd,'lowerValue')
                lowerValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                lowerValue.set('xmi:id','')
                if(my_list[5]==' lower:1'):
                    lowerValue.set('value','1')
                elif(my_list[5]==' lower:0'):
                    lowerValue.set('value','0')
                elif(my_list[5]==' lower:*'):
                    lowerValue.set('value','*')
                lowerValue.set('xmi:type','uml:LiteralInteger')
                lowerValue.set('xmi:id','')

                my_string = row[5]
                my_list = my_string.split(",")
                ownedEnd2=ET.SubElement(packageElement,'ownedEnd')
                ownedEnd2.set('xmi:id',row[4]+"b")
                namecounter = namecounter+1
                namestr=str(namecounter)
                ownedEnd2.set('name',namestr)
                ownedEnd2.set('aggregation','composite')
                if(my_list[8]==' visibility:public'):
                    ownedEnd2.set('visibility','public')
                elif(my_list[8]==' visibility:package'):
                    ownedEnd2.set('visibility','package')
                elif(my_list[8]==' visibility:protected'):
                    ownedEnd2.set('visibility','protected')
                elif(my_list[8]==' visibility:private'):
                    ownedEnd2.set('visibility','private')
                if(my_list[4]==' isUnique:true'):
                    ownedEnd2.set('isUnique','true')
                elif(my_list[4]==' isUnique:false'):
                    ownedEnd2.set('isUnique','false')
                ownedEnd2.set('type',row[4])
                ownedEnd2.set('association',row[0])
                upperValue2=ET.SubElement(ownedEnd2,'upperValue')
                upperValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                upperValue2.set('xmi:id','')
                if(my_list[7]==' upper:1'):
                    upperValue2.set('value','1')
                elif(my_list[7]==' upper:0'):
                    upperValue2.set('value','0')
                elif(my_list[7]==' upper:*'):
                    upperValue2.set('value','*')
                lowerValue2=ET.SubElement(ownedEnd2,'lowerValue')
                lowerValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                lowerValue2.set('xmi:id','')
                if(my_list[5]==' lower:1'):
                    lowerValue2.set('value','1')
                elif(my_list[5]==' lower:0'):
                    lowerValue2.set('value','0')
                elif(my_list[5]==' lower:*'):
                    lowerValue2.set('value','*')
                lowerValue2.set('xmi:type','uml:LiteralInteger')
                lowerValue2.set('xmi:id','')
    # create a new XML file with the results
    mydata = ET.tostring(uml)
    x = mydata
    mydata=BeautifulSoup(x,'xml').prettify()
    myfile = open("XMI Files For Each Tab\BIAN BOM SubSuperType Relations.xml", "w",encoding="utf-8")
    myfile.write(mydata)

def converttoxmiBIANBOMSubSuperType():
    # create the file structure
    comntcounter =0
    uml = ET.Element('uml:Model')
    uml.set('xmi:version','2.1')
    uml.set('xmlns:xmi','http://schema.omg.org/spec/XMI/2.1')
    uml.set('xmlns:uml','http://www.eclipse.org/uml2/3.0.0/UML')
    uml.set('xmi:id','BianID')
    uml.set('name','Bian')
    eAnnotations = ET.SubElement(uml, 'eAnnotations')
    eAnnotations.set('xmi:id','AnnotationID')
    eAnnotations.set('source','Objing')
    contents = ET.SubElement(eAnnotations, 'contents')
    contents.set('xmi:type','uml:Property')
    contents.set('xmi:id','contentID')
    contents.set('name','exporterVersion')
    defaultValue=ET.SubElement(contents,'defaultValue')
    defaultValue.set('xmi:type','uml:LiteralString')
    defaultValue.set('xmi:id','stringID')
    defaultValue.set('value','3.0.0')
    # open file in read mode
    with open('All CSV Files\BIAN BOM.csv', 'r',encoding="utf-8") as read_obj:
        # pass the file object to reader() to get the reader object
        indexvalue =0
        data=[]
        data2=[]
        data3 = []
        convertedstring = str(comntcounter)
        csv_reader = csv.reader(read_obj)
        #csv_reader.replace(" ",np.nan, inplace=True)
        with open('All CSV Files\BIAN BOM SubSuperType.csv','r',encoding="utf-8") as read2_obj:
            csv_reader2 = csv.reader (read2_obj)    
        # Iterate over each row in the csv using reader object
            for row2 in csv_reader2:
                data2.append(row2[2])
                data3.append(row2[1])
            for row in csv_reader:
                data.append(row[0])
                data = list(dict.fromkeys(data))
                if not (row[2] and row[3]):
                    packageElement=ET.SubElement(uml,'packagedElement')
                    packageElement.set('xmi:type','uml:Class')
                    packageElement.set('xmi:id',row[0])
                    packageElement.set('name',row[1])
                    for y in range(2,len(data2)):
                        if row[0] == data2[y]:
                            indexvalue = data3[y]
                            genrealization = ET.SubElement(packageElement,'generalization')
                            genrealization.set('xmi:id','id')
                            genrealization.set('general',indexvalue)
                    ownedcomment=ET.SubElement(packageElement,'ownedComment')
                    ownedcomment.set('xmi:type','uml:Comment')
                    ownedcomment.set('xmi:id',convertedstring)
                    comntcounter = comntcounter +1
                    convertedstring = str(comntcounter)
                    body=ET.SubElement(ownedcomment,'body')
                    body.text=row[4]
                elif row[0] != 'UID BO' :
                    ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                    ownedAttribute.set('xmi:id',row[2])
                    ownedAttribute.set('name',row[3])
                    ownedcomment=ET.SubElement(ownedAttribute,'ownedComment')
                    ownedcomment.set('xmi:type','uml:Comment')
                    ownedcomment.set('xmi:id',convertedstring)
                    comntcounter = comntcounter +1
                    convertedstring = str(comntcounter)
                    body=ET.SubElement(ownedcomment,'body')
                    body.text=row[4]
                    types=ET.SubElement(ownedAttribute,'type')
                    types.set('xmi:type','uml:PrimitiveType')
                    types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')
    # create a new XML file with the results
    mydata = ET.tostring(uml)
    x = mydata
    mydata=BeautifulSoup(x,'xml').prettify()
    myfile = open("XMI Files For Each Tab\BIAN BOM SubSuperType.xml", "w",encoding="utf-8")
    myfile.write(mydata)

def converttoxmiBIANBOM():
    # create the file structure
    uml = ET.Element('uml:Model')
    uml.set('xmi:version','2.1')
    uml.set('xmlns:xmi','http://schema.omg.org/spec/XMI/2.1')
    uml.set('xmlns:uml','http://www.eclipse.org/uml2/3.0.0/UML')
    uml.set('xmi:id','BianID')
    uml.set('name','Bian')
    
    eAnnotations = ET.SubElement(uml, 'eAnnotations')
    eAnnotations.set('xmi:id','AnnotationID')
    eAnnotations.set('source','Objing')
    contents = ET.SubElement(eAnnotations, 'contents')
    contents.set('xmi:type','uml:Property')
    contents.set('xmi:id','contentID')
    contents.set('name','exporterVersion')
    
    defaultValue=ET.SubElement(contents,'defaultValue')
    defaultValue.set('xmi:type','uml:LiteralString')
    defaultValue.set('xmi:id','stringID')
    defaultValue.set('value','3.0.0')
    
    # open file in read mode
    with open('All CSV Files\BIAN BOM.csv', 'r',encoding="utf-8") as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)
        #csv_reader.replace(" ",np.nan, inplace=True)

        # Iterate over each row in the csv using reader object
        for row in csv_reader:
        
            # if not row[0]:
            #     row[0] = 'NaN'
            if not (row[2] and row[3]):
                packageElement=ET.SubElement(uml,'packagedElement')
                packageElement.set('xmi:type','uml:Class')
                packageElement.set('xmi:id',row[0])
                packageElement.set('name',row[1])
                ownedcomment=ET.SubElement(packageElement,'ownedComment')
                ownedcomment.set('xmi:id','commentid')
                body=ET.SubElement(ownedcomment,'body')
                body.text=row[4]
            elif row[0] != 'UID BO' :
                ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                ownedAttribute.set('xmi:id',row[2])
                ownedAttribute.set('name',row[3])
                ownedcomment=ET.SubElement(ownedAttribute,'ownedComment')
                ownedcomment.set('xmi:id','commentid')
                body=ET.SubElement(ownedcomment,'body')
                body.text=row[4]
                types=ET.SubElement(ownedAttribute,'type')
                types.set('xmi:type','uml:PrimitiveType')
                types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')
    
    # create a new XML file with the results
    mydata = ET.tostring(uml)
    x = mydata
    mydata=BeautifulSoup(x,'xml').prettify()
    myfile = open("XMI Files For Each Tab\BIAN BOM.xml", "w",encoding="utf-8")
    myfile.write(mydata)

def converttoxmiSDBOMOneFile():
    # create the file structure
    comntcounter =0
    uml = ET.Element('uml:Model')
    uml.set('xmi:version','2.1')
    uml.set('xmlns:xmi','http://schema.omg.org/spec/XMI/2.1')
    uml.set('xmlns:uml','http://www.eclipse.org/uml2/3.0.0/UML')
    uml.set('xmi:id','BianID')
    uml.set('name','Bian')
    eAnnotations = ET.SubElement(uml, 'eAnnotations')
    eAnnotations.set('xmi:id','AnnotationID')
    eAnnotations.set('source','Objing')
    contents = ET.SubElement(eAnnotations, 'contents')
    contents.set('xmi:type','uml:Property')
    contents.set('xmi:id','contentID')
    contents.set('name','exporterVersion')
    defaultValue=ET.SubElement(contents,'defaultValue')
    defaultValue.set('xmi:type','uml:LiteralString')
    defaultValue.set('xmi:id','stringID')
    defaultValue.set('value','3.0.0')
     # open file in read mode
    with open('All CSV Files\SDBOM.csv', 'r',encoding="utf-8") as read_obj5:
        csv_reader5 = csv.reader(read_obj5)
        DiagramName=[]
        con=''
        DiagramUID=[]
        ObjectUID=[]
        objectsCreated=[]
        saveUID=[]
        checkID=[]
        makeGeneral=[]
        for row5 in csv_reader5:
            DiagramName.append(row5[1])
            ObjectUID.append(row5[2])
            DiagramUID.append(row5[0])
    with open('All CSV Files\SDBOM.csv', 'r',encoding="utf-8") as read_obj:
        # pass the file object to reader() to get the reader object
        temp='s'
        classDiagramObjectsID=[]
        found=-1
        Duplicates=[]
        RelationDuplicates=[]
        genCounter=1
        ClassObjectUID='s'
        UIDclassdiagram=[]
        classDiagramName='d'
        UIDRelations=[]
        Relations=[]
        UIDBO=[]
        ObjectName=[]
        comm=[]
        UIDAttr=[]
        AttrName=[]
        indexvalue =0
        Specialization=[]
        Generalization = []
        convertedstring = str(comntcounter)
        csv_reader = csv.reader(read_obj)
        
        with open('All CSV Files\BIAN SDBOM Relations.csv','r',encoding="utf-8") as read2_obj:
            csv_reader2 = csv.reader(read2_obj)
            with open('All CSV Files\BIAN BOM.csv','r',encoding="utf-8") as read3_obj:
                csv_reader3 = csv.reader(read3_obj)
                with open('All CSV Files\BIAN BOM SubSuperType.csv','r',encoding="utf-8") as read4_obj:
                    csv_reader4 = csv.reader(read4_obj)    
        # Iterate over each row in the csv using reader object
                    for row4 in csv_reader4:
                        Specialization.append(row4[2])
                        Generalization.append(row4[1])
                    for row2 in csv_reader2:
                        UIDclassdiagram.append(row2[0])
                        UIDRelations.append(row2[1])
                    for row3 in csv_reader3:
                        UIDBO.append(row3[0])
                        ObjectName.append(row3[1])
                        UIDAttr.append(row3[2])
                        AttrName.append(row3[3])
                        comm.append(row3[4])
                    namecounter = 5555
                    idcounter=90078601
                    for row in csv_reader:
                    #if row[1] in search:
                        if(row[0]!='UID Class Diagram'):
                            classDiagramName=row[1]
                            ClassObjectUID=row[2]
                            if(classDiagramName!=temp):
                                for z in range(2,len(UIDRelations)):
                                    if(row[0]==UIDclassdiagram[z]):
                                        Relations.append(UIDRelations[z])
                                package=ET.SubElement(uml,'packagedElement')
                                package.set('xmi:type','uml:Package')
                                package.set('xmi:id',row[0])
                                NameChange=row[1].replace('Diagram','SD')
                                package.set('name',NameChange)
                                package.set('visibility','public')
                                temp=classDiagramName
                                #relations
                                idcounter=idcounter+78601
                                idString=str(idcounter)
                                with open('All CSV Files\BIAN BOM Relations.csv','r',encoding="utf-8") as csvfile:
                                    reader = csv.reader(csvfile)
                                    for z in range(2,len(DiagramUID)):
                                        if(classDiagramName==DiagramName[z]):
                                            classDiagramObjectsID.append(ObjectUID[z])
                                    for row in reader:
                                        my_string = row[3]
                                        my_list = my_string.split(",")
                                    #Association
                                        if(row[0] in Relations):
                                            if(my_list[0] == 'aggregation:shared'):
                                                packageElement=ET.SubElement(package,'packagedElement')
                                                packageElement.set('xmi:type','uml:Association')
                                                if(row[0] in RelationDuplicates):
                                                    packageElement.set('xmi:id',row[0]+idString)
                                                else:
                                                    packageElement.set('xmi:id',row[0])
                                                packageElement.set('name',row[1])
                                                if(row[2] and row[4] in Duplicates):
                                                    con=row[2]+idString+" "+row[4]+idString
                                                    packageElement.set('navigableOwnedEnd',row[4]+idString)
                                                elif(row[2] in Duplicates):
                                                    con=row[2]+idString+" "+row[4]+"b"
                                                    packageElement.set('navigableOwnedEnd',row[4]+"b")
                                                elif(row[4] in Duplicates):
                                                    con=row[2]+"a"+" "+row[4]+idString
                                                    packageElement.set('navigableOwnedEnd',row[4]+idString)
                                                else:
                                                    con=row[2]+"a"+" "+row[4]+"b"
                                                    packageElement.set('navigableOwnedEnd',row[4]+"b")
                                                packageElement.set('memberEnd',con)
                                                ownedEnd=ET.SubElement(packageElement,'ownedEnd')
                                                if(row[2] in Duplicates):
                                                    ownedEnd.set('xmi:id',row[2]+idString)
                                                else:
                                                    ownedEnd.set('xmi:id',row[2]+"a")
                                                namecounter = namecounter+1
                                                namestr=str(namecounter)
                                                ownedEnd.set('name',namestr)
                                                if(my_list[8]==' visibility:public'):
                                                    ownedEnd.set('visibility','public')
                                                elif(my_list[8]==' visibility:package'):
                                                    ownedEnd.set('visibility','package')
                                                elif(my_list[8]==' visibility:protected'):
                                                    ownedEnd.set('visibility','protected')
                                                elif(my_list[8]==' visibility:private'):
                                                    ownedEnd.set('visibility','private')
                                                if(my_list[4]==' isUnique:true'):
                                                    ownedEnd.set('isUnique','true')
                                                elif(my_list[4]==' isUnique:false'):
                                                    ownedEnd.set('isUnique','false')
                                                if(row[2] in Duplicates):
                                                    ownedEnd.set('type',row[2]+idString)
                                                else:
                                                    ownedEnd.set('type',row[2])
                                                if(row[0] in RelationDuplicates):
                                                    ownedEnd.set('association',row[0]+idString)
                                                else:
                                                    ownedEnd.set('association',row[0])
                                                upperValue=ET.SubElement(ownedEnd,'upperValue')
                                                upperValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                upperValue.set('xmi:id','')
                                                if(my_list[7]==' upper:1'):
                                                    upperValue.set('value','1')
                                                elif(my_list[7]==' upper:0'):
                                                    upperValue.set('value','0')
                                                elif(my_list[7]==' upper:*'):
                                                    upperValue.set('value','*')
                                                lowerValue=ET.SubElement(ownedEnd,'lowerValue')
                                                lowerValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                lowerValue.set('xmi:id','')
                                                if(my_list[5]==' lower:1'):
                                                    lowerValue.set('value','1')
                                                elif(my_list[5]==' lower:0'):
                                                    lowerValue.set('value','0')
                                                elif(my_list[5]==' lower:*'):
                                                    lowerValue.set('value','*')
                                                lowerValue.set('xmi:type','uml:LiteralInteger')
                                                lowerValue.set('xmi:id','')
                                                my_string = row[5]
                                                my_list = my_string.split(",")
                                                ownedEnd2=ET.SubElement(packageElement,'ownedEnd')
                                                if(row[4] in Duplicates):
                                                    ownedEnd2.set('xmi:id',row[4]+idString)
                                                else:
                                                    ownedEnd2.set('xmi:id',row[4]+"b")
                                                namecounter = namecounter+1
                                                namestr=str(namecounter)
                                                ownedEnd2.set('name',namestr)
                                                if(my_list[8]==' visibility:public'):
                                                    ownedEnd2.set('visibility','public')
                                                elif(my_list[8]==' visibility:package'):
                                                    ownedEnd2.set('visibility','package')
                                                elif(my_list[8]==' visibility:protected'):
                                                    ownedEnd2.set('visibility','protected')
                                                elif(my_list[8]==' visibility:private'):
                                                    ownedEnd2.set('visibility','private')
                                                if(my_list[4]==' isUnique:true'):
                                                    ownedEnd2.set('isUnique','true')
                                                elif(my_list[4]==' isUnique:false'):
                                                    ownedEnd2.set('isUnique','false')
                                                if(row[4] in Duplicates):
                                                    ownedEnd2.set('type',row[4]+idString)
                                                else:
                                                    ownedEnd2.set('type',row[4])
                                                if(row[0] in RelationDuplicates):
                                                    RelationDuplicates.remove(row[0])
                                                    ownedEnd2.set('association',row[0]+idString)
                                                else:
                                                    ownedEnd2.set('association',row[0])
                                                upperValue2=ET.SubElement(ownedEnd2,'upperValue')
                                                upperValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                upperValue2.set('xmi:id','')
                                                if(my_list[7]==' upper:1'):
                                                    upperValue2.set('value','1')
                                                elif(my_list[7]==' upper:0'):
                                                    upperValue2.set('value','0')
                                                elif(my_list[7]==' upper:*'):
                                                    upperValue2.set('value','*')
                                                lowerValue2=ET.SubElement(ownedEnd2,'lowerValue')
                                                lowerValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                lowerValue2.set('xmi:id','')
                                                if(my_list[5]==' lower:1'):
                                                    lowerValue2.set('value','1')
                                                elif(my_list[5]==' lower:0'):
                                                    lowerValue2.set('value','0')
                                                elif(my_list[5]==' lower:*'):
                                                    lowerValue2.set('value','*')
                                                lowerValue2.set('xmi:type','uml:LiteralInteger')
                                                lowerValue2.set('xmi:id','')
                                            #NONE
                                            elif(my_list[0] == 'aggregation:none'):
                                                packageElement=ET.SubElement(package,'packagedElement')
                                                packageElement.set('xmi:type','uml:Association')
                                                if(row[0] in RelationDuplicates):
                                                    packageElement.set('xmi:id',row[0]+idString)
                                                else:
                                                    packageElement.set('xmi:id',row[0])
                                                packageElement.set('name',row[1])
                                                ownedEnd=ET.SubElement(packageElement,'ownedEnd')
                                                if(row[2] in Duplicates):
                                                    ownedEnd.set('xmi:id',row[2]+idString)
                                                else:
                                                    ownedEnd.set('xmi:id',row[4]+"a")
                                                namecounter = namecounter+1
                                                namestr=str(namecounter)
                                                ownedEnd.set('name',namestr)
                                                if(my_list[8]==' visibility:public'):
                                                    ownedEnd.set('visibility','public')
                                                elif(my_list[8]==' visibility:package'):
                                                    ownedEnd.set('visibility','package')
                                                elif(my_list[8]==' visibility:protected'):
                                                    ownedEnd.set('visibility','protected')
                                                elif(my_list[8]==' visibility:private'):
                                                    ownedEnd.set('visibility','private')
                                                if(my_list[4]==' isUnique:true'):
                                                    ownedEnd.set('isUnique','true')
                                                elif(my_list[4]==' isUnique:false'):
                                                    ownedEnd.set('isUnique','false')
                                                if(row[2] in Duplicates):
                                                    ownedEnd.set('type',row[2]+idString)
                                                else:
                                                    ownedEnd.set('type',row[2])
                                                if(row[0] in RelationDuplicates):
                                                    ownedEnd.set('association',row[0]+idString)
                                                else:
                                                    ownedEnd.set('association',row[0])
                                                upperValue=ET.SubElement(ownedEnd,'upperValue')
                                                upperValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                upperValue.set('xmi:id','')
                                                if(my_list[7]==' upper:1'):
                                                    upperValue.set('value','1')
                                                elif(my_list[7]==' upper:0'):
                                                    upperValue.set('value','0')
                                                elif(my_list[7]==' upper:*'):
                                                    upperValue.set('value','*')
                                                lowerValue=ET.SubElement(ownedEnd,'lowerValue')
                                                lowerValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                lowerValue.set('xmi:id','')
                                                if(my_list[5]==' lower:1'):
                                                    lowerValue.set('value','1')
                                                elif(my_list[5]==' lower:0'):
                                                    lowerValue.set('value','0')
                                                elif(my_list[5]==' lower:*'):
                                                    lowerValue.set('value','*')
                                                lowerValue.set('xmi:type','uml:LiteralInteger')
                                                lowerValue.set('xmi:id','')
                                                my_string = row[5]
                                                my_list = my_string.split(",")
                                                ownedEnd2=ET.SubElement(packageElement,'ownedEnd')
                                                if(row[4] in Duplicates):
                                                    ownedEnd2.set('xmi:id',row[4]+idString)
                                                else:
                                                    ownedEnd2.set('xmi:id',row[4]+"b")
                                                namecounter = namecounter+1
                                                namestr=str(namecounter)
                                                ownedEnd2.set('name',namestr)
                                                if(my_list[8]==' visibility:public'):
                                                    ownedEnd2.set('visibility','public')
                                                elif(my_list[8]==' visibility:package'):
                                                    ownedEnd2.set('visibility','package')
                                                elif(my_list[8]==' visibility:protected'):
                                                    ownedEnd2.set('visibility','protected')
                                                elif(my_list[8]==' visibility:private'):
                                                    ownedEnd2.set('visibility','private')
                                                if(my_list[4]==' isUnique:true'):
                                                    ownedEnd2.set('isUnique','true')
                                                elif(my_list[4]==' isUnique:false'):
                                                    ownedEnd2.set('isUnique','false')
                                                if(row[4] in Duplicates):
                                                    ownedEnd2.set('type',row[4]+idString)
                                                else:
                                                    ownedEnd2.set('type',row[4])
                                                if(row[0] in RelationDuplicates):
                                                    RelationDuplicates.remove(row[0])
                                                    ownedEnd2.set('association',row[0]+idString)
                                                else:
                                                    ownedEnd2.set('association',row[0])
                                                upperValue2=ET.SubElement(ownedEnd2,'upperValue')
                                                upperValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                upperValue2.set('xmi:id','')
                                                if(my_list[7]==' upper:1'):
                                                    upperValue2.set('value','1')
                                                elif(my_list[7]==' upper:0'):
                                                    upperValue2.set('value','0')
                                                elif(my_list[7]==' upper:*'):
                                                    upperValue2.set('value','*')
                                                lowerValue2=ET.SubElement(ownedEnd2,'lowerValue')
                                                lowerValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                lowerValue2.set('xmi:id','')
                                                if(my_list[5]==' lower:1'):
                                                    lowerValue2.set('value','1')
                                                elif(my_list[5]==' lower:0'):
                                                    lowerValue2.set('value','0')
                                                elif(my_list[5]==' lower:*'):
                                                    lowerValue2.set('value','*')
                                                lowerValue2.set('xmi:type','uml:LiteralInteger')
                                                lowerValue2.set('xmi:id','')
                                            #Composition
                                            elif(my_list[0] == 'aggregation:composite'):
                                                packageElement=ET.SubElement(package,'packagedElement')
                                                packageElement.set('xmi:type','uml:Association')
                                                if(row[0] in RelationDuplicates):
                                                    packageElement.set('xmi:id',row[0]+idString)
                                                else:
                                                    packageElement.set('xmi:id',row[0])
                                                packageElement.set('name',row[1])
                                                if(row[2] and row[4] in Duplicates):
                                                    con=row[2]+idString+" "+row[4]+idString
                                                    packageElement.set('navigableOwnedEnd',row[4]+idString)
                                                elif(row[2] in Duplicates):
                                                    con=row[2]+idString+" "+row[4]+"b"
                                                    packageElement.set('navigableOwnedEnd',row[4]+"b")
                                                elif(row[4] in Duplicates):
                                                    con=row[2]+"a"+" "+row[4]+idString
                                                    packageElement.set('navigableOwnedEnd',row[4]+idString)
                                                else:
                                                    con=row[2]+"a"+" "+row[4]+"b"
                                                    packageElement.set('navigableOwnedEnd',row[4]+"b")
                                                packageElement.set('memberEnd',con)
                                                ownedEnd=ET.SubElement(packageElement,'ownedEnd')
                                                if(row[2] in Duplicates):
                                                    ownedEnd.set('xmi:id',row[2]+idString)
                                                else:
                                                    ownedEnd.set('xmi:id',row[2]+"a")
                                                namecounter = namecounter+1
                                                namestr=str(namecounter)
                                                ownedEnd.set('name',namestr)
                                                if(my_list[8]==' visibility:public'):
                                                    ownedEnd.set('visibility','public')
                                                elif(my_list[8]==' visibility:package'):
                                                    ownedEnd.set('visibility','package')
                                                elif(my_list[8]==' visibility:protected'):
                                                    ownedEnd.set('visibility','protected')
                                                elif(my_list[8]==' visibility:private'):
                                                    ownedEnd.set('visibility','private')
                                                if(my_list[4]==' isUnique:true'):
                                                    ownedEnd.set('isUnique','true')
                                                elif(my_list[4]==' isUnique:false'):
                                                    ownedEnd.set('isUnique','false')
                                                if(row[2] in Duplicates):
                                                    ownedEnd.set('type',row[2]+idString)
                                                else:
                                                    ownedEnd.set('type',row[2])
                                                if(row[0] in RelationDuplicates):
                                                    ownedEnd.set('association',row[0]+idString)
                                                else:
                                                    ownedEnd.set('association',row[0])
                                                upperValue=ET.SubElement(ownedEnd,'upperValue')
                                                upperValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                upperValue.set('xmi:id','')
                                                if(my_list[7]==' upper:1'):
                                                    upperValue.set('value','1')
                                                elif(my_list[7]==' upper:0'):
                                                    upperValue.set('value','0')
                                                elif(my_list[7]==' upper:*'):
                                                    upperValue.set('value','*')
                                                lowerValue=ET.SubElement(ownedEnd,'lowerValue')
                                                lowerValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                lowerValue.set('xmi:id','')
                                                if(my_list[5]==' lower:1'):
                                                    lowerValue.set('value','1')
                                                elif(my_list[5]==' lower:0'):
                                                    lowerValue.set('value','0')
                                                elif(my_list[5]==' lower:*'):
                                                    lowerValue.set('value','*')
                                                lowerValue.set('xmi:type','uml:LiteralInteger')
                                                lowerValue.set('xmi:id','')
                                                my_string = row[5]
                                                my_list = my_string.split(",")
                                                ownedEnd2=ET.SubElement(packageElement,'ownedEnd')
                                                if(row[4] in Duplicates):
                                                    ownedEnd2.set('xmi:id',row[4]+idString)
                                                else:
                                                    ownedEnd2.set('xmi:id',row[4]+"b")
                                                namecounter = namecounter+1
                                                namestr=str(namecounter)
                                                ownedEnd2.set('name',namestr)
                                                ownedEnd2.set('aggregation','composite')
                                                if(my_list[8]==' visibility:public'):
                                                    ownedEnd2.set('visibility','public')
                                                elif(my_list[8]==' visibility:package'):
                                                    ownedEnd2.set('visibility','package')
                                                elif(my_list[8]==' visibility:protected'):
                                                    ownedEnd2.set('visibility','protected')
                                                elif(my_list[8]==' visibility:private'):
                                                    ownedEnd2.set('visibility','private')
                                                if(my_list[4]==' isUnique:true'):
                                                    ownedEnd2.set('isUnique','true')
                                                elif(my_list[4]==' isUnique:false'):
                                                    ownedEnd2.set('isUnique','false')
                                                if(row[4] in Duplicates):
                                                    ownedEnd2.set('type',row[4]+idString)
                                                else:
                                                    ownedEnd2.set('type',row[4])
                                                if(row[0] in RelationDuplicates):
                                                    RelationDuplicates.remove(row[0])
                                                    ownedEnd2.set('association',row[0]+idString)
                                                else:
                                                    ownedEnd2.set('association',row[0])
                                                upperValue2=ET.SubElement(ownedEnd2,'upperValue')
                                                upperValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                upperValue2.set('xmi:id','')
                                                if(my_list[7]==' upper:1'):
                                                    upperValue2.set('value','1')
                                                elif(my_list[7]==' upper:0'):
                                                    upperValue2.set('value','0')
                                                elif(my_list[7]==' upper:*'):
                                                    upperValue2.set('value','*')
                                                lowerValue2=ET.SubElement(ownedEnd2,'lowerValue')
                                                lowerValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                lowerValue2.set('xmi:id','')
                                                if(my_list[5]==' lower:1'):
                                                    lowerValue2.set('value','1')
                                                elif(my_list[5]==' lower:0'):
                                                    lowerValue2.set('value','0')
                                                elif(my_list[5]==' lower:*'):
                                                    lowerValue2.set('value','*')
                                                lowerValue2.set('xmi:type','uml:LiteralInteger')
                                                lowerValue2.set('xmi:id','')
                                    for z in range(0,len(Relations)):
                                            RelationDuplicates.append(Relations[z])
                                    for z in range(0,len(classDiagramObjectsID)):
                                            Duplicates.append(classDiagramObjectsID[z])
                                    Duplicates = list(dict.fromkeys(Duplicates))
                                    classDiagramObjectsID.clear()
                                    Relations.clear() 
                        for y in range(2,len(UIDBO)):
                            if(ClassObjectUID==UIDBO[y]):
                                if not ( UIDAttr[y] and AttrName[y]):
                                    temp=classDiagramName
                                    packageElement=ET.SubElement(package,'packagedElement')
                                    packageElement.set('xmi:type','uml:Class')
                                    if(UIDBO[y] in objectsCreated):
                                        packageElement.set('xmi:id',UIDBO[y]+idString)
                                    else:
                                        packageElement.set('xmi:id',UIDBO[y])
                                    packageElement.set('name',ObjectName[y])
                                    for x in range(2,len(Specialization)):
                                        if UIDBO[y] == Specialization[x]:
                                            indexvalue = Generalization[x]
                                            for z in range(2,len(ObjectUID)): 
                                                if( classDiagramName == DiagramName[z]):
                                                    saveUID.append(ObjectUID[z])
                                            if(indexvalue in saveUID):
                                                found=1
                                            else:
                                                found=0
                                                makeGeneral.append(indexvalue)
                                            genrealization = ET.SubElement(packageElement,'generalization')
                                            genrealization.set('xmi:type','uml:Generalization')
                                            convertedGen = str(genCounter)
                                            genrealization.set('xmi:id','gen'+convertedGen)
                                            genCounter=genCounter+1
                                            genrealization.set('general',indexvalue)
                                    ownedcomment=ET.SubElement(packageElement,'ownedComment')
                                    ownedcomment.set('xmi:type','uml:Comment')
                                    ownedcomment.set('xmi:id','comm'+convertedstring)
                                    comntcounter = comntcounter +1
                                    convertedstring = str(comntcounter)
                                    body=ET.SubElement(ownedcomment,'body')
                                    body.text=comm[y]
                                    objectsCreated.append(UIDBO[y])
                                elif UIDBO[y] != 'UID BO' :
                                    ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                                    if(UIDBO[y] in objectsCreated):
                                        ownedAttribute.set('xmi:id',UIDAttr[y]+idString)
                                    else:
                                        ownedAttribute.set('xmi:id',UIDAttr[y])
                                    ownedAttribute.set('name',AttrName[y])
                                    ownedcomment=ET.SubElement(ownedAttribute,'ownedComment')
                                    ownedcomment.set('xmi:type','uml:Comment')
                                    ownedcomment.set('xmi:id','comm'+convertedstring)
                                    comntcounter = comntcounter +1
                                    convertedstring = str(comntcounter)
                                    body=ET.SubElement(ownedcomment,'body')
                                    body.text=comm[y]
                                    types=ET.SubElement(ownedAttribute,'type')
                                    types.set('xmi:type','uml:PrimitiveType')
                                    types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')
                        if(found==0):
                            found=-1
                            for x in range(0,len(makeGeneral)):
                                for d in range(2,len(UIDBO)):
                                    if(makeGeneral[x] not in checkID):
                                        if (makeGeneral[x]==UIDBO[d]):
                                            if not ( UIDAttr[d] and AttrName[d]):
                                                packageElement=ET.SubElement(package,'packagedElement')
                                                packageElement.set('xmi:type','uml:Class')
                                                packageElement.set('xmi:id',UIDBO[d])
                                                packageElement.set('name',ObjectName[d])
                                                ownedcomment=ET.SubElement(packageElement,'ownedComment')
                                                ownedcomment.set('xmi:type','uml:Comment')
                                                ownedcomment.set('xmi:id','comm'+convertedstring)
                                                comntcounter = comntcounter +1
                                                convertedstring = str(comntcounter)
                                                body=ET.SubElement(ownedcomment,'body')
                                                body.text=comm[d]
                                            elif UIDBO[d] != 'UID BO' :
                                                ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                                                ownedAttribute.set('xmi:id',UIDAttr[d])
                                                ownedAttribute.set('name',AttrName[d])
                                                ownedcomment=ET.SubElement(ownedAttribute,'ownedComment')
                                                ownedcomment.set('xmi:type','uml:Comment')
                                                ownedcomment.set('xmi:id','comm'+convertedstring)
                                                comntcounter = comntcounter +1
                                                convertedstring = str(comntcounter)
                                                body=ET.SubElement(ownedcomment,'body')
                                                body.text=comm[d]
                                                types=ET.SubElement(ownedAttribute,'type')
                                                types.set('xmi:type','uml:PrimitiveType')
                                                types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')
                                            checkID.append(makeGeneral[x])



    # create a new XML file with the results
    mydata = ET.tostring(uml)
    x = mydata
    mydata=BeautifulSoup(x,'xml').prettify()
    myfile = open("XMI Files For Each Tab\ALL SDBOM Relations OneFile.xml", "w",encoding="utf-8")
    myfile.write(mydata)

def converttoxmiSDBOMSeparateFile():
        # create the file structure
    comntcounter =0
    DName=[]
    with open('All CSV Files\SDBOM.csv', 'r',encoding="utf-8") as read_obj5:
            csv_reader = csv.reader(read_obj5)
            for row in csv_reader:
                DName.append(row[1])
                DName = list(dict.fromkeys(DName))
            DName.pop(0)
            DName.pop(0)

    while DName:
        find=DName[0]
        DName.pop(0)
        uml = ET.Element('uml:Model')
        uml.set('xmi:version','2.1')
        uml.set('xmlns:xmi','http://schema.omg.org/spec/XMI/2.1')
        uml.set('xmlns:uml','http://www.eclipse.org/uml2/3.0.0/UML')
        uml.set('xmi:id','BianID')
        uml.set('name','Bian')
        eAnnotations = ET.SubElement(uml, 'eAnnotations')
        eAnnotations.set('xmi:id','AnnotationID')
        eAnnotations.set('source','Objing')
        contents = ET.SubElement(eAnnotations, 'contents')
        contents.set('xmi:type','uml:Property')
        contents.set('xmi:id','contentID')
        contents.set('name','exporterVersion')
        defaultValue=ET.SubElement(contents,'defaultValue')
        defaultValue.set('xmi:type','uml:LiteralString')
        defaultValue.set('xmi:id','stringID')
        defaultValue.set('value','3.0.0')
         # open file in read mode
        with open('All CSV Files\SDBOM.csv', 'r',encoding="utf-8") as read_obj5:
            csv_reader5 = csv.reader(read_obj5)
            DiagramName=[]
            con=''
            DiagramUID=[]
            ObjectUID=[]
            objectsCreated=[]
            saveUID=[]
            checkID=[]
            makeGeneral=[]
            for row5 in csv_reader5:
                DiagramName.append(row5[1])
                ObjectUID.append(row5[2])
                DiagramUID.append(row5[0])
        with open('All CSV Files\SDBOM.csv', 'r',encoding="utf-8") as read_obj:
            # pass the file object to reader() to get the reader object
            temp='s'
            classDiagramObjectsID=[]
            found=-1
            Duplicates=[]
            RelationDuplicates=[]
            genCounter=1
            ClassObjectUID='s'
            UIDclassdiagram=[]
            classDiagramName='d'
            UIDRelations=[]
            Relations=[]
            UIDBO=[]
            ObjectName=[]
            comm=[]
            UIDAttr=[]
            AttrName=[]
            indexvalue =0
            Specialization=[]
            Generalization = []
            convertedstring = str(comntcounter)
            csv_reader = csv.reader(read_obj)

            with open('All CSV Files\BIAN SDBOM Relations.csv','r',encoding="utf-8") as read2_obj:
                csv_reader2 = csv.reader(read2_obj)
                with open('All CSV Files\BIAN BOM.csv','r',encoding="utf-8") as read3_obj:
                    csv_reader3 = csv.reader(read3_obj)
                    with open('All CSV Files\BIAN BOM SubSuperType.csv','r',encoding="utf-8") as read4_obj:
                        csv_reader4 = csv.reader(read4_obj)    
            # Iterate over each row in the csv using reader object
                        for row4 in csv_reader4:
                            Specialization.append(row4[2])
                            Generalization.append(row4[1])
                        for row2 in csv_reader2:
                            UIDclassdiagram.append(row2[0])
                            UIDRelations.append(row2[1])
                        for row3 in csv_reader3:
                            UIDBO.append(row3[0])
                            ObjectName.append(row3[1])
                            UIDAttr.append(row3[2])
                            AttrName.append(row3[3])
                            comm.append(row3[4])
                        namecounter = 5555
                        idcounter=90078601
                        for row in csv_reader:
                            if row[1] == find:
                                if(row[0]!='UID Class Diagram'):
                                    classDiagramName=row[1]
                                    ClassObjectUID=row[2]
                                    if(classDiagramName!=temp):
                                        for z in range(2,len(UIDRelations)):
                                            if(row[0]==UIDclassdiagram[z]):
                                                Relations.append(UIDRelations[z])
                                        package=ET.SubElement(uml,'packagedElement')
                                        package.set('xmi:type','uml:Package')
                                        package.set('xmi:id',row[0])
                                        NameChange=row[1].replace('Diagram','SD')
                                        package.set('name',NameChange)
                                        package.set('visibility','public')
                                        temp=classDiagramName
                                        #relations
                                        idcounter=idcounter+78601
                                        idString=str(idcounter)
                                        with open('All CSV Files\BIAN BOM Relations.csv','r',encoding="utf-8") as csvfile:
                                            reader = csv.reader(csvfile)
                                            for z in range(2,len(DiagramUID)):
                                                if(classDiagramName==DiagramName[z]):
                                                    classDiagramObjectsID.append(ObjectUID[z])
                                            for row in reader:
                                                my_string = row[3]
                                                my_list = my_string.split(",")
                                            #Association
                                                if(row[0] in Relations):
                                                    if(my_list[0] == 'aggregation:shared'):
                                                        packageElement=ET.SubElement(package,'packagedElement')
                                                        packageElement.set('xmi:type','uml:Association')
                                                        if(row[0] in RelationDuplicates):
                                                            packageElement.set('xmi:id',row[0]+idString)
                                                        else:
                                                            packageElement.set('xmi:id',row[0])
                                                        packageElement.set('name',row[1])
                                                        if(row[2] and row[4] in Duplicates):
                                                            con=row[2]+idString+" "+row[4]+idString
                                                            packageElement.set('navigableOwnedEnd',row[4]+idString)
                                                        elif(row[2] in Duplicates):
                                                            con=row[2]+idString+" "+row[4]+"b"
                                                            packageElement.set('navigableOwnedEnd',row[4]+"b")
                                                        elif(row[4] in Duplicates):
                                                            con=row[2]+"a"+" "+row[4]+idString
                                                            packageElement.set('navigableOwnedEnd',row[4]+idString)
                                                        else:
                                                            con=row[2]+"a"+" "+row[4]+"b"
                                                            packageElement.set('navigableOwnedEnd',row[4]+"b")
                                                        packageElement.set('memberEnd',con)
                                                        ownedEnd=ET.SubElement(packageElement,'ownedEnd')
                                                        if(row[2] in Duplicates):
                                                            ownedEnd.set('xmi:id',row[2]+idString)
                                                        else:
                                                            ownedEnd.set('xmi:id',row[2]+"a")
                                                        namecounter = namecounter+1
                                                        namestr=str(namecounter)
                                                        ownedEnd.set('name',namestr)
                                                        if(my_list[8]==' visibility:public'):
                                                            ownedEnd.set('visibility','public')
                                                        elif(my_list[8]==' visibility:package'):
                                                            ownedEnd.set('visibility','package')
                                                        elif(my_list[8]==' visibility:protected'):
                                                            ownedEnd.set('visibility','protected')
                                                        elif(my_list[8]==' visibility:private'):
                                                            ownedEnd.set('visibility','private')
                                                        if(my_list[4]==' isUnique:true'):
                                                            ownedEnd.set('isUnique','true')
                                                        elif(my_list[4]==' isUnique:false'):
                                                            ownedEnd.set('isUnique','false')
                                                        if(row[2] in Duplicates):
                                                            ownedEnd.set('type',row[2]+idString)
                                                        else:
                                                            ownedEnd.set('type',row[2])
                                                        if(row[0] in RelationDuplicates):
                                                            ownedEnd.set('association',row[0]+idString)
                                                        else:
                                                            ownedEnd.set('association',row[0])
                                                        upperValue=ET.SubElement(ownedEnd,'upperValue')
                                                        upperValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                        upperValue.set('xmi:id','')
                                                        if(my_list[7]==' upper:1'):
                                                            upperValue.set('value','1')
                                                        elif(my_list[7]==' upper:0'):
                                                            upperValue.set('value','0')
                                                        elif(my_list[7]==' upper:*'):
                                                            upperValue.set('value','*')
                                                        lowerValue=ET.SubElement(ownedEnd,'lowerValue')
                                                        lowerValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                        lowerValue.set('xmi:id','')
                                                        if(my_list[5]==' lower:1'):
                                                            lowerValue.set('value','1')
                                                        elif(my_list[5]==' lower:0'):
                                                            lowerValue.set('value','0')
                                                        elif(my_list[5]==' lower:*'):
                                                            lowerValue.set('value','*')
                                                        lowerValue.set('xmi:type','uml:LiteralInteger')
                                                        lowerValue.set('xmi:id','')
                                                        my_string = row[5]
                                                        my_list = my_string.split(",")
                                                        ownedEnd2=ET.SubElement(packageElement,'ownedEnd')
                                                        if(row[4] in Duplicates):
                                                            ownedEnd2.set('xmi:id',row[4]+idString)
                                                        else:
                                                            ownedEnd2.set('xmi:id',row[4]+"b")
                                                        namecounter = namecounter+1
                                                        namestr=str(namecounter)
                                                        ownedEnd2.set('name',namestr)
                                                        if(my_list[8]==' visibility:public'):
                                                            ownedEnd2.set('visibility','public')
                                                        elif(my_list[8]==' visibility:package'):
                                                            ownedEnd2.set('visibility','package')
                                                        elif(my_list[8]==' visibility:protected'):
                                                            ownedEnd2.set('visibility','protected')
                                                        elif(my_list[8]==' visibility:private'):
                                                            ownedEnd2.set('visibility','private')
                                                        if(my_list[4]==' isUnique:true'):
                                                            ownedEnd2.set('isUnique','true')
                                                        elif(my_list[4]==' isUnique:false'):
                                                            ownedEnd2.set('isUnique','false')
                                                        if(row[4] in Duplicates):
                                                            ownedEnd2.set('type',row[4]+idString)
                                                        else:
                                                            ownedEnd2.set('type',row[4])
                                                        if(row[0] in RelationDuplicates):
                                                            RelationDuplicates.remove(row[0])
                                                            ownedEnd2.set('association',row[0]+idString)
                                                        else:
                                                            ownedEnd2.set('association',row[0])
                                                        upperValue2=ET.SubElement(ownedEnd2,'upperValue')
                                                        upperValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                        upperValue2.set('xmi:id','')
                                                        if(my_list[7]==' upper:1'):
                                                            upperValue2.set('value','1')
                                                        elif(my_list[7]==' upper:0'):
                                                            upperValue2.set('value','0')
                                                        elif(my_list[7]==' upper:*'):
                                                            upperValue2.set('value','*')
                                                        lowerValue2=ET.SubElement(ownedEnd2,'lowerValue')
                                                        lowerValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                        lowerValue2.set('xmi:id','')
                                                        if(my_list[5]==' lower:1'):
                                                            lowerValue2.set('value','1')
                                                        elif(my_list[5]==' lower:0'):
                                                            lowerValue2.set('value','0')
                                                        elif(my_list[5]==' lower:*'):
                                                            lowerValue2.set('value','*')
                                                        lowerValue2.set('xmi:type','uml:LiteralInteger')
                                                        lowerValue2.set('xmi:id','')
                                                    #NONE
                                                    elif(my_list[0] == 'aggregation:none'):
                                                        packageElement=ET.SubElement(package,'packagedElement')
                                                        packageElement.set('xmi:type','uml:Association')
                                                        if(row[0] in RelationDuplicates):
                                                            packageElement.set('xmi:id',row[0]+idString)
                                                        else:
                                                            packageElement.set('xmi:id',row[0])
                                                        packageElement.set('name',row[1])
                                                        ownedEnd=ET.SubElement(packageElement,'ownedEnd')
                                                        if(row[2] in Duplicates):
                                                            ownedEnd.set('xmi:id',row[2]+idString)
                                                        else:
                                                            ownedEnd.set('xmi:id',row[4]+"a")
                                                        namecounter = namecounter+1
                                                        namestr=str(namecounter)
                                                        ownedEnd.set('name',namestr)
                                                        if(my_list[8]==' visibility:public'):
                                                            ownedEnd.set('visibility','public')
                                                        elif(my_list[8]==' visibility:package'):
                                                            ownedEnd.set('visibility','package')
                                                        elif(my_list[8]==' visibility:protected'):
                                                            ownedEnd.set('visibility','protected')
                                                        elif(my_list[8]==' visibility:private'):
                                                            ownedEnd.set('visibility','private')
                                                        if(my_list[4]==' isUnique:true'):
                                                            ownedEnd.set('isUnique','true')
                                                        elif(my_list[4]==' isUnique:false'):
                                                            ownedEnd.set('isUnique','false')
                                                        if(row[2] in Duplicates):
                                                            ownedEnd.set('type',row[2]+idString)
                                                        else:
                                                            ownedEnd.set('type',row[2])
                                                        if(row[0] in RelationDuplicates):
                                                            ownedEnd.set('association',row[0]+idString)
                                                        else:
                                                            ownedEnd.set('association',row[0])
                                                        upperValue=ET.SubElement(ownedEnd,'upperValue')
                                                        upperValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                        upperValue.set('xmi:id','')
                                                        if(my_list[7]==' upper:1'):
                                                            upperValue.set('value','1')
                                                        elif(my_list[7]==' upper:0'):
                                                            upperValue.set('value','0')
                                                        elif(my_list[7]==' upper:*'):
                                                            upperValue.set('value','*')
                                                        lowerValue=ET.SubElement(ownedEnd,'lowerValue')
                                                        lowerValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                        lowerValue.set('xmi:id','')
                                                        if(my_list[5]==' lower:1'):
                                                            lowerValue.set('value','1')
                                                        elif(my_list[5]==' lower:0'):
                                                            lowerValue.set('value','0')
                                                        elif(my_list[5]==' lower:*'):
                                                            lowerValue.set('value','*')
                                                        lowerValue.set('xmi:type','uml:LiteralInteger')
                                                        lowerValue.set('xmi:id','')
                                                        my_string = row[5]
                                                        my_list = my_string.split(",")
                                                        ownedEnd2=ET.SubElement(packageElement,'ownedEnd')
                                                        if(row[4] in Duplicates):
                                                            ownedEnd2.set('xmi:id',row[4]+idString)
                                                        else:
                                                            ownedEnd2.set('xmi:id',row[4]+"b")
                                                        namecounter = namecounter+1
                                                        namestr=str(namecounter)
                                                        ownedEnd2.set('name',namestr)
                                                        if(my_list[8]==' visibility:public'):
                                                            ownedEnd2.set('visibility','public')
                                                        elif(my_list[8]==' visibility:package'):
                                                            ownedEnd2.set('visibility','package')
                                                        elif(my_list[8]==' visibility:protected'):
                                                            ownedEnd2.set('visibility','protected')
                                                        elif(my_list[8]==' visibility:private'):
                                                            ownedEnd2.set('visibility','private')
                                                        if(my_list[4]==' isUnique:true'):
                                                            ownedEnd2.set('isUnique','true')
                                                        elif(my_list[4]==' isUnique:false'):
                                                            ownedEnd2.set('isUnique','false')
                                                        if(row[4] in Duplicates):
                                                            ownedEnd2.set('type',row[4]+idString)
                                                        else:
                                                            ownedEnd2.set('type',row[4])
                                                        if(row[0] in RelationDuplicates):
                                                            RelationDuplicates.remove(row[0])
                                                            ownedEnd2.set('association',row[0]+idString)
                                                        else:
                                                            ownedEnd2.set('association',row[0])
                                                        upperValue2=ET.SubElement(ownedEnd2,'upperValue')
                                                        upperValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                        upperValue2.set('xmi:id','')
                                                        if(my_list[7]==' upper:1'):
                                                            upperValue2.set('value','1')
                                                        elif(my_list[7]==' upper:0'):
                                                            upperValue2.set('value','0')
                                                        elif(my_list[7]==' upper:*'):
                                                            upperValue2.set('value','*')
                                                        lowerValue2=ET.SubElement(ownedEnd2,'lowerValue')
                                                        lowerValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                        lowerValue2.set('xmi:id','')
                                                        if(my_list[5]==' lower:1'):
                                                            lowerValue2.set('value','1')
                                                        elif(my_list[5]==' lower:0'):
                                                            lowerValue2.set('value','0')
                                                        elif(my_list[5]==' lower:*'):
                                                            lowerValue2.set('value','*')
                                                        lowerValue2.set('xmi:type','uml:LiteralInteger')
                                                        lowerValue2.set('xmi:id','')
                                                    #Composition
                                                    elif(my_list[0] == 'aggregation:composite'):
                                                        packageElement=ET.SubElement(package,'packagedElement')
                                                        packageElement.set('xmi:type','uml:Association')
                                                        if(row[0] in RelationDuplicates):
                                                            packageElement.set('xmi:id',row[0]+idString)
                                                        else:
                                                            packageElement.set('xmi:id',row[0])
                                                        packageElement.set('name',row[1])
                                                        if(row[2] and row[4] in Duplicates):
                                                            con=row[2]+idString+" "+row[4]+idString
                                                            packageElement.set('navigableOwnedEnd',row[4]+idString)
                                                        elif(row[2] in Duplicates):
                                                            con=row[2]+idString+" "+row[4]+"b"
                                                            packageElement.set('navigableOwnedEnd',row[4]+"b")
                                                        elif(row[4] in Duplicates):
                                                            con=row[2]+"a"+" "+row[4]+idString
                                                            packageElement.set('navigableOwnedEnd',row[4]+idString)
                                                        else:
                                                            con=row[2]+"a"+" "+row[4]+"b"
                                                            packageElement.set('navigableOwnedEnd',row[4]+"b")
                                                        packageElement.set('memberEnd',con)
                                                        ownedEnd=ET.SubElement(packageElement,'ownedEnd')
                                                        if(row[2] in Duplicates):
                                                            ownedEnd.set('xmi:id',row[2]+idString)
                                                        else:
                                                            ownedEnd.set('xmi:id',row[2]+"a")
                                                        namecounter = namecounter+1
                                                        namestr=str(namecounter)
                                                        ownedEnd.set('name',namestr)
                                                        if(my_list[8]==' visibility:public'):
                                                            ownedEnd.set('visibility','public')
                                                        elif(my_list[8]==' visibility:package'):
                                                            ownedEnd.set('visibility','package')
                                                        elif(my_list[8]==' visibility:protected'):
                                                            ownedEnd.set('visibility','protected')
                                                        elif(my_list[8]==' visibility:private'):
                                                            ownedEnd.set('visibility','private')
                                                        if(my_list[4]==' isUnique:true'):
                                                            ownedEnd.set('isUnique','true')
                                                        elif(my_list[4]==' isUnique:false'):
                                                            ownedEnd.set('isUnique','false')
                                                        if(row[2] in Duplicates):
                                                            ownedEnd.set('type',row[2]+idString)
                                                        else:
                                                            ownedEnd.set('type',row[2])
                                                        if(row[0] in RelationDuplicates):
                                                            ownedEnd.set('association',row[0]+idString)
                                                        else:
                                                            ownedEnd.set('association',row[0])
                                                        upperValue=ET.SubElement(ownedEnd,'upperValue')
                                                        upperValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                        upperValue.set('xmi:id','')
                                                        if(my_list[7]==' upper:1'):
                                                            upperValue.set('value','1')
                                                        elif(my_list[7]==' upper:0'):
                                                            upperValue.set('value','0')
                                                        elif(my_list[7]==' upper:*'):
                                                            upperValue.set('value','*')
                                                        lowerValue=ET.SubElement(ownedEnd,'lowerValue')
                                                        lowerValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                        lowerValue.set('xmi:id','')
                                                        if(my_list[5]==' lower:1'):
                                                            lowerValue.set('value','1')
                                                        elif(my_list[5]==' lower:0'):
                                                            lowerValue.set('value','0')
                                                        elif(my_list[5]==' lower:*'):
                                                            lowerValue.set('value','*')
                                                        lowerValue.set('xmi:type','uml:LiteralInteger')
                                                        lowerValue.set('xmi:id','')
                                                        my_string = row[5]
                                                        my_list = my_string.split(",")
                                                        ownedEnd2=ET.SubElement(packageElement,'ownedEnd')
                                                        if(row[4] in Duplicates):
                                                            ownedEnd2.set('xmi:id',row[4]+idString)
                                                        else:
                                                            ownedEnd2.set('xmi:id',row[4]+"b")
                                                        namecounter = namecounter+1
                                                        namestr=str(namecounter)
                                                        ownedEnd2.set('name',namestr)
                                                        ownedEnd2.set('aggregation','composite')
                                                        if(my_list[8]==' visibility:public'):
                                                            ownedEnd2.set('visibility','public')
                                                        elif(my_list[8]==' visibility:package'):
                                                            ownedEnd2.set('visibility','package')
                                                        elif(my_list[8]==' visibility:protected'):
                                                            ownedEnd2.set('visibility','protected')
                                                        elif(my_list[8]==' visibility:private'):
                                                            ownedEnd2.set('visibility','private')
                                                        if(my_list[4]==' isUnique:true'):
                                                            ownedEnd2.set('isUnique','true')
                                                        elif(my_list[4]==' isUnique:false'):
                                                            ownedEnd2.set('isUnique','false')
                                                        if(row[4] in Duplicates):
                                                            ownedEnd2.set('type',row[4]+idString)
                                                        else:
                                                            ownedEnd2.set('type',row[4])
                                                        if(row[0] in RelationDuplicates):
                                                            RelationDuplicates.remove(row[0])
                                                            ownedEnd2.set('association',row[0]+idString)
                                                        else:
                                                            ownedEnd2.set('association',row[0])
                                                        upperValue2=ET.SubElement(ownedEnd2,'upperValue')
                                                        upperValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                        upperValue2.set('xmi:id','')
                                                        if(my_list[7]==' upper:1'):
                                                            upperValue2.set('value','1')
                                                        elif(my_list[7]==' upper:0'):
                                                            upperValue2.set('value','0')
                                                        elif(my_list[7]==' upper:*'):
                                                            upperValue2.set('value','*')
                                                        lowerValue2=ET.SubElement(ownedEnd2,'lowerValue')
                                                        lowerValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                        lowerValue2.set('xmi:id','')
                                                        if(my_list[5]==' lower:1'):
                                                            lowerValue2.set('value','1')
                                                        elif(my_list[5]==' lower:0'):
                                                            lowerValue2.set('value','0')
                                                        elif(my_list[5]==' lower:*'):
                                                            lowerValue2.set('value','*')
                                                        lowerValue2.set('xmi:type','uml:LiteralInteger')
                                                        lowerValue2.set('xmi:id','')
                                            for z in range(0,len(Relations)):
                                                    RelationDuplicates.append(Relations[z])
                                            for z in range(0,len(classDiagramObjectsID)):
                                                    Duplicates.append(classDiagramObjectsID[z])
                                            Duplicates = list(dict.fromkeys(Duplicates))
                                            classDiagramObjectsID.clear()
                                            Relations.clear() 
                                for y in range(2,len(UIDBO)):
                                    if(ClassObjectUID==UIDBO[y]):
                                        if not ( UIDAttr[y] and AttrName[y]):
                                            temp=classDiagramName
                                            packageElement=ET.SubElement(package,'packagedElement')
                                            packageElement.set('xmi:type','uml:Class')
                                            if(UIDBO[y] in objectsCreated):
                                                packageElement.set('xmi:id',UIDBO[y]+idString)
                                            else:
                                                packageElement.set('xmi:id',UIDBO[y])
                                            packageElement.set('name',ObjectName[y])
                                            for x in range(2,len(Specialization)):
                                                if UIDBO[y] == Specialization[x]:
                                                    indexvalue = Generalization[x]
                                                    for z in range(2,len(ObjectUID)): 
                                                        if( classDiagramName == DiagramName[z]):
                                                            saveUID.append(ObjectUID[z])
                                                    if(indexvalue in saveUID):
                                                        found=1
                                                    else:
                                                        found=0
                                                        makeGeneral.append(indexvalue)
                                                    genrealization = ET.SubElement(packageElement,'generalization')
                                                    genrealization.set('xmi:type','uml:Generalization')
                                                    convertedGen = str(genCounter)
                                                    genrealization.set('xmi:id','gen'+convertedGen)
                                                    genCounter=genCounter+1
                                                    genrealization.set('general',indexvalue)
                                            ownedcomment=ET.SubElement(packageElement,'ownedComment')
                                            ownedcomment.set('xmi:type','uml:Comment')
                                            ownedcomment.set('xmi:id','comm'+convertedstring)
                                            comntcounter = comntcounter +1
                                            convertedstring = str(comntcounter)
                                            body=ET.SubElement(ownedcomment,'body')
                                            body.text=comm[y]
                                            objectsCreated.append(UIDBO[y])
                                        elif UIDBO[y] != 'UID BO' :
                                            ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                                            ownedAttribute.set('xmi:id',UIDAttr[y])
                                            ownedAttribute.set('name',AttrName[y])
                                            ownedcomment=ET.SubElement(ownedAttribute,'ownedComment')
                                            ownedcomment.set('xmi:type','uml:Comment')
                                            ownedcomment.set('xmi:id','comm'+convertedstring)
                                            comntcounter = comntcounter +1
                                            convertedstring = str(comntcounter)
                                            body=ET.SubElement(ownedcomment,'body')
                                            body.text=comm[y]
                                            types=ET.SubElement(ownedAttribute,'type')
                                            types.set('xmi:type','uml:PrimitiveType')
                                            types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')
                                if(found==0):
                                    found=-1
                                    for x in range(0,len(makeGeneral)):
                                        for d in range(2,len(UIDBO)):
                                            if(makeGeneral[x] not in checkID):
                                                if (makeGeneral[x]==UIDBO[d]):
                                                    if not ( UIDAttr[d] and AttrName[d]):
                                                        packageElement=ET.SubElement(package,'packagedElement')
                                                        packageElement.set('xmi:type','uml:Class')
                                                        packageElement.set('xmi:id',UIDBO[d])
                                                        packageElement.set('name',ObjectName[d])
                                                        ownedcomment=ET.SubElement(packageElement,'ownedComment')
                                                        ownedcomment.set('xmi:type','uml:Comment')
                                                        ownedcomment.set('xmi:id','comm'+convertedstring)
                                                        comntcounter = comntcounter +1
                                                        convertedstring = str(comntcounter)
                                                        body=ET.SubElement(ownedcomment,'body')
                                                        body.text=comm[d]
                                                    elif UIDBO[d] != 'UID BO' :
                                                        ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                                                        ownedAttribute.set('xmi:id',UIDAttr[d])
                                                        ownedAttribute.set('name',AttrName[d])
                                                        ownedcomment=ET.SubElement(ownedAttribute,'ownedComment')
                                                        ownedcomment.set('xmi:type','uml:Comment')
                                                        ownedcomment.set('xmi:id','comm'+convertedstring)
                                                        comntcounter = comntcounter +1
                                                        convertedstring = str(comntcounter)
                                                        body=ET.SubElement(ownedcomment,'body')
                                                        body.text=comm[d]
                                                        types=ET.SubElement(ownedAttribute,'type')
                                                        types.set('xmi:type','uml:PrimitiveType')
                                                        types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')
                                                    checkID.append(makeGeneral[x])



        # create a new XML file with the results
        mydata = ET.tostring(uml)
        x = mydata
        mydata=BeautifulSoup(x,'xml').prettify()
        myfile = open("Separate XMI files For Each Diagram/"+find+".xml", "w",encoding="utf-8")
        myfile.write(mydata)
        print(find+' File Converted')

def main(arg):
    print('Converting Excel to CSV...')
    getExcel(arg)
    print('Completed')
    time.sleep(0.5)
    print('Converting BIAN BOM CSV to XMI...')
    converttoxmiBIANBOM()
    print('Completed')
    time.sleep(0.5)
    print('Converting BIAN BOM SubSuper Type CSV to XMI...')
    converttoxmiBIANBOMSubSuperType()
    print('Completed')
    time.sleep(0.5)
    print('Converting BIAN BOM SubSuper Type Relations CSV to XMI...')
    converttoxmiBIANBOMSubSuperTypeRelations()
    print('Completed')
    time.sleep(0.5)
    print('Converting SDBOM CSV to XMI One File...')
    converttoxmiSDBOMOneFile()
    print('Completed')
    time.sleep(0.5)
    print('Converting SDBOM CSV to XMI Separate File...')
    converttoxmiSDBOMSeparateFile()
    print('Completed')
   



if __name__ == "__main__":

    myarg1= sys.argv[1]

    main(myarg1)