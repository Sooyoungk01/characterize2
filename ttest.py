import os


# download pSp encoder
path = MODEL_PATHS["encoder"]
download_command = get_download_model_command(file_id=path["id"], file_name=path["name"])
# !{download_command}
os.system(f"{download_command}")

# download dualstylegan
path = MODEL_PATHS[style_type+'-G']
download_command = get_download_model_command(file_id=path["id"], file_name=os.path.join(style_type, path["name"]))
# !{download_command}
os.system(f"{download_command}")

# download sampler
path = MODEL_PATHS[style_type+'-N']
download_command = get_download_model_command(file_id=path["id"], file_name=os.path.join(style_type, path["name"]))
# !{download_command}
os.system(f"{download_command}")

# download extrinsic style code
path = MODEL_PATHS[style_type+'-S']
download_command = get_download_model_command(file_id=path["id"], file_name=os.path.join(style_type, path["name"]))
os.system(f"{download_command}")

# !{download_command}