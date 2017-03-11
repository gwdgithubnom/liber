package edu.muc.jxd.distance;

import edu.muc.jxd.item.ImageItemVector;

public class MixDistance implements DistenceInter {

	@Override
	public <T extends Number> int getDistence(ImageItemVector<T> a, ImageItemVector<T> b) {
		// logger.debug("Distance"+a.getId()+"-"+b.getId());
		T[] dataA = (T[]) a.getData();
		T[] dataB = (T[]) b.getData();
		int distance = 0;
		int pos = 0;
		for (int i = 0; i < dataB.length; i++) {
			int ta = dataA[i].intValue();
			int tb = dataB[i].intValue();
			if (ta != tb) {
				pos = pos + i;
			}
			distance = distance + Math.abs((ta - tb));
		}
		return distance + (int) (pos * 0.003);
	}

}
