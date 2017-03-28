import java.io.File;
import java.util.ArrayList;
import java.util.List;

import edu.muc.core.distance.DistenceInter;
import edu.muc.core.distance.ImageDistence;
import edu.muc.core.distance.MixDistance;
import org.junit.Test;

import edu.muc.jxd.item.ImageItemVector;


public class Main {

	@Test
	public void domain() {
		ImageItemVector<Number> item1 = new ImageItemVector<>();
		Integer[] data1 = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
		item1.setData(data1);
		Integer[] data2 = { 0, 2, 1, 3, 4, 3, 6, 6, 1, 9 };
		ImageItemVector<Number> item2 = new ImageItemVector<>();
		item2.setData(data2);

		List<ImageItemVector<Number>> list = new ArrayList<>();
		list.add(item1);
		list.add(item2);

		ImageDistence distance = new ImageDistence();
		//Cluster cluster = new Cluster(list, distance);
		//System.out.println(cluster.getDelta().toString());
	}

	@Test
	public void testData() {
		DistenceInter distance = new MixDistance();
		//DistenceInter distance = new ImageDistence();
		//List<ImageItemVector<Number>> itemList = ToImageVec.getImageVec();
		//Cluster cluster = new Cluster(itemList, distance);
		/*System.out.println("ItemList");
		for (ImageItemVector<Number> imageItemVector : itemList) {
			System.out.println(imageItemVector);
		}
		System.out.println("p");
		System.out.println(cluster.getP().toString());
		cluster.getP().writetoFile(new File("E:\\project\\cluster\\p.txt"));
		System.out.println("Delta");
		System.out.println(cluster.getDelta().toString());
		cluster.getDelta().writetoFile(new File("E:\\project\\cluster\\delta.txt"));
		System.out.println("dc="+cluster.getP().getDc());
		cluster.printResult();*/
	}
}
