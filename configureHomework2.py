import json
import zipfile
import os

def get_dependencies(package_file):
    dependencies = []

    with zipfile.ZipFile(package_file, 'r') as zip_ref:
        nuspec_files = [f for f in zip_ref.namelist() if f.endswith('.nuspec')]
        if not nuspec_files:
            return dependencies

        nuspec_file = nuspec_files[0]
        with zip_ref.open(nuspec_file) as nuspec:
            lines = nuspec.read().decode('utf-8').splitlines()
            inside_dependencies = False

            for line in lines:
                line = line.strip()
                if '<dependencies>' in line:
                    inside_dependencies = True
                elif '</dependencies>' in line:
                    inside_dependencies = False
                if inside_dependencies and '<dependency' in line:
                    package_name = line.split('id="')[1].split('"')[0]
                    version = line.split('version="')[1].split('"')[0]
                    dependencies.append((package_name, version))
            
    return dependencies


def build_dependency_graph(package_name, depth, max_depth, package_directory, graph):
    if depth > max_depth:
        return
    package_file = os.path.join(package_directory, f'{package_name}.nupkg')
    if not os.path.exists(package_file):
        return
    dependencies = get_dependencies(package_file)
    for dep, version in dependencies:
        graph.append(f'{package_name} --> {dep}')
        build_dependency_graph(dep, depth + 1, max_depth, package_directory, graph)


def get_mermaid_code(package_name, max_depth, package_directory):
    graph = []
    build_dependency_graph(package_name, 1, max_depth, package_directory, graph)
    unique_graph = list(set(graph))
    return '\n'.join(unique_graph)


        
with open('config.json', 'r') as file:
        config = json.load(file)
package_name = config["package_name"]
max_depth = config["max_depth"]
output_file = config["output_file"]

package_directory = "C:/Users/Ян/.nuget/packages/newtonsoft.json/13.0.3"

mermaid_code = 'graph TD\n'+get_mermaid_code(package_name, max_depth, package_directory)


print(mermaid_code)

with open(output_file, 'w') as file:
        file.write(mermaid_code)
