from urllib import response
import requests

"""Modules"""
from modules.utils import *


def execute_request(mode,method,url,headers=None, body=None):
    
    if isinstance(body, dict):
        x = requests.request(method, url, headers=headers, json=body)
    else:
        x = requests.request(method, url, headers=headers, data=body)

    if mode=='debug':
        print(f"[DEBUG] {x.status_code} status code")

    return x



def run_http_network(node,variables,mode,system_vars):
    headers=None
    if mode=='debug':
        print("[+] Running Http")

    url = node.get('url', '')
    resolved_url  = replace_all_variables_in_command(url, variables,system_vars)
    headers = node.get('headers', {})
    body = node.get('body', '')
    body = replace_all_variables_in_command(body, variables,system_vars)
    # Si headers est une chaîne, le parser en dict
    if isinstance(headers, str):
        headers_list = [h.strip() for h in headers.strip('[]').split(',')]
        headers_dict = {}
        for h in headers_list:
            if ':' in h:
                key, val = h.split(':', 1)
                headers_dict[key.strip()] = val.strip()
            elif '=' in h:
                key, val = h.split('=', 1)
                headers_dict[key.strip()] = val.strip()
        headers = headers_dict
    elif isinstance(headers, list):
        headers_dict = {}
        for h in headers:
            if ':' in h:
                key, val = h.split(':', 1)
                headers_dict[key.strip()] = val.strip()
            elif '=' in h:
                key, val = h.split('=', 1)
                headers_dict[key.strip()] = val.strip()
        headers = headers_dict
    method = node.get('method', 'GET').upper()

    if resolved_url.startswith("http://") or resolved_url.startswith("https://"):
        url = resolved_url

    output=[]
    if url:
        if mode == 'debug':
            print("[DEBUG] REQUEST INFO:")
            print(f"Method: {method}")
            print(f"URL: {url}")
            print(f"Headers: {headers}")

        x=execute_request(mode,method,url, headers, body)
        output.append(f"Status Code: {x.status_code}")
        output.append("\n")
        for k, v in x.headers.items():
            output.append(f"{k}: {v}")
        output.append("\n")
        for line in x.text.splitlines():
            output.append(line.rstrip())

    if node.get('output_file'):
        save_output(node, output, system_vars,mode)





def run_api_call_network(node,variables,mode,system_vars):
    if mode=='debug':
        print("[+] Running Api-call")
    url = node.get('url', '')
    resolved_url  = replace_all_variables_in_command(url, variables,system_vars)
    headers = node.get('headers', {})
    body = node.get('body', '')
    body = replace_all_variables_in_command(body, variables,system_vars)
    # Si headers est une chaîne, le parser en dict
    if isinstance(headers, str):
        headers_list = [h.strip() for h in headers.strip('[]').split(',')]
        headers_dict = {}
        for h in headers_list:
            if ':' in h:
                key, val = h.split(':', 1)
                headers_dict[key.strip()] = val.strip()
            elif '=' in h:
                key, val = h.split('=', 1)
                headers_dict[key.strip()] = val.strip()
        headers = headers_dict
    elif isinstance(headers, list):
        headers_dict = {}
        for h in headers:
            if ':' in h:
                key, val = h.split(':', 1)
                headers_dict[key.strip()] = val.strip()
            elif '=' in h:
                key, val = h.split('=', 1)
                headers_dict[key.strip()] = val.strip()
        headers = headers_dict
    method = node.get('method', 'GET').upper()

    if resolved_url.startswith("http://") or resolved_url.startswith("https://"):
        url = resolved_url

    output=[]
    if url:
        if mode == 'debug':
            print("[DEBUG] REQUEST INFO:")
            print(f"Method: {method}")
            print(f"URL: {url}")
            print(f"Headers: {headers}")

        x=execute_request(mode,method,url, headers, body)
        output.append(f"Status Code: {x.status_code}")
        output.append("\n")
        for k, v in x.headers.items():
            output.append(f"{k}: {v}")
        output.append("\n")
        for line in x.text.splitlines():
            output.append(line.rstrip())

    if node.get('output_file'):
        save_output(node, output, system_vars,mode)

def run_webhook_network(node,variables,mode,system_vars):

    if mode=='debug':
        print("[+] Running Webhook")

    url = node.get('url', '')
    resolved_url  = replace_all_variables_in_command(url, variables,system_vars)
    headers = node.get('headers', {})
    body = node.get('body', '')
    body = replace_all_variables_in_command(body, variables,system_vars)
    # Si headers est une chaîne, le parser en dict
    if isinstance(headers, str):
        headers_list = [h.strip() for h in headers.strip('[]').split(',')]
        headers_dict = {}
        for h in headers_list:
            if ':' in h:
                key, val = h.split(':', 1)
                headers_dict[key.strip()] = val.strip()
            elif '=' in h:
                key, val = h.split('=', 1)
                headers_dict[key.strip()] = val.strip()
        headers = headers_dict
    elif isinstance(headers, list):
        headers_dict = {}
        for h in headers:
            if ':' in h:
                key, val = h.split(':', 1)
                headers_dict[key.strip()] = val.strip()
            elif '=' in h:
                key, val = h.split('=', 1)
                headers_dict[key.strip()] = val.strip()
        headers = headers_dict
    method = node.get('method', 'GET').upper()

    if resolved_url.startswith("http://") or resolved_url.startswith("https://"):
        url = resolved_url

    output=[]
    if url:
        if mode == 'debug':
            print("[DEBUG] REQUEST INFO:")
            print(f"Method: {method}")
            print(f"URL: {url}")
            print(f"Headers: {headers}")
            print(f"Body: {body}")

        x=execute_request(mode,method,url, headers, body)
        output.append(f"Status Code: {x.status_code}")
        output.append("\n")
        for k, v in x.headers.items():
            output.append(f"{k}: {v}")
        output.append("\n")
        for line in x.text.splitlines():
            output.append(line.rstrip())

    if node.get('output_file'):
        save_output(node, output, system_vars,mode)
