package edu.muc.util;

/**
 * File Name : liber - edu.muc.util
 * CopyRright (c) 1949-xxxx:
 * File Number：
 * Author：gwd
 * Date：on 5/1/17
 * Modify：gwd
 * Time ：
 * Comment：
 * Description：
 * Version：
 */
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
public class XmlDataBuilder {

    private static Logger logger = Logger.getLogger(XmlDataBuilder.class.getName());

    @Test
    public void test() {
        try {
            XmlDataBuilder.builderFromTxtToClusterXml("iris.data");
        } catch (IOException e) {
            e.printStackTrace();
        }
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

                List<String> stringList=Arrays.asList(line.split("\t| "));
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

    private static double computeDistance(String str1,String str2){
        String[] str1s=str1.split("\t| ");
        String[] str2s=str2.split("\t| ");
        double result=0;
        for(int i=0;i<str1s.length;i++){
            double t=(Double.parseDouble(str1s[i])-Double.parseDouble(str2s[i]));
            result+=(Double.parseDouble(str1s[i])-Double.parseDouble(str2s[i]))*(Double.parseDouble(str1s[i])-Double.parseDouble(str2s[i]));
        }
        return Math.sqrt(result);
    }

    public static void builderFromTxtToClusterXml(String name) throws IOException {
        File file= new File(PathKit.getCanonicalPath()+"src/main/python/data/txt/"+name+".txt");
        File f=new File(PathKit.getCanonicalPath()+"src/main/python/data/txt/"+name+".tmp.txt");
        Scanner scanner=null;
        ImageItemXml imageItemXml=new ImageItemXml();
        List<ImageItemXmlElement> imageItemXmlElementList=new ArrayList<>();
        List<String> string = new ArrayList<>();
        try {
            //FileReader fileReader=new FileReader(file);
            scanner=new Scanner(file,"UTF-8");
            int i=1;
            while (scanner.hasNext()){
                String line=scanner.nextLine();
                string.add(line);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        String temp=null;
        String line=null;
        double distance=0;

        FileOutputStream fileOutputStream=new FileOutputStream(f);
        for(int i=0;i<string.size();i++){
            line=string.get(i);

            for(int j=i+1;j<string.size();j++){
                temp=string.get(j);
                distance=computeDistance(line,temp);
                temp=i+" "+j+" "+distance+"\n";
                fileOutputStream.write(temp.getBytes());
            }
            fileOutputStream.flush();
            ImageItemXmlElement imageItemXmlElement=new ImageItemXmlElement();
            List<String> stringList=Arrays.asList(line.split("\t| "));
            //stringList.set(0, (Double.parseDouble(stringList.get(0)))+"");
            //stringList.set(1, (Double.parseDouble(stringList.get(1)))+"");
            //stringList=new ArrayList<>(stringList);
            //String type=stringList.get(stringList.size()-1);
            //stringList.remove(stringList.size()-1);
            imageItemXmlElement.setId(""+i);
            imageItemXmlElement.setData(stringList.toString());
            imageItemXmlElementList.add(imageItemXmlElement);

        }
        fileOutputStream.close();
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

