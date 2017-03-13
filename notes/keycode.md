# scikits
```

f=misc.imread("filename.extention")
plt.imshow(f)
剪切：crop_face=f[1x/4:-1x/4,1y/4:-1y/4]

剪切：ndimage.rotate(f,45)

翻转：ff=np.flipud(f)

锐化：blurred_f=ndimge.gaussian_filter(f,3)

```
