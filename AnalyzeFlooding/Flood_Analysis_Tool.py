# Imports
import os
from glob import glob
import arcpy
from arcpy.sa import *

# Set the input and output folder location variables.
# These must point to the locations of the folders in the Sentinel_2_Clipped folder you extracted.
# The "r" prefixes to the path strings indicate that these are "raw" strings in Python, and 
# the \ characters should not be treated as an escape character. If you edit these paths, remember
# to keep the \Before, \After, and \Output folder names in the paths.

# This is the folder containing the pre-flood imagery
# before_img_folder = r"C:\Lessons\AnalyzeFlooding\Sentinel_2_Clipped\Before"
before_img_folder = arcpy.GetParameterAsText(0)

# This is the folder containing the post-flood imagery
#after_img_folder = r"C:\Lessons\AnalyzeFlooding\Sentinel_2_Clipped\After"
after_img_folder = arcpy.GetParameterAsText(1)

# This is the folder where the final result files will be written
#final_output_folder = r"C:\Lessons\AnalyzeFlooding\Sentinel_2_Clipped\Output"
final_output_folder = arcpy.GetParameterAsText(2)

def create_sen2_band_variables(in_folder):
    """A function that creates band variables for Sentinel-2 imagery given the folder with all the band images."""
    
    # Use arcpy.AddMessage like print() to print to the ArcGIS Geoprocessing messages
    arcpy.AddMessage("Creating variables for image bands...")

    # Get a list of the jpg2000 files in the input folder and store it in a list
    band_list = glob(in_folder + "/*.jp2")

    # Use list comprehension to get files in the band_list which correspond to the specific Sentinel-2 band file names
    Blue = [x for x in band_list if x.endswith("B02.jp2")][0]
    Green = [x for x in band_list if x.endswith("B03.jp2")][0]
    Red = [x for x in band_list if x.endswith("B04.jp2")][0]
    Red_Edge_1 = [x for x in band_list if x.endswith("B05.jp2")][0]
    NIR = [x for x in band_list if x.endswith("B08.jp2")][0]
    SWIR2 = [x for x in band_list if x.endswith("B12.jp2")][0]

    # Return the band variables
    return Blue, Green, Red, Red_Edge_1, NIR, SWIR2

# call the create_sen2_band_variables function on the folder containing the after imagery
after_Blue, after_Green, after_Red, after_Red_Edge_1, after_NIR, after_SWIR2 = create_sen2_band_variables(after_img_folder)

# print a couple bands to see the results
print(after_Red)  # print the path of the Red band
print(after_NIR)  # print the path of the NIR band

# create the composite image, storing the output in memory
arcpy.CompositeBands_management(in_rasters=f"{after_NIR};{after_Red};{after_Green}",
                                out_raster=r"memory\after_composite_img")

# creates SWI processor function
def swi_processor(red_edge1_band, swir2_band):
    """Create a function which calculates the SWI for the given input image."""
    
    arcpy.AddMessage("\nBegining SWI Calculation...")
    
    # Calculate the SWI - Sentinel-2 Water Index
    # SWI Formula = (Red_Edge1 - SWIR2) / (Red_Edge1 + SWIR2)
    
    # Create a variable to store the calculation for the numerator
    # using arcpy spatial analyst Float tool to create a raster with floating point cell values
    Numerator = arcpy.sa.Float(Raster(red_edge1_band) - Raster(swir2_band))
    
    # Create a variable to store the calculation for the denominator
    # using arcpy spatial analyst Float tool to create a raster with floating point cell values
    Denominator = arcpy.sa.Float(Raster(red_edge1_band) + Raster(swir2_band))
    
    # Use the arcpy spatial analyst Divide tool to divide the numerator and the denominator 
    SWI = arcpy.sa.Divide(Numerator, Denominator)

    # return the results
    return SWI
    
    arcpy.AddMessage("SWI Successfully Generated")

# creates NDWI processor function
def ndwi_processor(green_band, nir_band):
    """Create a function which calculates the NDWI for the given input image."""

    arcpy.AddMessage("\nBegining NDWI Calculation...")
    
    # Calculate the NDWI - Normalized Difference Water Index
    # NDWI Formula = (Green - NIR) / (Green + NIR)

    # Create a variable to store the calculation for the numerator
    # using arcpy spatial analyst Float tool to create a raster with floating point cell values
    Num = arcpy.sa.Float(Raster(green_band) - Raster(nir_band))
    
    # Create a variable to store the calculation for the denominator
    # using arcpy spatial analyst Float tool to create a raster with floating point cell values
    Denom = arcpy.sa.Float(Raster(green_band) + Raster(nir_band))
    
    # Use the arcpy spatial analyst Divide tool to divide the numerator and the denominator 
    NDWI = arcpy.sa.Divide(Num, Denom)
    
    # return the results
    return NDWI
    
    arcpy.AddMessage("NDWI Successfully Generated")

