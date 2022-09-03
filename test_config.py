from kubernetes import client, config
from kubernetes.client import ApiClient
from kubernetes.client.rest import ApiException
import yaml
import json

config.load_kube_config()
v1 = client.CoreV1Api()

def __format_data_for_create_configmap(client_output):
        temp_dict={}
        temp_list=[]
        json_data=ApiClient().sanitize_for_serialization(client_output)
        
        if type(json_data) is str:
            print("FORMAT_DATA :{}".format(type(json_data)))
            json_data = json.loads(json_data)
        temp_list.append(json_data)
        return temp_list

def create_configmap(yaml_body=None,namespace="default"):
    try:
        yaml_data=open("config.yaml", "rb").read().decode('utf-8')
        yaml_body=yaml.safe_load(yaml_data)
        resp = v1.create_namespaced_config_map(
            body=yaml_body, namespace="{}".format(namespace))

        data=__format_data_for_create_configmap(resp)
        print (data)    
    except ApiException as e:
        print("ERROR IN create_configmap:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return __format_data_for_create_configmap(e.body)

def update_configmap(k8s_object_name=None,yaml_body=None,namespace="default"):
    try:
        yaml_data=open("change_config.yaml", "rb").read().decode('utf-8')
        yaml_body=yaml.safe_load(yaml_data)
        resp = v1.patch_namespaced_config_map(
            name=k8s_object_name,
            body=yaml_body, 
            namespace="{}".format(namespace))

        data=__format_data_for_create_configmap(resp)
        return data
    except ApiException as e:
        print("ERROR IN create_deployment:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return __format_data_for_create_configmap(e.body)

def delete_configmap(k8s_object_name=None,namespace="default"):
    try:
        resp = v1.delete_namespaced_config_map(
                name=k8s_object_name,
                namespace="{}".format(namespace),
                body=v1.delete_namespaced_config_map(k8s_object_name, namespace)
            )
    except ApiException as e:
        print("ERROR IN create_deployment:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return __format_data_for_create_configmap(e.body)

# export secret=$(kubectl get serviceaccount default -o json | jq -r '.secrets[].name')
# kubectl get secret $secret -o yaml | grep "token:" | awk {'print $2'} |  base64 -d > token
# APISERVER=$(kubectl config view | grep server | cut -f 2- -d ":" | tr -d " ")
if __name__ == '__main__':
    create_configmap("default")
    #update_configmap(k8s_object_name="munish")
    #delete_configmap(k8s_object_name="munish")