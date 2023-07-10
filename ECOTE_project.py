class HTML_node:
    def __init__(self, tagName):
        self.tag_name = tagName
        self.children = []
        self.attributesNames = []
        self.attributesContent = []
        self.text = ''

error_file = "errors12.txt"
input_file = "input12.html" 
output_file = "output12.html"

def test_new_node() -> None:
    root = HTML_node('!DOCTYPE html')
    assert root.tag_name == '!DOCTYPE html'

def tree_to_html(tree, file_path):
    def write_node(node, file):
        if node is None:
            return

        tag = f"<{node.tag_name}"

        # adding atributes if they exist
        if node.attributesNames:
            attributes = ' '.join(f'{name}="{content}"' for name, content in zip(node.attributesNames, node.attributesContent))
            tag += f" {attributes}"

        tag += ">"

        # add opening tag to a file
        file.write(tag + "\n")

        # adding text if it exists
        if node.text:
            file.write(node.text + "\n")

        # repeat recursively for every child of current node
        for child in node.children:
            write_node(child, file)

        # writing the closing tag
        file.write(f"</{node.tag_name}>\n")

    
    with open(file_path, "w") as file:
        # execute the function
        write_node(tree, file)

def remove_decorations(root):
    delete_node('br', root)
    for child in root.children:
        if child.tag_name == 'u' or child.tag_name == 'i':
            child.tag_name = 'b'
        if child.attributesNames:
            for i in range(len(child.attributesNames)):
                if child.attributesNames[i] == 'style':
                    child.attributesContent[i] = 'color:red'
        if child.tag_name == 'img':
            for i in range(len(child.attributesNames)):
                if child.attributesNames[i] == 'width':
                    child.attributesContent[i] = '100'
                if child.attributesNames[i] == 'height':
                    child.attributesContent[i] = '100'
 
        if child.tag_name == 'font':
            child.tag_name = 'b'
            child.attributesNames = []

        

        remove_decorations(child)

# function that deletes a node with a given 'tag_name' from node 'root' and its children
def delete_node(tag_name, root):
    i = 0
    while is_child(tag_name, root):
        i = is_child(tag_name, root)
        i -= 1
        root.children.pop(i)

    for child in root.children:
        while is_child(tag_name, child):
            i = is_child(tag_name, child)
            i -= 1
            child.children.pop(i)

# function that check if a node with a given 'tag_name' is a child of a 'node'

def is_child(tag_name, node):
    for i in range (len(node.children)):
        if node.children[i].tag_name == tag_name:
            return i+1 # if it is a child it returns number greater by 1 from an index of this child (so that it is possible to dectect it the index is 0)
    return 0 # if it is not a child it returns 0

# function that check what is a line number of a character with a given index
def line_nb(i, string):
    line_count = 1
    for k in range (i):
        if string[k] == "\n":
            line_count += 1
    return line_count

def print_node(node):
        output_file = open("output.txt", "w")       
        output_file.close
        
        
        if node is None:
            return

        # Start the opening tag
        tag = f"<{node.tag_name}"

        # Add attributes if any
        if node.attributesNames:
            attributes = ' '.join(f'{name}="{content}"' for name, content in zip(node.attributesNames, node.attributesContent))
            tag += f" {attributes}"

        # Close the opening tag
        tag += ">"

        # Print the opening tag
        print(tag)
        output_file = open("output.txt", "a")
        output_file.write(tag)
        output_file.close

        # Print the node's text if present
        if node.text:
            print(node.text)
            #output_file = open("output.txt", "a")
            #output_file.write(node.text)
           # output_file.close

        # Print children recursively
        for child in node.children:
            print_node(child)


        # Print the closing tag
        print(f"</{node.tag_name}>")
        output_file = open("output.txt", "a")
        output_file.write(f"</{node.tag_name}>")
        output_file.close



#function checking tag - if a opening tag matches a closing tag
def TagCheck(k, tagName): 
    while content[k] != "<":
        k += 1
    k += 1
    tagName2 = ""
    while content[k] != ">":
        tagName2 += content[k]
        k += 1
    if tagName2 == tagName:
        return k
    else:
        errors_file = open(error_file, "a")
        errors_file.write("Error: incorrect " + tagName + " tag. Line: " + str(line_nb(k, content)))
        errors_file.close()
        return 0
    
