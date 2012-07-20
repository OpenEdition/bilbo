# -*- coding: iso-8859-1 -*-
# regression test for SAX 2.0
# $Id: test_sax2.py,v 1.5 2002/09/10 21:37:29 fdrake Exp $

from xml.sax import handler, make_parser, ContentHandler, \
                    SAXException, SAXReaderNotAvailable, SAXParseException
try:
    make_parser()
except SAXReaderNotAvailable:
    # don't try to test this module if we cannot create a parser
    raise ImportError("no XML parsers available")
from xml.sax.saxutils import XMLGenerator, escape, quoteattr, XMLFilterBase, Location
from xml.sax import expatreader
from xml.sax.sax2exts import make_parser
from xml.sax.xmlreader import InputSource, AttributesImpl, AttributesNSImpl
from cStringIO import StringIO
from test.test_support import verbose, TestFailed, findfile
import types

# ===== Utilities

tests = 0
fails = 0

def confirm(outcome, name):
    global tests, fails

    tests = tests + 1
    if not outcome:
        print "Failed " + name
        fails = fails + 1

def test_make_parser2():
    try:
        # Creating parsers several times in a row should succeed.
        # Testing this because there have been failures of this kind
        # before.
        from xml.sax import make_parser
        p = make_parser()
        from xml.sax import make_parser
        p = make_parser()
        from xml.sax import make_parser
        p = make_parser()
        from xml.sax import make_parser
        p = make_parser()
        from xml.sax import make_parser
        p = make_parser()
        from xml.sax import make_parser
        p = make_parser()
    except:
        return 0
    else:
        return p


# ===========================================================================
#
#   saxutils tests
#
# ===========================================================================

# ===== escape

def test_escape_basic():
    return escape("Donald Duck & Co") == "Donald Duck &amp; Co"

def test_escape_all():
    return escape("<Donald Duck & Co>") == "&lt;Donald Duck &amp; Co&gt;"

def test_escape_extra():
    return escape("Hei p� deg", {"�" : "&aring;"}) == "Hei p&aring; deg"

# ===== quoteattr

def test_quoteattr_basic():
    return quoteattr("Donald Duck & Co") == '"Donald Duck &amp; Co"'

def test_single_quoteattr():
    return (quoteattr('Includes "double" quotes')
            == '\'Includes "double" quotes\'')

def test_double_quoteattr():
    return (quoteattr("Includes 'single' quotes")
            == "\"Includes 'single' quotes\"")

def test_single_double_quoteattr():
    return (quoteattr("Includes 'single' and \"double\" quotes")
            == "\"Includes 'single' and &quot;double&quot; quotes\"")

# ===== make_parser

def test_make_parser():
    try:
        # Creating a parser should succeed - it should fall back
        # to the expatreader
        p = make_parser(['xml.parsers.no_such_parser'])
    except:
        return 0
    else:
        return p


# ===== XMLGenerator

start = '<?xml version="1.0" encoding="iso-8859-1"?>\n'

def test_xmlgen_basic():
    result = StringIO()
    gen = XMLGenerator(result)
    gen.startDocument()
    gen.startElement("doc", {})
    gen.endElement("doc")
    gen.endDocument()

    return result.getvalue() == start + "<doc></doc>"

def test_xmlgen_content():
    result = StringIO()
    gen = XMLGenerator(result)

    gen.startDocument()
    gen.startElement("doc", {})
    gen.characters("huhei")
    gen.endElement("doc")
    gen.endDocument()

    return result.getvalue() == start + "<doc>huhei</doc>"

def test_xmlgen_pi():
    result = StringIO()
    gen = XMLGenerator(result)

    gen.startDocument()
    gen.processingInstruction("test", "data")
    gen.startElement("doc", {})
    gen.endElement("doc")
    gen.endDocument()

    return result.getvalue() == start + "<?test data?><doc></doc>"

def test_xmlgen_content_escape():
    result = StringIO()
    gen = XMLGenerator(result)

    gen.startDocument()
    gen.startElement("doc", {})
    gen.characters("<huhei&")
    gen.endElement("doc")
    gen.endDocument()

    return result.getvalue() == start + "<doc>&lt;huhei&amp;</doc>"

