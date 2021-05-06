import random

class Agent:
    def __init__(self, environment, agents, y, x):
        # Pointers to the gloabl environment and agents lists, shared by all
        # agents.
        self.environment = environment
        self.agents = agents
        
        # The agents store, unique to this agent.
        self.store = 0

        # Set the initial position of the agent. We have to test against None
        # as the scraped data from the web may produce this value.
        if x is None:
            self._x = random.randint(0,100)
        else:
            self._x = x
            
        if y is None:
            self._y = random.randint(0,100)
        else:
            self._y = y
    
    # Nice representation for the agent class.
    def __repr__(self):
        return "Agent({y}, {x})".format(y=self.y, x=self.x)

    # Defines the variable x as a propety.
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    # Define the variable y as a property.
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    def move(self):
        """Moves the agent randomly."""
        if random.random() < 0.5:
            self.y = (self.y + 1) % 100
        else:
            self.y = (self.y - 1) % 100

        if random.random() < 0.5:
            self.x = (self.x + 1) % 100
        else:
            self.x = (self.x - 1) % 100

    def eat(self):
        """Let the agent eat the environment."""
        if self.environment[self.y][self.x] > 10:
           self.environment[self.y][self.x] -= 10
        else:
           self.store += 10

    def distance_between(self, agent):
        """Returns the distance between two agents."""
        return (((self.x - agent.x)**2) + ((self.y - agent.y)**2))**0.5 
    
    def share_with_neighbours(self, neighbourhood):
        """Divides the stores between two agents."""
        for agent in self.agents:
            distance = self.distance_between(agent)
            if distance <= neighbourhood:
                total = agent.store + self.store
                
                # If either of the agents has a greater store then we exchange
                # which agent has the larger store. Otherwise the stores are
                # divided evenly between the two agents.
                if self.store < agent.store:
                    agent.store = total*0.25
                    self.store = total*0.75
                elif agent.store < self.store:
                    self.store = total*0.25
                    agent.store = total*0.75
                else:
                    self.store = total*0.5
                    agent.store = total*0.5