# function that checks if a name of a given tag 'tagName' is accepted by the parser. Char_nb is passed in case there is an error to pass the line number.
def checkTagName(tagName, char_nb):
    TagList = ['p' , 'fony', 'h1' , 'h2' , 'h3' , 'h4' , 'h5' , 'h6' , 'b', 'u' , 'i' , 'ul' , 'li' , 'div' , 'img' , 'table' , 'tr' , 'td' , 'th' , 'a' , 'br' , 'font', 'title']
    if not any(tagName in x for x in TagList):
        errors_file = open(error_file, "a")
        errors_file.write("Error: unsupported tag name: " + tagName + ". Line: " + str(line_nb(char_nb, content)))
        errors_file.close()
        return 0
    return 1

def checkText(text, char_nb):
    if '>' in text:
        errors_file = open(error_file, "a")
        errors_file.write("Error: Forbidden character in a free text. Line: " + str(line_nb(char_nb, content)))
        errors_file.close()
        return 0
    return 1


def checkAttributeName(attName, char_nb):
    TagList = [ 'href', 'style', 'src' , 'width', 'height', 'alt' ,'title','size']
    if not any(attName in x for x in TagList):
        errors_file = open(error_file, "a")
        errors_file.write("Error: unsupported attribute name: " + attName + ". Line: " + str(line_nb(char_nb, content)))
        errors_file.close()
        return 0
    return 1