def test_xmlgen_attr_escape():
    result = StringIO()
    gen = XMLGenerator(result)

    gen.startDocument()
    gen.startElement("doc", {"a": '"'})
    gen.startElement("e", {"a": "'"})
    gen.endElement("e")
    gen.startElement("e", {"a": "'\""})
    gen.endElement("e")
    gen.endElement("doc")
    gen.endDocument()

    return result.getvalue() == start \
           + "<doc a='\"'><e a=\"'\"></e><e a=\"'&quot;\"></e></doc>"

def test_xmlgen_ignorable():
    result = StringIO()
    gen = XMLGenerator(result)

    gen.startDocument()
    gen.startElement("doc", {})
    gen.ignorableWhitespace(" ")
    gen.endElement("doc")
    gen.endDocument()

    return result.getvalue() == start + "<doc> </doc>"

ns_uri = "http://www.python.org/xml-ns/saxtest/"

def test_xmlgen_ns():
    result = StringIO()
    gen = XMLGenerator(result)

    gen.startDocument()
    gen.startPrefixMapping("ns1", ns_uri)
    gen.startElementNS((ns_uri, "doc"), "ns1:doc", {})
    # add an unqualified name
    gen.startElementNS((None, "udoc"), None, {})
    gen.endElementNS((None, "udoc"), None)
    gen.endElementNS((ns_uri, "doc"), "ns1:doc")
    gen.endPrefixMapping("ns1")
    gen.endDocument()

    return result.getvalue() == start + \
           ('<ns1:doc xmlns:ns1="%s"><udoc></udoc></ns1:doc>' %
                                         ns_uri)

# ===== XMLFilterBase

def test_filter_basic():
    result = StringIO()
    gen = XMLGenerator(result)
    filter = XMLFilterBase()
    filter.setContentHandler(gen)

    filter.startDocument()
    filter.startElement("doc", {})
    filter.characters("content")
    filter.ignorableWhitespace(" ")
    filter.endElement("doc")
    filter.endDocument()

    return result.getvalue() == start + "<doc>content </doc>"

# ===========================================================================
#
#   expatreader tests
#
# ===========================================================================

# ===== XMLReader support

def test_expat_file():
    parser = make_parser()
    result = StringIO()
    xmlgen = XMLGenerator(result)

    parser.setContentHandler(xmlgen)
    parser.parse(open(findfile("test.xml")))

    #print result.getvalue() , xml_test_out
    f = open(findfile("test.xml.result"), 'wt')
    f.write(result.getvalue())
    f.close()

    return result.getvalue() == xml_test_out

# ===== DTDHandler support

class TestDTDHandler:

    def __init__(self):
        self._notations = []
        self._entities  = []

    def notationDecl(self, name, publicId, systemId):
        self._notations.append((name, publicId, systemId))

    def unparsedEntityDecl(self, name, publicId, systemId, ndata):
        self._entities.append((name, publicId, systemId, ndata))

class LexicalHandler:
    _start_dtd = None
    _end_dtd = None

    def startDTD(self, *args):
        self._start_dtd = args

    def endDTD(self, *args):
        self._end_dtd = args

    def comment(self, text):
        pass

    def startCDATA(self):
        pass

    def endCDATA(self):
        pass

def test_expat_dtdhandler():
    parser = make_parser()
    dtdhandler = TestDTDHandler()
    lexhandler = LexicalHandler()
    parser.setDTDHandler(dtdhandler)
    parser.setProperty(handler.property_lexical_handler, lexhandler)

    parser.parse(StringIO('''<!DOCTYPE doc [
  <!ENTITY img SYSTEM "expat.gif" NDATA GIF>
  <!NOTATION GIF PUBLIC "-//CompuServe//NOTATION Graphics Interchange Format 89a//EN">
]>
<doc></doc>'''))

    if hasattr(types, 'UnicodeType'):
        def makestr(uni):
            if uni is None: return uni
            return str(uni)
        dtdhandler._notations = [tuple(map(makestr, dtdhandler._notations[0]))]
        dtdhandler._entities = [tuple(map(makestr, dtdhandler._entities[0]))]

    return dtdhandler._notations == [("GIF", "-//CompuServe//NOTATION Graphics Interchange Format 89a//EN", None)] and \
           dtdhandler._entities == [("img", None, "expat.gif", "GIF")] and \
           lexhandler._start_dtd == ("doc", None, None) and \
           lexhandler._end_dtd == ()


