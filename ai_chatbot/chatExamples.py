## https://python.langchain.com/en/latest/modules/prompts/example_selectors/examples/custom_example_selector.html
## Implement custom example selector
from langchain import PromptTemplate
from langchain.prompts.example_selector.base import BaseExampleSelector
from typing import Dict, List
import numpy as np


class CustomExampleSelector(BaseExampleSelector):

    def __init__(self, examples: List[Dict[str, str]]):
        self.examples = examples

    def add_example(self, example: Dict[str, str]) -> None:
        """Add new example to store for a key."""
        self.examples.append(example)

    def select_examples(self, input_variables: Dict[str, str]) -> List[dict]:
        """Select which examples to use based on the inputs."""
        return np.random.choice(self.examples, size=1, replace=False)


##### EXAMPLES======================================
# create our examples
examples = [
    {
        "CSV_output": 'a 2 day itinerary to London of budget 600 in UK currency staying in 1 centralised hotel:'
                      '```'
                      '"date","name","addr","pop","hrs","mode","cost","remark","type"\\n'
                      '"2023-05-28","The Clermont Hotel, Charing Cross","Strand","95","NA","NA","400","87-floor glass skyscraper with jagged peak","POI"\\n'
                      '"2023-05-28","The Shard","32 London Bridge St","90","3","NA","0","87-floor glass skyscraper with jagged peak","POI"\\n'
                      '"2023-05-28","Borough Market","8 Southwark St","80","2","WK","50","Under-railway market with artisanal goods","POI"\\n'
                      '"2023-05-28","Tate Modern","Bankside","90","2","WK","0", "Modern-art gallery with panoramic river views","POI"\\n'
                      '"2023-05-28","St. Pauls Cathedral","St. Pauls Churchyard","85","3","WK","0","17th-century cathedral with recitals and churchyard","POI"\\n'
                      '"2023-05-29","Covent Garden","Covent Garden","85","PT","100","Shopping and entertainment hub in West End,","POI"\\n'
                      '"2023-05-29","Trafalgar Square","Trafalgar Sq","85","2","WK","0","Square with fountains, artworks and lion statues","POI"\\n'
                      '"2023-05-29","London Eye","Riverside Building, County Hall","90","3","WK","50","Huge observation wheel","POI"\\n'
                      '"2023-05-29","Big Ben","Palace of Westminster","90","2.5","WK","0","16-storey Gothic clocktower","POI"\\n'
                      '"2023-05-29","Westminster Abbey","20 Deans Yd","85","2.5","WK","0","Protestant abbey hosting coronations since 1066","POI"\\n'
                      '```'
    }
# }, {
#         "CSV_output": "What time is it?"
#     }
]

# create a example template
example_template = """{CSV_output}"""

# create a prompt example from above template
example_prompt = PromptTemplate(
    input_variables=["CSV_output"],
    template=example_template
)


######## Initialize & choose 1 example selector.
from langchain.prompts.example_selector import LengthBasedExampleSelector

# example_selector = LengthBasedExampleSelector(
#     examples=examples,
#     example_prompt=example_prompt,
#     max_length=50  # this sets the max length that examples should be
# )
example_selector = CustomExampleSelector(examples)