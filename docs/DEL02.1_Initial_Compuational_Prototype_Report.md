# DEL02.1 Initial Computational Prototype Report

## §1 Revised inquiry and response to feedback

* **Current inquiry question:** How does changing the weight assigned to existing creator popularity in video ranking affect the percentage of recommendation slots occupied by new creators on YouTube's Home page over repeated recommendation rounds in a simplified model?
* **Current boundary:** This inquiry focuses on long-form video recommendations on YouTube's Home page. It includes fictional new and established content creators, viewers with different interests, creator popularity, engagement histories, and a limited number of recommendation positions. The model represents repeated video ranking and recommendation rounds, examining how the percentage of recommendation slots occupied by new creators changes under different popularity-weighting conditions. It excludes real user data and YouTube's actual recommendation algorithm.
* **Revision from DEL01:** The platform context was narrowed from a general simulated social media recommendation feed to long-form video recommendations on YouTube's Home page. The primary visibility measure was also narrowed to the percentage of recommendation slots occupied by new creators. The original focus on comparing new and established creators, popularity weighting, viewer interests, engagement histories, and repeated recommendation rounds was retained.
* **Reason for the revision:** The formative feedback indicated that the original formulation needed to identify a specific deployed recommendation service and a clearly defined visibility measure. YouTube's Home page was selected to provide a more specific platform context, and the percentage of recommendation slots occupied by new creators was selected as the primary output to make the phenomenon measurable. The inquiry was also reframed to examine differences in visibility under different popularity-weighting conditions without assuming that popularity necessarily causes unequal visibility on actual platforms.

## §2.1 Model plan

* **Focal activity:** The model will represent how long-form videos appear in YouTube's Home page recommendations over repeated rounds, comparing recommendation visibility between new and established creators under different popularity-weighting conditions.
* **Agents or entities:** The broader model will include fictional new and established content creators, viewers with different interests, long-form videos associated with creators, and a limited number of recommendation positions. Creators will have popularity values and engagement histories that can influence their future recommendation visibility.
* **Rules or updates:** Videos will be ranked using a combination of existing creator popularity and viewer interest. Recommended videos can receive engagement, which may contribute to changes in creator popularity and influence rankings in subsequent rounds. This recommendation and ranking process will repeat over multiple rounds.
* **Parameter or comparison condition:** The model will vary the weight assigned to existing creator popularity in the video-ranking process. The baseline and alternative conditions will use different popularity weights while keeping other starting conditions and rules consistent.
* **Intended output:** The primary output will be the percentage of recommendation slots occupied by new creators across repeated rounds. This will allow recommendation visibility to be compared between the baseline and alternative popularity-weighting conditions.

## §2.1 Evidence and source materials

| Source or material | What it informs | Access and use conditions | Status |
| :--- | :--- | :--- | :--- |
| **DEL01 Formative Feedback** | Identifies the need for a specific deployed recommendation service, a measurable visibility outcome, and a distinction between the real platform and its simplified representation. | Received through the course's formative feedback. Used to revise the inquiry and modelling direction. | Observed course feedback |
| **CM11 Modelling Worksheet (revised)** | Identifies long-form YouTube Home page recommendations as the platform context and the percentage of recommendation slots occupied by new creators as the primary visibility measure. | Developed as part of the project planning process. Used to establish the revised inquiry and initial modelling choices. | Project planning material |
| **DEL02 Specification** | Informs the required report structure, targeted computational prototype, baseline and alternative comparison, output requirements, and Mesa implementation expectations. | Course-provided assignment specification. Used to guide the DEL02 report and implementation. | Observed course material |
| **Synthetic creators, popularity values, viewer interests, and engagement histories** | Provide the initial characteristics and conditions needed to represent new and established creators and repeated recommendation rounds. | Created for the simulation. No real user or creator data is used. | Synthetic and illustrative |
| **Simplified popularity-weighting and ranking rules** | Provide the mechanism for comparing how different popularity weights influence recommendation visibility. | Implemented as model assumptions rather than obtained from YouTube's proprietary ranking system. | Illustrative; requires implementation verification |

## §2.1 Representation choices and assumptions

* **What is represented:** The model represents fictional new and established content creators, their long-form videos, creator popularity, viewer interests, engagement histories, limited recommendation positions, and repeated video-ranking and recommendation rounds. It also represents the influence of existing popularity on video rankings and the possibility that engagement can affect future recommendations.
* **What is not represented:** The model does not represent real YouTube users, actual creator or video data, YouTube's proprietary recommendation algorithm, or every factor that influences Home page recommendations. It also does not reproduce the complete complexity of viewer behaviour or YouTube's recommendation infrastructure.
* **Assumptions:** Creator popularity and viewer interest can be represented using numerical values that contribute to video rankings. New and established creators can be distinguished using synthetic starting characteristics and engagement histories. The number of available recommendation positions is limited, and changing the popularity weight allows its influence on rankings to be examined while other conditions remain consistent. These are operational assumptions for the simulation and are not established facts about YouTube's actual recommendation system.

