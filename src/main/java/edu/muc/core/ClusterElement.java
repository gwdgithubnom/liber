package edu.muc.core;

/**
 * File Name : liber - edu.muc.core
 * CopyRright (c) 1949-xxxx:
 * File Number：
 * Author：gwd
 * Date：on 4/26/17
 * Modify：gwd
 * Time ：
 * Comment：
 * Description：
 * Version：
 */
public class ClusterElement {

    private String id=null;
    private String type=null;
    private String name=null;


    public ClusterElement(String str) {


    }


    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }
}
