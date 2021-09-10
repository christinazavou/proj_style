
Data ?= building_yu
ThisDir ?= /media/graphicslab/BigData/zavou/ANNFASS_CODE/proj_style
SampleAndHogExe ?= $(ThisDir)/sample_and_hog/cmake-build-debug/SampleAndHog
ConvolutionalExe ?= $(ThisDir)/convolutional/cmake-build-debug/Convolutional

#build:
#	build sample_and_hog

# sample
#	creates folders under "patch" and off files under "sample_points"
# 	in every patch (.txt) file the HOG (900 dimension) of the patch is saved
# 	and it is accompanied with a .bmp file showing the patch
# 	creates up to 30 patches per mesh file ... takes ~2 hours for 329 buildings
step1:
	chmod 777 $(SampleAndHogExe) \
		&& chmod 777 $(ThisDir)/data/$(Data)/* \
		&& $(SampleAndHogExe) "sampling" "$(ThisDir)/sample_and_hog/configs/$(Data).yml"

# cluster
# 	runs the "run_CT":
#		creates folder "hog" which stores the V matrix for each view
#		V has maximum (num_of_models * num_of_patches) rows and hog_dimension columns
#		vector CT (of size num_of_models * num_of_patches) holds the patch indices or zero
#		if the patch is discarded (i.e. if the sum of HOG features is less than 25)
# 	runs the "run_cluster":
#		creates the folder "cluster"
#		loads V and CT of each view and creates 50 hog (k-means) clusters
#		note: if any cluster center has nans we replace it with zeros
#	runs the "run_cluster_idf":
#		creates folder "kernel"
#		each view will generate a directory containing one patch for each of its 50 clusters
#		accompanied with a file listing which cluster each patch represents
#		creates also the file kernelModel.mat which consists of one kernel matrix per view
#		each kernelMatrix is of size [num_clusters, num_models] and keeps the frequency of each patch-cluster per model
#	runs the "preCNN":
#		creates folder txt which stores the filenames of models per view-file
#		creates folder imagesnames which stores a file per view containing the .bmp of models per view
step2:
	cd $(ThisDir) \
		&& matlab -nodesktop -nosplash -r "Complete_run('$(Data)',1);exit"

# convolution
#	creates ".txt" files for each ".bmp" file in "3dlines" folder
#		uses again HOG calculation with same parameters (patch size 48, block size 16, block stride 8, n_bins 9==>dim 900)
#		each image (model) is representation by matrix VM with size (height-patch_size+1, width-patch_size+1, 900)
# 		i.e. stores a HOG for each possible patch (centered around each pixel, without padding)
#		then it basically uses max pooling to output 5 values per patch-kernel for each image, and outputs this
# 		(250 dim) representation in the .txt file
# 		takes ~ 8 hours to process one view for 329 (building) models
step3:
	chmod 777 $(ConvolutionalExe) \
    		&& chmod 777 $(ThisDir)/data/$(Data)/* \
    		&& $(ConvolutionalExe) "$(ThisDir)/convolutional/configs/$(Data).yml"


step4:
	cd $(ThisDir) \
		&& matlab -nodesktop -nosplash -r "Complete_run('$(Data)',0);exit"

