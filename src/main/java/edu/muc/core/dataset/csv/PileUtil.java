package edu.muc.core.dataset.csv;

import edu.muc.core.entity.EvaluationIndex;

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
public abstract class PileUtil {
    abstract public boolean splitPile(String path,String name,String pattern);
    abstract public EvaluationIndex splitPileWithEvaluation(String path,String name,String pattern);
}
