package edu.muc.jxd.main;

import java.io.File;
import java.util.List;

import edu.muc.jxd.cluster.Cluster;
import edu.muc.jxd.distance.DistenceInter;
import edu.muc.jxd.distance.MixDistance;
import edu.muc.jxd.item.ImageItemVector;
import edu.muc.jxd.tools.ToImageVec;

public class Main {

	public static void main(String[] args) {

		DistenceInter distance = new MixDistance();
		// DistenceInter distance = new ImageDistence();
		String path = "7";
		// String path = "test";
		// String path = "all";
		String filePath = path + File.separator;
		List<ImageItemVector<Number>> itemList = ToImageVec.getImageVec(filePath + "image.xml");
		Cluster cluster = new Cluster(itemList, distance, 1, -1, 1);
		// System.out.println("ItemList");

		/*
		 * for (ImageItemVector<Number> imageItemVector : itemList) {
		 * System.out.println(imageItemVector);
		 * 
		 * }
		 * 
		 */
		System.out.println(cluster.getP().toString());
		cluster.getP().writetoFile(new File("E:\\project\\cluster\\" + filePath + "p.txt"));
		System.out.println(cluster.getDelta().toString());
		cluster.getDelta().writetoFile(new File("E:\\project\\cluster\\" + filePath + "delta.txt"));
		System.out.println("dc=" + cluster.getP().getDc());
		cluster.printResult();
		cluster.getP().printEntropy();
	}

}
