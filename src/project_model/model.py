import mesa

TOPICS = ["Tech", "Gaming", "Education", "Lifestyle", "Music"]


def compute_percent_new(model):
    """Calculates the percentage of Home page recommendation slots occupied by new creators."""
    if model.num_slots == 0:
        return 0.0
    new_count = sum(1 for agent in model.recommended_agents if agent.is_new_creator)
    return (new_count / model.num_slots) * 100.0


def compute_topic_match_rate(model):
    """Calculates the percentage of recommended slots matching the active viewer's primary topic."""
    if model.num_slots == 0 or model.active_viewer is None:
        return 0.0
    match_count = sum(
        1 for agent in model.recommended_agents if agent.topic == model.active_viewer.preferred_topic
    )
    return (match_count / model.num_slots) * 100.0


def compute_engagement_rate(model):
    """Calculates the percentage of recommended slots that received viewer engagement in the current round."""
    if model.num_slots == 0:
        return 0.0
    return (model.round_engagements / model.num_slots) * 100.0


def compute_mean_new_popularity(model):
    """Calculates mean popularity across all new creators."""
    new_creators = [a for a in model.creator_agents if a.is_new_creator]
    return sum(a.popularity for a in new_creators) / len(new_creators) if new_creators else 0.0


def compute_mean_est_popularity(model):
    """Calculates mean popularity across all established creators."""
    est_creators = [a for a in model.creator_agents if not a.is_new_creator]
    return sum(a.popularity for a in est_creators) / len(est_creators) if est_creators else 0.0


class CreatorAgent(mesa.Agent):
    """Represents a content creator publishing long-form videos within a primary topic."""

    def __init__(self, model, is_new_creator, topic):
        super().__init__(model)
        self.is_new_creator = is_new_creator
        self.topic = topic

        if self.is_new_creator:
            self.popularity = self.model.random.uniform(0.05, 0.20)
        else:
            self.popularity = self.model.random.uniform(0.70, 1.00)

        self.recommended = False
        self.engaged_this_round = False
        self.total_impressions = 0
        self.total_engagements = 0

    def step(self):
        # Update popularity based on realized viewer engagement and baseline decay
        if self.engaged_this_round:
            self.popularity = min(1.0, self.popularity + 0.03)
        self.popularity = max(0.01, self.popularity - 0.002)


class ViewerAgent(mesa.Agent):
    """Represents a YouTube Home page viewer with a primary long-form topic preference."""

    def __init__(self, model, preferred_topic):
        super().__init__(model)
        self.preferred_topic = preferred_topic

    def step(self):
        pass


class RecommendationModel(mesa.Model):
    """
    DEL03 Agent-Based Model of YouTube Home Page Long-Form Video Recommendations.

    Compares an interest-weighted ranking rule (weight=0.10) against a popularity-weighted
    ranking rule (weight=0.90) with explicit ViewerAgents, topic alignment, conditional
    engagement feedback, and baseline popularity decay.
    """

    def __init__(self, weight=0.10, num_creators=100, num_viewers=200, num_slots=10, seed=42):
        super().__init__(seed=seed)
        self.weight = weight
        self.num_creators = num_creators
        self.num_viewers = num_viewers
        self.num_slots = num_slots

        self.creator_agents = []
        self.viewer_agents = []
        self.recommended_agents = []
        self.active_viewer = None
        self.round_engagements = 0

        # Initialize equal split of 50 new and 50 established creators across 5 topics
        for i in range(self.num_creators):
            is_new = (i % 2 == 0)
            topic = TOPICS[i % len(TOPICS)]
            self.creator_agents.append(CreatorAgent(self, is_new_creator=is_new, topic=topic))

        # Initialize 200 viewers evenly across the 5 topics (40 per topic)
        for v in range(self.num_viewers):
            topic = TOPICS[v % len(TOPICS)]
            self.viewer_agents.append(ViewerAgent(self, preferred_topic=topic))

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Percent_New_Creators_Recommended": compute_percent_new,
                "Topic_Match_Rate": compute_topic_match_rate,
                "Engagement_Rate": compute_engagement_rate,
                "Mean_New_Creator_Popularity": compute_mean_new_popularity,
                "Mean_Est_Creator_Popularity": compute_mean_est_popularity,
            }
        )

    def step(self):
        # Sample an active Home page session viewer for this round
        self.active_viewer = self.random.choice(self.viewer_agents)
        self.round_engagements = 0
        scores = []

        for creator in self.creator_agents:
            creator.recommended = False
            creator.engaged_this_round = False

            # Topic-aligned viewer interest score
            if creator.topic == self.active_viewer.preferred_topic:
                viewer_interest = self.random.uniform(0.65, 1.00)
            else:
                viewer_interest = self.random.uniform(0.00, 0.35)

            # Composite ranking score combining existing popularity and viewer interest
            score = (self.weight * creator.popularity) + ((1.0 - self.weight) * viewer_interest)
            scores.append((score, creator))

        # Rank descending and select top K=10 Home page recommendation slots
        scores.sort(key=lambda x: x[0], reverse=True)
        self.recommended_agents = [creator for _, creator in scores[:self.num_slots]]

        for creator in self.recommended_agents:
            creator.recommended = True
            creator.total_impressions += 1

            # Topic-conditional viewer engagement probability
            p_engage = 0.65 if creator.topic == self.active_viewer.preferred_topic else 0.10
            if self.random.random() < p_engage:
                creator.engaged_this_round = True
                creator.total_engagements += 1
                self.round_engagements += 1

        # Record metrics for this round before updating creator popularity
        self.datacollector.collect(self)

        # Advance creator popularity states (shuffled order)
        self.random.shuffle(self.creator_agents)
        for creator in self.creator_agents:
            creator.step()