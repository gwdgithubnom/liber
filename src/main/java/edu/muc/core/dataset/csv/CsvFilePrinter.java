import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Date;

import org.apache.commons.lang.time.DateFormatUtils;

import com.Ostermiller.util.CSVPrint;
import com.Ostermiller.util.CSVPrinter;
/**
 *
 * @author alex.wang
 * csv文件写入
 *
 */
public class CsvFilePrinter{

    private CSVPrint csvPrint;

    /**
     *
     * @param fileName 文件路径
     * @param append 是否支持追加
     * @throws IOException
     */
    public CsvFilePrinter(String fileName,boolean append) throws IOException {
        File file = new File(fileName);
        if(!file.exists()){
            csvPrint = new CSVPrinter(new FileWriter(fileName,append));
            init();
        }else{
            csvPrint = new CSVPrinter(new FileWriter(fileName,append));
            if(!append){
                init();
            }
        }

    }

    public void init() throws IOException{
        write(new String[]{"id","mac","val","date"});
    }

    public void write(String[] values) throws IOException {
        csvPrint.writeln(values);
    }

    public static void main(String[] args) throws Exception {
        String csvFile = "0.005.csv";
        CsvFilePrinter print = new CsvFilePrinter(csvFile,true);

        for(int i=0;i<10;i++){
            print.write(new String[]{"50001"+i,"C914"+i,Integer.toString(-80+i),DateFormatUtils.format(new Date(), "yyyy-MM-dd")});
        }

    }

}