# ===== EntityResolver support

class TestEntityResolver:

    def resolveEntity(self, publicId, systemId):
        inpsrc = InputSource()
        inpsrc.setByteStream(StringIO("<entity/>"))
        return inpsrc

def test_expat_entityresolver():
    parser = make_parser()
    parser.setEntityResolver(TestEntityResolver())
    result = StringIO()
    parser.setContentHandler(XMLGenerator(result))

    parser.parse(StringIO('''<!DOCTYPE doc [
  <!ENTITY test SYSTEM "whatever">
]>
<doc>&test;</doc>'''))

    return result.getvalue() == start + "<doc><entity></entity></doc>"

# ===== Attributes support

class AttrGatherer(ContentHandler):

    def startElement(self, name, attrs):
        self._attrs = attrs

    def startElementNS(self, name, qname, attrs):
        self._attrs = attrs

def test_expat_attrs_empty():
    parser = make_parser()
    gather = AttrGatherer()
    parser.setContentHandler(gather)

    parser.parse(StringIO("<doc/>"))

    return verify_empty_attrs(gather._attrs)

def test_expat_nsattrs_qnames():
    parser = make_parser()
    parser.setFeature(handler.feature_namespaces, 1)
    assert parser._namespaces
    testhandler = AttrGatherer()
    parser.setContentHandler(testhandler)
    ns_uri = 'http://relaxng.org/ns/structure/1.0'
    stream = StringIO("<grammar xmlns='%s' foo='bar'/>" % ns_uri)
    parser.parse(stream)
    attrs = testhandler._attrs

    return attrs.getQNames() == ["foo"] and \
           attrs.has_key((None, "foo"))

def test_expat_attrs_wattr():
    parser = make_parser()
    parser.setFeature(handler.feature_namespaces, 0)
    gather = AttrGatherer()
    parser.setContentHandler(gather)

    parser.parse(StringIO("<doc attr='val'/>"))

    return verify_attrs_wattr(gather._attrs)

def test_expat_nsattrs_empty():
    parser = make_parser()
    parser.setFeature(handler.feature_namespaces, 1)
    gather = AttrGatherer()
    parser.setContentHandler(gather)

    parser.parse(StringIO("<doc/>"))

    return verify_empty_nsattrs(gather._attrs)

def test_expat_nsattrs_wattr():
    parser = make_parser()
    parser.setFeature(handler.feature_namespaces, 1)
    gather = AttrGatherer()
    parser.setContentHandler(gather)

    parser.parse(StringIO("<doc xmlns:ns='%s' ns:attr='val'/>" % ns_uri))

    attrs = gather._attrs

    return attrs.getLength() == 1 and \
           attrs.getNames() == [(ns_uri, "attr")] and \
           attrs.getQNames() == ['ns:attr'] and \
           len(attrs) == 1 and \
           attrs.has_key((ns_uri, "attr")) and \
           attrs.keys() == [(ns_uri, "attr")] and \
           attrs.get((ns_uri, "attr")) == "val" and \
           attrs.get((ns_uri, "attr"), 25) == "val" and \
           attrs.items() == [((ns_uri, "attr"), "val")] and \
           attrs.values() == ["val"] and \
           attrs.getValue((ns_uri, "attr")) == "val" and \
           attrs[(ns_uri, "attr")] == "val"

# ===== InputSource support

xml_test_out = open(findfile("test.xml.out")).read()

def test_expat_inpsource_filename():
    parser = make_parser()
    result = StringIO()
    xmlgen = XMLGenerator(result)

    parser.setContentHandler(xmlgen)
    parser.parse(findfile("test.xml"))

    return result.getvalue() == xml_test_out

