package edu.muc.jxd.main;

import java.io.File;
import java.util.List;

import edu.muc.jxd.cluster.Cluster;
import edu.muc.jxd.dataset.DataFormat;
import edu.muc.jxd.distance.DistenceInter;
import edu.muc.jxd.distance.SimpleDistance;
import edu.muc.jxd.item.ImageItemVector;

public class TestOtherDataSet {

	public static void main(String[] args) {

		DistenceInter distance = new SimpleDistance();
		String path = "unbance";
		String filePath = path + File.separator;
		List<ImageItemVector<Number>> result = DataFormat
				.getDataSetFromTxt("E:\\project\\cluster\\" + path + "\\data.txt", " ", "double");
		for (ImageItemVector<Number> imageItemVector : result) {
			System.out.println(imageItemVector);

		}
		Cluster cluster = new Cluster(result, distance, 0, -1, 5);

		System.out.println(cluster.getP().toString());
		cluster.getP().writetoFile(new File("E:\\project\\cluster\\" + filePath + "p.txt"));
		System.out.println(cluster.getDelta().toString());
		cluster.getDelta().writetoFile(new File("E:\\project\\cluster\\" + filePath + "delta.txt"));
		System.out.println("dc=" + cluster.getP().getDc());
		cluster.printResult();

		cluster.getP().printEntropy();

	}

}
