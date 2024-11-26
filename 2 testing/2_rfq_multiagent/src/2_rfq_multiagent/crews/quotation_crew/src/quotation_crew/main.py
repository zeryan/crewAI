#!/usr/bin/env python
import sys
from quotation_crew.crew import QuotationCrewCrew

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

#INSERT INPUTS HERE

inputs = {
        # We will use Tirana Oeste PV Plant Environmental Qualification Resolution
        'rca_url': 'https://seia.sea.gob.cl/archivos/2024/05/14/RCA_20240100117_Tirana_Oeste_Firmada_RGC_DPR.PDF'
    }

def run():
    """
    Run the crew.
    """
    inputs = inputs
    QuotationCrewCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = inputs
    try:
        QuotationCrewCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        QuotationCrewCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = inputs
    try:
        QuotationCrewCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
