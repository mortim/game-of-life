import re

class RLE:
    def __init__(self,filename,coords):
        self.filename = filename
        self.x,self.y = coords
        # ---
        self.patterns = [
            r"(x = [0-9]+), (y = [0-9]+)(, rule = [a-zA-Z/]+)*",
            r"([0-9]*)(b+|o+)"
        ]
        self.output = {"name": "", "author": "", "description": "","cells":[]}

    def parse(self):
        try:
            with open(self.filename, "r") as f:
                for line in f.read().split("\n"):
                    m = re.findall(self.patterns[0],line)

                    if m:
                        (a,b,_) = m[0]
                        x,y = int(a.split()[-1]), int(b.split()[-1])
                        self.x = (self.x - x)//2
                        self.y = (self.y - y)//2

                    elif line[0] != "#":
                        tmp = self.x
                        for cells in line.split("$"):
                            for (n,l) in re.findall(self.patterns[1],cells):
                                if not n:
                                    if l == "b":
                                        self.x += 1
                                    else:
                                        self.x += 1
                                        self.output["cells"].append((self.x,self.y))
                                else:
                                    if l == "b":
                                        self.x += int(n)
                                    else:
                                        for k in range(1,int(n)+1):
                                            self.output["cells"].append((self.x+k,self.y))
                                        self.x += int(n)
                            self.x = tmp
                            self.y += 1
                    else:
                        content = line[2:].strip()
                        if line[1] == "N":
                            self.output["name"] = content
                        elif line[1] == "O":
                            self.output["author"] = content
                        elif line[1] == "C":
                            self.output["description"] += content + "\n"
                return self.output
        except FileNotFoundError:
            print(f"Le fichier '{self.filename}' est introuvable.")
            exit()