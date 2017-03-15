# scikits
```

f=misc.imread("filename.extention")
plt.imshow(f)
剪切：crop_face=f[1x/4:-1x/4,1y/4:-1y/4]

剪切：ndimage.rotate(f,45)

翻转：ff=np.flipud(f)

锐化：blurred_f=ndimge.gaussian_filter(f,3)

a=[i+1 for i in range(10)]

a=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
a = map(lambda x:x+1,a)


row=data[-1]
column=data[:,-1]
np.row_stack((data,row))
np.column_stack((data,row))


```
