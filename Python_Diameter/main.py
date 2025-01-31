import torch
import transformers
import llama_cpp
import requests
import fastener_toolkit as ft
import math
import prompts
import sys_prompt
import sp
from transformers import AutoTokenizer, AutoModelForCausalLM

device = "cuda" if torch.cuda.is_available() else "cpu"

llm = llama_cpp.Llama.from_pretrained(
    repo_id="bartowski/WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B-GGUF",
    filename="WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B-IQ4_XS.gguf",
    n_ctx=16000,
    n_gpu_layers = -1,
    device = device
)

def llm_engine(messages, stop_sequences = ["Task"]) -> str:
    response = llm.create_chat_completion(
        messages = messages,
        stop = stop_sequences,
        max_tokens = 10000,
    )

    if "choices" in response and len(response["choices"]) > 0:
        if "message" in response["choices"][0] and "content" in response["choices"][0]["message"]:
            answer = response["choices"][0]["message"]["content"]
        else:
            # Handle the case where "message" or "content" is missing
            answer = "Error: Incomplete response structure."
    else:
        # Handle the case where the "choices" list is empty or missing
        answer = "Error: No valid response received."
    return answer


class FastenatingCalculator(transformers.Tool):
    name = "FOS_Calculation"
    description = "Calculates the factor of safety for fasteners using Yield Strength."

    inputs = {
            "desired_safety_factor": {
                "type": "number",
                "description": "Desired factor of safety",
            },
            "joint_constant": {
                "type": "number",
                "description": "Joint Constant in N/mm",
            },
            "d_major": {
                "type": "number",
                "description": "Major diameter of the bolt in mm",
            },
            "d_minor": {
                "type": "number",
                "description": "Minor diameter of the bolt in mm",
            },
            "load": {
                "type": "number",
                "description": "Load applied to the bolt in Newtons",
            },
            "yield_strength": {
                "type": "number",
                "description": "Yield strength of the bolt material in MPa",
            },
            "preload": {
                "type": "number",
                "description": "Preload applied to the bolt in Newtons",
            },
            "pitch": {
                "type": "number",
                "description": "Pitch of the bolt in mm",
            },
            # "E_b": {
            #     "type": "number",
            #     "description": "Young's modulus of the bolt in MPa or psi",
            # },
            # "E_m": {
            #     "type": "number",
            #     "description": "Young's modulus of the material in MPa or psi",
            # },
            # "l_unthreaded": {
            #     "type": "number",
            #     "description": "Length of unthreaded portion within the grip zone in mm",
            # },
            # "l_threaded": {
            #     "type": "number",
            #     "description": "Length of threaded portion within the grip zone in mm",
            # },
            # "s_ut": {
            #     "type": "number",
            #     "description": "Ultimate tensile strength of the bolt in MPa",
            # },
            # "s_end": {
            #     "type": "number",
            #     "description": "Endurance limit of the bolt in MPa or psi",
            # }
        }

    output_type = "number"

    def __init__(self):
            self.ft = ft
            # self.vis = vis

    # def cal_tensile_area(self,d_major,d_minor):
    #     area = (math.pi / 4) * ((d_major + d_minor)/2)**2
    #     return area

    def forward(
        self,
        desired_safety_factor: float,
        joint_constant: float,
        d_major: float,
        d_minor: float,
        load: float,
        yield_strength: float,
        preload: float,
        pitch: float) -> str:

        print(f"Inputs: desired_safety_factor={desired_safety_factor}, joint_constant={joint_constant}, d_major={d_major}, d_minor={d_minor}, load={load}, yield_strength={yield_strength}, preload={preload}, pitch={pitch}")

        try:
            tensile_area = self.ft.get_tensile_stress_area(d_major, d_minor, pitch)
            print(f"Calculated Tensile Area: {tensile_area}")

            sf = self.ft.bolt_yield_safety_factor(
                c=joint_constant, load=load, preload=preload, a_ts=tensile_area, b_ys=yield_strength)
            print(f"Calculated Safety Factor: {sf}")

            # output = f"Code: Calculate Safety Factor\nResult: {sf:.2f}"
            # print(f"Output: {output}")
            # higher_or_lower = "higher" if sf > desired_safety_factor else "lower"
            return f"The factor of safety is {sf:.2f}."
            # return sf

        except requests.RequestException as e:
            error_message = f"Error occurred while fetching data: {str(e)}"
            print(f"Error: {error_message}")
            return f"Action: Error\nResult: {error_message}"
        except KeyError:
            error_message = "Unable to calculate the safety factor. Please check the input values."
            print(f"Error: {error_message}")
            return f"Action: Error\nResult: {error_message}"
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            print(f"Error: {error_message}")
            return f"Action: Error\nResult: {error_message}"


def main():

    if torch.cuda.is_available():
        print("CUDA is available. Running on GPU.")
    else:
        print("CUDA is not available. Running on CPU.")

    # Another way to check if CUDA is being used
    print(f"Using device: {device}")
    
    agent = transformers.ReactCodeAgent(
        tools=[FastenatingCalculator()],
        llm_engine = llm_engine,
        add_base_tools=False,
        verbose=2,
        max_iterations = 20,
        system_prompt = sp.system_pr
    )
    # agent = transformers.ReactJsonAgent(
    #     tools=[FastenatingCalculator()],
    #     llm_engine = llm_engine,
    #     add_base_tools=False,
    #     verbose=2,
    #     max_iterations = 2,
    #     system_prompt = sp.system_pr
    # )

    response = agent.run(prompts.test_prompt)

    # # Process the response
    # if "choices" in response and len(response["choices"]) > 0:
    #     if "message" in response["choices"][0] and "content" in response["choices"][0]["message"]:
    #         answer = response["choices"][0]["message"]["content"]
    #     else:
    #         # Handle the case where "message" or "content" is missing
    #         answer = "Error: Incomplete response structure."
    # else:
    #     # Handle the case where the "choices" list is empty or missing
    #     answer = "Error: No valid response received."

    print(response)

if __name__ == "__main__":
    main()