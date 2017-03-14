import json

def json2txt(s, out):
    f = open(s)
    json_content = json.load(f)
    l = list(json_content.iteritems())
    f.close()
    with open(out,'w+') as L:
        tag = 'image'
        for t in l:
            idx = t[0].find(tag)
            L.write(t[0][idx + len(tag) + 1:] + ' ')
            for i in t[1]:
                L.write(str(i) + ' ')
            L.write('\n')


if __name__ == "__main__":
    # json2txt("./train_labels.json", 'train_list.txt')
    json2txt("./train_labels.json", 'train_list.txt')
