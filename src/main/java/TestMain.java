import java.io.*;
import java.util.Iterator;

import com.kindlebird.tools.CommonsBetwixt;
import com.kindlebird.tools.XmlUtil;
import com.kindlebird.tools.kit.PathKit;
import org.apache.log4j.Logger;


import edu.muc.jxd.item.ImageItemXml;
import edu.muc.jxd.item.ImageItemXmlElement;


/**
 * Created by gwd on 9/11/2016.
 */
public class TestMain {

	private static Logger logger = Logger.getLogger(TestMain.class.getName());

	//@Test
	public void test() {
		logger.debug(PathKit.getRootClassPath() + "\\image.xml");

		ImageItemXml object = (ImageItemXml) XmlUtil.convertXmlFileToObject(ImageItemXml.class,
				PathKit.getRootClassPath() + "\\image.xml");
		logger.debug(object.getImagesData().toArray());
		Iterator<ImageItemXmlElement> images = object.getImagesData().iterator();
		CommonsBetwixt.persistObjectToFile(images);

	}

	/**
	 * 测试使用txt转xml，进行评估算法性能
	 */


	public void testBuildXml(){
		File file= new File(PathKit.getCanonicalPath()+"src/python/data/txt/flame.txt");
		try {
			FileReader fileReader=new FileReader(file);
			String s=null;
			char[] c=new char[20];
			int i=0;
			while(fileReader.read()>0&&i<20){
				fileReader.read(c);
				s=s+c;
				i++;
			}
			logger.debug(s);
		} catch (Exception e) {
			e.printStackTrace();
		}

	}
}
