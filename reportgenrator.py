import re
import json
from collections import OrderedDict

class Generator:

    def __escape_str(self, s):
        return s.replace("\a", "\\a").replace("\b", "\\b").replace("\f", "\\f").replace("\r", "\\r").replace("\t", "\\t").replace("\v", "\\v")

    def generate_report(self, json_content):
        if type(json_content) is str:
            return json_content.replace("%", "\%")

        if "name" not in json_content:
            json_content["name"] = ""
        if "content" not in json_content:
            json_content["content"] = ""

        file_content = None
        with open("templates/" + json_content["type"] + ".tex") as f:
            file_content = f.read()
        final_content = file_content
        final_content = re.sub("##.*NAME##", json_content["name"],final_content)

        content = ""
        if type(json_content["content"]) is list:
            for e in json_content["content"]:
                content += self.generate_report(e)
        elif type(json_content["content"]) is dict:
            content += self.generate_report(json_content["content"])
        elif type(json_content["content"]) is str:
            content += self.generate_report(json_content["content"])

        final_content = re.sub("##.*CONTENT##", content,final_content)
        return self.__escape_str(final_content)

    def __sub_dict(self, d, text):
        for k in d:
            if type(d[k]) is str:
                text = re.sub("##"+k+"##", d[k], text)
        return text

    def __do_fill(self, d, content):
        if type(d) is str:
            d = self.__sub_dict(content, d)
            return d
        if "content" not in d:
            return d
        if d["type"] == "unordered_list" or d["type"] == "ordered_list":
            l = []
            for e in content[d["filer"]]:
                template = dict(d["content"][0])
                template["content"] = self.__do_fill(template["content"],e)
                l.append(template)
            d["content"] = l
            return d
        if "filer" in d:
            content = content[d["filer"]]
        if type(d["content"]) is list:
            l = []
            for e in d["content"]:
                l.append(self.__do_fill(e, content))
            d["content"] = l
        elif type(d["content"]) is str:
            d["content"] = self.__sub_dict(content, d["content"])
        else:
                d["content"] = self.__do_fill(d["content"], content)
        return d


    def generate_json(self, json_content):
        structure = None
        with open("content/structure.json", "r") as f:
            structure = f.read()
            structure = json.loads(structure)

        result_json = {}
        result_json["type"] = "report"
        result_json["content"] = []
        for e in structure:
            with open("content/" + e + ".json", "r") as f:
                file_content = f.read()
            json_file_content = json.loads(file_content)
            res = self.__do_fill(json_file_content, json_content)
            result_json["content"].append(res)
        return result_json


d = {"general": {"date_start": "11/11/11",
                 "date_end": "12/12/12"},

     "clients": [{"name": "john doe",
                  "email": "john@doe.com",
                  "tel": "+33 66 55 44 33",
                  "role": "CEO"}],

     "auditors": [{"name": "haxor auditor",
                   "email": "haxor@auditor.com",
                   "tel": "31337",
                   "role": "pro-hacker"},

                  {"name": "script kiddie",
                   "email": "skiddie@mail.com",
                   "tel": "123456",
                   "role": "skiddie"}]}

p = (Generator().generate_json(d))
#print(p)
print(Generator().generate_report(p))
