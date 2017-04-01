import java.io.*;
import java.util.*;

import com.kindlebird.tools.CommonsBetwixt;
import com.kindlebird.tools.XmlTool;
import com.kindlebird.tools.XmlUtil;
import com.kindlebird.tools.kit.PathKit;
import com.sun.org.apache.xerces.internal.xs.StringList;
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
	public void testBuildFlameXml(){
		File file= new File(PathKit.getCanonicalPath()+"src/main/python/data/txt/Aggregation.txt");
		Scanner scanner=null;
		ImageItemXml imageItemXml=new ImageItemXml();
		List<ImageItemXmlElement> imageItemXmlElementList=new ArrayList<>();
		try {
			//FileReader fileReader=new FileReader(file);
			scanner=new Scanner(file,"UTF-8");
			int i=0;
			while (scanner.hasNext()){
				String line=scanner.nextLine();
				ImageItemXmlElement imageItemXmlElement=new ImageItemXmlElement();

				List<String> stringList=Arrays.asList(line.split("\t"));
				stringList=new ArrayList<>(stringList);
				String type=stringList.get(stringList.size()-1);
				stringList.remove(stringList.size()-1);
				imageItemXmlElement.setId(type+"_"+i);

				imageItemXmlElement.setData(stringList.toString());
				imageItemXmlElementList.add(imageItemXmlElement);
				i++;
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		imageItemXml.setImage(imageItemXmlElementList);
		XmlUtil.convertToXml(imageItemXml,PathKit.getCanonicalPath()+"src/main/python/data/xml/Aggregation.xml");

	}


	//@Test
	public void testBuildUnbalanceXml(){
		File file= new File(PathKit.getCanonicalPath()+"src/main/python/data/txt/unbalance.txt");
		Scanner scanner=null;
		ImageItemXml imageItemXml=new ImageItemXml();
		List<ImageItemXmlElement> imageItemXmlElementList=new ArrayList<>();
		try {
			//FileReader fileReader=new FileReader(file);
			scanner=new Scanner(file,"UTF-8");
			int i=0;
			while (scanner.hasNext()){
				int a=scanner.nextInt();
				int b=scanner.nextInt();
				ImageItemXmlElement imageItemXmlElement=new ImageItemXmlElement();
				int[] l={a,b};
				imageItemXmlElement.setId("_"+i);
				imageItemXmlElement.setData(Arrays.toString(l));
				imageItemXmlElementList.add(imageItemXmlElement);
				i++;
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		imageItemXml.setImage(imageItemXmlElementList);
		XmlUtil.convertToXml(imageItemXml,PathKit.getCanonicalPath()+"src/main/python/data/xml/unbalance.xml");

	}
}
