#!/bin/bash
function recursive_copy_file(){
	dir=$(ls $1)
	for name in ${dir[*]}
	do
		if [ -f $1/$name ]; then
			if [ ! -f  $2/$name ]; then
				# ho "$1/$name $2/$name"
				cp $1/$name $2/$name
			fi
		elif [ -d $1/$name ]; then
			if [ ! -d $2/$name ]; then
				mkdir -p $2/$name
			fi
			recursive_copy_file $1/$name $2/$name
		fi	
	done
}

target='/home/gwd/Github/liber/'
delete_target='/home/gwd/Projects/liber/src/main/python/data/result/temp/*'
for l in $(cat deploy.list)
do
	t=$target$l
	echo "copy file to $t"
	recursive_copy_file $l $t 
done
rm -fr $delete_target
echo 'delete file ok at location: '$delete_target
