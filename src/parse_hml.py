# This file is part of hml-parser.
#
# hml-parser is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# hml-parser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with hml-parser. If not, see <http://www.gnu.org/licenses/>.

import xml.etree.ElementTree
import sys
import os
from os import listdir, makedirs

from os.path import isfile, join, split


def parseHmlDocument(documentFileNameWithPath, outputFileNameWithPath):
    print ('parsing this hml document:\n' + documentFileNameWithPath)
    print ('I will put the results here:\n' + outputFileNameWithPath)
    
    hmlNameSpace = '{http://schemas.nmdp.org/spec/hml/1.0.1}'
    
    # document root is an 
    # Hml diagram can be found at http://schemas.nmdp.org/
    # root node is an "hml" node, with "sample" nodes underneath it.
    # hml also has an "hmlid" and "reporting center" underneath, im ignoring those for now.
    documentRoot = xml.etree.ElementTree.parse(inputFileName).getroot()
    
    outputFile = createOutputFile(outputFileNameWithPath)


        
    for sampleNode in documentRoot.findall(hmlNameSpace + 'sample'):
        sampleID = sampleNode.attrib['id']
        
        outputFile.write('sample,' + str(sampleID) + '\n')
        
        print ('I found a sample node:' + sampleNode.tag)
        #print ('sampleID=' + str(sampleID))
        
        for typingNode in sampleNode.findall(hmlNameSpace + 'typing'):
            #print ('I found a typing node:' + typingNode.tag)
            
            
            
            for alleleAssignmentNode in typingNode.findall(hmlNameSpace + 'allele-assignment'):
                #print ('I found a allele-assignment node:' + alleleAssignmentNode.tag)
                
                # Skip the haploid nodes for now, go with glstring.
                #for haploidNode in alleleAssignmentNode.findall(hmlNameSpace + 'haploid'):
                #    print ('I found a haploid node:' + haploidNode.tag)                    
                #    sequenceLocus = haploidNode.attrib['locus']
                #    sequenceType = haploidNode.attrib['type']
                #    typeString = sequenceLocus + '*' + sequenceType
                #    outputFile.write('HLA_genotyping,' + str(typeString) + '\n')
                
                for glstringNode in alleleAssignmentNode.findall(hmlNameSpace + 'glstring'):
                    #print ('I found a glstring node:' + glstringNode.tag) 
                    #print ('glstringText:' + str(glstringNode.text))
                    outputFile.write('glstring,' + str(glstringNode.text) + '\n')
                    
            # typing nodes have many consensus sequence nodes           
            for consensusSequenceNode in typingNode.findall(hmlNameSpace + 'consensus-sequence'):
                #print ('I found a consensus-sequence node:' + consensusSequenceNode.tag) 
                
                for referenceDatabaseNode in consensusSequenceNode.findall(hmlNameSpace + 'reference-database'):
                    #print ('I found a reference-database node:' + referenceDatabaseNode.tag) 
                    
                    for referenceSequenceNode in referenceDatabaseNode.findall(hmlNameSpace + 'reference-sequence'):
                        #print ('I found a reference-sequence node:' + referenceSequenceNode.tag)
                        
                        refSeqID = referenceSequenceNode.attrib['id']
                        refSeqName = referenceSequenceNode.attrib['name']  
                        
                        referenceStart = referenceSequenceNode.attrib['start']
                        referenceEnd = referenceSequenceNode.attrib['end']  
                   
                        outputFile.write('reference_' + refSeqID 
                            + '[' + str(referenceStart) + ':' + str(referenceEnd) + ']'
                            + ',' + str(refSeqName) + '\n')
                       
                for consensusSequenceBlockNode in consensusSequenceNode.findall(hmlNameSpace + 'consensus-sequence-block'):
                    #print ('I found a consensus-sequence-block node:' + consensusSequenceBlockNode.tag) 
                    
                    consensusSequenceRefID = consensusSequenceBlockNode.attrib['reference-sequence-id']
                    consensusStart = consensusSequenceBlockNode.attrib['start']
                    consensusEnd = consensusSequenceBlockNode.attrib['end']
                    
                    for sequenceNode in consensusSequenceBlockNode.findall(hmlNameSpace + 'sequence'):
                        #print ('I found a sequence node:' + sequenceNode.tag)
                        
                        sequenceValue = sequenceNode.text
                        
                        
                        outputFile.write('consensus_' + consensusSequenceRefID 
                            + '[' + str(consensusStart) + ':' + str(consensusEnd) + ']'
                            + ',' + str(sequenceValue) + '\n')
                         
        
        outputFile.write('\n\n')
    
    outputFile.close()



# This method is a directory-safe way to open up a write file.
def createOutputFile(outputfileName):
    tempDir, tempFilename = split(outputfileName)
    if not os.path.isdir(tempDir):
        os.makedirs(tempDir)
    resultsOutput = open(outputfileName, 'w')
    return resultsOutput



if __name__=='__main__':
    try:
        #The [0] arg is apparently the name of the script.  Interesting, I guess that makes sense.
        #First arg is the input file.  Second arg is the output directory.
        inputFileName = sys.argv[1]
        outputDirectory = sys.argv[2]
        print('*** Parsing an HML document. ***')
        print('Input:' + inputFileName + '\nOutput:' + outputDirectory)
        print('Just a second...')
        
        if not os.path.isdir(outputDirectory):
            os.makedirs(outputDirectory)
            
        outputFileName = join(outputDirectory,'results.csv')
        parseHmlDocument(inputFileName, outputFileName)

        print('Done.  Ben did a great job.')

    except Exception:
        # Top Level exception handling like a pro.
        # This is not really doing anything.
        print 'Unexpected problem during execution:'
        print sys.exc_info()[1]
        raise
