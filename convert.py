#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys

def convert_to_set(input_text):
    output = ""
    cmd = []
    for line in input_text.splitlines():
        if "; ##" in line:
            line = line[:line.index(" ##")]
        tail = line[:-1].strip()
        if line[-1] == '{':
            cmd.append(tail)
        elif line[-1] == '}':
            if "inactive: " in cmd[-1]:
                output += ("deactivate " + " ".join(cmd) + "\n").replace("inactive: ","")
            cmd.pop(-1)
        elif line[-1] == ';':
            if "];" in line:
                slist = line[line.index("[") + 2:line.index("]")-1]
                for p in slist.split(" "):
                    output += ("set " + " ".join(cmd) + " " + line[:line.index("[")].replace("  ","") + p + "\n").replace("inactive: ","")
            elif "file " == tail[:5]:
                output += ("set " + " ".join(cmd) + " file " + tail[5:].split(" ")[0] + "\n").replace("inactive: ","")
                output += ("set " + " ".join(cmd) + " file " + " ".join(tail[5:].split(" ")[1:]) + "\n").replace("inactive: ","")
            else:
                output += ("set " + " ".join(cmd) + " " + tail + "\n").replace("inactive: ","")
            if "inactive: " in line:
                if "import " in tail:
                    output += ("deactivate " + " ".join(cmd) + " " + tail[:tail.index("import ")+6] + "\n").replace("inactive: ","")
                elif "export " in tail:
                    output += ("deactivate " + " ".join(cmd) + " " + tail[:tail.index("export ")+6] + "\n").replace("inactive: ","")
                else:    
                    output += ("deactivate " + " ".join(cmd) + " " + tail + "\n").replace("inactive: ","")
    return output

if __name__ == "__main__":
    try:
        source_file = sys.argv[1]
        destination_file = sys.argv[2]
    except:
        print("usage: python3 convert.py source_file destination_file")
        exit()
    try:
        text = open(source_file,'r').read()
    except BaseException as e:
        print("can not open file '{0}'\n{1}".format(source_file,e))
        exit()
    s = convert_to_set(text)
    try:
        file = open(destination_file,"w")
        file.write(s)
        file.close()
    except BaseException as e:
        print("can not write file '{0}'\n{1}".format(source_file,e))
        exit()