def test_expat_inpsource_sysid():
    parser = make_parser()
    result = StringIO()
    xmlgen = XMLGenerator(result)

    parser.setContentHandler(xmlgen)
    parser.parse(InputSource(findfile("test.xml")))

    return result.getvalue() == xml_test_out

def test_expat_inpsource_stream():
    parser = make_parser()
    result = StringIO()
    xmlgen = XMLGenerator(result)

    parser.setContentHandler(xmlgen)
    inpsrc = InputSource()
    inpsrc.setByteStream(open(findfile("test.xml")))
    parser.parse(inpsrc)

    return result.getvalue() == xml_test_out

# ===== IncrementalParser support

def test_expat_incremental():
    result = StringIO()
    xmlgen = XMLGenerator(result)
    parser = expatreader.create_parser()
    parser.setContentHandler(xmlgen)

    parser.feed("<doc>")
    parser.feed("</doc>")
    parser.close()

    return result.getvalue() == start + "<doc></doc>"

def test_expat_incremental_reset():
    result = StringIO()
    xmlgen = XMLGenerator(result)
    parser = expatreader.create_parser()
    parser.setContentHandler(xmlgen)

    parser.feed("<doc>")
    parser.feed("text")

    result = StringIO()
    xmlgen = XMLGenerator(result)
    parser.setContentHandler(xmlgen)
    parser.reset()

    parser.feed("<doc>")
    parser.feed("text")
    parser.feed("</doc>")
    parser.close()

    return result.getvalue() == start + "<doc>text</doc>"

# ===== Locator support

class LocatorTest(XMLGenerator):
    def __init__(self, out=None, encoding="iso-8859-1"):
        XMLGenerator.__init__(self, out, encoding)
        self.location = None

    def endDocument(self):
        XMLGenerator.endDocument(self)
        self.location = Location(self._locator)

def test_expat_locator_noinfo():
    result = StringIO()
    xmlgen = LocatorTest(result)
    parser = make_parser()
    parser.setContentHandler(xmlgen)

    parser.parse(StringIO("<doc></doc>"))

    return xmlgen.location.getSystemId() is None and \
           xmlgen.location.getPublicId() is None and \
           xmlgen.location.getLineNumber() == 1

def test_expat_locator_withinfo():
    result = StringIO()
    xmlgen = LocatorTest(result)
    parser = make_parser()
    parser.setContentHandler(xmlgen)
    parser.parse(findfile("test.xml"))

    return xmlgen.location.getSystemId() == findfile("test.xml") and \
           xmlgen.location.getPublicId() is None


# ===========================================================================
#
#   error reporting
#
# ===========================================================================

def test_expat_inpsource_location():
    parser = make_parser()
    parser.setContentHandler(ContentHandler()) # do nothing
    source = InputSource()
    source.setByteStream(StringIO("<foo bar foobar>"))   #ill-formed
    name = "a file name"
    source.setSystemId(name)
    try:
        parser.parse(source)
    except SAXException, e:
        return e.getSystemId() == name

def test_expat_incomplete():
    parser = make_parser()
    parser.setContentHandler(ContentHandler()) # do nothing
    try:
        parser.parse(StringIO("<foo>"))
    except SAXParseException:
        return 1 # ok, error found
    else:
        return 0


# ===========================================================================
#
#   xmlreader tests
#
# ===========================================================================

# ===== AttributesImpl

def verify_empty_attrs(attrs):
    try:
        attrs.getValue("attr")
        gvk = 0
    except KeyError:
        gvk = 1

    try:
        attrs.getValueByQName("attr")
        gvqk = 0
    except KeyError:
        gvqk = 1

    try:
        attrs.getNameByQName("attr")
        gnqk = 0
    except KeyError:
        gnqk = 1

    try:
        attrs.getQNameByName("attr")
        gqnk = 0
    except KeyError:
        gqnk = 1

    try:
        attrs["attr"]
        gik = 0
    except KeyError:
        gik = 1

    return attrs.getLength() == 0 and \
           attrs.getNames() == [] and \
           attrs.getQNames() == [] and \
           len(attrs) == 0 and \
           not attrs.has_key("attr") and \
           attrs.keys() == [] and \
           attrs.get("attrs") is None and \
           attrs.get("attrs", 25) == 25 and \
           attrs.items() == [] and \
           attrs.values() == [] and \
           gvk and gvqk and gnqk and gik and gqnk

