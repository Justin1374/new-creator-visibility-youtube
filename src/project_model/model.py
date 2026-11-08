import mesa

def compute_percent_new(model):
    """Calculates the percentage of new creators in the recommended slots."""
    if model.num_slots == 0:
        return 0
    new_count = sum(1 for agent in model.recommended_agents if agent.is_new_creator)
    return (new_count / model.num_slots) * 100

class CreatorAgent(mesa.Agent):
    def __init__(self, model, is_new_creator):
        # In Mesa 3.0+, super().__init__(model) automatically adds this agent to model.agents
        super().__init__(model)
        self.is_new_creator = is_new_creator
        
        # Synthetic starting conditions
        if self.is_new_creator:
            self.popularity = self.model.random.uniform(0.05, 0.20)
        else:
            self.popularity = self.model.random.uniform(0.70, 1.0)
            
        self.recommended = False

    def step(self):
        # Simplistic engagement feedback loop: 
        # If exposed in the recommendation feed, popularity gets a synthetic boost.
        if self.recommended:
            self.popularity += 0.02
            self.popularity = min(self.popularity, 1.0)

class RecommendationModel(mesa.Model):
    def __init__(self, weight=0.1, num_creators=100, num_slots=10, seed=None):
        super().__init__(seed=seed)
        self.weight = weight
        self.num_creators = num_creators
        self.num_slots = num_slots
        self.recommended_agents = []
        
        # Initialize an equal split of new and established creators
        for i in range(self.num_creators):
            is_new = (i % 2 == 0)
            CreatorAgent(self, is_new)
            
        self.datacollector = mesa.DataCollector(
            model_reporters={"Percent_New_Creators_Recommended": compute_percent_new}
        )

    def step(self):
        scores = []
        
        # Calculate ranking score for each agent
        for agent in self.agents:
            # Abstracted randomized viewer interest for the DEL02 slice
            viewer_interest = self.random.uniform(0.0, 1.0)
            
            # The core algorithmic ranking formula
            score = (self.weight * agent.popularity) + ((1 - self.weight) * viewer_interest)
            scores.append((score, agent))
            
            # Reset recommended flag for this round
            agent.recommended = False
            
        # Rank by score in descending order
        scores.sort(key=lambda x: x[0], reverse=True)
        
        # Isolate the top slots for exposure
        self.recommended_agents = [agent for score, agent in scores[:self.num_slots]]
        
        for agent in self.recommended_agents:
            agent.recommended = True
            
        # Collect data before agents step (so it records the ranking results for this round)
        self.datacollector.collect(self)
        
        # Mesa 3.0+ alternative to RandomActivation schedule
        self.agents.shuffle_do("step")