class Function():
    ''' basically a function that is responsible for getting its own inputs '''

    def __init__(self, inputs: dict = None):
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

    def function(self):
        ''' main '''
        return self.output
