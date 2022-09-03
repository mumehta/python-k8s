from kubernetes import client, config
from kubernetes.client import ApiClient
from kubernetes.client.rest import ApiException
import json
import yaml

config.load_kube_config()
v1 = client.CoreV1Api()

def __get_kubernetes_corev1client(bearer_token,api_server_endpoint):
    try:
        configuration = client.Configuration()
        configuration.host = api_server_endpoint
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + bearer_token}
        client.Configuration.set_default(configuration)
        client_api = client.CoreV1Api()
        return client_api
    except Exception as e:
        print("Error getting kubernetes client \n{}".format(e))
        return None

def __format_data_for_secret(client_output):
        temp_dict={}
        temp_list=[]
        json_data=ApiClient().sanitize_for_serialization(client_output)
        if len(json_data["items"]) != 0:
            for secret in json_data["items"]:
                temp_dict={
                    "secret": secret["metadata"]["name"],
                    "namespace": secret["metadata"]["namespace"]
                }
                temp_list.append(temp_dict)
        return temp_list

def __format_data_for_create_secret(client_output):
        temp_dict={}
        temp_list=[]
        json_data=ApiClient().sanitize_for_serialization(client_output)
        
        if type(json_data) is str:
            print("FORMAT_DATA :{}".format(type(json_data)))
            json_data = json.loads(json_data)
        temp_list.append(json_data)
        return temp_list
    

def create_secret(yaml_body=None,namespace="default"):
    try:
        yaml_data=open("secret.yaml", "rb").read().decode('utf-8')
        yaml_body=yaml.safe_load(yaml_data)
        resp = v1.create_namespaced_secret(
            body=yaml_body, namespace="{}".format(namespace))

        data=__format_data_for_create_secret(resp)
        print (data)    
    except ApiException as e:
        print("ERROR IN create_secret:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return __format_data_for_create_secret(e.body)

def update_secret(k8s_object_name=None,yaml_body=None,namespace="default"):
    try:
        yaml_data=open("change_secret.yaml", "rb").read().decode('utf-8')
        yaml_body=yaml.safe_load(yaml_data)
        resp = v1.patch_namespaced_secret(
            name=k8s_object_name,
            body=yaml_body, 
            namespace="{}".format(namespace))

        data=__format_data_for_create_secret(resp)
        return data
    except ApiException as e:
        print("ERROR IN create_deployment:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return __format_data_for_create_secret(e.body)

def delete_secret(k8s_object_name=None,namespace="default"):
    try:
        resp = v1.delete_namespaced_secret(
                name=k8s_object_name,
                namespace="{}".format(namespace),
                body=client.V1DeleteOptions(
                    propagation_policy="Foreground", grace_period_seconds=5)
            )

        data=__format_data_for_create_secret(resp)
        return data
    except ApiException as e:
        print("ERROR IN create_deployment:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return __format_data_for_create_secret(e.body)

# export secret=$(kubectl get serviceaccount default -o json | jq -r '.secrets[].name')
# kubectl get secret $secret -o yaml | grep "token:" | awk {'print $2'} |  base64 -d > token
# APISERVER=$(kubectl config view | grep server | cut -f 2- -d ":" | tr -d " ")
if __name__ == '__main__':
    create_secret("default")
    #update_secret(k8s_object_name="munish")
    #delete_secret(k8s_object_name="munish")