def dir_to_dataset(glob_files):
    # print("Gonna process:\n\t %s" % glob_files)
    dataset = []
    clazz = []
    for file_count, file_name in enumerate(sorted(glob(glob_files), key=len)):
        image = Image.open(file_name)
        # print file_name
        img = Image.open(file_name).convert('LA')  # tograyscale
        pixels = [f[0] for f in list(img.getdata())]
        dataset.append(pixels)
        classLabel = file_name.split("_")[1];
        # print file_name, "<--->", classLabel
        clazz.append(classLabel)
        if file_count % 1000 == 0:
            print("\t %s files processed" % file_count)
    # outfile = glob_files+"out"
    # np.save(outfile, dataset)
    return np.array(dataset), np.array(clazz)


def rename(path=".",src="./src"):
    directorys=os.listdir(src);
    i=0;
    for directory in directorys:
        print "####",directory," is doing ####";
        path=src+"/"+directory;
        files=subfilesName(path)
        i=0;
        for f in files:
            print os.path.join(f),"...."
            if os.path.isfile(os.path.join(path,f))==True:
                i=i+1;
                name='{0}_{1:0{2}d}'.format(directory,i,4);
                print os.path.join(path,f),os.path.join(path,name);
                os.rename(os.path.join(path,f),os.path.join(path,name));
                print f,"-->",name

# get sub dirs
def subdirs(path):
    dl = [];
    for i in os.walk(path, False):
        for d in i[1]:
            dl.append(os.path.join(path, d))
    return dl

#get sub file
def subfiles(path):
    fl = [];
    for i in os.walk(path, False):
        for f in i[2]:
            fl.append(os.path.join(path, f))
    return fl

def subfilesName(path):
    fl = [];
    for i in os.walk(path, False):
        for f in i[2]:
            fl.append(f)
    return fl


def _random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

def _random_string(randomlength=8):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])
