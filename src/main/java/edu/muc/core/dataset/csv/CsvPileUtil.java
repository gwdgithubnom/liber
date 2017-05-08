package edu.muc.core.dataset.csv;

import com.csvreader.CsvReader;
import com.opencsv.CSVWriter;
import edu.muc.core.entity.EvaluationIndex;
import org.apache.log4j.Logger;

import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

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
public class CsvPileUtil extends PileUtil{

    private static Logger logger=Logger.getLogger(CsvPileUtil.class.getName());

    public boolean splitPile(String path, String name, String pattern){
        EvaluationIndex  evaluationIndex=splitPileWithEvaluation(path, name, pattern);
        if(evaluationIndex==null)
            return false;
        else
            return true;
    }

    @Override
    public EvaluationIndex splitPileWithEvaluation(String path, String name, String pattern) {
        Set<String> typeSets=new HashSet<>();
        HashMap<String,Integer> allTypeSizes=new HashMap<>();
        HashMap<String,String> typeLocation=new HashMap<>();
        int allSizes=0;
        if(pattern==null)
            pattern="_";
        if(null==name)
            name="pile";
        // HashMap<Integer, String> map_line_num=new HashMap<>();
        String filePath = path;
        int tp=0,tn=allSizes,fp=0,fn=allSizes;
        String filePathTemp=path+".csv";
        List<String[]> csvStrings=new ArrayList<>();
        List<String> headValues=null;
        int iname=0;
        int headCount=0;
        try {
            // 创建CSV读对象
            //logger.debug(filePath);
            CsvReader csvReader = new CsvReader(filePath);
            csvReader.readHeaders();
            // 读表头
            //boolean headerStatus = csvReader.readHeaders();
            // String[] head=csvReader.getHeaders();
            //logger.debug(csvReader.getHeaderCount());

            headValues=new ArrayList<String>(Arrays.asList(csvReader.getHeaders()));
            headCount=csvReader.getHeaderCount();

            List<HashMap<String, Integer>> count=new ArrayList<HashMap<String, Integer>>();
            int max_number=0;
            String max_type=null;
            int index=0;
            String pileType=null;
            while (csvReader.readRecord()) {
                List<String> listStrings=new ArrayList<>();
                String line = csvReader.get(name);

                line = line.replaceAll("(\')|(\\[)|(\\])", "");
                //HashMap<String, String> clusterSizes = new HashMap<>();
                HashMap<String, Integer> typeSizes = new HashMap<>();
                String[] lines=line.split(",");
                for (String pile : lines) {
                    String[] pileElement=pile.split(pattern);
                    pileType=pileElement[0].trim();
                    typeSets.add(pileType);
                    if (typeSizes.containsKey(pileType)) {

                        int number = typeSizes.get(pileType);
                        number++;
                        typeSizes.put(pileType,number);

                        number = allTypeSizes.get(pileType);
                        number++;
                        allTypeSizes.put(pileType,number);

                    } else{
                        typeSizes.put(pileType,1);
                        //allTypeSizes.get(s+"_TYPE_MAX_INDEX")
                        if(allTypeSizes.containsKey(pileType)){
                            int number=allTypeSizes.get(pileType);
                            number++;
                            allTypeSizes.put(pileType,number);
                        }else{
                            allTypeSizes.put(pileType,1);
                        }
                        /*allTypeSizes.put(index+"_MAX",1);
                        allTypeSizes.put(pileElement[0]+"_MAX_INDEX",index);*/
                    }
                }
                int indexMaxNumber=0;
                String indexMaxType=null;
                for(String s:typeSizes.keySet()){
                    int number=typeSizes.get(s);
                    if(indexMaxNumber<number){
                        indexMaxNumber=number;
                        indexMaxType=s;
                    }
                    //max_type=typeLocation.get(pileElement[0]+"_TYPE_MAX_INDEX");
                    if(allTypeSizes.containsKey(s+"_TYPE_MAX_SIZE")){
                        max_number=allTypeSizes.get(s+"_TYPE_MAX_SIZE");
                        if(max_number<number){
                            //allTypeSizes.put(index+"_INDEX_MAX_TYPE_SIZE",max_number);
                            //typeLocation.put(index+"_INDEX_MAX_TYPE",s);
                            allTypeSizes.put(s+"_TYPE_MAX_SIZE",max_number);
                            typeLocation.put(s+"_TYPE_MAX_INDEX",index+"");
                        }
                        typeLocation.put(index+"_INDEX_MAX_TYPE",indexMaxType);
                        allTypeSizes.put(index+"_INDEX_MAX_TYPE_SIZE",indexMaxNumber);
                    }else {
                        allTypeSizes.put(s+"_TYPE_MAX_SIZE",typeSizes.get(s));
                        typeLocation.put(s+"_TYPE_MAX_INDEX",index+"");
                        typeLocation.put(index+"_INDEX_MAX_TYPE",indexMaxType);
                        allTypeSizes.put(index+"_INDEX_MAX_TYPE_SIZE",indexMaxNumber);
                    }

                }
                allTypeSizes.put(index+"_INDEX_SIZE",lines.length);
                count.add(typeSizes);
                int i=0;
                while (csvReader.getColumnCount()>i){
                    String v = csvReader.get(i);
                    listStrings.add(v);
                    i++;
                }
                allSizes+=lines.length;

                listStrings.set(0,index+"");
                csvStrings.add(listStrings.toArray(new String[listStrings.size()]));
                index++;
            }

            int i=0;
            List<String> headIndex=new ArrayList<>();
            for(String s:typeSets){
                if(headValues.contains(s)){
                    typeLocation.put(s,headCount-(typeSets.size())+i+++"");
                    continue;
                }
                typeLocation.put(s,headCount+i+"");
                headValues.add(headCount+i++,s);
                headIndex.add(s);
            }

            // appendTFHeaders(headIndex,headValues);
            String pile=null;
            Iterator<String[]> csvStringIterator=csvStrings.iterator();
            i=0;
            tn=allSizes;
            fn=allSizes;

            while (csvStringIterator.hasNext()){
                boolean state=false;
                List<String> listString=new ArrayList<>(Arrays.asList(csvStringIterator.next()));
                //pile=listString.get(iname);
                //pile=pile.replaceAll("(\')|(\\[)|(\\])", "");
                headIndex.forEach(s->listString.add(s));
                for(String s:typeSets){
                    if(count.get(i).containsKey(s)){
                        listString.set(Integer.parseInt(typeLocation.get(s)),count.get(i).get(s)+"");
                        if(typeLocation.get(s+"_TYPE_MAX_INDEX").equals(i+"")){
                            //HashMap<String, Integer> ss=count.get(i);
                            /*allTypeSizes.put(s+"_TP",count.get(i).get(s));
                            allTypeSizes.put(s+"_FP",allTypeSizes.get(i+"_INDEX_SIZE")-count.get(i).get(s));*/
                            //fn=allSize
                            /*tp+=count.get(i).get(s);
                            fp+= allTypeSizes.get(i+"_INDEX_SIZE")-count.get(i).get(s);*/
                            /*
                            tp+=count.get(i).get(s);
                            fp+= allTypeSizes.get(i+"_INDEX_SIZE")-count.get(i).get(s);
                            fn+=allSizes-allTypeSizes.get(s)-(allTypeSizes.get(i+"_INDEX_SIZE")-count.get(i).get(s));
                            tn+=allSizes-allTypeSizes.get(s)-(allSizes-allTypeSizes.get(s)-(allTypeSizes.get(i+"_INDEX_SIZE")-count.get(i).get(s)));
                             */
                            if(!typeLocation.get(i+"_INDEX_MAX_TYPE").equals(s)){
                                continue;
                            }else{
                                tp+=count.get(i).get(s);
                                state=true;
                                //logger.warn(allTypeSizes.get(i+"_INDEX_SIZE"));
                                fp+=allTypeSizes.get(i+"_INDEX_SIZE")-count.get(i).get(s);
                                String aa=count.get(i).get(s)+"";
                            }
                        }
                    }
                    else{
                        listString.set(Integer.parseInt(typeLocation.get(s)),0+"");
                    }

                }

                if(state){
                    tn=tn-allTypeSizes.get(i+"_INDEX_SIZE");
                    fn=fn-allTypeSizes.get(i+"_INDEX_SIZE");
                }
                //listString.add("null");

                csvStrings.set(i,listString.toArray(new String[listString.size()]));
                i++;
            }
            csvStrings.add(0,headValues.toArray(new String[headValues.size()]));
            CSVWriter csvWriter = new CSVWriter(new FileWriter(filePath, false));
            csvWriter.writeAll(csvStrings);
            csvWriter.flush();
            csvReader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        /*//FP,TP

        fp=allSizes;
        for(String s:typeSets){
            fp=fp-allTypeSizes.get(s+"_TP");
            tp+=allTypeSizes.get(s+"_TP");
        }

        //FN
        //FN
        for(String s:typeSets){
            fn+=allTypeSizes.get(s)-allTypeSizes.get(s+"_TP");
        }*/

        EvaluationIndex evaluationIndex=new EvaluationIndex(allSizes,tp,tn,fp,fn);

        return evaluationIndex;
    }


}
