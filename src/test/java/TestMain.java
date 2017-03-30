import java.io.*;
import java.util.Iterator;
import java.util.Scanner;

import com.kindlebird.tools.CommonsBetwixt;
import com.kindlebird.tools.XmlUtil;
import com.kindlebird.tools.kit.PathKit;
import org.apache.log4j.Logger;


import edu.muc.jxd.item.ImageItemXml;
import edu.muc.jxd.item.ImageItemXmlElement;
import org.junit.Test;


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


	@Test
	public void testBuildXml(){
		File file= new File(PathKit.getCanonicalPath()+"src/main/python/data/txt/flame.txt");
		Scanner scanner=null;
		try {
			//FileReader fileReader=new FileReader(file);
			scanner=new Scanner(file,"UTF-8");
			while (scanner.hasNext()){
				String line=scanner.nextLine();
				String[] c=line.split("\t");
				logger.debug(new String(c.toString()));
			}
		} catch (Exception e) {
			e.printStackTrace();
		}

	}
}
