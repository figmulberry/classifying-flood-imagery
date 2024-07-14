# Classify Flooding in Imagery with Python 


## Scenario

As a remote sensing analyst in a *humanitarian organization*, your tasks involve conducting analyses to support responses to disasters in your region. For such events, you are required to conduct analysis quickly to get the impact of the disaster and the nature of response required. Recently, the region of Bukombe in the valley of Chemba (one of your organization’s programming areas), has been hit by a devastating flooding event that has claimed many lives and properties. Your task is to quickly analyze satellite imagery and identify areas that have been recently flooded (extent) before a dispatch team is sent on the ground to assess the damage caused.


## Objective

The objective of this project is to develop an automated tool to identify flooded areas in satellite imagery using Python and ArcGIS tools. Initially, the analysis will be conducted in ArcGIS Pro using Python code within a notebook environment. Later, the code will be converted into a script tool that can be used by analysts who may not have a programming background.

## Requirements
- You must have an ArcGIS Spatial Analyst license to use this notebook.

### Additional Learning Resources
This lesson uses Python and ArcGIS Notebooks and assumes some familiarity with remote sensing.  
If you are not familiar with Python in ArcGIS, you may want to complete some more introductory lessons before this one.

- Python in ArcGIS *[Introductory Courses](www.esri.com/training/Bookmark/FKPA9BYUN)*.

- For a quick introduction to Python, see the first three lessons in the *[Learn Python with ArcGIS Notebooks](https://learn.arcgis.com/en/paths/learn-python-with-arcgis-notebooks/)* path.

- For more information about remote sensing in ArcGIS, see the *[Introduction to Imagery and Remote Sensing](https://introduction-to-remote-sensing-learngis.hub.arcgis.com/)* curriculum.



## About the Analysis Data

The imagery you'll use is a pair of clipped scenes from the *[Sentinel](https://sentinels.copernicus.eu/web/sentinel/home)* satellite program, from the European Union's *[Copernicus](https://www.copernicus.eu/en/about-copernicus)* Earth observation program. One scene shows the area of interest before the flooding event, and the other scene shows the area after the flood.

### Download & Extract the Imagery

You'll download the *[Sentinel_2_Clipped.zip](https://arcgis.com/sharing/rest/content/items/9cfeb37e929a4b0484be5235da16e0bf/data)* imagery data for the analysis. The *Sentinel_2_Clipped.zip* file contains a folder named *Sentinel_2_Clipped*.

1. In the file explorer, create a folder on your C:\ drive named `Lessons`.
2. In the `Lessons` folder, create a folder named `AnalyzeFlooding`.
3. Extract the `Sentinel_2_Clipped` folder from the zip file to *C:\Lessons\AnalyzeFlooding\Sentinel_2_Clipped*. If you use another location, you must adjust the paths in the code in this notebook. The `Sentinel_2_Clipped` folder contains folders named `Before`, `After`, and `Output`.

## Jupyter Notebooks for Analysis

We have two Jupyter notebooks that are integral to this project:

1. *[Classify_Imagery_with_Python.ipynb](link_to_the_notebook)*: In this notebook, we create a script that runs locally in ArcGIS Pro using Python code within a notebook environment. This notebook includes the initial analysis and code development to identify flooded areas in satellite imagery.

2. *[Build_a_script_tool.ipynb](link_to_the_notebook)*: In this notebook, we turn the aforementioned script into a script tool. This notebook includes the steps to modify the code for use in a script tool, export the script to a Python file, and create a script tool in ArcGIS Pro.

These notebooks can be found in the repository and are essential for both the initial analysis and the conversion of the script into a usable tool for non-programmers.

## Creating a Script Tool in ArcGIS Pro

With your Python code written, you can now modify it slightly to create a *[script tool](https://pro.arcgis.com/en/pro-app/latest/arcpy/geoprocessing_and_python/a-quick-tour-of-creating-script-tools.htm)*. A script tool will allow anyone with ArcGIS Pro and the Spatial Analyst extension to run the Python script you created without any knowledge of Python or Notebooks. It will look and work like any other geoprocessing tool in ArcGIS.

Converting a script to a script tool allows non-programmers to use your analysis workflow.

### Steps to Create a Script Tool

1. *Modify the Code for Use in the Script Tool*: Make modifications to allow the script tool to pass parameter values to the Python code. In the original script, set several variables at the beginning of the code, including `before_img_folder`, `after_img_folder`, and `final_output_folder`. These variables must be changed to accept input when the script tool is run.
2. *Export the Notebook's Contents to a Python (.py) File*: Export the modified code to a Python file.
3. *Create a Toolbox*: In ArcGIS Pro, create a new toolbox.
4. *Create a Script Tool in the Toolbox**: Add a new script tool to the toolbox.
5. *Set Parameters for the Tool*: Configure the parameters for the script tool to accept inputs.
6. *Document the Tool*: Add metadata and documentation to the script tool.
7. *Connect the Tool to the Python Script*: Link the script tool to the exported Python script.
8. *Run the Tool*: Test the script tool to ensure it works as expected.


## Results

*Write the results here...(inlcude the images)*

## Conclusion

By following this guide, you will have developed an automated tool to identify flooded areas in satellite imagery using Python and ArcGIS tools. This tool will enable quick analysis and support disaster response efforts effectively.

For further assistance and resources, please refer to the *[ArcGIS documentation](https://www.esri.com/en-us/arcgis/products/arcgis-pro/overview)* and the *[Esri Community](https://community.esri.com/)*.