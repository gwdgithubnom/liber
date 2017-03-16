from tools import  image_xml_builder
from tools import logger
l=logger.getLogger()
from tools import  binaryzation_crop
from tools import  file_manage
file_manage.rename_files()
from  tools import  image_xml_builder
from tools import  image_rebuild
image_rebuild.start_image_rebuild()
image_xml_builder.start_imagexml_builder()

