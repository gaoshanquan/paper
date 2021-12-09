import re
from xml.dom.minidom import parse, parseString
import ImageToText

def get_all_interactive_node(root):
    all_interactive_elements = []
    for child in root.childNodes:
        if child.nodeName != '#text':
            if child.getAttribute('clickable') == 'true':
                all_interactive_elements.append(child)
            elif child.getAttribute('long-clickable') == 'true':
                all_interactive_elements.append(child)
            all_interactive_elements.extend(get_all_interactive_node(child))
    return all_interactive_elements


def get_sibling_text(node):
    next = node.nextSibling
    if next.nodeName == '#text':
        next_sibling = next.nextSibling
    else:
        next_sibling = next
    if next_sibling is not None and next_sibling.nodeName != '#text':
        if next_sibling.getAttribute('text') != '':
            return next_sibling.getAttribute('text')
    return ""


def get_child_text_deep(node):
    childNodes = node.childNodes
    text = ''
    for child in childNodes:
        if child.nodeName != '#text':
            if child.getAttribute('text') != '':
                text = text + child.getAttribute('text') + ' '
            else:
                text = text + get_child_text_deep(child)
    return text


def get_child_content(node):
    childNodes = node.childNodes
    num = 0
    for child in childNodes:
        if child.nodeName == '#text':
            num = num + 1
    text = get_child_text_deep(node)
    return text


def get_feature(node):
    text = ''
    text = text + node.getAttribute('text')
    text = text + get_child_content(node)
    text = text + get_sibling_text(node)
    return text


def check_contain_upper(word):
    pattern = re.compile('[A-Z]+')
    match = pattern.findall(word)
    if match:
        return True
    else:
        return False


def check_contain_lower(word):
    pattern = re.compile('[a-z]+')
    match = pattern.findall(word)
    if match:
        return True
    else:
        return False


if __name__ == "__main__":
        xml_path = '' # give the path of .xml file
        output_path = '' # give the path of output file
        f = open(output_path , 'a+', encoding='utf-8')
        DOMTree = parse(xml_path)
        root = DOMTree.documentElement
        clickable_elements = get_all_interactive_node(root)
        for e in clickable_elements:
            text = e.getAttribute('text')
            content_des = e.getAttribute('content-desc')
            child_content = get_child_content(e)
            sibling_text = get_sibling_text(e)
            if text != '':
                if len(text.split()) <= 6:
                    f.write(e.getAttribute('text'))
                    f.write('\n')
            elif child_content != '':
                if len(child_content.split()) <= 6:
                    f.write(get_child_content(e))
                    f.write('\n')
            elif sibling_text != '':
                if len(sibling_text.split()) <= 6:
                    f.write(get_sibling_text(e))
                    f.write('\n')
            elif content_des != '':
                if len(text.split()) <= 6:
                    f.write(content_des)
                    f.write('\n')
        f.close()





