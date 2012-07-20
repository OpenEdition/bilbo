########################################################################
#
# File Name:            CommentElement.py
#
#
"""
Implementation of the XSLT Spec comment stylesheet element.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 FourThought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""
import cStringIO
import xml.dom.Element
import xml.dom.ext
import xml.xslt
from xml.xslt import XsltException, Error
from xml.xslt import XsltElement
from xml.xpath import Conversions

class CommentElement(XsltElement):
    legalAttrs = ()

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='comment',
                 prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)
        return
        
    def instantiate(self, context, processor):

        origState = context.copy()
        context.setNamespaces(self._nss)

        #FIXME: Add error checking of child nodes
        processor.pushResult()
        for child in self.childNodes:
            context = child.instantiate(context, processor)[0]
        result = processor.popResult()
        data = Conversions.StringValue(result)
        processor.writers[-1].comment(data)
        processor.releaseRtf(result)

        context.set(origState)

        return (context,)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, )
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        return

