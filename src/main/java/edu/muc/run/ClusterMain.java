package edu.muc.run;

import com.kindlebird.tools.kit.PathKit;
import com.opencsv.CSVReader;
import com.opencsv.CSVWriter;
import com.opencsv.bean.*;
import com.opencsv.exceptions.CsvDataTypeMismatchException;
import com.opencsv.exceptions.CsvRequiredFieldEmptyException;
import edu.muc.core.dataset.csv.CSVFileUtil;
import edu.muc.core.dataset.csv.CsvPileUtil;
import edu.muc.core.entity.EvaluationIndex;
import org.apache.commons.io.FilenameUtils;
import org.apache.log4j.Logger;
import org.apache.poi.sl.draw.geom.Path;
import org.junit.Test;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

/**
 * File Name : liber - edu.muc.run
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
public class ClusterMain {

        private static Logger logger=Logger.getLogger(ClusterMain.class.getName());
        @Test
        public  void runSplit() throws IOException {
            CsvPileUtil csvPileUtil=new CsvPileUtil();
            logger.debug(PathKit.getCanonicalPath());
            File file=new File("/home/gwd/Projects/liber/src/main/python/data/result/aggregation/2017-05-08-14-36-58/2017-05-08-14-36-58/");
            File evalutionFile=new File(file.getParent()+"/evalution.csv");
            if(!evalutionFile.exists()){
                try {
                    evalutionFile.createNewFile();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            FileWriter evalutionFileWriter=new FileWriter(evalutionFile);

            File[] files=file.listFiles();
            //List<EvaluationIndex> listEvaluationIndex=getEvaluationIndex(new File(file+"/evalution.csv"));
            List<String[]> listEvaluationIndex=new ArrayList<String[]>();
            listEvaluationIndex.add(EvaluationIndex.getOpenCSVFormat());

            for (File f:
                 files) {
                EvaluationIndex e=csvPileUtil.splitPileWithEvaluation(f.getPath(),"pile",null);
                e.setId(FilenameUtils.getBaseName(f.getPath()));
                listEvaluationIndex.add(e.getOpenCSVString());
            }

            writeToCSV(listEvaluationIndex,evalutionFileWriter);
        }


        public static boolean writeToCSV(List<String[]> csvString,FileWriter fileWriter){
            CSVWriter csvWriter=null;
            try {
                csvWriter=new CSVWriter(fileWriter);
                csvWriter.writeAll(csvString);
                csvWriter.flush();
            } catch (IOException e) {
                logger.fatal(e.toString());
            }

            return true;
        }

        public static List<EvaluationIndex> getEvaluationIndex(File file){
            logger.info("running function getEvaluationIndex from"+file);
            List<EvaluationIndex> listEvaluationIndex=null;
            ColumnPositionMappingStrategy strat = new ColumnPositionMappingStrategy();
            strat.setType(EvaluationIndex.class);
            String[] columns = EvaluationIndex.getOpenCSVFormat(); // the fields to bind do in your JavaBean
            strat.setColumnMapping(columns);
            CSVReader csvReader=null;
            try {
                csvReader=new CSVReader(new FileReader(file));
            } catch (FileNotFoundException e1) {
                logger.warn(file+" is not found.");
                try {
                    file.createNewFile();
                    logger.warn(file+" has build.");
                } catch (IOException e2) {
                    e2.printStackTrace();
                }
            }
            CsvToBean csv = new CsvToBean();
            try{
                listEvaluationIndex=csv.parse(strat,csvReader);
            }catch (Exception e){
                logger.warn("did not found any Bean by default strategy.");
                listEvaluationIndex=new ArrayList<EvaluationIndex>();
            }

            return listEvaluationIndex;
        }


        public static boolean toCsv(List<EvaluationIndex> listEvaluationIndex,File file){
            logger.info("running tocsv.."+file);
            StatefulBeanToCsvBuilder statefulBeanToCsvBuilder= null;
            //new FileWriter(file+"evalution.csv")
            try {
                statefulBeanToCsvBuilder = new StatefulBeanToCsvBuilder<EvaluationIndex>(new FileWriter(file));
            } catch (IOException e1) {
                e1.printStackTrace();
            }

            StatefulBeanToCsv statefulBeanToCsv=statefulBeanToCsvBuilder.build();
            try {
                statefulBeanToCsv.write(listEvaluationIndex);

            } catch (CsvDataTypeMismatchException e1) {
                e1.printStackTrace();
            } catch (CsvRequiredFieldEmptyException e1) {
                e1.printStackTrace();
            }

            return true;
        }

}