# parser of a html file
def make_html_tree(html_file):
    list(html_file)     # make a list of characters of a HTML file 
    i = 0               # variable to iterate the list

    errors_file = open(error_file, "w")       # creating a file for errors
    errors_file.write("Errors: \n")
    errors_file.close()
        
    i = TagCheck(i, '!DOCTYPE html') # checking the first tag (HTML)
    
    if i == 0:      # if there is a mistake in the first tag -> stop execution
        return 0
    
    root = HTML_node('!DOCTYPE html')

    i = TagCheck(i, 'head')
    if i == 0:      # if there is a mistake in the first tag -> stop execution
        return 0
    
    headNode = HTML_node('head')
    root.children = [headNode]

    currentNode = headNode
    currentTag = ''
    # inside head tag
    while i< len(html_file):        # algorithm for the 'head' part
        if(html_file[i] == "<"):
            if(html_file[i+1] == "/"):
                if html_file[i+2:i+6] == 'head':
                    i += 6
                    break       # </head> tag so going to the 'body' part
            else:
                i += 1 
                while html_file[i] != '>' and html_file[i] != ' ':      # saving the tag name
                    currentTag += html_file[i]
                    i += 1
                if not checkTagName(currentTag, i):
                    return 0
                
                newNode = HTML_node(currentTag) # node for this tag

                if html_file[i] == ' ': # there are attributes 
                    
                    while html_file[i].isspace():
                        i += 1 
                    endIndex = html_file.find(' ', i)
                    attName = html_file[i:endIndex] # atribute name
                    if not checkAttributeName(attName, i):
                        return 0
                    newNode.attributesNames.append(attName)

                    i = endIndex
                    while html_file[i].isspace():
                        i += 1 
                    if html_file[i] != '=':
                        errors_file = open(errors_file, "a")       # no =
                        errors_file.write("Errors: No '=' in attribute section. Line: " + str(line_nb(i, html_file)) + '\n')
                        errors_file.close()
                        return 0
                    i += 1
                    while html_file[i].isspace():
                        i += 1 
                    
                    endIndex = html_file.find('"', i+1)
                    attContent = html_file[i+1:endIndex] # atribute content
                    newNode.attributesContent.append(attContent)
                    i = endIndex  
                
                i += 1  # move after "
                endIndex = html_file.find('<',i)
                while html_file[i].isspace():
                        i += 1
                newNode.text = html_file[i: endIndex]
                
                i = endIndex+1
                if html_file[i] != '/':
                    errors_file = open(error_file, "a")       # nested tags
                    errors_file.write("Errors: Forbidden nested tag. Line: "+str(line_nb(i, html_file)))
                    errors_file.close()
                    return 0
                i += 1
                endIndex = html_file.find('>', i)
                endTag = html_file[i:endIndex]
                if newNode.tag_name != endTag:
                        errors_file = open(error_file, "a")       # no end tag or wrong end tag
                        errors_file.write("Errors: Incorrect end tag: " +endTag + ". Line: " + str(line_nb(i, html_file)))
                        errors_file.close()
                        return 0
                i = endIndex
                currentNode.children.append(newNode)
                currentTag =''
                
                break
        i += 1
     
    i += 1 # move after >
    while html_file[i].isspace():
        i += 1

    i += 2 # move after </
    if html_file[i:i+4] != 'head':
            errors_file = open(error_file, "a")       # no end tag or wrong end tag
            errors_file.write("Errors: error in end head tag. Line: " + str(line_nb(i, html_file)))
            errors_file.close()
            return 0
    
    i += 5 # end of head tag


   

    while html_file[i].isspace():
        i += 1
    i += 1 # move ater <
    if (html_file[i:i+4]) != 'body':
            errors_file = open(error_file, "a")       # no end tag or wrong end tag
            errors_file.write("Errors: wrong body tag. Line: " + str(i, html_file))
            errors_file.close()
            return 0 

    i += 5
    
    bodyNode = HTML_node('body')
    root.children.append(bodyNode)


    while i < len(html_file):
        #open tag
        endIndex = html_file.find('<', i)
        i = endIndex + 1
        
        if html_file[i:i+5] =='/body':  #end of body part
            break
        endIndex = html_file.find('>', i)
        endIndex1 = html_file.find(' ', i)

        if endIndex < endIndex1:
            currentTag = html_file[i:endIndex]
            if not checkTagName(currentTag, i):
                    return 0
            i = endIndex + 1
            if currentTag == '/body':
                break
            newNode = HTML_node(currentTag)
            newNode.tag_name = currentTag
            
        else:
            # atributes
            while html_file[i].isspace():
                i += 1
            currentTag = html_file[i:endIndex1]
            newNode = HTML_node(currentTag)
            newNode.tag_name = currentTag
            
            i = endIndex1
            if not checkTagName(currentTag, i):
                    return 0
            i += 1
            while html_file[i] != '>':
                while html_file[i].isspace():
                    i += 1
                endIndex = html_file.find(' ', i)
                endIndex1 = html_file.find('=', i)
                if (endIndex1 < endIndex):
                    endIndex = endIndex1
                while html_file[i].isspace():
                    i += 1
                attName = html_file[i:endIndex]
                if not checkAttributeName(attName, i):
                    return 0
                i = endIndex

                while html_file[i].isspace():
                    i += 1  

                if html_file[i] != '=':
                    errors_file = open(error_file, "a")      
                    errors_file.write("Errors: Wrong syntax of an attribute! Line: " + str(line_nb(i, html_file)))
                    errors_file.close()
                    return 0
                    
                i += 1
                while html_file[i].isspace():
                    i += 1
                endIndex = html_file.find('"', i)
                endIndex1 = html_file.find('"',i+1)
                attContent = html_file[endIndex+1:endIndex1]
                i = endIndex1 +1
                while html_file[i].isspace():
                    i += 1 

                newNode.attributesNames.append(attName)
                newNode.attributesContent.append(attContent)\

                
                
            
        while html_file[i].isspace():
            i += 1

        if newNode.attributesNames:
            i += 1 

        #i = endIndex + 1

        # text
        endIndex = html_file.find('<', i)
        currentText = html_file[i:endIndex]
        if not checkText(currentText, i):
            return 0
        newNode.text = currentText
        i = endIndex 
        # end tag
        i += 1 # <
        endIndex = html_file.find('>', i)
        #i += 1
        if html_file[i] != "/":
            errors_file = open(error_file, "a")       # no end tag or wrong end tag
            errors_file.write("Errors: No closing tag! Line: " + str(line_nb(i, html_file)))
            errors_file.close()
            return 0
        i += 1
        closeTag = html_file[i:endIndex]
        if closeTag != currentTag:
            errors_file = open(error_file, "a")       # no end tag or wrong end tag
            errors_file.write("Errors: Closing tag does not match opening tag! Line: " + str(line_nb(i, html_file)))
            errors_file.close()
            return 0

        
        bodyNode.children.append(newNode)

    return root

f = open(input_file, "r")
content = f.read()
root = make_html_tree(content)

if root:
    remove_decorations(root)
    tree_to_html(root, output_file)

