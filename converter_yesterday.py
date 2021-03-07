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



def getExcel():
    global read_file
    try:
        path = glob(os.path.join(os.getcwd(), "*.xlsx"))[0]
    except IndexError:
        raise IOError("No .xlsx files found in %r" % os.getcwd())
        return
    excel_file = path
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
    #print('Completed')
    #time.sleep(0.5)
    #print('Converting BIAN BOM SubSuper Type Relations CSV to XMI...')
    #converttoxmiBIANBOMSubSuperTypeRelations()
    #print('Completed')
    #time.sleep(0.5)
    #print('Converting SDBOM CSV to XMI One File...')
    #converttoxmiSDBOMOneFile()
    #print('Completed')
    #time.sleep(0.5)
    #print('Converting SDBOM CSV to XMI Separate File...')
    #converttoxmiSDBOMSeparateFile()
    #print('Completed')
   



#if __name__ == "__main__":

    #myarg1= sys.argv[1]

main()