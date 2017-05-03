package edu.muc.jxd.item;


import java.util.StringTokenizer;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;

/**
 * Created by gwd on 9/13/2016.
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlRootElement(name = "Image")
@XmlType(propOrder = {"id", "data"})
public class ImageItemXmlElement {
    private String id;
    private String data;

    public ImageItemXmlElement() {
        // data=new ArrayList<>();
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    /**
     * to covert the string to Number[]
     *
     * @return
     */
    public ImageItemVector<Number> getDataToImageItemVector() {
        if (data == null || id.equals("")) {
            return null;
        }
        ImageItemVector<Number> imageItemVector = new ImageItemVector<>();
        // TODO
        String temp = data;
        temp = temp.replace("[", "");
        temp = temp.replace("]", "");
        StringTokenizer tokenizer = new StringTokenizer(temp, ",");
        int l = tokenizer.countTokens();
        Number[] numbers = new Number[l];
        int i = 0;
        while (tokenizer.hasMoreElements()) {
            Integer x = Integer.valueOf(tokenizer.nextToken().trim());
            Integer y = 0;
            if (x > 128) {
                y = 0;
            } else {
                y = 1;
            }
            numbers[i++] = y;
        }
        //TODO this would throw not Integer error.
        imageItemVector.setId(Integer.parseInt(id));
        imageItemVector.setData(numbers);
        return imageItemVector;
    }

    @Override
    public String toString() {
        return "ImageItemXmlElement{" +
                "id=" + id +
                ", data='" + data + '\'' +
                '}';
    }

    public String getData() {
        return data;
    }

    public void setData(String data) {
        this.data = data;
    }
}
