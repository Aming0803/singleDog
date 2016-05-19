#coding=utf-8
__author__ = 'wan'

from xml.dom import minidom, Node


class XMLStore(object):
    """
    XML 存储类，可方便转换为 Dict
    """
    def __init__(self, xml_string):
        self._raw = xml_string
        self._doc = minidom.parseString(xml_string)

    @property
    def xml2dict(self):
        """
        将 XML 转换为 dict
        """
        self._remove_whitespace_nodes(self._doc.childNodes[0])
        return self._element2dict(self._doc.childNodes[0])

    def _element2dict(self, parent):
        """
        将单个节点转换为 dict
        """
        d = {}
        for node in parent.childNodes:
            if not isinstance(node, minidom.Element):
                continue
            if not node.hasChildNodes():
                continue

            if node.childNodes[0].nodeType == minidom.Node.ELEMENT_NODE:
                try:
                    d[node.tagName]
                except KeyError:
                    d[node.tagName] = []
                d[node.tagName].append(self._element2dict(node))
            elif len(node.childNodes) == 1 and node.childNodes[0].nodeType in [minidom.Node.CDATA_SECTION_NODE, minidom.Node.TEXT_NODE]:
                d[node.tagName] = node.childNodes[0].data
        return d

    def _remove_whitespace_nodes(self, node, unlink=True):
        """
        删除空白无用节点
        """
        remove_list = []
        for child in node.childNodes:
            if child.nodeType == Node.TEXT_NODE and not child.data.strip():
                remove_list.append(child)
            elif child.hasChildNodes():
                self._remove_whitespace_nodes(child, unlink)
        for node in remove_list:
            node.parentNode.removeChild(node)
            if unlink:
                node.unlink()



if __name__ == '__main__':
    test_xml = """
            <xml>
                <ToUserName><![CDATA[toUser]]></ToUserName>
                <FromUserName><![CDATA[FromUser]]></FromUserName>
                <CreateTime>123456789</CreateTime>
                <MsgType><![CDATA[event]]></MsgType>
                <Event><![CDATA[VIEW]]></Event>
                <EventKey><![CDATA[www.qq.com]]></EventKey>
            </xml>
            """
    test_obj = XMLStore(test_xml)
    print test_obj.xml2dict
