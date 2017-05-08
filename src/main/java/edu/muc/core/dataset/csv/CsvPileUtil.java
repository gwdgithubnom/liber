package edu.muc.core.dataset.csv;

import au.com.bytecode.opencsv.CSVWriter;
import com.Ostermiller.util.CSVPrinter;
import com.csvreader.CsvReader;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

/**
 * File Name : liber - edu.muc.core.dataset.csv
 * CopyRright (c) 1949-xxxx:
 * File Number：
 * Author：gwd
 * Date：on 5/4/17
 * Modify：gwd
 * Time ：
 * Comment：
 * Description：
 * Version：
 */
public class PileCsvUtil {

    public boolean splitPile(String path){
        HashMap<String, Integer> typeSizes = new HashMap<>();
        // HashMap<Integer, String> map_line_num=new HashMap<>();
        String filePath = path;
        String filePathTemp=path+".csv";

        try {
            // 创建CSV读对象
            CsvReader csvReader = new CsvReader(filePath);
            // 读表头
            boolean headerStatus = csvReader.readHeaders();
            if (!headerStatus)
                System.err.println("csv is not stander.");
            // String[] head=csvReader.getHeaders();
            int n = 0;
            CSVWriter csvWriter = new CSVWriter(new FileWriter(filePathTemp, false));
            while (csvReader.readRecord()) {
                String line = csvReader.get("pile");
                line = line.replaceAll("(\')|(\\[)|(\\])", "");
                n++;
                //HashMap<String, String> clusterSizes = new HashMap<>();
                for (String pile : line.split(",")) {
                    String[] pileElement=pile.split("_");
                    if (typeSizes.containsKey(pileElement[0])) {
                        int number = typeSizes.get(pileElement[0]);
                        number++;
                        typeSizes.put(pileElement[0],number);
                    } else{
                        typeSizes.put(pileElement[0],1);
                    }
                }
            }
            CSVPrinter
            csvReader.close();
            csvReader.readHeaders();
            System.out.println(Arrays.asList(csvReader.getHeaders()).getClass());
            String[] headers=csvReader.getHeaders();
            List<String[]> listStrings=new ArrayList<>();

            for (String element : typeSizes.keySet()) {
                String ele = element;

            }

            listStrings.add(csvReader.getHeaders());
            csvWriter.writeln();

            while (csvReader.readRecord()) {
                String p_id = csvReader.get("p_id");
                String line1 = "";
                line1 = csvReader.get("pile");
                line1 = line1.replaceAll("(\')|(\\[)|(\\])", "");
                n++;

                HashMap<String, String> map3 = new HashMap<>();
                for (String pile : line1.split(",")) {
                    int m = 0;
                    for (String num : pile.split("_")) {
                        if (m % 2 == 0) {
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
                for(String key:csvReader.getHeaders()){
                    if(key=="")
                        csvWriter.print(csvReader.get(0));
                    else
                        csvWriter.print(csvReader.get(key));
                }

                for (String each : typeSizes.keySet()) {
                    if (null!=map3.get(each)) {
                        csvWriter.write(map3.get(each));
                    } else {
                        csvWriter.write("0");
                    }
                }
                csvWriter.writeln();
            }

            System.out.println(typeSizes.keySet());

        } catch (IOException e) {
            e.printStackTrace();
        }



    }

}
