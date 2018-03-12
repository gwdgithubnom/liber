import java.io.*;
import java.util.*;

import com.kindlebird.tools.CommonsBetwixt;
import com.kindlebird.tools.XmlTool;
import com.kindlebird.tools.XmlUtil;
import com.kindlebird.tools.kit.PathKit;
import com.sun.org.apache.xerces.internal.impl.dv.xs.DoubleDV;
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

	@Test
	public void test() {

		TestMain.testBuildIntegerXml();
	}

	public void cache(){
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




	public static void testBuildNormalXml(){
		String name="path";
		File file= new File(PathKit.getCanonicalPath()+"src/main/python/data/txt/"+name+".txt");
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
		XmlUtil.convertToXml(imageItemXml,PathKit.getCanonicalPath()+"src/main/python/data/xml/"+name+".xml");

	}



	public static void testBuildIntegerXml(){
		String name="path";
		File file= new File(PathKit.getCanonicalPath()+"src/main/python/data/txt/"+name+".txt");
		Scanner scanner=null;
		ImageItemXml imageItemXml=new ImageItemXml();
		List<ImageItemXmlElement> imageItemXmlElementList=new ArrayList<>();
		try {
			//FileReader fileReader=new FileReader(file);
			scanner=new Scanner(file,"UTF-8");
			int i=1;
			while (scanner.hasNext()){
				String line=scanner.nextLine();
				ImageItemXmlElement imageItemXmlElement=new ImageItemXmlElement();

				List<String> stringList=Arrays.asList(line.split("\t"));
				stringList.set(0, (int)(Double.parseDouble(stringList.get(0))*100)+"");
				stringList.set(1, (int)(Double.parseDouble(stringList.get(1))*100)+"");
				stringList=new ArrayList<>(stringList);
				String type=stringList.get(stringList.size()-1);
				stringList.remove(stringList.size()-1);
				imageItemXmlElement.setId(""+i);
				imageItemXmlElement.setData(stringList.toString());
				imageItemXmlElementList.add(imageItemXmlElement);
				i++;
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		imageItemXml.setImage(imageItemXmlElementList);
		XmlUtil.convertToXml(imageItemXml,PathKit.getCanonicalPath()+"src/main/python/data/xml/"+name+"_integer.xml");

	}


	public static void testBuildUnbalanceXml(){
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
