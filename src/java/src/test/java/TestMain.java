import java.util.Iterator;

import org.apache.log4j.Logger;
import org.junit.Test;

import edu.muc.jxd.item.ImageItemXml;
import edu.muc.jxd.item.ImageItemXmlElement;
import edu.muc.jxd.tools.CommonsBetwixt;
import edu.muc.jxd.tools.PathKit;
import edu.muc.jxd.tools.XmlUtil;

/**
 * Created by gwd on 9/11/2016.
 */
public class TestMain {

	private static Logger logger = Logger.getLogger(TestMain.class.getName());

	@Test
	public void test() {
		logger.debug(PathKit.getRootClassPath() + "\\image.xml");

		ImageItemXml object = (ImageItemXml) XmlUtil.convertXmlFileToObject(ImageItemXml.class,
				PathKit.getRootClassPath() + "\\image.xml");
		logger.debug(object.getImagesData().toArray());
		Iterator<ImageItemXmlElement> images = object.getImagesData().iterator();
		CommonsBetwixt.persistObjectToFile(images);	
		
	}
}
