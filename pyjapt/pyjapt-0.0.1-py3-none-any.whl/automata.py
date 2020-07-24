from typing import Any, Dict, Set, List, Tuple, Union


class State:
    def __init__(self, state: Any, final: bool = False):
        self.state: Any = state
        self.final: bool = final
        self.transitions: Dict[str, List['State']] = {}
        self.epsilon_transitions: Set['State'] = set()
        self.tag = None

    def has_transition(self, symbol):
        return symbol in self.transitions

    def add_transition(self, symbol: str, state: 'State'):
        try:
            self.transitions[symbol].append(state)
        except KeyError:
            self.transitions[symbol] = [state]
        return self

    def add_epsilon_transition(self, state: 'State'):
        self.epsilon_transitions.add(state)
        return self

    def recognize(self, string: str):
        states = self.epsilon_closure
        for symbol in string:
            states = self.move_by_state(symbol, *states)
            states = self.epsilon_closure_by_state(*states)

        return any(s.final for s in states)

    def to_deterministic(self) -> 'State':
        closure = self.epsilon_closure
        start = State(tuple(closure), any(s.final for s in closure))

        closures = [closure]
        states = [start]
        pending = [start]

        while pending:
            state = pending.pop()
            symbols = {symbol for s in state.state for symbol in s.transitions}

            for symbol in symbols:
                move = self.move_by_state(symbol, *state.state)
                closure = self.epsilon_closure_by_state(*move)

                if closure not in closures:
                    new_state = State(tuple(closure), any(s.final for s in closure))
                    closures.append(closure)
                    states.append(new_state)
                    pending.append(new_state)
                else:
                    index = closures.index(closure)
                    new_state = states[index]

                state.add_transition(symbol, new_state)

        return start

    @staticmethod
    def from_nfa(nfa, get_states: bool = False) -> Union['State', Tuple['State', List['State']]]:
        states = []
        for n in range(nfa.states):
            state = State(n, n in nfa.finals)
            states.append(state)

        for (origin, symbol), destinations in nfa.map.items():
            origin = states[origin]
            origin[symbol] = [states[d] for d in destinations]

        if get_states:
            return states[nfa.start], states
        return states[nfa.start]

    @staticmethod
    def move_by_state(symbol, *states):
        return {s for state in states if state.has_transition(symbol) for s in state[symbol]}

    @staticmethod
    def epsilon_closure_by_state(*states):
        closure = set(states)

        n = 0
        while n != len(closure):
            n = len(closure)
            tmp = [s for s in closure]
            for s in tmp:
                for epsilon_state in s.epsilon_transitions:
                    closure.add(epsilon_state)
        return closure

    @property
    def epsilon_closure(self):
        return self.epsilon_closure_by_state(self)

    def get(self, symbol):
        target = self.transitions[symbol]
        assert len(target) == 1
        return target[0]

    def __getitem__(self, symbol):
        if symbol == '':
            return self.epsilon_transitions
        try:
            return self.transitions[symbol]
        except KeyError:
            return None

    def __setitem__(self, symbol, value):
        if symbol == '':
            self.epsilon_transitions = value
        else:
            self.transitions[symbol] = value

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.state)

    def __hash__(self):
        return hash(self.state)

    def __iter__(self):
        yield from self.__visit()

    def __visit(self, visited=None):
        if visited is None:
            visited = set()
        elif self in visited:
            return

        visited.add(self)
        yield self

        for destinations in self.transitions.values():
            for node in destinations:
                yield from node.__visit(visited)
        for node in self.epsilon_transitions:
            yield from node.__visit(visited)
