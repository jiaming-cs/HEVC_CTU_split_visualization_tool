# HEVC_CTU_split_visualization_tool

Visualize Coding Unit Splitation Result of HEVC/H.265 and AVC/H.264. Currently only support CU length of 64x64.

## Usage

* You can find a tool to generate Coding Unit depth of yuv files in another [repository](https://github.com/jiamingli9674/HEVC_CTU_split_dataset_generator) of my.

* Install python dependencies pillow and opencv

* Add the data to data_list on line 134 of `visualize.py`, you can also change different QPs at line 37

* Run the script

```bash
python visualize.py
```

## Examples

![HEVC Example 1](img/YachtRide_HEVC_1.png)

![HEVC Example 2](img/YachtRide_HEVC_100.png)
