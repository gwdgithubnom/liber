class Properties:
    @classmethod
    def getImageXmlResource(cls):
        return "data/xml/image.xml"

    @classmethod
    def getRootPath(cls):
        import os
        path=os.path.dirname(os.path.abspath(__file__))
        path = os.getcwd()
        return path