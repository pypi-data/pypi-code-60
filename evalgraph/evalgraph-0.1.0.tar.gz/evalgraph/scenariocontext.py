class ScenarioContext:
    Stack = []
    
    @staticmethod
    def CurrentScenario():
        return ScenarioContext.Stack[-1]

    @staticmethod
    def Push(scenario):
        ScenarioContext.Stack.append(scenario)
    
    @staticmethod
    def Pop():
        ScenarioContext.Stack.pop()
