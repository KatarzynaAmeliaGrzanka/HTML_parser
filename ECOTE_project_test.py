from ECOTE_project import HTML_node
from ECOTE_project import delete_node, is_child, line_nb, checkTagName

# test 1: creating a new node
def test_new_node() -> None:
    root = HTML_node('!DOCTYPE html')
    assert root.tag_name == '!DOCTYPE html'

# test 2: adding attributes to a node
def test_adding_attributes() -> None:
    root = HTML_node('!DOCTYPE html')
    root.text = 'test text'
    root.attributesNames = ['att1', 'att2']
    root.attributesContent = ['cont1', 'cont2']
    assert root.tag_name == '!DOCTYPE html'
    assert root.text == 'test text'
    assert root.attributesNames[0] == 'att1'
    assert root.attributesNames[1] == 'att2'
    assert root.attributesContent[0] == 'cont1'
    assert root.attributesContent[1] == 'cont2'

# test 3: adding children
def test_adding_children() -> None:
    root = HTML_node('!DOCTYPE html')
    root.text = 'test text'
    root.attributesNames = ['att1', 'att2']
    root.attributesContent = ['cont1', 'cont2']

    child = HTML_node('head')
    child.text = 'child text'
    child.attributesNames = ['child att1']
    child.attributesContent = ['cont1']

    root.children.append(child)

    assert root.children[0].tag_name == 'head'
    assert root.children[0].text == 'child text'
    assert root.children[0].attributesNames[0] == 'child att1'
    assert root.children[0].attributesContent[0] == 'cont1'

# test 4: delete node function 
def test_delete_node() -> None:
    root = HTML_node('!DOCTYPE html')
    root.text = 'test text'
    root.attributesNames = ['att1', 'att2']
    root.attributesContent = ['cont1', 'cont2']

    child = HTML_node('head')
    child.text = 'child text'
    child.attributesNames = ['child att1']
    child.attributesContent = ['cont1']

    root.children.append(child)

    delete_node('head', root)
    assert not root.children

# test 5: check if a node is a child function
def test_is_child() -> None:
    root = HTML_node('!DOCTYPE html')
    root.text = 'test text'
    root.attributesNames = ['att1', 'att2']
    root.attributesContent = ['cont1', 'cont2']

    child = HTML_node('head')
    child2 = HTML_node('body')
    root.children.append(child)

    check1 = is_child('head', root)
    check2 = is_child('body', root)

    assert check1 != 0
    assert check2 == 0

# test 6: check a line number function
def test_line_nb() -> None:
    input = 'Paweł i Gaweł w jednym stali domu, \n Paweł na górze, a Gaweł na dole \n Paweł, spokojny, nie wadził nikomu,\nGaweł najdziksze wymyślał swawole.'
    nb = 50
    assert line_nb(nb, input) == 2


# test 7: check if tag name is correct function
def test_tag_check() -> None:
    check1 = checkTagName('h1', 4)
    check2 = checkTagName('wrong', 4)

    assert check1 != 0
    assert check2 == 0



    