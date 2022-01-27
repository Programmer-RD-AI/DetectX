import gc
import threading
import urllib.request

import numpy as np
import pandas as pd

try:
    from tqdm import tqdm
except Exception as e:
    raise ImportError(f"""
        Cannot Import Tqdm try installing it using 
        `pip3 install tqdm` 
        or 
        `conda install tqdm`.
        \n 
        {e}""")


class Download:
    """
    This class is used to download all of classes,
    for object detection
    """

    def __init__(
        self,
        idx: int = 0,
        idx_1: int = 0,
        idx_2: int = 0,
        idx_3: int = 0,
        data: dict = None,
        labels: list = None,
        labels_r: list = None,
        labels_and_imageids: list = None,
        bboxs: list = None,
        image_urls: list = None,
        init_imageids: list = None,
        images_and_bbox_and_imgid_: list = None,
        imgids: list = None,
        download_url_data: pd.DataFrame = None,
        imageids_labels: dict = None,
    ) -> None:
        """summary_line
        Keyword arguments:
        argument
            idx,idx_1,idx_2,idx_3 = the init starting index
            data = The data that is going to be download,
                   if want to add new info can be done.
            labels = labels from open images (Name of label)
            labels_r = labels from open images (Label Code of label)
            labels_and_imageids = loading files for getting the labels_and_imageids
            bboxs = loading files for getting the bboxs
            image_urls = loading files for getting the image_urls
            init_imageids = init imageids
            images_and_bbox_and_imgid_ = init images_and_bbox_and_imgid_
            init imgids = init imgids
        Return: None
        """
        if imageids_labels is None:
            imageids_labels = {}
        self.imageids_labels = imageids_labels
        if data is None:
            data = {
                "ImageID": [],
                "OriginalURL": [],
                "OriginalLandingURL": [],
                "XMin": [],
                "YMin": [],
                "XMax": [],
                "YMax": [],
            }
        if download_url_data is None:
            self.download_url_data = []
        if labels is None:
            labels = [
                "/m/021c5h",
                "/m/04_r5c",
                "/m/07kbbhf",
                "/m/0bwd_0j",
                "/m/0dflpy",
                "/m/021c5h",
                "/m/03yn1j",
            ]
        if labels_r is None:
            labels_r = [
                "/m/021c5h",
                "/m/04_r5c",
                "/m/07kbbhf",
                "/m/0bwd_0j",
                "/m/0dflpy",
                "/m/021c5h",
                "/m/03yn1j",
            ]
        if labels_and_imageids is None:
            labels_and_imageids = [
                "./open_image_raw_data/oidv6-train-annotations-human-imagelabels.csv",
                "./open_image_raw_data/test-annotations-human-imagelabels-boxable.csv",
                "./open_image_raw_data/test-annotations-machine-imagelabels.csv",
                "./open_image_raw_data/train-annotations-human-imagelabels-boxable.csv",
                "./open_image_raw_data/train-annotations-machine-imagelabels.csv",
                "./open_image_raw_data/validation-annotations-human-imagelabels-boxable.csv",
                "./open_image_raw_data/validation-annotations-machine-imagelabels.csv",
            ]
        if bboxs is None:
            bboxs = [
                "./open_image_raw_data/oidv6-train-annotations-bbox.csv",
                "./open_image_raw_data/test-annotations-bbox.csv",
                "./open_image_raw_data/validation-annotations-bbox.csv",
            ]
        if image_urls is None:
            image_urls = [
                "./open_image_raw_data/oidv6-train-images-with-labels-with-rotation.csv",
                "./open_image_raw_data/test-images-with-rotation.csv",
                "./open_image_raw_data/train-images-boxable-with-rotation.csv",
                "./open_image_raw_data/validation-images-with-rotation.csv",
            ]
        if init_imageids is None:
            init_imageids = []
        if images_and_bbox_and_imgid_ is None:
            images_and_bbox_and_imgid_ = []
        if imgids is None:
            imgids = []
        try:
            # Indexing
            self.idx = idx
            self.idx_1 = idx_1
            self.idx_2 = idx_2
            self.idx_3 = idx_3
        except Exception as e:
            raise ValueError(f"""
            In the indexing parameters 
            there was a error occurred 
            \n 
            {e}""")
        try:
            # Initinalizing Data Storage
            self.data = data
        except Exception as e:
            raise ValueError(f"""
                In the Initinalizing Data Storage
                parameters there was a error occurred.
                \n
                {e}""")
        try:
            # Labels of data
            self.labels = labels
            self.labels_r = labels_r
        except Exception as e:
            raise ValueError(f"""
            In the Labels of data 
            parameters there was a error occurred 
            \n 
            {e}
            """)
        try:
            # Data Loading file paths
            self.labels_and_imageids = labels_and_imageids
            self.bboxs = bboxs
            self.image_urls = image_urls
        except Exception as e:
            raise ValueError(f"""
                In the Data Loading
                file paths parameters there 
                was a error occurred.
                \n
                {e}""")
        try:
            # Collection of data
            self.imageids = init_imageids
            self.images_and_bbox_and_imgid_ = images_and_bbox_and_imgid_
            self.imgids = imgids
        except Exception as e:
            raise ValueError(f"""
            In the Collection of data 
            parameters there was a error occurred 
            \n 
            {e}
            """)

    # Loading data section

    def load_labels_and_imageid(self) -> pd.DataFrame:
        """summary_line
        Keyword arguments:
        argument load_labels_and_imageid
        Return: pd.DataFrame
        """
        try:
            print("load_labels_and_imageid")
            labels_and_imageid = pd.read_csv(self.labels_and_imageids[0])
            for i in tqdm(range(1, len(self.labels_and_imageids))):
                threading.Thread(
                    target=labels_and_imageid.append,
                    args=[pd.read_csv(self.labels_and_imageids[i])],
                ).start()
            labels_and_imageid.sample(frac=1)
            return labels_and_imageid
        except Exception as e:
            raise ValueError(f"""
                The function 
                self.load_labels_and_imageid()
                or 
                Download().load_labels_and_imageid() 
                is not working correctly. 
                \n
                {e}""")

    def load_bbox(self) -> pd.DataFrame:
        """summary_line
        Keyword arguments:
        argument load_bbox
        Return: pd.DataFrame
        """
        try:
            print("load_bbox")
            bboxs_df = pd.read_csv(self.bboxs[0])
            for i in tqdm(range(1, len(self.bboxs))):
                threading.Thread(
                    target=bboxs_df.append,
                    args=[pd.read_csv(self.bboxs[i])],
                ).start()
            bboxs_df.sample(frac=1)
            return bboxs_df
        except Exception as e:
            raise ValueError(f"""
                The function 
                self.load_bbox() 
                or 
                Download().load_bbox() 
                is not working correctly. 
                \n
                {e}""")

    def load_image_urls(self) -> pd.DataFrame:
        """summary_line
        Keyword arguments:
        argument load_image_urls
        Return: pd.DataFrame
        """
        try:
            print("load_image_urls")
            image_urls_df = pd.read_csv(self.image_urls[0])
            for i in tqdm(range(1, len(self.image_urls))):
                threading.Thread(
                    target=image_urls_df.append,
                    args=[pd.read_csv(self.image_urls[i])],
                ).start()
            image_urls_df.sample(frac=1)
            return image_urls_df
        except Exception as e:
            raise ValueError(f"""
                The function
                self.load_image_urls() 
                or 
                Download().load_image_urls() 
                is not working correctly.
                \n
                {e}""")

    # Creating data section

    def create_imageids(self) -> bool:
        """summary_line
        Keyword arguments:
        argument create_imageids
        Return: bool
        """
        try:
            print("create_imageids")
            labels_and_imageid = self.load_labels_and_imageid()
            for labelname, imageid in zip(
                    tqdm(labels_and_imageid["LabelName"]),
                    labels_and_imageid["ImageID"]):
                if labelname in self.labels_r:
                    self.idx_1 += 1
                    threading.Thread(
                        target=self.imageids.append,
                        args=[imageid],
                    ).start()
                    self.imageids_labels[imageid] = labelname
            del labels_and_imageid
            gc.collect()
            print(f"Number of Images : {self.idx_1}")
            return True
        except Exception as e:
            raise ValueError(f"""
                The function 
                self.create_imageids() 
                or 
                Download().create_imageids() 
                is not working correctly. 
                \n 
                {e}""")

    def create_bbox(self) -> bool:
        """summary_line
        Keyword arguments:
        argument create_bbox
        Return: bool
        """
        try:
            print("create_bbox")
            bboxs = self.load_bbox()
            for imgid in zip(
                    tqdm(bboxs["ImageID"]),
                    bboxs["XMin"],
                    bboxs["YMin"],
                    bboxs["XMax"],
                    bboxs["YMax"],
            ):
                imgid = list(imgid)
                if str(imgid[0]) in self.imageids:
                    threading.Thread(
                        target=imgid.append,
                        args=[self.imageids_labels[imgid[0]]],
                    ).start()
                    self.idx_2 += 1
                    threading.Thread(
                        target=self.images_and_bbox_and_imgid_.append,
                        args=[imgid],
                    ).start()
                    threading.Thread(
                        target=self.imgids.append,
                        args=[imgid[0]],
                    ).start()
            np.save("./imageids.npy", self.imgids)
            del bboxs
            gc.collect()
            self.images_and_bbox_and_imgid_ = pd.DataFrame(
                self.images_and_bbox_and_imgid_,
                columns=["ImageID", "XMin", "YMin", "XMax", "YMax", "Labels"],
            )
            self.images_and_bbox_and_imgid_.to_csv("./create_bbox.csv",
                                                   index=False)
            print(f"Number of Images : {self.idx_2}")
            return True
        except Exception as e:
            raise ValueError(f"""
                The function 
                self.create_bbox() 
                or 
                Download().create_bbox() 
                is not working correctly. 
                \n 
                {e}""")

    def create_image_urls(self) -> bool:
        """summary_line
        Keyword arguments:
        argument create_image_urls
        Return: bool
        """
        try:
            print("create_image_urls")
            data = {
                "ImageID": [],
                "OriginalURL": [],
                "OriginalLandingURL": [],
                "XMin": [],
                "YMin": [],
                "XMax": [],
                "YMax": [],
                "Labels": [],
            }
            image_urls = self.load_image_urls()
            for imgid in zip(
                    tqdm((image_urls["ImageID"])),
                    image_urls["OriginalURL"],
                    image_urls["OriginalLandingURL"],
            ):
                if imgid[0] in self.imgids:
                    imgid_of_iabaid = self.images_and_bbox_and_imgid_[
                        self.images_and_bbox_and_imgid_["ImageID"] == imgid[0]]
                    for idx_3 in tqdm(range(len(imgid_of_iabaid))):
                        imgid_of_iabaid_iter = self.images_and_bbox_and_imgid_[
                            self.images_and_bbox_and_imgid_["ImageID"] ==
                            imgid[0]].iloc[idx_3]
                        threading.Thread(
                            target=data["ImageID"].append,
                            args=[imgid[0]],
                        ).start()
                        threading.Thread(
                            target=data["OriginalURL"].append,
                            args=[imgid[1]],
                        ).start()
                        threading.Thread(
                            target=data["OriginalLandingURL"].append,
                            args=[imgid[2]],
                        ).start()
                        threading.Thread(
                            target=data["XMin"].append,
                            args=[imgid_of_iabaid_iter["XMin"]],
                        ).start()
                        threading.Thread(
                            target=data["YMin"].append,
                            args=[imgid_of_iabaid_iter["YMin"]],
                        ).start()
                        threading.Thread(
                            target=data["XMax"].append,
                            args=[imgid_of_iabaid_iter["XMax"]],
                        ).start()
                        threading.Thread(
                            target=data["YMax"].append,
                            args=[imgid_of_iabaid_iter["YMax"]],
                        ).start()
                        threading.Thread(
                            target=data["Labels"].append,
                            args=[imgid_of_iabaid_iter["Labels"]],
                        ).start()
            del self.images_and_bbox_and_imgid_
            gc.collect()
            data = pd.DataFrame(data)
            data.to_csv("./create_image_urls.csv", index=False)
            self.download_url_data = data
            print(f"Number of Images : {len(data)}")
        except Exception as e:
            raise ValueError(f"""
                The function 
                self.create_image_urls()
                or 
                Download().create_image_urls()
                is not working correctly.
                \n
                {e}""")

    # Downloading data section

    def download_images(self) -> pd.DataFrame:
        """summary_line
        Keyword arguments:
        argument download images
        Return: pd.DataFrame
        """
        try:
            print("download_images")
            new_data = {
                "Path": [],
                "XMin": [],
                "YMin": [],
                "XMax": [],
                "YMax": [],
                "ImageID": [],
                "Url": [],
            }
            for img_url, xmin, ymin, xmax, ymax, ourl in zip(
                    tqdm((self.download_url_data["ImageID"])),
                    self.download_url_data["XMin"],
                    self.download_url_data["YMin"],
                    self.download_url_data["XMax"],
                    self.download_url_data["YMax"],
                    self.download_url_data["OriginalURL"],
            ):
                self.idx += 1
                try:
                    threading.Thread(
                        target=urllib.request.urlretrieve,
                        args=[ourl, f"./Img/{self.idx}.png"],
                    ).start()
                except ValueError as e:
                    break
                threading.Thread(
                    target=new_data["Path"].append,
                    args=[f"{self.idx}.png"],
                ).start()
                threading.Thread(
                    target=new_data["XMin"].append,
                    args=[xmin],
                ).start()
                threading.Thread(
                    target=new_data["YMin"].append,
                    args=[ymin],
                ).start()
                threading.Thread(
                    target=new_data["XMax"].append,
                    args=[xmax],
                ).start()
                threading.Thread(
                    target=new_data["YMax"].append,
                    args=[ymax],
                ).start()
                threading.Thread(
                    target=new_data["Url"].append,
                    args=[ourl],
                ).start()
                threading.Thread(
                    target=new_data["ImageID"].append,
                    args=[img_url],
                ).start()
            data = pd.DataFrame(new_data)
            data.to_csv("./Data.csv", index=False)
            return new_data
        except Exception as e:
            raise ValueError(f"""
                The function
                self.download_images()
                or 
                Download().download_images() 
                is not working correctly.
                \n
                {e}""")

    def download(self) -> bool:
        """summary_line
        Keyword arguments:
        argument: This is the funtion which uses
            all of the funtions of this class
            and combines it and download and
            does all of the work.
        Return: bool
        """
        try:
            print("download")
            self.create_imageids()
            self.create_bbox()
            self.create_image_urls()
            return self.download_images()
        except Exception as e:
            raise ValueError(f"""
                The function self.download()
                or
                Download().download()
                is not working correctly.
                \n
                {e}""")


d = Download()
d.download()
