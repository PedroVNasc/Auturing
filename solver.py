from typing import TypedDict


class Connection(TypedDict):
    target: int
    data: str
    
class Result(TypedDict):
    path: list[int]
    result: bool
    
class Solver:
    def __init__(self, graph: dict[int, list[Connection]], initial_state: int, final_states: list[int]) -> None:
        self.graph = graph
        self.initial_state = initial_state
        self.final_states = final_states
        
    def solve(self, input: str) -> Result:
        current_state = self.initial_state
        connections = self.graph[current_state]
        path = [current_state]
        
        for i, c in enumerate(input):
            for conn in connections:
                if conn['data'] == c:
                    path.append(conn['target'])
                    current_state = conn['target']
                    connections = self.graph[current_state]
                    break
                
            if len(path) <= i + 1:
                return {'path': path, 'result': False}
        
        if current_state in self.final_states:
            return {'path': path, 'result': True}
        
        return {'path': path, 'result': False}
    
    
    
# def solver(graph: list[connection], input: str):
#     pass