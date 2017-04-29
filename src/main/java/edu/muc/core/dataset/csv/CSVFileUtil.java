package edu.muc.core.dataset.csv;

import java.util.*;
import java.awt.RenderingHints.Key;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.NotActiveException;
import java.lang.reflect.Array;
import java.nio.charset.Charset;

import com.Ostermiller.*;

import com.csvreader.CsvReader;
import com.csvreader.CsvWriter;

import org.apache.commons.lang.time.DateFormatUtils;

import com.Ostermiller.util.CSVPrint;
import com.Ostermiller.util.CSVPrinter;

public class CSVFileUtil {
	
	
	public static void main(String[] args) {

		// size
		HashMap<String, String> typeSizes = new HashMap<>();
		// HashMap<Integer, String> map_line_num=new HashMap<>();
		String filePath = "C:\\Users\\齐析屿\\Desktop\\gwd-accuracy rate\\2017-04-13-16-28\\0.005.csv";

		try {
			// 创建CSV读对象
			CsvReader csvReader = new CsvReader(filePath);
			// 读表头
			boolean headerStatus = csvReader.readHeaders();
			if (!headerStatus)
				System.err.println("csv is not stander.");
			// String[] head=csvReader.getHeaders();
			int n = 0;
			CSVPrinter csvPrint = new CSVPrinter(new FileWriter(
					"C:\\Users\\齐析屿\\Desktop\\gwd-accuracy rate\\2017-04-13-16-28\\0.005-解析.csv", false));
			while (csvReader.readRecord()) {

				// 读一整行
				// System.out.println(csvReader.getRawRecord());
				// 读这行的某一列
				// System.out.println(csvReader.get("pile"));
				String p_id = csvReader.get("p_id");
				String line = "";
				line = csvReader.get("pile");
				// System.out.println("zksk"+line);
				// line.replaceAll("'","");
				line = line.replaceAll("(\')|(\\[)|(\\])", "");

				// System.out.println(line);

				n++;
				HashMap<String, String> clusterSizes = new HashMap<>();
				for (String pile : line.split(",")) {
					int m = 0;
					// System.out.print(pile+n);
					// int a=0,b=0,c=0;
					for (String num : pile.split("_")) {
						if (m % 2 == 0) {
							// System.out.print("___"+num+" ");
							// map.put(p_id, num);
							if (typeSizes.containsKey(num)) {
								// System.out.println("Find the old
								// one:"+map.get(p_id)+" old
								// number:"+map2.get(map.get(p_id)));
								int number = Integer.parseInt(typeSizes.get(num));
								number++;
								Integer newvalue = new Integer(number);
								String new2 = newvalue.toString();
								typeSizes.replace(num, typeSizes.get(num), new2);
								// System.out.println("Find the old
								// one:"+map.get(p_id)+" total number:"+new2);
							} else {
								typeSizes.put(num, "1");
								// if(head.)
								// System.out.println("Add the new
								// one:"+map.get(p_id)+" "+"1");
							}
							// if(map3.containsKey(map.get(p_id))){
							// int
							// number3=Integer.parseInt(map3.get(map.get(p_id)));
							// number3++;
							// Integer newvalue3= new Integer(number3);
							// String new3=newvalue3.toString();
							// map3.replace(map.get(p_id),map3.get(map.get(p_id)),
							// new3);
							//// System.out.println("Find the old
							// one:"+map.get(p_id)+" total number:"+new3);
							// }else{
							// map3.put(map.get(p_id), "1");
							//// System.out.println("Add the new
							// one:"+map.get(p_id)+" "+"1");
							// }
							// System.out.println(map3.keySet());
						}
						m++;
					}
				}

			}
			csvReader.close();
			CsvReader csvReader1 = new CsvReader(filePath);
			csvReader1.readHeaders();
//			List<String>
			csvPrint.write(csvReader1.getHeaders());
			for (String element : typeSizes.keySet()) {
				String ele = element;
				csvPrint.write(ele);
			}
			csvPrint.writeln();
			while (csvReader1.readRecord()) {
				String p_id = csvReader1.get("p_id");
				String line1 = "";
				line1 = csvReader1.get("pile");
				line1 = line1.replaceAll("(\')|(\\[)|(\\])", "");
				// System.out.println(line);
				n++;

				HashMap<String, String> map3 = new HashMap<>();
				for (String pile : line1.split(",")) {
					int m = 0;
					for (String num : pile.split("_")) {
						if (m % 2 == 0) {
							// for(String header:map2.keySet()){
							// String string = header.split("'")[1];
							if (map3.containsKey(num)) {
								int number3 = Integer.parseInt(map3.get(num));
								number3++;
								Integer newvalue3 = new Integer(number3);
								String new3 = newvalue3.toString();
								map3.replace(num, map3.get(num), new3);
								System.out.println("Find the old one:" + num + "  total number:" + map3.get(num));
							} else {
								map3.put(num, "1");
								System.out.println("Add the new one:" + num + "  " + map3.get(num));
							}
							System.out.println(map3.keySet());
						}

						m++;
					}
				}
				for(String key:csvReader1.getHeaders()){
					if(key=="")
						csvPrint.print(csvReader1.get(0));
					else
						csvPrint.print(csvReader1.get(key));					
				}
				
				for (String each : typeSizes.keySet()) {					
					if (null!=map3.get(each)) {
						csvPrint.write(map3.get(each));						
					} else {
						csvPrint.write("0");
					}
				}
				csvPrint.writeln();
			}

			System.out.println(typeSizes.keySet());

		} catch (IOException e) {
			e.printStackTrace();
		}


		
	}


}