## §2.2 Targeted DEL02 slice

* **Included now:** The initial prototype will include fictional new and established creators, creator popularity values, long-form videos associated with creators, a limited number of recommendation positions, a popularity-weighted video-ranking rule, repeated recommendation rounds, and the recording of the percentage of recommendation slots occupied by new creators.
* **Deferred:** More detailed viewer-interest modelling, a fully developed engagement feedback mechanism, complex viewer-creator interactions, additional ranking factors, and more extensive visualizations and statistical comparisons will be deferred to later stages of the project.
* **Baseline and alternative condition:** The baseline and alternative runs will use different weights assigned to existing creator popularity in the ranking process. All other starting conditions and model rules will remain consistent so that popularity weighting is the single changed condition.
* **Output:** The prototype will produce the percentage of recommendation slots occupied by new creators across repeated recommendation rounds, allowing the baseline and alternative conditions to be compared.
* **Why this is an appropriate first implementation step:** This approach isolates the main mechanism being investigated: how the weight assigned to existing popularity influences recommendation visibility. Implementing a limited ranking process and measuring the percentage of recommendation slots occupied by new creators provides a manageable starting point for the broader model. It allows an initial comparison to be produced without attempting to reproduce the entire YouTube recommendation system. More complex engagement feedback and viewer interactions can be added in later stages.

## §3 Mesa model implementation summary

* **Source example:** Epstein Civil Violence
* **Current run:** The adapted model ranks fictional creators for a limited number of recommendation slots by combining an abstracted viewer interest score with existing creator popularity. It compares a baseline run with a low popularity weight (0.1) against an alternative run with a high popularity weight (0.9) to measure the percentage of slots occupied by new creators over 50 rounds.
* **Repository URL:** [GitHub repository URL](https://github.com/Justin1374/new-creator-visibility-youtube)
* **DEL02 Release URL:** [GitHub DEL02 Release URL]

## §4 Repository outputs: descriptions and comparison

* **Baseline raw file(s):** `baseline_raw_00_visibility_by_round.csv`
* **Baseline processed file(s):** `baseline_processed_00_visibility_by_round.png`
* **Alternative raw file(s):** `alternative_raw_00_visibility_by_round.csv`
* **Alternative processed file(s):** `alternative_processed_00_visibility_by_round.png`
* **Conditions:** Both runs feature 50 new creators (starting popularity 0.05-0.2) and 50 established creators (starting popularity 0.7-1.0) competing for 10 recommendation slots over 50 rounds. The ranking formula combines randomized viewer interest (0-1.0) with existing popularity. The baseline condition weights existing popularity at 0.1. The alternative condition weights existing popularity at 0.9.
* **What is visible:** In the `baseline_processed_00_visibility_by_round.png`, the percentage of new creators recommended fluctuates but remains significantly higher because random viewer interest heavily drives the ranking. In the `alternative_processed_00_visibility_by_round.png`, the percentage of new creators recommended remains at or near 0%, as the high popularity weight heavily favors established creators.
* **Comparison:** The comparison between the baseline and alternative processed PNG files shows a stark difference in new creator visibility. When popularity weight is low (baseline), new creators capture a substantial share of recommendation slots. When popularity weight is high (alternative), new creators are almost entirely excluded from the recommendations.
* **Connection to the inquiry:** These outputs begin to address the inquiry by demonstrating that a higher weight assigned to existing creator popularity in a simplified ranking algorithm directly suppresses the percentage of recommendation slots occupied by new creators, creating a substantial visibility gap over repeated rounds.

## §5 Interpretation, limitations, and next steps

* **What the model shows:** The model shows that under the stated synthetic starting conditions and rules, increasing the algorithm's popularity weight from 0.1 to 0.9 drastically reduces the percentage of recommendation slots occupied by new creators across repeated rounds, heavily favoring established creators.
* **What this helps investigate:** This helps investigate the mechanism of "rich-get-richer" feedback loops in recommendation systems, specifically how the mathematical weighting of existing popularity trades off against equal visibility opportunities for new participants.
* **What it does not establish:** These outputs cannot make claims about actual users, causation, or how real platforms operate. Specifically, they do not prove how YouTube's proprietary algorithm actually ranks videos.
* **Limitations and uncertainty:** The targeted DEL02 slice relies heavily on synthetic starting conditions and assumes viewer interest is entirely random, abstracting away individual viewer agents and complex viewing preferences. It also simplifies engagement by assuming all recommended videos receive engagement that universally boosts popularity, ignoring content quality or negative feedback.
* **Next steps:** Introduce explicit viewer agents with distinct preference states to replace the randomized viewer interest variable. Also, implement a more complex engagement feedback mechanism where viewer-creator preference alignment determines whether an exposure successfully converts into engagement and increased popularity.