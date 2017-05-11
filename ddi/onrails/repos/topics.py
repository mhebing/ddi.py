import pandas as pd

class Topic:
    
    all_topics = dict()
    root_topics = dict()
    missing_parents = dict()

    def __init__(self, name, parent_name):
        self.name = name
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
            cls.missing_parents[name] = parent_name

    def add_child(self, child):
        self.children.append(child)

    @classmethod
    def retry_missing_parents(cls):
        before_len = len(cls.missing_parents)
        missing_parents = cls.missing_parents
        cls.missing_parents = dict()
        for name, parent_name in missing_parents.items():
            cls(name, parent_name)
        if len(cls.missing_parents) < before_len:
            cls.retry_missing_parents()

    @classmethod
    def import_topics(cls, filename="metadata/topics.csv"):
        topics = pd.read_csv(filename)
        for sn, topic in topics.iterrows():
            cls(str(topic["topic"]), str(topic["parent"]))
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
    def import_all(cls):
        cls.import_topics()
        cls.import_concepts()
        print("[INFO] %s topics importet" %len(cls.all_topics))
        print("[INFO] %s root topics" %len(cls.root_topics))
        print("[INFO] %s missing parents" %len(cls.missing_parents))
