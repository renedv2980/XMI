import pandas as pd
# from lxml import etree
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import csv
import os
import sys
import time
from glob import glob
from xlrd import open_workbook



#def getExcel():
def getExcel(arg):
    global read_file
#        path = glob(os.path.join(os.getcwd(), "*.xlsx"))[0]
#   except IndexError:
#        raise IOError("No .xlsx files found in %r" % os.getcwd())
#        return
#   excel_file = path
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
def converttoxmiBIANBOM():
    # create the file structure
    EnumDuplicateCheck=[]
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
            if row[0]=='Class':
                packageElement=ET.SubElement(uml,'packagedElement')
                packageElement.set('xmi:type','uml:Class')
                packageElement.set('xmi:id',row[1])
                packageElement.set('name',row[2])
                if row[6]== 'Visibility=public':
                    packageElement.set('visibility','public')
                elif row[6]== 'Visibility=private':
                    packageElement.set('visibility','private')
                if row[7]== 'isSpecification=false':
                    packageElement.set('isSpecification','false')
                elif row[7]== 'isSpecification=true':
                    packageElement.set('isSpecification','true')
                if row[8]== 'isRoot=false':
                    packageElement.set('isRoot','false')
                elif row[8]== 'isRoot=true':
                    packageElement.set('isRoot','true')
                if row[9]== 'isLeaf=false':
                    packageElement.set('isLeaf','false')
                elif row[9]== 'isLeaf=true':
                    packageElement.set('isLeaf','true')
                if row[11]== 'isActive=false':
                    packageElement.set('isActive','false')
                elif row[11]== 'isActive=true':
                    packageElement.set('isActive','true')
                if row[12]== 'isAbstract=false':
                    packageElement.set('isAbstract','false')
                elif row[12]== 'isAbstract=true':
                    packageElement.set('isAbstract','true')
                ownedcomment=ET.SubElement(packageElement,'ownedComment')
                ownedcomment.set('xmi:id','commentid')
                body=ET.SubElement(ownedcomment,'body')
                body.text=row[5]
            elif row[0]=='Attribute':
                ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                ownedAttribute.set('xmi:id',row[1])
                ownedAttribute.set('name',row[4])
                if row[6]== 'Visibility=public':
                        ownedAttribute.set('visibility','public')
                elif row[6]== 'Visibility=private':
                        ownedAttribute.set('visibility','private')
                if row[7]== 'Multivalued=true':
                        ownedAttribute.set('Multivalued','true')
                elif row[7]== 'Multivalued=false':
                        ownedAttribute.set('Multivalued','false')
                if row[8]== 'Mandatory=true':
                        ownedAttribute.set('Mandatory','true')
                elif row[8]== 'Mandatory=false':
                        ownedAttribute.set('Mandatory','false')
                if row[10]== 'isDerived=true':
                        ownedAttribute.set('isDerived','true')
                elif row[10]== 'isDerived=false':
                        ownedAttribute.set('isDerived','false')
                if row[11]== 'isReadOnly=true':
                        ownedAttribute.set('isReadOnly','true')
                elif row[11]== 'isReadOnly=false':
                        ownedAttribute.set('isReadOnly','false')
                if row[14]== 'MultiplicityElement.isOrdered=true':
                        ownedAttribute.set('isOrdered','true')
                elif row[14]== 'MultiplicityElement.isOrdered=false':
                        ownedAttribute.set('isOrdered','false')
                if row[15]== 'MultiplicityElement.isUnique=true':
                        ownedAttribute.set('isUnique','true')
                elif row[15]== 'MultiplicityElement.isUnique=false':
                        ownedAttribute.set('isUnique','false')
                ownedcomment=ET.SubElement(ownedAttribute,'ownedComment')
                ownedcomment.set('xmi:id','commentid')
                body=ET.SubElement(ownedcomment,'body')
                body.text=row[5]
                if not row[13]:
                    types=ET.SubElement(ownedAttribute,'type')
                    types.set('xmi:type','uml:PrimitiveType')
                    types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')
                else:
                    my_string = row[13]
                    my_list = my_string.split("=")[1]
                    ownedAttribute.set('type',my_list)

            elif row[0]=='Enumeration':
                if not row[1] in EnumDuplicateCheck:
                    EnumDuplicateCheck.append(row[1])
                    packageElement=ET.SubElement(uml,'packagedElement')
                    packageElement.set('xmi:type','uml:Enumeration')
                    packageElement.set('xmi:id',row[1])
                    packageElement.set('name',row[2])
                    if row[6]== 'Visibility=public':
                        packageElement.set('visibility','public')
                    elif row[6]== 'Visibility=private':
                        packageElement.set('visibility','private')
                    if row[7]== 'isAbstract=false':
                        packageElement.set('isAbstract','false')
                    elif row[7]== 'isAbstract=true':
                        packageElement.set('isAbstract','true')
                    if row[8]== 'isRoot=false':
                        packageElement.set('isRoot','false')
                    elif row[8]== 'isRoot=true':
                        packageElement.set('isRoot','true')
                    if row[9]== 'isLeaf=false':
                        packageElement.set('isLeaf','false')
                    elif row[9]== 'isLeaf=true':
                        packageElement.set('isLeaf','true')
                    ownedcomment=ET.SubElement(packageElement,'ownedComment')
                    ownedcomment.set('xmi:id','commentid')
                    body=ET.SubElement(ownedcomment,'body')
                    body.text=row[5]
            elif row[0]=='Enumeration literal':
                ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                ownedAttribute.set('xmi:id',row[1])
                ownedAttribute.set('name',row[4])
                ownedcomment=ET.SubElement(ownedAttribute,'ownedComment')
                ownedcomment.set('xmi:id','commentid')
                body=ET.SubElement(ownedcomment,'body')
                body.text=row[5]
                types=ET.SubElement(ownedAttribute,'type')
                types.set('xmi:type','uml:PrimitiveType')
                types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')
            elif row[0]=='Primitive type':
                packageElement=ET.SubElement(uml,'packagedElement')
                packageElement.set('xmi:type','uml:PrimitiveType')
                packageElement.set('xmi:id',row[1])
                packageElement.set('name',row[2])
                if row[6]== 'Visibility=public':
                        packageElement.set('visibility','public')
                elif row[6]== 'Visibility=private':
                    packageElement.set('visibility','private')
                if row[7]== 'isAbstract=false':
                    packageElement.set('isAbstract','false')
                elif row[7]== 'isAbstract=true':
                    packageElement.set('isAbstract','true')
                if row[8]== 'isRoot=false':
                    packageElement.set('isRoot','false')
                elif row[8]== 'isRoot=true':
                    packageElement.set('isRoot','true')
                if row[9]== 'isLeaf=false':
                    packageElement.set('isLeaf','false')
                elif row[9]== 'isLeaf=true':
                    packageElement.set('isLeaf','true')
                ownedcomment=ET.SubElement(packageElement,'ownedComment')
                ownedcomment.set('xmi:id','commentid')
                body=ET.SubElement(ownedcomment,'body')
                body.text=row[5]
            elif row[0]=='Data type':
                packageElement=ET.SubElement(uml,'packagedElement')
                packageElement.set('xmi:type','uml:PrimitiveType')
                packageElement.set('xmi:id',row[1])
                packageElement.set('name',row[2])
                if row[6]== 'Visibility=public':
                    packageElement.set('visibility','public')
                elif row[6]== 'Visibility=private':
                    packageElement.set('visibility','private')
                if row[7]== 'isAbstract=false':
                    packageElement.set('isAbstract','false')
                elif row[7]== 'isAbstract=true':
                    packageElement.set('isAbstract','true')
                if row[8]== 'isRoot=false':
                    packageElement.set('isRoot','false')
                elif row[8]== 'isRoot=true':
                    packageElement.set('isRoot','true')
                if row[9]== 'isLeaf=false':
                    packageElement.set('isLeaf','false')
                elif row[9]== 'isLeaf=true':
                    packageElement.set('isLeaf','true')
                ownedcomment=ET.SubElement(packageElement,'ownedComment')
                ownedcomment.set('xmi:id','commentid')
                body=ET.SubElement(ownedcomment,'body')
                body.text=row[5]
                with open('All CSV Files\BIAN UML Elements.csv', 'r',encoding="utf-8") as read_obj:
                    # pass the file object to reader() to get the reader object
                    csv_reader2 = csv.reader(read_obj)
                    for row2 in csv_reader2:
                        if row[1]== row2[3]:
                            ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                            ownedAttribute.set('xmi:id',row2[0])
                            ownedAttribute.set('name',row2[2])
                            types=ET.SubElement(ownedAttribute,'type')
                            types.set('xmi:type','uml:PrimitiveType')
                            types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')
    # create a new XML file with the results
    mydata = ET.tostring(uml)
    x = mydata
    mydata=BeautifulSoup(x,'xml').prettify()
    myfile = open("XMI Files For Each Tab\BIAN BOM.xml", "w",encoding="utf-8")
    myfile.write(mydata)

def converttoxmiBIANBOMSubSuperType():
    # create the file structure
    EnumDuplicateCheck=[]
    GeneralizationClasses=[]
    SpecializationClasses=[]
    with open('All CSV Files\BIAN BOM SubSuperType.csv','r',encoding="utf-8") as read_obj:
            csv_reader = csv.reader (read_obj)    
        # Iterate over each row in the csv using reader object
            for row in csv_reader:
                SpecializationClasses.append(row[3])
                GeneralizationClasses.append(row[1])
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
            if row[0]=='Class':
                packageElement=ET.SubElement(uml,'packagedElement')
                packageElement.set('xmi:type','uml:Class')
                packageElement.set('xmi:id',row[1])
                packageElement.set('name',row[2])
                if row[6]== 'Visibility=public':
                    packageElement.set('visibility','public')
                elif row[6]== 'Visibility=private':
                    packageElement.set('visibility','private')
                if row[7]== 'isSpecification=false':
                    packageElement.set('isSpecification','false')
                elif row[7]== 'isSpecification=true':
                    packageElement.set('isSpecification','true')
                if row[8]== 'isRoot=false':
                    packageElement.set('isRoot','false')
                elif row[8]== 'isRoot=true':
                    packageElement.set('isRoot','true')
                if row[9]== 'isLeaf=false':
                    packageElement.set('isLeaf','false')
                elif row[9]== 'isLeaf=true':
                    packageElement.set('isLeaf','true')
                if row[11]== 'isActive=false':
                    packageElement.set('isActive','false')
                elif row[11]== 'isActive=true':
                    packageElement.set('isActive','true')
                if row[12]== 'isAbstract=false':
                    packageElement.set('isAbstract','false')
                elif row[12]== 'isAbstract=true':
                    packageElement.set('isAbstract','true')
                for y in range(2,len(SpecializationClasses)):
                        if row[1] == SpecializationClasses[y]:
                            indexvalue = GeneralizationClasses[y]
                            genrealization = ET.SubElement(packageElement,'generalization')
                            genrealization.set('xmi:id','id')
                            genrealization.set('general',indexvalue)
                ownedcomment=ET.SubElement(packageElement,'ownedComment')
                ownedcomment.set('xmi:id','commentid')
                body=ET.SubElement(ownedcomment,'body')
                body.text=row[5]
            elif row[0]=='Attribute':
                ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                ownedAttribute.set('xmi:id',row[3])
                ownedAttribute.set('name',row[4])
                if row[6]== 'Visibility=public':
                        ownedAttribute.set('visibility','public')
                elif row[6]== 'Visibility=private':
                        ownedAttribute.set('visibility','private')
                if row[7]== 'Multivalued=true':
                        ownedAttribute.set('Multivalued','true')
                elif row[7]== 'Multivalued=false':
                        ownedAttribute.set('Multivalued','false')
                if row[8]== 'Mandatory=true':
                        ownedAttribute.set('Mandatory','true')
                elif row[8]== 'Mandatory=false':
                        ownedAttribute.set('Mandatory','false')
                if row[10]== 'isDerived=true':
                        ownedAttribute.set('isDerived','true')
                elif row[10]== 'isDerived=false':
                        ownedAttribute.set('isDerived','false')
                if row[11]== 'isReadOnly=true':
                        ownedAttribute.set('isReadOnly','true')
                elif row[11]== 'isReadOnly=false':
                        ownedAttribute.set('isReadOnly','false')
                if row[14]== 'MultiplicityElement.isOrdered=true':
                        ownedAttribute.set('isOrdered','true')
                elif row[14]== 'MultiplicityElement.isOrdered=false':
                        ownedAttribute.set('isOrdered','false')
                if row[15]== 'MultiplicityElement.isUnique=true':
                        ownedAttribute.set('isUnique','true')
                elif row[15]== 'MultiplicityElement.isUnique=false':
                        ownedAttribute.set('isUnique','false')
                ownedcomment=ET.SubElement(ownedAttribute,'ownedComment')
                ownedcomment.set('xmi:id','commentid')
                body=ET.SubElement(ownedcomment,'body')
                body.text=row[5]
                if not row[13]:
                    types=ET.SubElement(ownedAttribute,'type')
                    types.set('xmi:type','uml:PrimitiveType')
                    types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')
                else:
                    my_string = row[13]
                    my_list = my_string.split("=")[1]
                    ownedAttribute.set('type',my_list)

            elif row[0]=='Enumeration':
                if not row[1] in EnumDuplicateCheck:
                    EnumDuplicateCheck.append(row[1])
                    packageElement=ET.SubElement(uml,'packagedElement')
                    packageElement.set('xmi:type','uml:Enumeration')
                    packageElement.set('xmi:id',row[1])
                    packageElement.set('name',row[2])
                    if row[6]== 'Visibility=public':
                        packageElement.set('visibility','public')
                    elif row[6]== 'Visibility=private':
                        packageElement.set('visibility','private')
                    if row[7]== 'isAbstract=false':
                        packageElement.set('isAbstract','false')
                    elif row[7]== 'isAbstract=true':
                        packageElement.set('isAbstract','true')
                    if row[8]== 'isRoot=false':
                        packageElement.set('isRoot','false')
                    elif row[8]== 'isRoot=true':
                        packageElement.set('isRoot','true')
                    if row[9]== 'isLeaf=false':
                        packageElement.set('isLeaf','false')
                    elif row[9]== 'isLeaf=true':
                        packageElement.set('isLeaf','true')
                    ownedcomment=ET.SubElement(packageElement,'ownedComment')
                    ownedcomment.set('xmi:id','commentid')
                    body=ET.SubElement(ownedcomment,'body')
                    body.text=row[5]
            elif row[0]=='Enumeration literal':
                ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                ownedAttribute.set('xmi:id',row[3])
                ownedAttribute.set('name',row[4])
                ownedcomment=ET.SubElement(ownedAttribute,'ownedComment')
                ownedcomment.set('xmi:id','commentid')
                body=ET.SubElement(ownedcomment,'body')
                body.text=row[5]
                types=ET.SubElement(ownedAttribute,'type')
                types.set('xmi:type','uml:PrimitiveType')
                types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')
            elif row[0]=='Primitive type':
                packageElement=ET.SubElement(uml,'packagedElement')
                packageElement.set('xmi:type','uml:PrimitiveType')
                packageElement.set('xmi:id',row[1])
                packageElement.set('name',row[2])
                if row[6]== 'Visibility=public':
                        packageElement.set('visibility','public')
                elif row[6]== 'Visibility=private':
                    packageElement.set('visibility','private')
                if row[7]== 'isAbstract=false':
                    packageElement.set('isAbstract','false')
                elif row[7]== 'isAbstract=true':
                    packageElement.set('isAbstract','true')
                if row[8]== 'isRoot=false':
                    packageElement.set('isRoot','false')
                elif row[8]== 'isRoot=true':
                    packageElement.set('isRoot','true')
                if row[9]== 'isLeaf=false':
                    packageElement.set('isLeaf','false')
                elif row[9]== 'isLeaf=true':
                    packageElement.set('isLeaf','true')
                ownedcomment=ET.SubElement(packageElement,'ownedComment')
                ownedcomment.set('xmi:id','commentid')
                body=ET.SubElement(ownedcomment,'body')
                body.text=row[5]
            elif row[0]=='Data type':
                packageElement=ET.SubElement(uml,'packagedElement')
                packageElement.set('xmi:type','uml:PrimitiveType')
                packageElement.set('xmi:id',row[1])
                packageElement.set('name',row[2])
                if row[6]== 'Visibility=public':
                    packageElement.set('visibility','public')
                elif row[6]== 'Visibility=private':
                    packageElement.set('visibility','private')
                if row[7]== 'isAbstract=false':
                    packageElement.set('isAbstract','false')
                elif row[7]== 'isAbstract=true':
                    packageElement.set('isAbstract','true')
                if row[8]== 'isRoot=false':
                    packageElement.set('isRoot','false')
                elif row[8]== 'isRoot=true':
                    packageElement.set('isRoot','true')
                if row[9]== 'isLeaf=false':
                    packageElement.set('isLeaf','false')
                elif row[9]== 'isLeaf=true':
                    packageElement.set('isLeaf','true')
                ownedcomment=ET.SubElement(packageElement,'ownedComment')
                ownedcomment.set('xmi:id','commentid')
                body=ET.SubElement(ownedcomment,'body')
                body.text=row[5]
                with open('All CSV Files\BIAN UML Elements.csv', 'r',encoding="utf-8") as read_obj:
                    # pass the file object to reader() to get the reader object
                    csv_reader2 = csv.reader(read_obj)
                    for row2 in csv_reader2:
                        if row[1]== row2[3]:
                            ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                            ownedAttribute.set('xmi:id',row2[0])
                            ownedAttribute.set('name',row2[2])
                            types=ET.SubElement(ownedAttribute,'type')
                            types.set('xmi:type','uml:PrimitiveType')
                            types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')
    # create a new XML file with the results
    mydata = ET.tostring(uml)
    x = mydata
    mydata=BeautifulSoup(x,'xml').prettify()
    myfile = open("XMI Files For Each Tab\BIAN BOM SubSuperType.xml", "w",encoding="utf-8")
    myfile.write(mydata)