# Process SWI 
# Create the SWI raster
after_swi_calc = swi_processor(red_edge1_band=after_Red_Edge_1,
                               swir2_band=after_SWIR2)

# Create path for output SWI file
after_swi_raster = r"memory\after_swi_raster"

# Save the result
after_swi_calc.save(after_swi_raster)


# Process NDWI 
# Create the NDWI raster
after_ndwi_calc = ndwi_processor(green_band=after_Green,
                                 nir_band=after_NIR)

# Create path for output NDWI file
after_ndwi_raster = r"memory\after_ndwi_raster"

# Save the result
after_ndwi_calc.save(after_ndwi_raster)

def create_threshold_raster(in_raster):
    """Creates a function that thresholds the input raster, and then returns it."""
    
    # Run the Ostu thresholding function on the input raster
    thresh_calc = arcpy.sa.Threshold(in_raster)
    
    # Return the result
    return thresh_calc

# Process NDWI 
# Use the threshold_raster function to process the NDWI raster
after_ndwi_thresh_calc = create_threshold_raster(in_raster=after_ndwi_raster)

# Create a path for output NDWI file
after_ndwi_thresh_raster = r"memory\after_ndwi_thresh"

# Save the NDWI thresh raster
after_ndwi_thresh_calc.save(after_ndwi_thresh_raster)

# Create a raster layer for the NDWI threshold file so it can be viewed in the results map tab
after_ndwi_threshold_layer = arcpy.MakeRasterLayer_management(after_ndwi_thresh_raster, 'after_ndwi_threshold')


# Process SWI 
# Use the threshold_raster function to process the SWI raster
after_swi_thresh_calc = create_threshold_raster(in_raster=after_swi_raster)

# Create a path for output NDWI file
after_swi_thresh_raster = r"memory\after_swi_thresh"

# Save the SWI thresh raster
after_swi_thresh_calc.save(after_swi_thresh_raster)

# Create a raster layer for the SWI threshold file so it can be viewed in the results map tab
after_swi_threshold_layer = arcpy.MakeRasterLayer_management(after_swi_thresh_raster, 'after_swi_threshold')

def create_water_confidence_raster(ndwi_threshold_raster, swi_threshold_raster):
    """Create a function that calculates the sum of two rasters."""
    
    # Add the two threshold rasters together by creating raster objects of each and combining them using the addition + operator
    water_confidence_raster = Raster(ndwi_threshold_raster) + Raster(swi_threshold_raster)

    # Return the result
    return water_confidence_raster

# Call the create_water_confidence_raster function
after_water_confidence_raster = create_water_confidence_raster(ndwi_threshold_raster=after_ndwi_thresh_raster, 
                                                         swi_threshold_raster=after_swi_thresh_raster)

# Create a path for output water confidence raster file
after_water_confidence_raster_path = r"memory\after_water_confidence_raster"

# Save the water confidence raster to a file in memory
after_water_confidence_raster.save(after_water_confidence_raster_path)

# Create a raster layer for the confidence raster file so it can be viewed in the results map tab
# after_water_confidence_matrix_layer = arcpy.MakeRasterLayer_management(after_water_confidence_raster, 'after_water_confidence_matrix')

# Create the remap values to set any pixels with the value of 1 to 0.
remap_value = RemapValue([[1, 0]])

# Reclassify the water mask
after_water_mask_reclass = Reclassify(in_raster=after_water_confidence_raster_path, 
                                      reclass_field="value", 
                                      remap=remap_value)

# Create a path for output water mask file
after_water_mask_raster = r"memory\after_water_mask_high_confidence"

# Save the water mask
after_water_mask_reclass.save(after_water_mask_raster)

# Create a raster layer so it can be viewed in the results map tab.
#after_water_mask_layer = arcpy.MakeRasterLayer_management(after_water_mask_reclass, 'after_water_mask_high_confidence')

# Step 1: create the band variables 
before_Blue, before_Green, before_Red, before_Red_Edge_1, before_NIR, before_SWIR2 = create_sen2_band_variables(
    in_folder=before_img_folder)


# Step 2: Create a false-color infrared composite image 
# create a composite image, storing the output in memory
arcpy.CompositeBands_management(in_rasters=f"{before_NIR};{before_Red};{before_Green}",
                                out_raster=r"memory\before_composite_img")

# Step 3: create indices 
# create the SWI raster
before_swi_calc = swi_processor(red_edge1_band=before_Red_Edge_1,
                                swir2_band=before_SWIR2)

# create path for output NDWI file
before_swi_raster = r"memory\before_swi_raster"

# Save result to file
before_swi_calc.save(before_swi_raster)

