import java.beans.IntrospectionException;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.StringWriter;
import java.util.Date;
import java.util.Iterator;

import com.kindlebird.tools.XmlUtil;
import com.kindlebird.tools.kit.PathKit;
import org.junit.Test;
import org.xml.sax.SAXException;

import edu.muc.jxd.item.ImageItemXml;
import edu.muc.jxd.item.ImageItemXmlElement;


import org.apache.commons.betwixt.io.BeanWriter;
import org.apache.log4j.Logger;

/**
 * 
 */

/**
 * @author Simon
 *
 */
public class ApacheTest {

	private static Logger logger = Logger.getLogger(ApacheTest.class.getName());
	@Test
	public void apacheTest() throws IOException, SAXException, IntrospectionException {
		
		  // Start by preparing the writer
        // We'll write to a string 
        StringWriter outputWriter = new StringWriter(); 
        
        // Betwixt just writes out the bean as a fragment
        // So if we want well-formed xml, we need to add the prolog
        outputWriter.write("<?xml version='1.0' ?>");
        
        // Create a BeanWriter which writes to our prepared stream
        BeanWriter beanWriter = new BeanWriter(outputWriter);
        
        // Configure betwixt
        // For more details see java docs or later in the main documentation
        beanWriter.getXMLIntrospector().getConfiguration().setAttributesForPrimitives(false);
        beanWriter.getBindingConfiguration().setMapIDs(false);
        beanWriter.enablePrettyPrint();

        // If the base element is not passed in, Betwixt will guess 
        // But let's write example bean as base element 'person'
        ImageItemXml object = (ImageItemXml) XmlUtil.convertXmlFileToObject(ImageItemXml.class,
				PathKit.getRootClassPath() + "\\image.xml");
		
		Iterator<ImageItemXmlElement> images = object.getImagesData().iterator();
		
			ImageItemXmlElement imageItemXmlElement = images.next();
			beanWriter.write((new Date()).toString(),imageItemXmlElement );
		
      
        
        // Write to System.out
        // (We could have used the empty constructor for BeanWriter 
        // but this way is more instructive)
        logger.debug(outputWriter.toString());
        
        // Betwixt writes fragments not documents so does not automatically close 
        // writers or streams.
        // This example will do no more writing so close the writer now.
        
    	FileOutputStream out=new FileOutputStream(new File(PathKit.getRootClassPath()+"/test.xml"));
		BeanWriter writer = new BeanWriter(out);
        writer.setEndTagForEmptyElement(true);
       
        writer.write((new Date()).toString(),imageItemXmlElement);   
        outputWriter.close();
        writer.flush();
        writer.close();
      
	}
}
