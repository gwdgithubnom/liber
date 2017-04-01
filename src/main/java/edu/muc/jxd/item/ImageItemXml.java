package edu.muc.jxd.item;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by gwd on 9/13/2016.
 */
@XmlRootElement(name="Images")
public class ImageItemXml {

    @XmlElement(name="Image")
    private List<ImageItemXmlElement> image;
    /**
     * init the entity
     */
    public ImageItemXml(){
        image=new ArrayList<>();
    }

    public List<ImageItemXmlElement> getImagesData() {
        return image;
    }


    public void setImage(List<ImageItemXmlElement> image) {
        this.image = image;
    }


}
