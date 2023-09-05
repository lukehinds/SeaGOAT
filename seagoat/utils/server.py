import os
import socket

import appdirs

from seagoat.utils.json_file import get_json_file_contents


def get_server_info_file(repo_path):
    repo_id = os.path.normpath(repo_path).replace(os.sep, "_")
    user_cache_dir = appdirs.user_cache_dir("seagoat-servers")
    os.makedirs(user_cache_dir, exist_ok=True)
    return os.path.join(user_cache_dir, f"{repo_id}.json")


def load_server_info(server_info_file):
    server_info = get_json_file_contents(server_info_file)
    host = server_info["host"]
    port = server_info["port"]
    pid = server_info.get("pid")
    server_address = f"http://{host}:{port}"
    return host, port, pid, server_address


def get_server_info(repo_path: str):
    return get_json_file_contents(get_server_info_file(repo_path))


def is_server_running(repo_path: str):
    server_info = get_server_info(repo_path)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_obj:
        return socket_obj.connect_ex((server_info["host"], server_info["port"])) == 0