def verify_attrs_wattr(attrs):
    return attrs.getLength() == 1 and \
           attrs.getNames() == ["attr"] and \
           attrs.getQNames() == ["attr"] and \
           len(attrs) == 1 and \
           attrs.has_key("attr") and \
           attrs.keys() == ["attr"] and \
           attrs.get("attr") == "val" and \
           attrs.get("attr", 25) == "val" and \
           attrs.items() == [("attr", "val")] and \
           attrs.values() == ["val"] and \
           attrs.getValue("attr") == "val" and \
           attrs.getValueByQName("attr") == "val" and \
           attrs.getNameByQName("attr") == "attr" and \
           attrs["attr"] == "val" and \
           attrs.getQNameByName("attr") == "attr"

def test_attrs_empty():
    return verify_empty_attrs(AttributesImpl({}))

def test_attrs_wattr():
    return verify_attrs_wattr(AttributesImpl({"attr" : "val"}))

# ===== AttributesImpl

def verify_empty_nsattrs(attrs):
    try:
        attrs.getValue((ns_uri, "attr"))
        gvk = 0
    except KeyError:
        gvk = 1

    try:
        attrs.getValueByQName("ns:attr")
        gvqk = 0
    except KeyError:
        gvqk = 1

    try:
        attrs.getNameByQName("ns:attr")
        gnqk = 0
    except KeyError:
        gnqk = 1

    try:
        attrs.getQNameByName((ns_uri, "attr"))
        gqnk = 0
    except KeyError:
        gqnk = 1

    try:
        attrs[(ns_uri, "attr")]
        gik = 0
    except KeyError:
        gik = 1

    return attrs.getLength() == 0 and \
           attrs.getNames() == [] and \
           attrs.getQNames() == [] and \
           len(attrs) == 0 and \
           not attrs.has_key((ns_uri, "attr")) and \
           attrs.keys() == [] and \
           attrs.get((ns_uri, "attr")) is None and \
           attrs.get((ns_uri, "attr"), 25) == 25 and \
           attrs.items() == [] and \
           attrs.values() == [] and \
           gvk and gvqk and gnqk and gik and gqnk

def test_nsattrs_empty():
    return verify_empty_nsattrs(AttributesNSImpl({}, {}))

def test_nsattrs_wattr():
    attrs = AttributesNSImpl({(ns_uri, "attr") : "val"},
                             {(ns_uri, "attr") : "ns:attr"})

    return attrs.getLength() == 1 and \
           attrs.getNames() == [(ns_uri, "attr")] and \
           attrs.getQNames() == ["ns:attr"] and \
           len(attrs) == 1 and \
           attrs.has_key((ns_uri, "attr")) and \
           attrs.keys() == [(ns_uri, "attr")] and \
           attrs.get((ns_uri, "attr")) == "val" and \
           attrs.get((ns_uri, "attr"), 25) == "val" and \
           attrs.items() == [((ns_uri, "attr"), "val")] and \
           attrs.values() == ["val"] and \
           attrs.getValue((ns_uri, "attr")) == "val" and \
           attrs.getValueByQName("ns:attr") == "val" and \
           attrs.getNameByQName("ns:attr") == (ns_uri, "attr") and \
           attrs[(ns_uri, "attr")] == "val" and \
           attrs.getQNameByName((ns_uri, "attr")) == "ns:attr"


# ===== Main program

def make_test_output():
    parser = make_parser()
    result = StringIO()
    xmlgen = XMLGenerator(result)

    parser.setContentHandler(xmlgen)
    parser.parse(findfile("test.xml"))

    outf = open(findfile("test.xml.out"), "w")
    outf.write(result.getvalue())
    outf.close()

if __name__ == "__main__":
    # print parser name if called directly
    ##print "Testing", make_parser()
    pass

items = locals().items()
items.sort()
for (name, value) in items:
    if name[ : 5] == "test_":
        confirm(value(), name)

if fails != 0:
    raise TestFailed, "%d of %d tests failed" % (fails, tests)
