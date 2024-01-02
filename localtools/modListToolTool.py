import os

def generate_code(parent_directory, model_category, model_name, author_name, cloud_directory, parent_directory_name, relative_directory):
    # Template for the generated code
    template = """manager.add_mod_childs("{model_category}", "{model_name}", [\n{files}\n])"""
    file_template = """    {{
        "downloadType": "cg",
        "url": "{author_name}/{cloud_directory}/{file_name}",
        "parentPath": "{parent_directory_name}",
        "sonPath": "{son_path}",
        "fileName": "{file_name}"
    }},"""

    files_list = []

    # Walk through the parent directory
    for root, dirs, files in os.walk(parent_directory):
        for file in files:
            # Calculate the sonPath as relative path from relative_directory
            son_path = os.path.relpath(os.path.join(root, file), relative_directory)
            # Ensure it starts with '/'
            if not son_path.startswith('/'):
                son_path = '/' + son_path

            # Generate the formatted string for each file
            files_list.append(file_template.format(
                author_name=author_name,
                cloud_directory=cloud_directory,
                file_name=file,
                parent_directory_name=parent_directory_name,
                son_path=os.path.dirname(son_path)  # Only the directory part
            ))
    
    # Join all file strings and insert into the main template
    files_str = "\n".join(files_list)
    code = template.format(model_category=model_category, model_name=model_name, files=files_str)

    return code

# Example usage
parent_directory = "/root/autodl-tmp/models/controlnet_annotator"
model_category = "插件所需依赖/模型"
model_name = "controlnet_annotator"
author_name = "xiaolxl"
cloud_directory = "controlnet-annotator"
parent_directory_name = "controlnet_annotator_models_path"
relative_directory = "/root/autodl-tmp/models/controlnet_annotator"

# Generate the code
generated_code = generate_code(parent_directory, model_category, model_name, author_name, cloud_directory, parent_directory_name, relative_directory)
print(generated_code)