def converttoxmiBIANBOMSubSuperTypeRelations():
    # create the file structure
    comntcounter =0
    EnumDuplicateCheck=[]
    GeneralizationClasses=[]
    SpecializationClasses=[]
    with open('All CSV Files\BIAN BOM SubSuperType.csv','r',encoding="utf-8") as read_obj:
            csv_reader = csv.reader (read_obj)    
        # Iterate over each row in the csv using reader object
            for row in csv_reader:
                SpecializationClasses.append(row[3])
                GeneralizationClasses.append(row[1])
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
            if row[0]=='Class':
                packageElement=ET.SubElement(uml,'packagedElement')
                packageElement.set('xmi:type','uml:Class')
                packageElement.set('xmi:id',row[1])
                packageElement.set('name',row[2])
                if row[6]== 'Visibility=public':
                    packageElement.set('visibility','public')
                elif row[6]== 'Visibility=private':
                    packageElement.set('visibility','private')
                if row[7]== 'isSpecification=false':
                    packageElement.set('isSpecification','false')
                elif row[7]== 'isSpecification=true':
                    packageElement.set('isSpecification','true')
                if row[8]== 'isRoot=false':
                    packageElement.set('isRoot','false')
                elif row[8]== 'isRoot=true':
                    packageElement.set('isRoot','true')
                if row[9]== 'isLeaf=false':
                    packageElement.set('isLeaf','false')
                elif row[9]== 'isLeaf=true':
                    packageElement.set('isLeaf','true')
                if row[11]== 'isActive=false':
                    packageElement.set('isActive','false')
                elif row[11]== 'isActive=true':
                    packageElement.set('isActive','true')
                if row[12]== 'isAbstract=false':
                    packageElement.set('isAbstract','false')
                elif row[12]== 'isAbstract=true':
                    packageElement.set('isAbstract','true')
                for y in range(2,len(SpecializationClasses)):
                        if row[1] == SpecializationClasses[y]:
                            indexvalue = GeneralizationClasses[y]
                            genrealization = ET.SubElement(packageElement,'generalization')
                            genrealization.set('xmi:id','id')
                            genrealization.set('general',indexvalue)
                ownedcomment=ET.SubElement(packageElement,'ownedComment')
                ownedcomment.set('xmi:id','commentid')
                body=ET.SubElement(ownedcomment,'body')
                body.text=row[5]
            elif row[0]=='Attribute':
                ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                ownedAttribute.set('xmi:id',row[3])
                ownedAttribute.set('name',row[4])
                if row[6]== 'Visibility=public':
                        ownedAttribute.set('visibility','public')
                elif row[6]== 'Visibility=private':
                        ownedAttribute.set('visibility','private')
                if row[7]== 'Multivalued=true':
                        ownedAttribute.set('Multivalued','true')
                elif row[7]== 'Multivalued=false':
                        ownedAttribute.set('Multivalued','false')
                if row[8]== 'Mandatory=true':
                        ownedAttribute.set('Mandatory','true')
                elif row[8]== 'Mandatory=false':
                        ownedAttribute.set('Mandatory','false')
                if row[10]== 'isDerived=true':
                        ownedAttribute.set('isDerived','true')
                elif row[10]== 'isDerived=false':
                        ownedAttribute.set('isDerived','false')
                if row[11]== 'isReadOnly=true':
                        ownedAttribute.set('isReadOnly','true')
                elif row[11]== 'isReadOnly=false':
                        ownedAttribute.set('isReadOnly','false')
                if row[14]== 'MultiplicityElement.isOrdered=true':
                        ownedAttribute.set('isOrdered','true')
                elif row[14]== 'MultiplicityElement.isOrdered=false':
                        ownedAttribute.set('isOrdered','false')
                if row[15]== 'MultiplicityElement.isUnique=true':
                        ownedAttribute.set('isUnique','true')
                elif row[15]== 'MultiplicityElement.isUnique=false':
                        ownedAttribute.set('isUnique','false')
                ownedcomment=ET.SubElement(ownedAttribute,'ownedComment')
                ownedcomment.set('xmi:id','commentid')
                body=ET.SubElement(ownedcomment,'body')
                body.text=row[5]
                if not row[13]:
                    types=ET.SubElement(ownedAttribute,'type')
                    types.set('xmi:type','uml:PrimitiveType')
                    types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')
                else:
                    my_string = row[13]
                    my_list = my_string.split("=")[1]
                    ownedAttribute.set('type',my_list)

            elif row[0]=='Enumeration':
                if not row[1] in EnumDuplicateCheck:
                    EnumDuplicateCheck.append(row[1])
                    packageElement=ET.SubElement(uml,'packagedElement')
                    packageElement.set('xmi:type','uml:Enumeration')
                    packageElement.set('xmi:id',row[1])
                    packageElement.set('name',row[2])
                    if row[6]== 'Visibility=public':
                        packageElement.set('visibility','public')
                    elif row[6]== 'Visibility=private':
                        packageElement.set('visibility','private')
                    if row[7]== 'isAbstract=false':
                        packageElement.set('isAbstract','false')
                    elif row[7]== 'isAbstract=true':
                        packageElement.set('isAbstract','true')
                    if row[8]== 'isRoot=false':
                        packageElement.set('isRoot','false')
                    elif row[8]== 'isRoot=true':
                        packageElement.set('isRoot','true')
                    if row[9]== 'isLeaf=false':
                        packageElement.set('isLeaf','false')
                    elif row[9]== 'isLeaf=true':
                        packageElement.set('isLeaf','true')
                    ownedcomment=ET.SubElement(packageElement,'ownedComment')
                    ownedcomment.set('xmi:id','commentid')
                    body=ET.SubElement(ownedcomment,'body')
                    body.text=row[5]
            elif row[0]=='Enumeration literal':
                ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                ownedAttribute.set('xmi:id',row[3])
                ownedAttribute.set('name',row[4])
                ownedcomment=ET.SubElement(ownedAttribute,'ownedComment')
                ownedcomment.set('xmi:id','commentid')
                body=ET.SubElement(ownedcomment,'body')
                body.text=row[5]
                types=ET.SubElement(ownedAttribute,'type')
                types.set('xmi:type','uml:PrimitiveType')
                types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')
            elif row[0]=='Primitive type':
                packageElement=ET.SubElement(uml,'packagedElement')
                packageElement.set('xmi:type','uml:PrimitiveType')
                packageElement.set('xmi:id',row[1])
                packageElement.set('name',row[2])
                if row[6]== 'Visibility=public':
                        packageElement.set('visibility','public')
                elif row[6]== 'Visibility=private':
                    packageElement.set('visibility','private')
                if row[7]== 'isAbstract=false':
                    packageElement.set('isAbstract','false')
                elif row[7]== 'isAbstract=true':
                    packageElement.set('isAbstract','true')
                if row[8]== 'isRoot=false':
                    packageElement.set('isRoot','false')
                elif row[8]== 'isRoot=true':
                    packageElement.set('isRoot','true')
                if row[9]== 'isLeaf=false':
                    packageElement.set('isLeaf','false')
                elif row[9]== 'isLeaf=true':
                    packageElement.set('isLeaf','true')
                ownedcomment=ET.SubElement(packageElement,'ownedComment')
                ownedcomment.set('xmi:id','commentid')
                body=ET.SubElement(ownedcomment,'body')
                body.text=row[5]
            elif row[0]=='Data type':
                packageElement=ET.SubElement(uml,'packagedElement')
                packageElement.set('xmi:type','uml:PrimitiveType')
                packageElement.set('xmi:id',row[1])
                packageElement.set('name',row[2])
                if row[6]== 'Visibility=public':
                    packageElement.set('visibility','public')
                elif row[6]== 'Visibility=private':
                    packageElement.set('visibility','private')
                if row[7]== 'isAbstract=false':
                    packageElement.set('isAbstract','false')
                elif row[7]== 'isAbstract=true':
                    packageElement.set('isAbstract','true')
                if row[8]== 'isRoot=false':
                    packageElement.set('isRoot','false')
                elif row[8]== 'isRoot=true':
                    packageElement.set('isRoot','true')
                if row[9]== 'isLeaf=false':
                    packageElement.set('isLeaf','false')
                elif row[9]== 'isLeaf=true':
                    packageElement.set('isLeaf','true')
                ownedcomment=ET.SubElement(packageElement,'ownedComment')
                ownedcomment.set('xmi:id','commentid')
                body=ET.SubElement(ownedcomment,'body')
                body.text=row[5]
                with open('All CSV Files\BIAN UML Elements.csv', 'r',encoding="utf-8") as read_obj:
                    # pass the file object to reader() to get the reader object
                    csv_reader2 = csv.reader(read_obj)
                    for row2 in csv_reader2:
                        if row[1]== row2[3]:
                            ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                            ownedAttribute.set('xmi:id',row2[0])
                            ownedAttribute.set('name',row2[2])
                            types=ET.SubElement(ownedAttribute,'type')
                            types.set('xmi:type','uml:PrimitiveType')
                            types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')
    namecounter = 5555
    #relations
    with open('All CSV Files\BIAN BOM Relations.csv','r',encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            #Association
            if(row[4] == 'aggregation=shared'):
                packageElement=ET.SubElement(uml,'packagedElement')
                packageElement.set('xmi:type','uml:Association')
                packageElement.set('xmi:id',row[0])
                packageElement.set('name',row[1])
                con=row[2]+"a"+" "+row[13]+"b"
                packageElement.set('memberEnd',con)
                packageElement.set('navigableOwnedEnd',row[13]+"b")
                ownedEnd=ET.SubElement(packageElement,'ownedEnd')
                ownedEnd.set('xmi:id',row[2]+"a")
                string= row[10]
                my_split=string.split('=')[1]
                #if my_split:
                #    ownedEnd.set('name',my_split)
                #else:
                namecounter = namecounter+1
                namestr=str(namecounter)
                ownedEnd.set('name',namestr)
                if(row[12]=='visibility=public'):
                    ownedEnd.set('visibility','public')
                elif(row[12]=='visibility=package'):
                    ownedEnd.set('visibility','package')
                elif(row[12]=='visibility=protected'):
                    ownedEnd.set('visibility','protected')
                elif(row[12]=='visibility=private'):
                    ownedEnd.set('visibility','private')
                if(row[8]=='isUnique=true'):
                    ownedEnd.set('isUnique','true')
                elif(row[8]=='isUnique=false'):
                    ownedEnd.set('isUnique','false')
                if(row[5]=='isDerived=true'):
                    ownedEnd.set('isDerived','true')
                elif(row[5]=='isDerived=false'):
                    ownedEnd.set('isDerived','false')
                if(row[6]=='isNavigable=true'):
                    ownedEnd.set('isNavigable','true')
                elif(row[6]=='isNavigable=false'):
                    ownedEnd.set('isNavigable','false')
                if(row[7]=='isOrdered=true'):
                    ownedEnd.set('isOrdered','true')
                elif(row[7]=='isOrdered=false'):
                    ownedEnd.set('isOrdered','false')
                
                ownedEnd.set('type',row[2])
                ownedEnd.set('association',row[0])
                upperValue=ET.SubElement(ownedEnd,'upperValue')
                upperValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                upperValue.set('xmi:id','')
                if(row[11]=='upper=1'):
                    upperValue.set('value','1')
                elif(row[11]=='upper=0'):
                    upperValue.set('value','0')
                elif(row[11]=='upper=*'):
                    upperValue.set('value','*')
                lowerValue=ET.SubElement(ownedEnd,'lowerValue')
                lowerValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                lowerValue.set('xmi:id','')
                if(row[9]=='lower=1'):
                    lowerValue.set('value','1')
                elif(row[9]=='lower=0'):
                    lowerValue.set('value','0')
                elif(row[9]=='lower=*'):
                    lowerValue.set('value','*')
                lowerValue.set('xmi:type','uml:LiteralInteger')
                lowerValue.set('xmi:id','')

                ownedEnd2=ET.SubElement(packageElement,'ownedEnd')
                ownedEnd2.set('xmi:id',row[13]+"b")
                string= row[21]
                my_split=string.split('=')[1]
                #if my_split:
                #    ownedEnd2.set('name',my_split)
                #else:
                namecounter = namecounter+1
                namestr=str(namecounter)
                ownedEnd2.set('name',namestr)
                if(row[23]=='visibility=public'):
                    ownedEnd2.set('visibility','public')
                elif(row[23]=='visibility=package'):
                    ownedEnd2.set('visibility','package')
                elif(row[23]=='visibility=protected'):
                    ownedEnd2.set('visibility','protected')
                elif(row[23]=='visibility=private'):
                    ownedEnd2.set('visibility','private')
                if(row[19]=='isUnique=true'):
                    ownedEnd2.set('isUnique','true')
                elif(row[19]=='isUnique=false'):
                    ownedEnd2.set('isUnique','false')
                if(row[16]=='isDerived=true'):
                    ownedEnd.set('isDerived','true')
                elif(row[16]=='isDerived=false'):
                    ownedEnd.set('isDerived','false')
                if(row[17]=='isNavigable=true'):
                    ownedEnd.set('isNavigable','true')
                elif(row[17]=='isNavigable=false'):
                    ownedEnd.set('isNavigable','false')
                if(row[18]=='isOrdered=true'):
                    ownedEnd.set('isOrdered','true')
                elif(row[18]=='isOrdered=false'):
                    ownedEnd.set('isOrdered','false')
                ownedEnd2.set('type',row[13])
                ownedEnd2.set('association',row[0])
                upperValue2=ET.SubElement(ownedEnd2,'upperValue')
                upperValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                upperValue2.set('xmi:id','')
                if(row[22]=='upper=1'):
                    upperValue2.set('value','1')
                elif(row[22]=='upper=0'):
                    upperValue2.set('value','0')
                elif(row[22]=='upper=*'):
                    upperValue2.set('value','*')
                lowerValue2=ET.SubElement(ownedEnd2,'lowerValue')
                lowerValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                lowerValue2.set('xmi:id','')
                if(row[20]=='lower=1'):
                    lowerValue2.set('value','1')
                elif(row[20]=='lower=0'):
                    lowerValue2.set('value','0')
                elif(row[20]=='lower=*'):
                    lowerValue2.set('value','*')
                lowerValue2.set('xmi:type','uml:LiteralInteger')
                lowerValue2.set('xmi:id','')
            #NONE
            elif(row[4] == 'aggregation=none'):
                packageElement=ET.SubElement(uml,'packagedElement')
                packageElement.set('xmi:type','uml:Association')
                packageElement.set('xmi:id',row[0])
                packageElement.set('name',row[1])
                ownedEnd=ET.SubElement(packageElement,'ownedEnd')
                ownedEnd.set('xmi:id',row[2]+"a")
                string= row[10]
                my_split=string.split('=')[1]
                #if my_split:
                #    ownedEnd.set('name',my_split)
                #else:
                namecounter = namecounter+1
                namestr=str(namecounter)
                ownedEnd.set('name',namestr)
                if(row[12]=='visibility=public'):
                    ownedEnd.set('visibility','public')
                elif(row[12]=='visibility=package'):
                    ownedEnd.set('visibility','package')
                elif(row[12]=='visibility=protected'):
                    ownedEnd.set('visibility','protected')
                elif(row[12]=='visibility=private'):
                    ownedEnd.set('visibility','private')
                if(row[8]=='isUnique=true'):
                    ownedEnd.set('isUnique','true')
                elif(row[8]=='isUnique=false'):
                    ownedEnd.set('isUnique','false')
                if(row[5]=='isDerived=true'):
                    ownedEnd.set('isDerived','true')
                elif(row[5]=='isDerived=false'):
                    ownedEnd.set('isDerived','false')
                if(row[6]=='isNavigable=true'):
                    ownedEnd.set('isNavigable','true')
                elif(row[6]=='isNavigable=false'):
                    ownedEnd.set('isNavigable','false')
                if(row[7]=='isOrdered=true'):
                    ownedEnd.set('isOrdered','true')
                elif(row[7]=='isOrdered=false'):
                    ownedEnd.set('isOrdered','false')
                ownedEnd.set('type',row[2])
                ownedEnd.set('association',row[0])
                upperValue=ET.SubElement(ownedEnd,'upperValue')
                upperValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                upperValue.set('xmi:id','')
                if(row[11]=='upper=1'):
                    upperValue.set('value','1')
                elif(row[11]=='upper=0'):
                    upperValue.set('value','0')
                elif(row[11]=='upper=*'):
                    upperValue.set('value','*')
                lowerValue=ET.SubElement(ownedEnd,'lowerValue')
                lowerValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                lowerValue.set('xmi:id','')
                if(row[9]=='lower=1'):
                    lowerValue.set('value','1')
                elif(row[9]=='lower=0'):
                    lowerValue.set('value','0')
                elif(row[9]=='lower=*'):
                    lowerValue.set('value','*')
                lowerValue.set('xmi:type','uml:LiteralInteger')
                lowerValue.set('xmi:id','')

                ownedEnd2=ET.SubElement(packageElement,'ownedEnd')
                ownedEnd2.set('xmi:id',row[13]+"b")
                string= row[21]
                my_split=string.split('=')[1]
                #if my_split:
                #    ownedEnd2.set('name',my_split)
                #else:
                namecounter = namecounter+1
                namestr=str(namecounter)
                ownedEnd2.set('name',namestr)
                if(row[23]=='visibility=public'):
                    ownedEnd2.set('visibility','public')
                elif(row[23]=='visibility=package'):
                    ownedEnd2.set('visibility','package')
                elif(row[23]=='visibility=protected'):
                    ownedEnd2.set('visibility','protected')
                elif(row[23]=='visibility=private'):
                    ownedEnd2.set('visibility','private')
                if(row[19]=='isUnique=true'):
                    ownedEnd2.set('isUnique','true')
                elif(row[19]=='isUnique=false'):
                    ownedEnd2.set('isUnique','false')
                if(row[16]=='isDerived=true'):
                    ownedEnd.set('isDerived','true')
                elif(row[16]=='isDerived=false'):
                    ownedEnd.set('isDerived','false')
                if(row[17]=='isNavigable=true'):
                    ownedEnd.set('isNavigable','true')
                elif(row[17]=='isNavigable=false'):
                    ownedEnd.set('isNavigable','false')
                if(row[18]=='isOrdered=true'):
                    ownedEnd.set('isOrdered','true')
                elif(row[18]=='isOrdered=false'):
                    ownedEnd.set('isOrdered','false')
                ownedEnd2.set('type',row[13])
                ownedEnd2.set('association',row[0])
                upperValue2=ET.SubElement(ownedEnd2,'upperValue')
                upperValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                upperValue2.set('xmi:id','')
                if(row[22]=='upper=1'):
                    upperValue2.set('value','1')
                elif(row[22]=='upper=0'):
                    upperValue2.set('value','0')
                elif(row[22]=='upper=*'):
                    upperValue2.set('value','*')
                lowerValue2=ET.SubElement(ownedEnd2,'lowerValue')
                lowerValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                lowerValue2.set('xmi:id','')
                if(row[20]=='lower=1'):
                    lowerValue2.set('value','1')
                elif(row[20]=='lower=0'):
                    lowerValue2.set('value','0')
                elif(row[20]=='lower=*'):
                    lowerValue2.set('value','*')
                lowerValue2.set('xmi:type','uml:LiteralInteger')
                lowerValue2.set('xmi:id','')
            #Composition
            elif(row[4] == 'aggregation=composite'):
                packageElement=ET.SubElement(uml,'packagedElement')
                packageElement.set('xmi:type','uml:Association')
                packageElement.set('xmi:id',row[0])
                packageElement.set('name',row[1])
                con=row[2]+"a"+" "+row[13]+"b"
                packageElement.set('memberEnd',con) 
                packageElement.set('navigableOwnedEnd',row[13]+"b")
                ownedEnd=ET.SubElement(packageElement,'ownedEnd')
                ownedEnd.set('xmi:id',row[2]+"a")
                string= row[10]
                my_split=string.split('=')[1]
                #if my_split:
                #    ownedEnd.set('name',my_split)
                #else:
                namecounter = namecounter+1
                namestr=str(namecounter)
                ownedEnd.set('name',namestr)
                if(row[12]=='visibility=public'):
                    ownedEnd.set('visibility','public')
                elif(row[12]=='visibility=package'):
                    ownedEnd.set('visibility','package')
                elif(row[12]=='visibility=protected'):
                    ownedEnd.set('visibility','protected')
                elif(row[12]=='visibility=private'):
                    ownedEnd.set('visibility','private')
                if(row[8]=='isUnique=true'):
                    ownedEnd.set('isUnique','true')
                elif(row[8]=='isUnique=false'):
                    ownedEnd.set('isUnique','false')
                if(row[5]=='isDerived=true'):
                    ownedEnd.set('isDerived','true')
                elif(row[5]=='isDerived=false'):
                    ownedEnd.set('isDerived','false')
                if(row[6]=='isNavigable=true'):
                    ownedEnd.set('isNavigable','true')
                elif(row[6]=='isNavigable=false'):
                    ownedEnd.set('isNavigable','false')
                if(row[7]=='isOrdered=true'):
                    ownedEnd.set('isOrdered','true')
                elif(row[7]=='isOrdered=false'):
                    ownedEnd.set('isOrdered','false')
                ownedEnd.set('type',row[2])
                ownedEnd.set('association',row[0])
                upperValue=ET.SubElement(ownedEnd,'upperValue')
                upperValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                upperValue.set('xmi:id','')
                if(row[11]=='upper=1'):
                    upperValue.set('value','1')
                elif(row[11]=='upper=0'):
                    upperValue.set('value','0')
                elif(row[11]=='upper=*'):
                    upperValue.set('value','*')
                lowerValue=ET.SubElement(ownedEnd,'lowerValue')
                lowerValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                lowerValue.set('xmi:id','')
                if(row[9]=='lower=1'):
                    lowerValue.set('value','1')
                elif(row[9]=='lower=0'):
                    lowerValue.set('value','0')
                elif(row[9]=='lower=*'):
                    lowerValue.set('value','*')
                lowerValue.set('xmi:type','uml:LiteralInteger')
                lowerValue.set('xmi:id','')

                ownedEnd2=ET.SubElement(packageElement,'ownedEnd')
                ownedEnd2.set('xmi:id',row[13]+"b")
                string= row[21]
                my_split=string.split('=')[1]
                #if my_split:
                #    ownedEnd2.set('name',my_split)
                #else:
                namecounter = namecounter+1
                namestr=str(namecounter)
                ownedEnd2.set('name',namestr)
                ownedEnd2.set('aggregation','composite')
                if(row[23]=='visibility=public'):
                    ownedEnd2.set('visibility','public')
                elif(row[23]=='visibility=package'):
                    ownedEnd2.set('visibility','package')
                elif(row[23]=='visibility=protected'):
                    ownedEnd2.set('visibility','protected')
                elif(row[23]=='visibility=private'):
                    ownedEnd2.set('visibility','private')
                if(row[19]=='isUnique=true'):
                    ownedEnd2.set('isUnique','true')
                elif(row[19]=='isUnique=false'):
                    ownedEnd2.set('isUnique','false')
                if(row[16]=='isDerived=true'):
                    ownedEnd.set('isDerived','true')
                elif(row[16]=='isDerived=false'):
                    ownedEnd.set('isDerived','false')
                if(row[17]=='isNavigable=true'):
                    ownedEnd.set('isNavigable','true')
                elif(row[17]=='isNavigable=false'):
                    ownedEnd.set('isNavigable','false')
                if(row[18]=='isOrdered=true'):
                    ownedEnd.set('isOrdered','true')
                elif(row[18]=='isOrdered=false'):
                    ownedEnd.set('isOrdered','false')
                ownedEnd2.set('type',row[13])
                ownedEnd2.set('association',row[0])
                upperValue2=ET.SubElement(ownedEnd2,'upperValue')
                upperValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                upperValue2.set('xmi:id','')
                if(row[22]=='upper=1'):
                    upperValue2.set('value','1')
                elif(row[22]=='upper=0'):
                    upperValue2.set('value','0')
                elif(row[22]=='upper=*'):
                    upperValue2.set('value','*')
                lowerValue2=ET.SubElement(ownedEnd2,'lowerValue')
                lowerValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                lowerValue2.set('xmi:id','')
                if(row[20]=='lower=1'):
                    lowerValue2.set('value','1')
                elif(row[20]=='lower=0'):
                    lowerValue2.set('value','0')
                elif(row[20]=='lower=*'):
                    lowerValue2.set('value','*')
                lowerValue2.set('xmi:type','uml:LiteralInteger')
                lowerValue2.set('xmi:id','')
    # create a new XML file with the results
    mydata = ET.tostring(uml)
    x = mydata
    mydata=BeautifulSoup(x,'xml').prettify()
    myfile = open("XMI Files For Each Tab\BIAN BOM SubSuperType Relations.xml", "w",encoding="utf-8")
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
        r6=[]
        r7=[]
        r8=[]
        r9=[]
        r10=[]
        r11=[]
        r12=[]
        r13=[]
        r14=[]
        r15=[]
        r16=[]
        r17=[]
        EnumDuplicateCheck=[]
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
        UMLType=[]
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
                        Specialization.append(row4[3])
                        Generalization.append(row4[1])
                    for row2 in csv_reader2:
                        UIDclassdiagram.append(row2[0])
                        UIDRelations.append(row2[1])
                    for row3 in csv_reader3:
                        UMLType.append(row3[0])
                        UIDBO.append(row3[1])
                        ObjectName.append(row3[2])
                        UIDAttr.append(row3[3])
                        AttrName.append(row3[4])
                        comm.append(row3[5])
                        r6.append(row3[6])
                        r7.append(row3[7])
                        r8.append(row3[8])
                        r9.append(row3[9])
                        r10.append(row3[10])
                        r11.append(row3[11])
                        r12.append(row3[12])
                        r13.append(row3[13])
                        r14.append(row3[14])
                        r15.append(row3[15])
                        r16.append(row3[16])
                        r17.append(row3[17])
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
                                    #Association
                                        if(row[0] in Relations):
                                            if(row[4] == 'aggregation=shared'):
                                                packageElement=ET.SubElement(package,'packagedElement')
                                                packageElement.set('xmi:type','uml:Association')
                                                if(row[0] in RelationDuplicates):
                                                    packageElement.set('xmi:id',row[0]+idString)
                                                else:
                                                    packageElement.set('xmi:id',row[0])
                                                packageElement.set('name',row[1])
                                                if(row[2] and row[13] in Duplicates):
                                                    con=row[2]+idString+" "+row[13]+idString
                                                    packageElement.set('navigableOwnedEnd',row[13]+idString)
                                                elif(row[2] in Duplicates):
                                                    con=row[2]+idString+" "+row[13]+"b"
                                                    packageElement.set('navigableOwnedEnd',row[13]+"b")
                                                elif(row[13] in Duplicates):
                                                    con=row[2]+"a"+" "+row[13]+idString
                                                    packageElement.set('navigableOwnedEnd',row[13]+idString)
                                                else:
                                                    con=row[2]+"a"+" "+row[13]+"b"
                                                    packageElement.set('navigableOwnedEnd',row[13]+"b")
                                                packageElement.set('memberEnd',con)
                                                ownedEnd=ET.SubElement(packageElement,'ownedEnd')
                                                if(row[2] in Duplicates):
                                                    ownedEnd.set('xmi:id',row[2]+idString)
                                                else:
                                                    ownedEnd.set('xmi:id',row[2]+"a")
                                                namecounter = namecounter+1
                                                namestr=str(namecounter)
                                                ownedEnd.set('name',namestr)
                                                if(row[12]=='visibility=public'):
                                                    ownedEnd.set('visibility','public')
                                                elif(row[12]=='visibility=package'):
                                                    ownedEnd.set('visibility','package')
                                                elif(row[12]=='visibility=protected'):
                                                    ownedEnd.set('visibility','protected')
                                                elif(row[12]=='visibility=private'):
                                                    ownedEnd.set('visibility','private')
                                                if(row[8]=='isUnique=true'):
                                                    ownedEnd.set('isUnique','true')
                                                elif(row[8]=='isUnique=false'):
                                                    ownedEnd.set('isUnique','false')
                                                if(row[5]=='isDerived=true'):
                                                    ownedEnd.set('isDerived','true')
                                                elif(row[5]=='isDerived=false'):
                                                    ownedEnd.set('isDerived','false')
                                                if(row[6]=='isNavigable=true'):
                                                    ownedEnd.set('isNavigable','true')
                                                elif(row[6]=='isNavigable=false'):
                                                    ownedEnd.set('isNavigable','false')
                                                if(row[7]=='isOrdered=true'):
                                                    ownedEnd.set('isOrdered','true')
                                                elif(row[7]=='isOrdered=false'):
                                                    ownedEnd.set('isOrdered','false')
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
                                                if(row[11]=='upper=1'):
                                                    upperValue.set('value','1')
                                                elif(row[11]=='upper=0'):
                                                    upperValue.set('value','0')
                                                elif(row[11]=='upper=*'):
                                                    upperValue.set('value','*')
                                                lowerValue=ET.SubElement(ownedEnd,'lowerValue')
                                                lowerValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                lowerValue.set('xmi:id','')
                                                if(row[9]=='lower=1'):
                                                    lowerValue.set('value','1')
                                                elif(row[9]=='lower=0'):
                                                    lowerValue.set('value','0')
                                                elif(row[9]=='lower=*'):
                                                    lowerValue.set('value','*')
                                                lowerValue.set('xmi:type','uml:LiteralInteger')
                                                lowerValue.set('xmi:id','')
                                               
                                                ownedEnd2=ET.SubElement(packageElement,'ownedEnd')
                                                if(row[13] in Duplicates):
                                                    ownedEnd2.set('xmi:id',row[13]+idString)
                                                else:
                                                    ownedEnd2.set('xmi:id',row[13]+"b")
                                                namecounter = namecounter+1
                                                namestr=str(namecounter)
                                                ownedEnd2.set('name',namestr)
                                                if(row[23]=='visibility=public'):
                                                    ownedEnd2.set('visibility','public')
                                                elif(row[23]=='visibility=package'):
                                                    ownedEnd2.set('visibility','package')
                                                elif(row[23]=='visibility=protected'):
                                                    ownedEnd2.set('visibility','protected')
                                                elif(row[23]=='visibility=private'):
                                                    ownedEnd2.set('visibility','private')
                                                if(row[19]=='isUnique=true'):
                                                    ownedEnd2.set('isUnique','true')
                                                elif(row[19]=='isUnique=false'):
                                                    ownedEnd2.set('isUnique','false')
                                                if(row[16]=='isDerived=true'):
                                                    ownedEnd.set('isDerived','true')
                                                elif(row[16]=='isDerived=false'):
                                                    ownedEnd.set('isDerived','false')
                                                if(row[17]=='isNavigable=true'):
                                                    ownedEnd.set('isNavigable','true')
                                                elif(row[17]=='isNavigable=false'):
                                                    ownedEnd.set('isNavigable','false')
                                                if(row[18]=='isOrdered=true'):
                                                    ownedEnd.set('isOrdered','true')
                                                elif(row[18]=='isOrdered=false'):
                                                    ownedEnd.set('isOrdered','false')
                                                if(row[13] in Duplicates):
                                                    ownedEnd2.set('type',row[13]+idString)
                                                else:
                                                    ownedEnd2.set('type',row[13])
                                                if(row[0] in RelationDuplicates):
                                                    RelationDuplicates.remove(row[0])
                                                    ownedEnd2.set('association',row[0]+idString)
                                                else:
                                                    ownedEnd2.set('association',row[0])
                                                upperValue2=ET.SubElement(ownedEnd2,'upperValue')
                                                upperValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                upperValue2.set('xmi:id','')
                                                if(row[22]=='upper=1'):
                                                    upperValue2.set('value','1')
                                                elif(row[22]=='upper=0'):
                                                    upperValue2.set('value','0')
                                                elif(row[22]=='upper=*'):
                                                    upperValue2.set('value','*')
                                                lowerValue2=ET.SubElement(ownedEnd2,'lowerValue')
                                                lowerValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                lowerValue2.set('xmi:id','')
                                                if(row[20]=='lower=1'):
                                                    lowerValue2.set('value','1')
                                                elif(row[20]=='lower=0'):
                                                    lowerValue2.set('value','0')
                                                elif(row[20]=='lower=*'):
                                                    lowerValue2.set('value','*')
                                                lowerValue2.set('xmi:type','uml:LiteralInteger')
                                                lowerValue2.set('xmi:id','')
                                            #NONE
                                            elif(row[4] == 'aggregation=none'):
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
                                                    ownedEnd.set('xmi:id',row[13]+"a")
                                                namecounter = namecounter+1
                                                namestr=str(namecounter)
                                                ownedEnd.set('name',namestr)
                                                if(row[12]=='visibility=public'):
                                                    ownedEnd.set('visibility','public')
                                                elif(row[12]=='visibility=package'):
                                                    ownedEnd.set('visibility','package')
                                                elif(row[12]=='visibility=protected'):
                                                    ownedEnd.set('visibility','protected')
                                                elif(row[12]=='visibility=private'):
                                                    ownedEnd.set('visibility','private')
                                                if(row[8]=='isUnique=true'):
                                                    ownedEnd.set('isUnique','true')
                                                elif(row[8]=='isUnique=false'):
                                                    ownedEnd.set('isUnique','false')
                                                if(row[5]=='isDerived=true'):
                                                    ownedEnd.set('isDerived','true')
                                                elif(row[5]=='isDerived=false'):
                                                    ownedEnd.set('isDerived','false')
                                                if(row[6]=='isNavigable=true'):
                                                    ownedEnd.set('isNavigable','true')
                                                elif(row[6]=='isNavigable=false'):
                                                    ownedEnd.set('isNavigable','false')
                                                if(row[7]=='isOrdered=true'):
                                                    ownedEnd.set('isOrdered','true')
                                                elif(row[7]=='isOrdered=false'):
                                                    ownedEnd.set('isOrdered','false')
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
                                                if(row[11]=='upper=1'):
                                                    upperValue.set('value','1')
                                                elif(row[11]=='upper=0'):
                                                    upperValue.set('value','0')
                                                elif(row[11]=='upper=*'):
                                                    upperValue.set('value','*')
                                                lowerValue=ET.SubElement(ownedEnd,'lowerValue')
                                                lowerValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                lowerValue.set('xmi:id','')
                                                if(row[9]=='lower=1'):
                                                    lowerValue.set('value','1')
                                                elif(row[9]=='lower=0'):
                                                    lowerValue.set('value','0')
                                                elif(row[9]=='lower=*'):
                                                    lowerValue.set('value','*')
                                                lowerValue.set('xmi:type','uml:LiteralInteger')
                                                lowerValue.set('xmi:id','')
                                              
                                                ownedEnd2=ET.SubElement(packageElement,'ownedEnd')
                                                if(row[13] in Duplicates):
                                                    ownedEnd2.set('xmi:id',row[13]+idString)
                                                else:
                                                    ownedEnd2.set('xmi:id',row[13]+"b")
                                                namecounter = namecounter+1
                                                namestr=str(namecounter)
                                                ownedEnd2.set('name',namestr)
                                                if(row[23]=='visibility=public'):
                                                    ownedEnd2.set('visibility','public')
                                                elif(row[23]=='visibility=package'):
                                                    ownedEnd2.set('visibility','package')
                                                elif(row[23]=='visibility=protected'):
                                                    ownedEnd2.set('visibility','protected')
                                                elif(row[23]=='visibility=private'):
                                                    ownedEnd2.set('visibility','private')
                                                if(row[19]=='isUnique=true'):
                                                    ownedEnd2.set('isUnique','true')
                                                elif(row[19]=='isUnique=false'):
                                                    ownedEnd2.set('isUnique','false')
                                                if(row[16]=='isDerived=true'):
                                                    ownedEnd.set('isDerived','true')
                                                elif(row[16]=='isDerived=false'):
                                                    ownedEnd.set('isDerived','false')
                                                if(row[17]=='isNavigable=true'):
                                                    ownedEnd.set('isNavigable','true')
                                                elif(row[17]=='isNavigable=false'):
                                                    ownedEnd.set('isNavigable','false')
                                                if(row[18]=='isOrdered=true'):
                                                    ownedEnd.set('isOrdered','true')
                                                elif(row[18]=='isOrdered=false'):
                                                    ownedEnd.set('isOrdered','false')
                                                if(row[13] in Duplicates):
                                                    ownedEnd2.set('type',row[13]+idString)
                                                else:
                                                    ownedEnd2.set('type',row[13])
                                                if(row[0] in RelationDuplicates):
                                                    RelationDuplicates.remove(row[0])
                                                    ownedEnd2.set('association',row[0]+idString)
                                                else:
                                                    ownedEnd2.set('association',row[0])
                                                upperValue2=ET.SubElement(ownedEnd2,'upperValue')
                                                upperValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                upperValue2.set('xmi:id','')
                                                if(row[22]=='upper=1'):
                                                    upperValue2.set('value','1')
                                                elif(row[22]=='upper=0'):
                                                    upperValue2.set('value','0')
                                                elif(row[22]=='upper=*'):
                                                    upperValue2.set('value','*')
                                                lowerValue2=ET.SubElement(ownedEnd2,'lowerValue')
                                                lowerValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                lowerValue2.set('xmi:id','')
                                                if(row[20]=='lower=1'):
                                                    lowerValue2.set('value','1')
                                                elif(row[20]=='lower=0'):
                                                    lowerValue2.set('value','0')
                                                elif(row[20]=='lower=*'):
                                                    lowerValue2.set('value','*')
                                                lowerValue2.set('xmi:type','uml:LiteralInteger')
                                                lowerValue2.set('xmi:id','')
                                            #Composition
                                            elif(row[4] == 'aggregation=composite'):
                                                packageElement=ET.SubElement(package,'packagedElement')
                                                packageElement.set('xmi:type','uml:Association')
                                                if(row[0] in RelationDuplicates):
                                                    packageElement.set('xmi:id',row[0]+idString)
                                                else:
                                                    packageElement.set('xmi:id',row[0])
                                                packageElement.set('name',row[1])
                                                if(row[2] and row[13] in Duplicates):
                                                    con=row[2]+idString+" "+row[13]+idString
                                                    packageElement.set('navigableOwnedEnd',row[13]+idString)
                                                elif(row[2] in Duplicates):
                                                    con=row[2]+idString+" "+row[13]+"b"
                                                    packageElement.set('navigableOwnedEnd',row[13]+"b")
                                                elif(row[13] in Duplicates):
                                                    con=row[2]+"a"+" "+row[13]+idString
                                                    packageElement.set('navigableOwnedEnd',row[13]+idString)
                                                else:
                                                    con=row[2]+"a"+" "+row[13]+"b"
                                                    packageElement.set('navigableOwnedEnd',row[13]+"b")
                                                packageElement.set('memberEnd',con)
                                                ownedEnd=ET.SubElement(packageElement,'ownedEnd')
                                                if(row[2] in Duplicates):
                                                    ownedEnd.set('xmi:id',row[2]+idString)
                                                else:
                                                    ownedEnd.set('xmi:id',row[2]+"a")
                                                namecounter = namecounter+1
                                                namestr=str(namecounter)
                                                ownedEnd.set('name',namestr)
                                                if(row[12]=='visibility=public'):
                                                    ownedEnd.set('visibility','public')
                                                elif(row[12]=='visibility=package'):
                                                    ownedEnd.set('visibility','package')
                                                elif(row[12]=='visibility=protected'):
                                                    ownedEnd.set('visibility','protected')
                                                elif(row[12]=='visibility=private'):
                                                    ownedEnd.set('visibility','private')
                                                if(row[8]=='isUnique=true'):
                                                    ownedEnd.set('isUnique','true')
                                                elif(row[8]=='isUnique=false'):
                                                    ownedEnd.set('isUnique','false')
                                                if(row[5]=='isDerived=true'):
                                                    ownedEnd.set('isDerived','true')
                                                elif(row[5]=='isDerived=false'):
                                                    ownedEnd.set('isDerived','false')
                                                if(row[6]=='isNavigable=true'):
                                                    ownedEnd.set('isNavigable','true')
                                                elif(row[6]=='isNavigable=false'):
                                                    ownedEnd.set('isNavigable','false')
                                                if(row[7]=='isOrdered=true'):
                                                    ownedEnd.set('isOrdered','true')
                                                elif(row[7]=='isOrdered=false'):
                                                    ownedEnd.set('isOrdered','false')
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
                                                if(row[11]=='upper=1'):
                                                    upperValue.set('value','1')
                                                elif(row[11]=='upper=0'):
                                                    upperValue.set('value','0')
                                                elif(row[11]=='upper=*'):
                                                    upperValue.set('value','*')
                                                lowerValue=ET.SubElement(ownedEnd,'lowerValue')
                                                lowerValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                lowerValue.set('xmi:id','')
                                                if(row[9]=='lower=1'):
                                                    lowerValue.set('value','1')
                                                elif(row[9]=='lower=0'):
                                                    lowerValue.set('value','0')
                                                elif(row[9]=='lower=*'):
                                                    lowerValue.set('value','*')
                                                lowerValue.set('xmi:type','uml:LiteralInteger')
                                                lowerValue.set('xmi:id','')
                                               
                                                ownedEnd2=ET.SubElement(packageElement,'ownedEnd')
                                                if(row[13] in Duplicates):
                                                    ownedEnd2.set('xmi:id',row[13]+idString)
                                                else:
                                                    ownedEnd2.set('xmi:id',row[13]+"b")
                                                namecounter = namecounter+1
                                                namestr=str(namecounter)
                                                ownedEnd2.set('name',namestr)
                                                ownedEnd2.set('aggregation','composite')
                                                if(row[23]=='visibility=public'):
                                                    ownedEnd2.set('visibility','public')
                                                elif(row[23]=='visibility=package'):
                                                    ownedEnd2.set('visibility','package')
                                                elif(row[23]=='visibility=protected'):
                                                    ownedEnd2.set('visibility','protected')
                                                elif(row[23]=='visibility=private'):
                                                    ownedEnd2.set('visibility','private')
                                                if(row[19]=='isUnique=true'):
                                                    ownedEnd2.set('isUnique','true')
                                                elif(row[19]=='isUnique=false'):
                                                    ownedEnd2.set('isUnique','false')
                                                if(row[16]=='isDerived=true'):
                                                    ownedEnd.set('isDerived','true')
                                                elif(row[16]=='isDerived=false'):
                                                    ownedEnd.set('isDerived','false')
                                                if(row[17]=='isNavigable=true'):
                                                    ownedEnd.set('isNavigable','true')
                                                elif(row[17]=='isNavigable=false'):
                                                    ownedEnd.set('isNavigable','false')
                                                if(row[18]=='isOrdered=true'):
                                                    ownedEnd.set('isOrdered','true')
                                                elif(row[18]=='isOrdered=false'):
                                                    ownedEnd.set('isOrdered','false')
                                                if(row[13] in Duplicates):
                                                    ownedEnd2.set('type',row[13]+idString)
                                                else:
                                                    ownedEnd2.set('type',row[13])
                                                if(row[0] in RelationDuplicates):
                                                    RelationDuplicates.remove(row[0])
                                                    ownedEnd2.set('association',row[0]+idString)
                                                else:
                                                    ownedEnd2.set('association',row[0])
                                                upperValue2=ET.SubElement(ownedEnd2,'upperValue')
                                                upperValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                upperValue2.set('xmi:id','')
                                                if(row[22]=='upper=1'):
                                                    upperValue2.set('value','1')
                                                elif(row[22]=='upper=0'):
                                                    upperValue2.set('value','0')
                                                elif(row[22]=='upper=*'):
                                                    upperValue2.set('value','*')
                                                lowerValue2=ET.SubElement(ownedEnd2,'lowerValue')
                                                lowerValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                lowerValue2.set('xmi:id','')
                                                if(row[20]=='lower=1'):
                                                    lowerValue2.set('value','1')
                                                elif(row[20]=='lower=0'):
                                                    lowerValue2.set('value','0')
                                                elif(row[20]=='lower=*'):
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
                                if UMLType[y]=='Class':
                                    temp=classDiagramName
                                    packageElement=ET.SubElement(package,'packagedElement')
                                    packageElement.set('xmi:type','uml:Class')
                                    if(UIDBO[y] in objectsCreated):
                                        packageElement.set('xmi:id',UIDBO[y]+idString)
                                    else:
                                        packageElement.set('xmi:id',UIDBO[y])
                                    packageElement.set('name',ObjectName[y])
                                    if r6[y]== 'Visibility=public':
                                        packageElement.set('visibility','public')
                                    elif r6[y]== 'Visibility=private':
                                        packageElement.set('visibility','private')
                                    if r7[y]== 'isSpecification=false':
                                        packageElement.set('isSpecification','false')
                                    elif r7[y]== 'isSpecification=true':
                                        packageElement.set('isSpecification','true')
                                    if r8[y]== 'isRoot=false':
                                        packageElement.set('isRoot','false')
                                    elif r8[y]== 'isRoot=true':
                                        packageElement.set('isRoot','true')
                                    if r8[y]== 'isLeaf=false':
                                        packageElement.set('isLeaf','false')
                                    elif r8[y]== 'isLeaf=true':
                                        packageElement.set('isLeaf','true')
                                    if r11[y]== 'isActive=false':
                                        packageElement.set('isActive','false')
                                    elif r11[y]== 'isActive=true':
                                        packageElement.set('isActive','true')
                                    if r12[y]== 'isAbstract=false':
                                        packageElement.set('isAbstract','false')
                                    elif r12[y]== 'isAbstract=true':
                                        packageElement.set('isAbstract','true')
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
                                elif UMLType[y]=='Attribute' :
                                    ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                                    if(UIDBO[y] in objectsCreated):
                                        ownedAttribute.set('xmi:id',UIDAttr[y]+idString)
                                    else:
                                        ownedAttribute.set('xmi:id',UIDAttr[y])
                                    ownedAttribute.set('name',AttrName[y])
                                    if r6[y]== 'Visibility=public':
                                        ownedAttribute.set('visibility','public')
                                    elif r6[y]== 'Visibility=private':
                                        ownedAttribute.set('visibility','private')
                                    if r7[y]== 'Multivalued=true':
                                        ownedAttribute.set('Multivalued','true')
                                    elif r7[y]== 'Multivalued=false':
                                        ownedAttribute.set('Multivalued','false')
                                    if r8[y]== 'Mandatory=true':
                                        ownedAttribute.set('Mandatory','true')
                                    elif r8[y]== 'Mandatory=false':
                                        ownedAttribute.set('Mandatory','false')
                                    if r10[y]== 'isDerived=true':
                                        ownedAttribute.set('isDerived','true')
                                    elif r10[y]== 'isDerived=false':
                                        ownedAttribute.set('isDerived','false')
                                    if r11[y]== 'isReadOnly=true':
                                        ownedAttribute.set('isReadOnly','true')
                                    elif r11[y]== 'isReadOnly=false':
                                        ownedAttribute.set('isReadOnly','false')
                                    if r14[y]== 'MultiplicityElement.isOrdered=true':
                                        ownedAttribute.set('isOrdered','true')
                                    elif r14[y]== 'MultiplicityElement.isOrdered=false':
                                        ownedAttribute.set('isOrdered','false')
                                    if r15[y]== 'MultiplicityElement.isUnique=true':
                                        ownedAttribute.set('isUnique','true')
                                    elif r15[y]== 'MultiplicityElement.isUnique=false':
                                        ownedAttribute.set('isUnique','false')
                                    ownedcomment=ET.SubElement(ownedAttribute,'ownedComment')
                                    ownedcomment.set('xmi:type','uml:Comment')
                                    ownedcomment.set('xmi:id','comm'+convertedstring)
                                    comntcounter = comntcounter +1
                                    convertedstring = str(comntcounter)
                                    body=ET.SubElement(ownedcomment,'body')
                                    body.text=comm[y]
                                    if not r13[y]:
                                        types=ET.SubElement(ownedAttribute,'type')
                                        types.set('xmi:type','uml:PrimitiveType')
                                        types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')
                                    else:
                                        my_string = r13[y]
                                        my_list = my_string.split("=")[1]
                                        ownedAttribute.set('type',my_list)
                                elif UMLType[y]=='Enumeration':
                                    if not UIDBO[y] in EnumDuplicateCheck:
                                        EnumDuplicateCheck.append(UIDBO[y])
                                        packageElement=ET.SubElement(package,'packagedElement')
                                        packageElement.set('xmi:type','uml:Enumeration')
                                        packageElement.set('xmi:id',UIDBO[y])
                                        packageElement.set('name',ObjectName[y])
                                        if r6[y]== 'Visibility=public':
                                            packageElement.set('visibility','public')
                                        elif r6[y]== 'Visibility=private':
                                            packageElement.set('visibility','private')
                                        if r7[y]== 'isAbstract=false':
                                            packageElement.set('isAbstract','false')
                                        elif r7[y]== 'isAbstract=true':
                                            packageElement.set('isAbstract','true')
                                        if r8[y]== 'isRoot=false':
                                            packageElement.set('isRoot','false')
                                        elif r8[y]== 'isRoot=true':
                                            packageElement.set('isRoot','true')
                                        if r9[y]== 'isLeaf=false':
                                            packageElement.set('isLeaf','false')
                                        elif r9[y]== 'isLeaf=true':
                                            packageElement.set('isLeaf','true')
                                        ownedcomment=ET.SubElement(packageElement,'ownedComment')
                                        ownedcomment.set('xmi:id','commentid')
                                        body=ET.SubElement(ownedcomment,'body')
                                        body.text=comm[y]
                                elif UMLType[y]=='Enumeration literal':
                                    ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                                    ownedAttribute.set('xmi:id',UIDBO[y])
                                    ownedAttribute.set('name',AttrName[y])
                                    ownedcomment=ET.SubElement(ownedAttribute,'ownedComment')
                                    ownedcomment.set('xmi:id','commentid')
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
                                            if UMLType[d]=='Class':
                                                packageElement=ET.SubElement(package,'packagedElement')
                                                packageElement.set('xmi:type','uml:Class')
                                                packageElement.set('xmi:id',UIDBO[d])
                                                packageElement.set('name',ObjectName[d])
                                                if r6[d]== 'Visibility=public':
                                                    packageElement.set('visibility','public')
                                                elif r6[d]== 'Visibility=private':
                                                    packageElement.set('visibility','private')
                                                if r7[d]== 'isSpecification=false':
                                                    packageElement.set('isSpecification','false')
                                                elif r7[d]== 'isSpecification=true':
                                                    packageElement.set('isSpecification','true')
                                                if r8[d]== 'isRoot=false':
                                                    packageElement.set('isRoot','false')
                                                elif r8[d]== 'isRoot=true':
                                                    packageElement.set('isRoot','true')
                                                if r8[d]== 'isLeaf=false':
                                                    packageElement.set('isLeaf','false')
                                                elif r8[d]== 'isLeaf=true':
                                                    packageElement.set('isLeaf','true')
                                                if r11[d]== 'isActive=false':
                                                    packageElement.set('isActive','false')
                                                elif r11[d]== 'isActive=true':
                                                    packageElement.set('isActive','true')
                                                if r12[d]== 'isAbstract=false':
                                                    packageElement.set('isAbstract','false')
                                                elif r12[d]== 'isAbstract=true':
                                                    packageElement.set('isAbstract','true')
                                                ownedcomment=ET.SubElement(packageElement,'ownedComment')
                                                ownedcomment.set('xmi:type','uml:Comment')
                                                ownedcomment.set('xmi:id','comm'+convertedstring)
                                                comntcounter = comntcounter +1
                                                convertedstring = str(comntcounter)
                                                body=ET.SubElement(ownedcomment,'body')
                                                body.text=comm[d]
                                            elif UMLType[d]=='Attribute':
                                                ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                                                ownedAttribute.set('xmi:id',UIDAttr[d])
                                                ownedAttribute.set('name',AttrName[d])
                                                if r6[d]== 'Visibility=public':
                                                    ownedAttribute.set('visibility','public')
                                                elif r6[d]== 'Visibility=private':
                                                    ownedAttribute.set('visibility','private')
                                                if r7[d]== 'Multivalued=true':
                                                    ownedAttribute.set('Multivalued','true')
                                                elif r7[d]== 'Multivalued=false':
                                                    ownedAttribute.set('Multivalued','false')
                                                if r8[d]== 'Mandatory=true':
                                                    ownedAttribute.set('Mandatory','true')
                                                elif r8[d]== 'Mandatory=false':
                                                    ownedAttribute.set('Mandatory','false')
                                                if r10[d]== 'isDerived=true':
                                                    ownedAttribute.set('isDerived','true')
                                                elif r10[d]== 'isDerived=false':
                                                    ownedAttribute.set('isDerived','false')
                                                if r11[d]== 'isReadOnly=true':
                                                    ownedAttribute.set('isReadOnly','true')
                                                elif r11[d]== 'isReadOnly=false':
                                                    ownedAttribute.set('isReadOnly','false')
                                                if r14[d]== 'MultiplicityElement.isOrdered=true':
                                                    ownedAttribute.set('isOrdered','true')
                                                elif r14[d]== 'MultiplicityElement.isOrdered=false':
                                                    ownedAttribute.set('isOrdered','false')
                                                if r15[d]== 'MultiplicityElement.isUnique=true':
                                                    ownedAttribute.set('isUnique','true')
                                                elif r15[d]== 'MultiplicityElement.isUnique=false':
                                                    ownedAttribute.set('isUnique','false')
                                                ownedcomment=ET.SubElement(ownedAttribute,'ownedComment')
                                                ownedcomment.set('xmi:type','uml:Comment')
                                                ownedcomment.set('xmi:id','comm'+convertedstring)
                                                comntcounter = comntcounter +1
                                                convertedstring = str(comntcounter)
                                                body=ET.SubElement(ownedcomment,'body')
                                                body.text=comm[d]
                                                if not r13[y]:
                                                    types=ET.SubElement(ownedAttribute,'type')
                                                    types.set('xmi:type','uml:PrimitiveType')
                                                    types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')
                                                else:
                                                    my_string = r13[y]
                                                    my_list = my_string.split("=")[1]
                                                    ownedAttribute.set('type',my_list)
                                            checkID.append(makeGeneral[x])

    with open('All CSV Files\BIAN BOM.csv', 'r',encoding="utf-8") as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)
        #csv_reader.replace(" ",np.nan, inplace=True)

        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            if row[0]=='Primitive type':
                packageElement=ET.SubElement(uml,'packagedElement')
                packageElement.set('xmi:type','uml:PrimitiveType')
                packageElement.set('xmi:id',row[1])
                packageElement.set('name',row[2])
                if row[6]== 'Visibility=public':
                        packageElement.set('visibility','public')
                elif row[6]== 'Visibility=private':
                    packageElement.set('visibility','private')
                if row[7]== 'isAbstract=false':
                    packageElement.set('isAbstract','false')
                elif row[7]== 'isAbstract=true':
                    packageElement.set('isAbstract','true')
                if row[8]== 'isRoot=false':
                    packageElement.set('isRoot','false')
                elif row[8]== 'isRoot=true':
                    packageElement.set('isRoot','true')
                if row[9]== 'isLeaf=false':
                    packageElement.set('isLeaf','false')
                elif row[9]== 'isLeaf=true':
                    packageElement.set('isLeaf','true')
                ownedcomment=ET.SubElement(packageElement,'ownedComment')
                ownedcomment.set('xmi:id','commentid')
                body=ET.SubElement(ownedcomment,'body')
                body.text=row[5]
            elif row[0]=='Data type':
                packageElement=ET.SubElement(uml,'packagedElement')
                packageElement.set('xmi:type','uml:PrimitiveType')
                packageElement.set('xmi:id',row[1])
                packageElement.set('name',row[2])
                if row[6]== 'Visibility=public':
                    packageElement.set('visibility','public')
                elif row[6]== 'Visibility=private':
                    packageElement.set('visibility','private')
                if row[7]== 'isAbstract=false':
                    packageElement.set('isAbstract','false')
                elif row[7]== 'isAbstract=true':
                    packageElement.set('isAbstract','true')
                if row[8]== 'isRoot=false':
                    packageElement.set('isRoot','false')
                elif row[8]== 'isRoot=true':
                    packageElement.set('isRoot','true')
                if row[9]== 'isLeaf=false':
                    packageElement.set('isLeaf','false')
                elif row[9]== 'isLeaf=true':
                    packageElement.set('isLeaf','true')
                ownedcomment=ET.SubElement(packageElement,'ownedComment')
                ownedcomment.set('xmi:id','commentid')
                body=ET.SubElement(ownedcomment,'body')
                body.text=row[5]
                with open('All CSV Files\BIAN UML Elements.csv', 'r',encoding="utf-8") as read_obj:
                    # pass the file object to reader() to get the reader object
                    csv_reader2 = csv.reader(read_obj)
                    for row2 in csv_reader2:
                        if row[1]== row2[3]:
                            ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                            ownedAttribute.set('xmi:id',row2[0])
                            ownedAttribute.set('name',row2[2])
                            types=ET.SubElement(ownedAttribute,'type')
                            types.set('xmi:type','uml:PrimitiveType')
                            types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')

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
    SaveDataType=[]
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
            r6=[]
            r7=[]
            r8=[]
            r9=[]
            r10=[]
            r11=[]
            r12=[]
            r13=[]
            r14=[]
            r15=[]
            r16=[]
            r17=[]
            EnumDuplicateCheck=[]
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
            UMLType=[]
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
                            Specialization.append(row4[3])
                            Generalization.append(row4[1])
                        for row2 in csv_reader2:
                            UIDclassdiagram.append(row2[0])
                            UIDRelations.append(row2[1])
                        for row3 in csv_reader3:
                            UMLType.append(row3[0])
                            UIDBO.append(row3[1])
                            ObjectName.append(row3[2])
                            UIDAttr.append(row3[3])
                            AttrName.append(row3[4])
                            comm.append(row3[5])
                            r6.append(row3[6])
                            r7.append(row3[7])
                            r8.append(row3[8])
                            r9.append(row3[9])
                            r10.append(row3[10])
                            r11.append(row3[11])
                            r12.append(row3[12])
                            r13.append(row3[13])
                            r14.append(row3[14])
                            r15.append(row3[15])
                            r16.append(row3[16])
                            r17.append(row3[17])
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
                                            #Association
                                                if(row[0] in Relations):
                                                    if(row[4] == 'aggregation=shared'):
                                                        packageElement=ET.SubElement(package,'packagedElement')
                                                        packageElement.set('xmi:type','uml:Association')
                                                        if(row[0] in RelationDuplicates):
                                                            packageElement.set('xmi:id',row[0]+idString)
                                                        else:
                                                            packageElement.set('xmi:id',row[0])
                                                        packageElement.set('name',row[1])
                                                        if(row[2] and row[13] in Duplicates):
                                                            con=row[2]+idString+" "+row[13]+idString
                                                            packageElement.set('navigableOwnedEnd',row[13]+idString)
                                                        elif(row[2] in Duplicates):
                                                            con=row[2]+idString+" "+row[13]+"b"
                                                            packageElement.set('navigableOwnedEnd',row[13]+"b")
                                                        elif(row[13] in Duplicates):
                                                            con=row[2]+"a"+" "+row[13]+idString
                                                            packageElement.set('navigableOwnedEnd',row[13]+idString)
                                                        else:
                                                            con=row[2]+"a"+" "+row[13]+"b"
                                                            packageElement.set('navigableOwnedEnd',row[13]+"b")
                                                        packageElement.set('memberEnd',con)
                                                        ownedEnd=ET.SubElement(packageElement,'ownedEnd')
                                                        if(row[2] in Duplicates):
                                                            ownedEnd.set('xmi:id',row[2]+idString)
                                                        else:
                                                            ownedEnd.set('xmi:id',row[2]+"a")
                                                        namecounter = namecounter+1
                                                        namestr=str(namecounter)
                                                        ownedEnd.set('name',namestr)
                                                        if(row[12]=='visibility=public'):
                                                            ownedEnd.set('visibility','public')
                                                        elif(row[12]=='visibility=package'):
                                                            ownedEnd.set('visibility','package')
                                                        elif(row[12]=='visibility=protected'):
                                                            ownedEnd.set('visibility','protected')
                                                        elif(row[12]=='visibility=private'):
                                                            ownedEnd.set('visibility','private')
                                                        if(row[8]=='isUnique=true'):
                                                            ownedEnd.set('isUnique','true')
                                                        elif(row[8]=='isUnique=false'):
                                                            ownedEnd.set('isUnique','false')
                                                        if(row[5]=='isDerived=true'):
                                                            ownedEnd.set('isDerived','true')
                                                        elif(row[5]=='isDerived=false'):
                                                            ownedEnd.set('isDerived','false')
                                                        if(row[6]=='isNavigable=true'):
                                                            ownedEnd.set('isNavigable','true')
                                                        elif(row[6]=='isNavigable=false'):
                                                            ownedEnd.set('isNavigable','false')
                                                        if(row[7]=='isOrdered=true'):
                                                            ownedEnd.set('isOrdered','true')
                                                        elif(row[7]=='isOrdered=false'):
                                                            ownedEnd.set('isOrdered','false')
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
                                                        if(row[11]=='upper=1'):
                                                            upperValue.set('value','1')
                                                        elif(row[11]=='upper=0'):
                                                            upperValue.set('value','0')
                                                        elif(row[11]=='upper=*'):
                                                            upperValue.set('value','*')
                                                        lowerValue=ET.SubElement(ownedEnd,'lowerValue')
                                                        lowerValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                        lowerValue.set('xmi:id','')
                                                        if(row[9]=='lower=1'):
                                                            lowerValue.set('value','1')
                                                        elif(row[9]=='lower=0'):
                                                            lowerValue.set('value','0')
                                                        elif(row[9]=='lower=*'):
                                                            lowerValue.set('value','*')
                                                        lowerValue.set('xmi:type','uml:LiteralInteger')
                                                        lowerValue.set('xmi:id','')

                                                        ownedEnd2=ET.SubElement(packageElement,'ownedEnd')
                                                        if(row[13] in Duplicates):
                                                            ownedEnd2.set('xmi:id',row[13]+idString)
                                                        else:
                                                            ownedEnd2.set('xmi:id',row[13]+"b")
                                                        namecounter = namecounter+1
                                                        namestr=str(namecounter)
                                                        ownedEnd2.set('name',namestr)
                                                        if(row[23]=='visibility=public'):
                                                            ownedEnd2.set('visibility','public')
                                                        elif(row[23]=='visibility=package'):
                                                            ownedEnd2.set('visibility','package')
                                                        elif(row[23]=='visibility=protected'):
                                                            ownedEnd2.set('visibility','protected')
                                                        elif(row[23]=='visibility=private'):
                                                            ownedEnd2.set('visibility','private')
                                                        if(row[19]=='isUnique=true'):
                                                            ownedEnd2.set('isUnique','true')
                                                        elif(row[19]=='isUnique=false'):
                                                            ownedEnd2.set('isUnique','false')
                                                        if(row[16]=='isDerived=true'):
                                                            ownedEnd.set('isDerived','true')
                                                        elif(row[16]=='isDerived=false'):
                                                            ownedEnd.set('isDerived','false')
                                                        if(row[17]=='isNavigable=true'):
                                                            ownedEnd.set('isNavigable','true')
                                                        elif(row[17]=='isNavigable=false'):
                                                            ownedEnd.set('isNavigable','false')
                                                        if(row[18]=='isOrdered=true'):
                                                            ownedEnd.set('isOrdered','true')
                                                        elif(row[18]=='isOrdered=false'):
                                                            ownedEnd.set('isOrdered','false')
                                                        if(row[13] in Duplicates):
                                                            ownedEnd2.set('type',row[13]+idString)
                                                        else:
                                                            ownedEnd2.set('type',row[13])
                                                        if(row[0] in RelationDuplicates):
                                                            RelationDuplicates.remove(row[0])
                                                            ownedEnd2.set('association',row[0]+idString)
                                                        else:
                                                            ownedEnd2.set('association',row[0])
                                                        upperValue2=ET.SubElement(ownedEnd2,'upperValue')
                                                        upperValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                        upperValue2.set('xmi:id','')
                                                        if(row[22]=='upper=1'):
                                                            upperValue2.set('value','1')
                                                        elif(row[22]=='upper=0'):
                                                            upperValue2.set('value','0')
                                                        elif(row[22]=='upper=*'):
                                                            upperValue2.set('value','*')
                                                        lowerValue2=ET.SubElement(ownedEnd2,'lowerValue')
                                                        lowerValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                        lowerValue2.set('xmi:id','')
                                                        if(row[20]=='lower=1'):
                                                            lowerValue2.set('value','1')
                                                        elif(row[20]=='lower=0'):
                                                            lowerValue2.set('value','0')
                                                        elif(row[20]=='lower=*'):
                                                            lowerValue2.set('value','*')
                                                        lowerValue2.set('xmi:type','uml:LiteralInteger')
                                                        lowerValue2.set('xmi:id','')
                                                    #NONE
                                                    elif(row[4] == 'aggregation=none'):
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
                                                            ownedEnd.set('xmi:id',row[13]+"a")
                                                        namecounter = namecounter+1
                                                        namestr=str(namecounter)
                                                        ownedEnd.set('name',namestr)
                                                        if(row[12]=='visibility=public'):
                                                            ownedEnd.set('visibility','public')
                                                        elif(row[12]=='visibility=package'):
                                                            ownedEnd.set('visibility','package')
                                                        elif(row[12]=='visibility=protected'):
                                                            ownedEnd.set('visibility','protected')
                                                        elif(row[12]=='visibility=private'):
                                                            ownedEnd.set('visibility','private')
                                                        if(row[8]=='isUnique=true'):
                                                            ownedEnd.set('isUnique','true')
                                                        elif(row[8]=='isUnique=false'):
                                                            ownedEnd.set('isUnique','false')
                                                        if(row[5]=='isDerived=true'):
                                                            ownedEnd.set('isDerived','true')
                                                        elif(row[5]=='isDerived=false'):
                                                            ownedEnd.set('isDerived','false')
                                                        if(row[6]=='isNavigable=true'):
                                                            ownedEnd.set('isNavigable','true')
                                                        elif(row[6]=='isNavigable=false'):
                                                            ownedEnd.set('isNavigable','false')
                                                        if(row[7]=='isOrdered=true'):
                                                            ownedEnd.set('isOrdered','true')
                                                        elif(row[7]=='isOrdered=false'):
                                                            ownedEnd.set('isOrdered','false')
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
                                                        if(row[11]=='upper=1'):
                                                            upperValue.set('value','1')
                                                        elif(row[11]=='upper=0'):
                                                            upperValue.set('value','0')
                                                        elif(row[11]=='upper=*'):
                                                            upperValue.set('value','*')
                                                        lowerValue=ET.SubElement(ownedEnd,'lowerValue')
                                                        lowerValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                        lowerValue.set('xmi:id','')
                                                        if(row[9]=='lower=1'):
                                                            lowerValue.set('value','1')
                                                        elif(row[9]=='lower=0'):
                                                            lowerValue.set('value','0')
                                                        elif(row[9]=='lower=*'):
                                                            lowerValue.set('value','*')
                                                        lowerValue.set('xmi:type','uml:LiteralInteger')
                                                        lowerValue.set('xmi:id','')

                                                        ownedEnd2=ET.SubElement(packageElement,'ownedEnd')
                                                        if(row[13] in Duplicates):
                                                            ownedEnd2.set('xmi:id',row[13]+idString)
                                                        else:
                                                            ownedEnd2.set('xmi:id',row[13]+"b")
                                                        namecounter = namecounter+1
                                                        namestr=str(namecounter)
                                                        ownedEnd2.set('name',namestr)
                                                        if(row[23]=='visibility=public'):
                                                            ownedEnd2.set('visibility','public')
                                                        elif(row[23]=='visibility=package'):
                                                            ownedEnd2.set('visibility','package')
                                                        elif(row[23]=='visibility=protected'):
                                                            ownedEnd2.set('visibility','protected')
                                                        elif(row[23]=='visibility=private'):
                                                            ownedEnd2.set('visibility','private')
                                                        if(row[19]=='isUnique=true'):
                                                            ownedEnd2.set('isUnique','true')
                                                        elif(row[19]=='isUnique=false'):
                                                            ownedEnd2.set('isUnique','false')
                                                        if(row[16]=='isDerived=true'):
                                                            ownedEnd.set('isDerived','true')
                                                        elif(row[16]=='isDerived=false'):
                                                            ownedEnd.set('isDerived','false')
                                                        if(row[17]=='isNavigable=true'):
                                                            ownedEnd.set('isNavigable','true')
                                                        elif(row[17]=='isNavigable=false'):
                                                            ownedEnd.set('isNavigable','false')
                                                        if(row[18]=='isOrdered=true'):
                                                            ownedEnd.set('isOrdered','true')
                                                        elif(row[18]=='isOrdered=false'):
                                                            ownedEnd.set('isOrdered','false')
                                                        if(row[13] in Duplicates):
                                                            ownedEnd2.set('type',row[13]+idString)
                                                        else:
                                                            ownedEnd2.set('type',row[13])
                                                        if(row[0] in RelationDuplicates):
                                                            RelationDuplicates.remove(row[0])
                                                            ownedEnd2.set('association',row[0]+idString)
                                                        else:
                                                            ownedEnd2.set('association',row[0])
                                                        upperValue2=ET.SubElement(ownedEnd2,'upperValue')
                                                        upperValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                        upperValue2.set('xmi:id','')
                                                        if(row[22]=='upper=1'):
                                                            upperValue2.set('value','1')
                                                        elif(row[22]=='upper=0'):
                                                            upperValue2.set('value','0')
                                                        elif(row[22]=='upper=*'):
                                                            upperValue2.set('value','*')
                                                        lowerValue2=ET.SubElement(ownedEnd2,'lowerValue')
                                                        lowerValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                        lowerValue2.set('xmi:id','')
                                                        if(row[20]=='lower=1'):
                                                            lowerValue2.set('value','1')
                                                        elif(row[20]=='lower=0'):
                                                            lowerValue2.set('value','0')
                                                        elif(row[20]=='lower=*'):
                                                            lowerValue2.set('value','*')
                                                        lowerValue2.set('xmi:type','uml:LiteralInteger')
                                                        lowerValue2.set('xmi:id','')
                                                    #Composition
                                                    elif(row[4] == 'aggregation=composite'):
                                                        packageElement=ET.SubElement(package,'packagedElement')
                                                        packageElement.set('xmi:type','uml:Association')
                                                        if(row[0] in RelationDuplicates):
                                                            packageElement.set('xmi:id',row[0]+idString)
                                                        else:
                                                            packageElement.set('xmi:id',row[0])
                                                        packageElement.set('name',row[1])
                                                        if(row[2] and row[13] in Duplicates):
                                                            con=row[2]+idString+" "+row[13]+idString
                                                            packageElement.set('navigableOwnedEnd',row[13]+idString)
                                                        elif(row[2] in Duplicates):
                                                            con=row[2]+idString+" "+row[13]+"b"
                                                            packageElement.set('navigableOwnedEnd',row[13]+"b")
                                                        elif(row[13] in Duplicates):
                                                            con=row[2]+"a"+" "+row[13]+idString
                                                            packageElement.set('navigableOwnedEnd',row[13]+idString)
                                                        else:
                                                            con=row[2]+"a"+" "+row[13]+"b"
                                                            packageElement.set('navigableOwnedEnd',row[13]+"b")
                                                        packageElement.set('memberEnd',con)
                                                        ownedEnd=ET.SubElement(packageElement,'ownedEnd')
                                                        if(row[2] in Duplicates):
                                                            ownedEnd.set('xmi:id',row[2]+idString)
                                                        else:
                                                            ownedEnd.set('xmi:id',row[2]+"a")
                                                        namecounter = namecounter+1
                                                        namestr=str(namecounter)
                                                        ownedEnd.set('name',namestr)
                                                        if(row[12]=='visibility=public'):
                                                            ownedEnd.set('visibility','public')
                                                        elif(row[12]=='visibility=package'):
                                                            ownedEnd.set('visibility','package')
                                                        elif(row[12]=='visibility=protected'):
                                                            ownedEnd.set('visibility','protected')
                                                        elif(row[12]=='visibility=private'):
                                                            ownedEnd.set('visibility','private')
                                                        if(row[8]=='isUnique=true'):
                                                            ownedEnd.set('isUnique','true')
                                                        elif(row[8]=='isUnique=false'):
                                                            ownedEnd.set('isUnique','false')
                                                        if(row[5]=='isDerived=true'):
                                                            ownedEnd.set('isDerived','true')
                                                        elif(row[5]=='isDerived=false'):
                                                            ownedEnd.set('isDerived','false')
                                                        if(row[6]=='isNavigable=true'):
                                                            ownedEnd.set('isNavigable','true')
                                                        elif(row[6]=='isNavigable=false'):
                                                            ownedEnd.set('isNavigable','false')
                                                        if(row[7]=='isOrdered=true'):
                                                            ownedEnd.set('isOrdered','true')
                                                        elif(row[7]=='isOrdered=false'):
                                                            ownedEnd.set('isOrdered','false')
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
                                                        if(row[11]=='upper=1'):
                                                            upperValue.set('value','1')
                                                        elif(row[11]=='upper=0'):
                                                            upperValue.set('value','0')
                                                        elif(row[11]=='upper=*'):
                                                            upperValue.set('value','*')
                                                        lowerValue=ET.SubElement(ownedEnd,'lowerValue')
                                                        lowerValue.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                        lowerValue.set('xmi:id','')
                                                        if(row[9]=='lower=1'):
                                                            lowerValue.set('value','1')
                                                        elif(row[9]=='lower=0'):
                                                            lowerValue.set('value','0')
                                                        elif(row[9]=='lower=*'):
                                                            lowerValue.set('value','*')
                                                        lowerValue.set('xmi:type','uml:LiteralInteger')
                                                        lowerValue.set('xmi:id','')

                                                        ownedEnd2=ET.SubElement(packageElement,'ownedEnd')
                                                        if(row[13] in Duplicates):
                                                            ownedEnd2.set('xmi:id',row[13]+idString)
                                                        else:
                                                            ownedEnd2.set('xmi:id',row[13]+"b")
                                                        namecounter = namecounter+1
                                                        namestr=str(namecounter)
                                                        ownedEnd2.set('name',namestr)
                                                        ownedEnd2.set('aggregation','composite')
                                                        if(row[23]=='visibility=public'):
                                                            ownedEnd2.set('visibility','public')
                                                        elif(row[23]=='visibility=package'):
                                                            ownedEnd2.set('visibility','package')
                                                        elif(row[23]=='visibility=protected'):
                                                            ownedEnd2.set('visibility','protected')
                                                        elif(row[23]=='visibility=private'):
                                                            ownedEnd2.set('visibility','private')
                                                        if(row[19]=='isUnique=true'):
                                                            ownedEnd2.set('isUnique','true')
                                                        elif(row[19]=='isUnique=false'):
                                                            ownedEnd2.set('isUnique','false')
                                                        if(row[16]=='isDerived=true'):
                                                            ownedEnd.set('isDerived','true')
                                                        elif(row[16]=='isDerived=false'):
                                                            ownedEnd.set('isDerived','false')
                                                        if(row[17]=='isNavigable=true'):
                                                            ownedEnd.set('isNavigable','true')
                                                        elif(row[17]=='isNavigable=false'):
                                                            ownedEnd.set('isNavigable','false')
                                                        if(row[18]=='isOrdered=true'):
                                                            ownedEnd.set('isOrdered','true')
                                                        elif(row[18]=='isOrdered=false'):
                                                            ownedEnd.set('isOrdered','false')
                                                        if(row[13] in Duplicates):
                                                            ownedEnd2.set('type',row[13]+idString)
                                                        else:
                                                            ownedEnd2.set('type',row[13])
                                                        if(row[0] in RelationDuplicates):
                                                            RelationDuplicates.remove(row[0])
                                                            ownedEnd2.set('association',row[0]+idString)
                                                        else:
                                                            ownedEnd2.set('association',row[0])
                                                        upperValue2=ET.SubElement(ownedEnd2,'upperValue')
                                                        upperValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                        upperValue2.set('xmi:id','')
                                                        if(row[22]=='upper=1'):
                                                            upperValue2.set('value','1')
                                                        elif(row[22]=='upper=0'):
                                                            upperValue2.set('value','0')
                                                        elif(row[22]=='upper=*'):
                                                            upperValue2.set('value','*')
                                                        lowerValue2=ET.SubElement(ownedEnd2,'lowerValue')
                                                        lowerValue2.set('xmi:type','uml:LiteralUnlimitedNatural')
                                                        lowerValue2.set('xmi:id','')
                                                        if(row[20]=='lower=1'):
                                                            lowerValue2.set('value','1')
                                                        elif(row[20]=='lower=0'):
                                                            lowerValue2.set('value','0')
                                                        elif(row[20]=='lower=*'):
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
                                        if UMLType[y]=='Class':
                                            temp=classDiagramName
                                            packageElement=ET.SubElement(package,'packagedElement')
                                            packageElement.set('xmi:type','uml:Class')
                                            if(UIDBO[y] in objectsCreated):
                                                packageElement.set('xmi:id',UIDBO[y]+idString)
                                            else:
                                                packageElement.set('xmi:id',UIDBO[y])
                                            packageElement.set('name',ObjectName[y])
                                            if r6[y]== 'Visibility=public':
                                                packageElement.set('visibility','public')
                                            elif r6[y]== 'Visibility=private':
                                                packageElement.set('visibility','private')
                                            if r7[y]== 'isSpecification=false':
                                                packageElement.set('isSpecification','false')
                                            elif r7[y]== 'isSpecification=true':
                                                packageElement.set('isSpecification','true')
                                            if r8[y]== 'isRoot=false':
                                                packageElement.set('isRoot','false')
                                            elif r8[y]== 'isRoot=true':
                                                packageElement.set('isRoot','true')
                                            if r8[y]== 'isLeaf=false':
                                                packageElement.set('isLeaf','false')
                                            elif r8[y]== 'isLeaf=true':
                                                packageElement.set('isLeaf','true')
                                            if r11[y]== 'isActive=false':
                                                packageElement.set('isActive','false')
                                            elif r11[y]== 'isActive=true':
                                                packageElement.set('isActive','true')
                                            if r12[y]== 'isAbstract=false':
                                                packageElement.set('isAbstract','false')
                                            elif r12[y]== 'isAbstract=true':
                                                packageElement.set('isAbstract','true')
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
                                        elif UMLType[y]=='Attribute' :
                                            ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                                            if(UIDBO[y] in objectsCreated):
                                                ownedAttribute.set('xmi:id',UIDAttr[y]+idString)
                                            else:
                                                ownedAttribute.set('xmi:id',UIDAttr[y])
                                            ownedAttribute.set('name',AttrName[y])
                                            if r6[y]== 'Visibility=public':
                                                ownedAttribute.set('visibility','public')
                                            elif r6[y]== 'Visibility=private':
                                                ownedAttribute.set('visibility','private')
                                            if r7[y]== 'Multivalued=true':
                                                ownedAttribute.set('Multivalued','true')
                                            elif r7[y]== 'Multivalued=false':
                                                ownedAttribute.set('Multivalued','false')
                                            if r8[y]== 'Mandatory=true':
                                                ownedAttribute.set('Mandatory','true')
                                            elif r8[y]== 'Mandatory=false':
                                                ownedAttribute.set('Mandatory','false')
                                            if r10[y]== 'isDerived=true':
                                                ownedAttribute.set('isDerived','true')
                                            elif r10[y]== 'isDerived=false':
                                                ownedAttribute.set('isDerived','false')
                                            if r11[y]== 'isReadOnly=true':
                                                ownedAttribute.set('isReadOnly','true')
                                            elif r11[y]== 'isReadOnly=false':
                                                ownedAttribute.set('isReadOnly','false')
                                            if r14[y]== 'MultiplicityElement.isOrdered=true':
                                                ownedAttribute.set('isOrdered','true')
                                            elif r14[y]== 'MultiplicityElement.isOrdered=false':
                                                ownedAttribute.set('isOrdered','false')
                                            if r15[y]== 'MultiplicityElement.isUnique=true':
                                                ownedAttribute.set('isUnique','true')
                                            elif r15[y]== 'MultiplicityElement.isUnique=false':
                                                ownedAttribute.set('isUnique','false')
                                            ownedcomment=ET.SubElement(ownedAttribute,'ownedComment')
                                            ownedcomment.set('xmi:type','uml:Comment')
                                            ownedcomment.set('xmi:id','comm'+convertedstring)
                                            comntcounter = comntcounter +1
                                            convertedstring = str(comntcounter)
                                            body=ET.SubElement(ownedcomment,'body')
                                            body.text=comm[y]
                                            if not r13[y]:
                                                types=ET.SubElement(ownedAttribute,'type')
                                                types.set('xmi:type','uml:PrimitiveType')
                                                types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')
                                            else:
                                                my_string = r13[y]
                                                my_list = my_string.split("=")[1]
                                                ownedAttribute.set('type',my_list)
                                                SaveDataType.append(my_list)
                                        elif UMLType[y]=='Enumeration':
                                            if not UIDBO[y] in EnumDuplicateCheck:
                                                EnumDuplicateCheck.append(UIDBO[y])
                                                packageElement=ET.SubElement(package,'packagedElement')
                                                packageElement.set('xmi:type','uml:Enumeration')
                                                packageElement.set('xmi:id',UIDBO[y])
                                                packageElement.set('name',ObjectName[y])
                                                if r6[y]== 'Visibility=public':
                                                    packageElement.set('visibility','public')
                                                elif r6[y]== 'Visibility=private':
                                                    packageElement.set('visibility','private')
                                                if r7[y]== 'isAbstract=false':
                                                    packageElement.set('isAbstract','false')
                                                elif r7[y]== 'isAbstract=true':
                                                    packageElement.set('isAbstract','true')
                                                if r8[y]== 'isRoot=false':
                                                    packageElement.set('isRoot','false')
                                                elif r8[y]== 'isRoot=true':
                                                    packageElement.set('isRoot','true')
                                                if r9[y]== 'isLeaf=false':
                                                    packageElement.set('isLeaf','false')
                                                elif r9[y]== 'isLeaf=true':
                                                    packageElement.set('isLeaf','true')
                                                ownedcomment=ET.SubElement(packageElement,'ownedComment')
                                                ownedcomment.set('xmi:id','commentid')
                                                body=ET.SubElement(ownedcomment,'body')
                                                body.text=comm[y]
                                        elif UMLType[y]=='Enumeration literal':
                                            ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                                            ownedAttribute.set('xmi:id',UIDBO[y])
                                            ownedAttribute.set('name',AttrName[y])
                                            ownedcomment=ET.SubElement(ownedAttribute,'ownedComment')
                                            ownedcomment.set('xmi:id','commentid')
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
                                                    if UMLType[d]=='Class':
                                                        packageElement=ET.SubElement(package,'packagedElement')
                                                        packageElement.set('xmi:type','uml:Class')
                                                        packageElement.set('xmi:id',UIDBO[d])
                                                        packageElement.set('name',ObjectName[d])
                                                        if r6[d]== 'Visibility=public':
                                                            packageElement.set('visibility','public')
                                                        elif r6[d]== 'Visibility=private':
                                                            packageElement.set('visibility','private')
                                                        if r7[d]== 'isSpecification=false':
                                                            packageElement.set('isSpecification','false')
                                                        elif r7[d]== 'isSpecification=true':
                                                            packageElement.set('isSpecification','true')
                                                        if r8[d]== 'isRoot=false':
                                                            packageElement.set('isRoot','false')
                                                        elif r8[d]== 'isRoot=true':
                                                            packageElement.set('isRoot','true')
                                                        if r8[d]== 'isLeaf=false':
                                                            packageElement.set('isLeaf','false')
                                                        elif r8[d]== 'isLeaf=true':
                                                            packageElement.set('isLeaf','true')
                                                        if r11[d]== 'isActive=false':
                                                            packageElement.set('isActive','false')
                                                        elif r11[d]== 'isActive=true':
                                                            packageElement.set('isActive','true')
                                                        if r12[d]== 'isAbstract=false':
                                                            packageElement.set('isAbstract','false')
                                                        elif r12[d]== 'isAbstract=true':
                                                            packageElement.set('isAbstract','true')
                                                        ownedcomment=ET.SubElement(packageElement,'ownedComment')
                                                        ownedcomment.set('xmi:type','uml:Comment')
                                                        ownedcomment.set('xmi:id','comm'+convertedstring)
                                                        comntcounter = comntcounter +1
                                                        convertedstring = str(comntcounter)
                                                        body=ET.SubElement(ownedcomment,'body')
                                                        body.text=comm[d]
                                                    elif UMLType[d]=='Attribute':
                                                        ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                                                        ownedAttribute.set('xmi:id',UIDAttr[d])
                                                        ownedAttribute.set('name',AttrName[d])
                                                        if r6[d]== 'Visibility=public':
                                                            ownedAttribute.set('visibility','public')
                                                        elif r6[d]== 'Visibility=private':
                                                            ownedAttribute.set('visibility','private')
                                                        if r7[d]== 'Multivalued=true':
                                                            ownedAttribute.set('Multivalued','true')
                                                        elif r7[d]== 'Multivalued=false':
                                                            ownedAttribute.set('Multivalued','false')
                                                        if r8[d]== 'Mandatory=true':
                                                            ownedAttribute.set('Mandatory','true')
                                                        elif r8[d]== 'Mandatory=false':
                                                            ownedAttribute.set('Mandatory','false')
                                                        if r10[d]== 'isDerived=true':
                                                            ownedAttribute.set('isDerived','true')
                                                        elif r10[d]== 'isDerived=false':
                                                            ownedAttribute.set('isDerived','false')
                                                        if r11[d]== 'isReadOnly=true':
                                                            ownedAttribute.set('isReadOnly','true')
                                                        elif r11[d]== 'isReadOnly=false':
                                                            ownedAttribute.set('isReadOnly','false')
                                                        if r14[d]== 'MultiplicityElement.isOrdered=true':
                                                            ownedAttribute.set('isOrdered','true')
                                                        elif r14[d]== 'MultiplicityElement.isOrdered=false':
                                                            ownedAttribute.set('isOrdered','false')
                                                        if r15[d]== 'MultiplicityElement.isUnique=true':
                                                            ownedAttribute.set('isUnique','true')
                                                        elif r15[d]== 'MultiplicityElement.isUnique=false':
                                                            ownedAttribute.set('isUnique','false')
                                                        ownedcomment=ET.SubElement(ownedAttribute,'ownedComment')
                                                        ownedcomment.set('xmi:type','uml:Comment')
                                                        ownedcomment.set('xmi:id','comm'+convertedstring)
                                                        comntcounter = comntcounter +1
                                                        convertedstring = str(comntcounter)
                                                        body=ET.SubElement(ownedcomment,'body')
                                                        body.text=comm[d]
                                                        if not r13[y]:
                                                            types=ET.SubElement(ownedAttribute,'type')
                                                            types.set('xmi:type','uml:PrimitiveType')
                                                            types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')
                                                        else:
                                                            my_string = r13[y]
                                                            my_list = my_string.split("=")[1]
                                                            ownedAttribute.set('type',my_list)
                                                            SaveDataType.append(my_list)
                                                    checkID.append(makeGeneral[x])

        with open('All CSV Files\BIAN BOM.csv', 'r',encoding="utf-8") as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = csv.reader(read_obj)
            #csv_reader.replace(" ",np.nan, inplace=True)
            SaveDataType = list(dict.fromkeys(SaveDataType))
            # Iterate over each row in the csv using reader object
            for row in csv_reader:
                if row[0]=='Data type' and row[0] in SaveDataType:
                    packageElement=ET.SubElement(uml,'packagedElement')
                    packageElement.set('xmi:type','uml:PrimitiveType')
                    packageElement.set('xmi:id',row[1])
                    packageElement.set('name',row[2])
                    if row[6]== 'Visibility=public':
                        packageElement.set('visibility','public')
                    elif row[6]== 'Visibility=private':
                        packageElement.set('visibility','private')
                    if row[7]== 'isAbstract=false':
                        packageElement.set('isAbstract','false')
                    elif row[7]== 'isAbstract=true':
                        packageElement.set('isAbstract','true')
                    if row[8]== 'isRoot=false':
                        packageElement.set('isRoot','false')
                    elif row[8]== 'isRoot=true':
                        packageElement.set('isRoot','true')
                    if row[9]== 'isLeaf=false':
                        packageElement.set('isLeaf','false')
                    elif row[9]== 'isLeaf=true':
                        packageElement.set('isLeaf','true')
                    ownedcomment=ET.SubElement(packageElement,'ownedComment')
                    ownedcomment.set('xmi:id','commentid')
                    body=ET.SubElement(ownedcomment,'body')
                    body.text=row[5]
                    with open('All CSV Files\BIAN UML Elements.csv', 'r',encoding="utf-8") as read_obj:
                        # pass the file object to reader() to get the reader object
                        csv_reader2 = csv.reader(read_obj)
                        for row2 in csv_reader2:
                            if row[1]== row2[3]:
                                ownedAttribute=ET.SubElement(packageElement, 'ownedAttribute')
                                ownedAttribute.set('xmi:id',row2[0])
                                ownedAttribute.set('name',row2[2])
                                types=ET.SubElement(ownedAttribute,'type')
                                types.set('xmi:type','uml:PrimitiveType')
                                types.set('href','pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String')



        # create a new XML file with the results
        mydata = ET.tostring(uml)
        x = mydata
        mydata=BeautifulSoup(x,'xml').prettify()
        myfile = open("Separate XMI files For Each Diagram/"+find+".xml", "w",encoding="utf-8")
        myfile.write(mydata)
        print(find+' File Converted')



def main():
    print('Converting Excel to CSV...')
    getExcel()
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