import os
import copy
import threading

class dataLoader():
    def __init__(self, folder_path):
        self.img_dir = os.path.join(folder_path, "images")
        self.diff_map_dir = os.path.join(folder_path, "diff_maps")
        self.labels_dir = os.path.join(folder_path, "labels")
        self._check_data_consistency()
        self._grouping()
        

    def _check_data_consistency(self):
        '''
        check if a data have both img diff_map and label
        '''
        self._fnames = {}
        self._fnames["img"] = [ n[:-4] for n in os.listdir(self.img_dir)]
        self._fnames["diff_map"] = [ n[:-4] for n in os.listdir(self.diff_map_dir)]
        self._fnames["labels"] = [ n[:-4] for n in os.listdir(self.labels_dir)]
        assert len(self._fnames["img"]) == len(self._fnames["diff_map"]) == len(self._fnames["labels"]), "inconsistent data"
        self.fnames = copy.deepcopy(self._fnames["img"])
        self.fnames.sort()

    
    def _grouping(self):
        '''
        assume self.fanmes sorted
        group imgs from the same camera 
        e.g.
        [...
            {"site_id": "035-50-01-0069-01", "cam_no": 2,
             "entries":["035-50-01-0069-01-2-2024-07-17 14-20-22.450625",
                     "035-50-01-0069-01-2-2024-07-17 14-40-22.513126",
                     ...
                     "035-50-01-0069-01-2-2024-07-17 15-50-22.731840"]
             ...
            },
        ...
        ]
        each data need to have at least "entries" data 
        '''
        self.groups = []
        
        for fname in self.fnames:
            parts = fname.split('-')
            # TODO
            # save other labesl if necessary
            if len(parts) > 5:
                site_id = "-".join(parts[:5])
                cam_no = parts[5]
            is_same_camera = lambda dic: (dic["site_id"] == site_id and dic["cam_no"] == cam_no)
            if len(self.groups) == 0 or not is_same_camera(self.groups[-1]):
                self.groups.append({"site_id": site_id, "cam_no": cam_no, "entries":[fname]})
            else:
                self.groups[-1]["entries"].append(fname)
        return True

    
    def get_batch(self):
        '''
        get a batch of data and return it
        '''
        batch_imgs, batch_labels, batch_diff_map = [], [], []
        return batch_imgs, batch_labels, batch_diff_map

    
    def save_list(self, output_file):
        '''
        save full list into a local text file
        arg:
            output_file: path to the save location
        '''
        # Write sorted names to the output file 
        with open(output_file, 'w') as file:
            # TODO change it 
            for c, filename in img_with_cam_no:
                file.write(f"{filename} -> c = {c}\n")
        
        print(f"Sorted names extracted and saved in {output_file}")


# Usage and basic tests
if __name__ == "__main__":
    folder_path = os.path.dirname("./data/")
    dl = dataLoader(folder_path)
    print(len(dl.groups))
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    count = 0
    for img_name in dl.groups[0]['entries']:
        img_path = os.path.join("./data/images/", img_name+'.jpg')
        img = mpimg.imread(img_path)
        imgplot = plt.imshow(img)
        plt.show()
        count += 1
