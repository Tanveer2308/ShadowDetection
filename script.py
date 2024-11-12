import os

def extract_and_sort_names_by_camera(folder_path, output_file):
    names_with_c = []
    
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            parts = filename.split('-')
            if len(parts) > 5:
                c = parts[5]  # 'c' is the 6th part in the format
                names_with_c.append((c, filename))
    
    # Sort the list by the `c` value (camera identifier)
    names_with_c.sort(key=lambda x: x[0])
    
    # Write sorted names to the output file
    with open(output_file, 'w') as file:
        for c, filename in names_with_c:
            file.write(f"{filename} -> c = {c}\n")
    
    print(f"Sorted names extracted and saved in {output_file}")

# Usage
folder_path = r"C:\Users\bhati\Downloads\20240724_original (1)\20240724_original\images"
output_file = "output_names.txt"
extract_and_sort_names_by_camera(folder_path, output_file)