package edu.muc.core.entity;

/**
 * File Name : liber - edu.muc.core.entity
 * CopyRright (c) 1949-xxxx:
 * File Number：
 * Author：gwd
 * Date：on 5/7/17
 * Modify：gwd
 * Time ：
 * Comment：
 * Description：
 * Version：
 */
public class EvaluationIndex {


    private String id;
    private double tp;
    private double tn;
    private double fp;
    private double fn;
    private double n;
    private double tnr;
    private double fnr;
    private double fpr;
    private double p;
    private double a;
    private double r;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public EvaluationIndex(double n, double tp, double tn, double fp, double fn){
        this.id="";
        this.n=n;
        this.tp=tp;
        this.tn=tn;
        this.fp=fp;
        this.fn=fn;
        this.tnr=tn/(tn+fp);
        this.fnr=fn/(tp+fn);
        this.fpr=fp/(tp+fn);
        this.p=tp/(tp+fp);
        this.a=(tp+tn)/(tp+fn+fp+tn);
        this.r=tp/(tp+fn);
    }

    public static String[] getOpenCSVFormat(){
        return new String[]{"id","N","TP","TN","FP","FN","TNR","FPR","P","A","R"};
    }

    public double getTp() {
        return tp;
    }

    public void setTp(double tp) {
        this.tp = tp;
    }

    public double getTn() {
        return tn;
    }

    public void setTn(double tn) {
        this.tn = tn;
    }

    public double getFp() {
        return fp;
    }

    public void setFp(double fp) {
        this.fp = fp;
    }

    public double getFn() {
        return fn;
    }

    public void setFn(double fn) {
        this.fn = fn;
    }


    @Override
    public String toString() {
        return "EvaluationIndex{" +
                "id='" + id + '\'' +
                ", tp=" + tp +
                ", tn=" + tn +
                ", fp=" + fp +
                ", fn=" + fn +
                ", n=" + n +
                ", tnr=" + tnr +
                ", fnr=" + fnr +
                ", fpr=" + fpr +
                ", p=" + p +
                ", a=" + a +
                ", r=" + r +
                '}';
    }

    public String[] getOpenCSVString(){
        return new String[]{id,n+"",tp+"",tn+"",fp+"",fn+"",tnr+"",fpr+"",p+"",a+"",r+""};
    }

    /**
     * 添加TP，FN，FP，FN的头设置

     *
     * True Positive （真正, TP）被模型预测为正的正样本；可以称作判断为真的正确率

     True Negative（真负 , TN）被模型预测为负的负样本 ；可以称作判断为假的正确率

     False Positive （假正, FP）被模型预测为正的负样本；可以称作误报率

     False Negative（假负 , FN）被模型预测为负的正样本；可以称作漏报率

     True Positive Rate（真正率 , TPR）或灵敏度（sensitivity）
     TPR = TP /（TP + FN）
     正样本预测结果数 / 正样本实际数

     True Negative Rate（真负率 , TNR）或特指度（specificity）
     TNR = TN /（TN + FP）
     负样本预测结果数 / 负样本实际数

     False Positive Rate （假正率, FPR）
     FPR = FP /（FP + TN）
     被预测为正的负样本结果数 /负样本实际数

     False Negative Rate（假负率 , FNR）
     FNR = FN /（TP + FN）
     被预测为负的正样本结果数 / 正样本实际数

     精确度（Precision）：
     P = TP/(TP+FP) ; 反映了被分类器判定的正例中真正的正例样本的比重

     准确率（Accuracy）
     A = (TP + TN)/(P+N) = (TP + TN)/(TP + FN + FP + TN);

     反映了分类器统对整个样本的判定能力——能将正的判定为正，负的判定为负

     召回率(Recall)，也称为 True Positive Rate:
     R = TP/(TP+FN) = 1 - FN/T; 反映了被正确判定的正例占总的正例的比重
     */
}
