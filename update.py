import boto3
import os
import json 

def run(): 
    client = boto3.client('cloudformation')

    stack_name = os.environ['INPUT_STACK-NAME']
    parameters_raw = os.environ['INPUT_PARAMETERS']
    capabilities = os.environ['INPUT_CAPABILITIES']

    new_parameters = json.loads(parameters_raw)

    response = client.describe_stacks(
        StackName=stack_name,
    )

    current_parameters = response['Stacks'][0]['Parameters']
    original_dict = {item['ParameterKey']: item['ParameterValue'] for item in new_parameters}

    for item in current_parameters:
        parameter_key = item['ParameterKey']

        if parameter_key in original_dict:
            parameter_value = original_dict[parameter_key]
        else:
            original_dict[parameter_key] = None

    updated_parameters = []
    for key, value in original_dict.items():
        if value is None:
            updated_parameters.append({'ParameterKey': key, 'UsePreviousValue': True})
        else:
            updated_parameters.append({'ParameterKey': key, 'ParameterValue': value})

    response = client.update_stack(
        StackName=stack_name,
        UsePreviousTemplate=True,
        Parameters=updated_parameters,
        Capabilities=[
            capabilities,
        ]
    )

if __name__ == '__main__':
    run()