class Function():
    ''' basically a function that is responsible for getting its own inputs '''

    def __init__(self, inputs: dict = None, name: str = None):
        self.name = name or self.__repr__().split()[0].split('.')[-1]
        self.set_inputs(inputs=inputs or {})
        self.clear(memory=True)

    def set_inputs(self, inputs: dict):
        self.inputs = inputs
        self.kwargs = {name: None for name in self.inputs.keys()}

    def clear(self, memory: bool = False):
        self.cached = False
        self.getout = False
        if memory:
            self.output = None
            self.latest = None

    def run(self, gas: int = 1, verbose: bool = False):
        '''
        gas can specify if we should pull from cache or not in this way:
        -1 - infinite gas (DAGs only!)
        0 - if cache: cache, else: get inputs, do function, save as cache
        1 - request cached inputs and run functionality (default)
        2 - request non-cached inputs and run functionality
        3 - request that inputs request non-cached inputs and recalculate...
        4+ - so on and so forth...
        '''
        if gas == 0 and self.cached:
            pass
        else:
            if gas == 0 and not self.cached:
                self.aquire(gas=0)
            elif gas >= 1:
                self.aquire(gas=gas - 1)
            elif gas == -1:
                self.aquire(gas)
            else:
                self.aquire(0)
            self.output = self.function()
            self.cached = True
        return self.get()

    def aquire(self, gas: int = 0):
        for name, function_object in self.inputs.items():
            self.kwargs[name] = function_object.run(gas)

    def get(self):
        return self.output

    def visualize(self, size=(8,5)):
        '''
        minimal, no uniformly layout, unable to save to file, no namespacing
        and no indications such as cached, cost in time, or popularity, etc.
        '''

        def graph_heritage(current, seen):
            seen.append(current)
            parents = [v for v in current.inputs.values()]
            for parent in parents:
                if not graph.has_node(parent.name):
                    graph.add_node(parent.name)
                    if parent in [v for v in self.inputs.values()]:
                        colors.append('#d7a9e3')
                    else:
                        colors.append('#8bbee8')
                ancestors.append((parent.name, current.name))
                if parent not in seen:
                    graph_heritage(current=parent, seen=seen)

        import networkx as nx
        import matplotlib.pyplot as plt
        graph = nx.DiGraph()
        colors = []
        ancestors = []
        if not graph.has_node(self.name):
            graph.add_node(self.name)
            colors.append('#a8d5ba')
        graph_heritage(current=self, seen=[])
        graph.add_edges_from(ancestors, weight=1)
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_color=colors, node_size=1500)
        plt.rcParams["figure.figsize"] = size
        plt.show()

    def function(self):
        ''' main '''
        return self.output
