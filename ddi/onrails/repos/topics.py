import pandas as pd

class Topic:
    
    all_topics = dict()
    root_topics = dict()
    missing_parents = dict()

    def __init__(self, name, parent_name, label=""):
        self.name = name
        self.label = label
        self.children = list()
        self.concepts = dict()
        cls = self.__class__
        cls.all_topics[name] = self
        if parent_name == "nan":
            cls.root_topics[name] = self
        elif parent_name in cls.all_topics.keys():
            parent = cls.all_topics[parent_name]
            parent.add_child(self)
        else:
            cls.missing_parents[name] = (name, parent_name, label)

    def add_child(self, child):
        self.children.append(child)

    def to_markdown(self, depth=1):
        if depth == 1:
            md = "---\ntopic: %s\nlabel: %s\n---\n\n#" % (self.name, self.label)
        else:
            md = "#" * depth
        md += " %s [%s]\n\n" % (self.label, self.name)
        for concept in self.concepts.items():
            md += "- {%s}: %s\n" % concept
        md += "\n"
        for child in self.children:
            md += child.to_markdown(depth + 1)
        return md

    @classmethod
    def retry_missing_parents(cls):
        before_len = len(cls.missing_parents)
        missing_parents = cls.missing_parents
        cls.missing_parents = dict()
        for name, object_tupel in missing_parents.items():
            cls(*object_tupel)
        if len(cls.missing_parents) < before_len:
            cls.retry_missing_parents()

    @classmethod
    def import_topics(cls, filename="metadata/topics.csv"):
        topics = pd.read_csv(filename)
        for sn, topic in topics.iterrows():
            cls(str(topic["topic"]), str(topic["parent"]), str(topic["label"]))
        cls.retry_missing_parents()

    @classmethod
    def import_concepts(cls, filename="metadata/concepts.csv"):
        concepts = pd.read_csv(filename)
        for sn, concept in concepts.iterrows():
            try:
                topic = cls.all_topics[concept["topic_prefix"]]
                topic.concepts[concept["concept"]] = concept["label"]
            except:
                print("[ERROR] Could not import concept %s" % concept["concept"])

    @classmethod
    def export_markdown(cls):
        for key, topic in cls.root_topics.items():
            with open("ddionrails/topics/%s.md" % key, "w") as f:
                f.write(topic.to_markdown())

    @classmethod
    def import_all(cls):
        cls.import_topics()
        cls.import_concepts()
        print("[INFO] %s topics importet" %len(cls.all_topics))
        print("[INFO] %s root topics" %len(cls.root_topics))
        print("[INFO] %s missing parents" %len(cls.missing_parents))
        print("[INFO] Write md")
        cls.export_markdown()
