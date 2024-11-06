import re

class buffer_paragraph:
    def __init__(self):
        self.separator = ""
        self.paragraph = ""
        self.l_before_readed = False
        self.l_after_readed = False


# Simple test for read rtf file and print the content
path = "D:/DemoFiles"
file = "Honda-SYS-EBD-ts.txt"
buffer_lines = []
buffer_tc = []
pattern = re.compile(r"^\[")
with open('{}/{}'.format(path, file), 'r', encoding="utf-8") as file:
    for line in file:
        buffer_lines.append(line)
        if re.search(pattern, line.strip()):
            buffer_object = buffer_paragraph()
            buffer_object.separator = pattern
            if len(buffer_lines) > 2:
                for i in range(-2, -len(buffer_lines), -1):
                    if re.search(r"^[0-9]+\.", buffer_lines[i]):
                        buffer_object.paragraph = buffer_lines[i] + buffer_object.paragraph
                    else:
                        break
            buffer_object.paragraph = buffer_object.paragraph + line
            buffer_object.l_before_readed = True
            buffer_tc.append(buffer_object)
        elif re.search(r"^\s*$", line):
            if len(buffer_tc) > 0:
                buffer_tc[-1].paragraph += line
                buffer_tc[-1].l_after_readed = True
        else:
            if len(buffer_tc) > 0:
                if buffer_tc[-1].l_after_readed == False:
                    buffer_tc[-1].paragraph += line
            

for i in buffer_tc:
    print("--------------------")
    print(i.paragraph)
    print("\n")