# create a raster layer for the NDWI threshold file so it can be viewed in the results map tab.
before_swi_layer = arcpy.MakeRasterLayer_management(before_swi_raster, 'before_swi')

# create the NDWI raster
before_ndwi_calc = ndwi_processor(green_band=before_Green,
                                  nir_band=before_NIR)

# create path for output NDWI file
before_ndwi_raster = r"memory\before_ndwi_raster"

# Save result to file
before_ndwi_calc.save(before_ndwi_raster)

# create a raster layer for the NDWI threshold file so it can be viewed in the results map tab.
before_ndwi_layer = arcpy.MakeRasterLayer_management(before_ndwi_raster, 'before_ndwi')


# Step 4: threshold indices 
# Threshold for NDWI
before_ndwi_thresh_calc = create_threshold_raster(in_raster=before_ndwi_raster)

# create path for output NDWI file
before_ndwi_thresh_raster = r"memory\before_ndwi_thresh"

# save the NDWI thresh raster
before_ndwi_thresh_calc.save(before_ndwi_thresh_raster)

# create a raster layer for the NDWI threshold file so it can be viewed in the results map tab.
before_ndwi_threshold_layer = arcpy.MakeRasterLayer_management(before_ndwi_thresh_raster, 'before_ndwi_threshold')

# Threshold for SWI
before_swi_thresh_calc = create_threshold_raster(in_raster=before_swi_raster)

# create path for output SWI file
before_swi_thresh_raster = r"memory\before_swi_thresh"

# save the SWI thresh raster
before_swi_thresh_calc.save(before_swi_thresh_raster)

# create a raster layer for the SWI threshold file so it can be viewed in the results map tab.
before_swi_threshold_layer = arcpy.MakeRasterLayer_management(before_swi_thresh_raster, 'before_swi_threshold')


# Step 5: calculate confidence raster 
# create water confidence raster
before_water_confidence_raster = create_water_confidence_raster(ndwi_threshold_raster=before_ndwi_thresh_raster,
                                                                swi_threshold_raster=before_swi_thresh_raster)

# create path for output water confidence matrix file
before_water_confidence_raster_path = r"memory\before_water_confidence_raster"

# save the water confidence matrix to a file in memory
before_water_confidence_raster.save(before_water_confidence_raster_path)

# create a raster layer for the NDWI threshold file so it can be viewed in the results map tab.
# before_water_confidence_layer = arcpy.MakeRasterLayer_management(before_water_confidence_raster, 'before_water_confidence_raster')

# Step 6: extract water pixels 
# create the remap value to set any pixels with the value of 1 to 0.
remap_value = RemapValue([[1, 0]])

# reclassify the water mask
before_water_mask_reclass = Reclassify(in_raster=before_water_confidence_raster_path,
                                       reclass_field="value",
                                       remap=remap_value)

# create path for output water mask file
before_water_mask_raster = r"memory\before_water_mask_high_confidence"

# save the water mask to
before_water_mask_reclass.save(before_water_mask_raster)

# Using raster objects, subtract the before water mask from the after water mask
flooded_area_calc = Raster(after_water_mask_reclass) - Raster(before_water_mask_reclass)

# Create a path for flooded_area_calc
flooded_area_calc_raster = r"memory\flooded_area_calc"

# Save the flooded_area_calc raster
flooded_area_calc.save(flooded_area_calc_raster)

# Reclassify the final flood area 

# Create the remap values lists
remap_value_final = RemapValue([[-2, "NoData"], [0, "NoData"]])

# Reclassify the water mask
flooded_area_final = Reclassify(in_raster=flooded_area_calc, 
                                reclass_field="value", 
                                remap=remap_value_final)

# Create path for output flooded area tif file
flooded_area_final_raster = os.path.join(final_output_folder, "Flooded_Area_Final_Raster.tif")

# Save the final flooded area to a tif file
flooded_area_final.save(flooded_area_final_raster)

# Create path for output flooded area polygon file
flooded_area_final_poly = os.path.join(final_output_folder, "Flooded_Area_Final_Poly.shp")

# Convert to polygon
arcpy.RasterToPolygon_conversion(in_raster=flooded_area_final, 
                                 out_polygon_features=flooded_area_final_poly, 
                                 simplify="NO_SIMPLIFY", 
                                 raster_field="Value")
'''
# Get the currently open ArcGIS Pro Project
aprx = arcpy.mp.ArcGISProject("current")
# Get the map
m = aprx.listMaps("Map")[0]
# Get a list of the layers on the map
thelyrs = m.listLayers()
# Check each layer to determine if it is a temporary, in memory layer, 
# and remove the layer if it is.
for lyr in thelyrs:
    print(lyr.dataSource)
    if "INSTANCE_ID=GPProMemoryWorkspace" in lyr.dataSource:
        print("Removing: ", lyr.name )
        m.removeLayer(lyr)
'''