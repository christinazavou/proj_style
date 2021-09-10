
Data ?= building_yu
ThisDir ?= /media/graphicslab/BigData/zavou/ANNFASS_CODE/proj_style
SampleAndHogExe ?= $(ThisDir)/sample_and_hog/cmake-build-debug/SampleAndHog
ConvolutionalExe ?= $(ThisDir)/convolutional/cmake-build-debug/Convolutional
BackProjectExe ?= $(ThisDir)/Back_projected/cmake-build-debug/BackProjected

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
# 		takes ~ 8 hours to process all views for 329 (building) models
#		      ~ 50 min                           30 (demo) models
step3:
	chmod 777 $(ConvolutionalExe) \
    		&& chmod 777 $(ThisDir)/data/$(Data)/* \
    		&& $(ConvolutionalExe) "$(ThisDir)/convolutional/configs/$(Data).yml"

#	runs "add_data_to_matrix"
#		creates pslf folder and stores the matrix VM (5*num_clusters, num_models) calculated in step3 into file input.mat
#	runs "make_label_split_data"
#		uses pectlabels
#		in case pectlables is 0.5 it will get half the data per each label
#		Y will be a one-hot-encoded matrix of e.g. half the models
#		G will be a matrix of all the models and their label
#	runs "run_kernel_filter" which calls the "pslf"
#		calculates in each iteration (default 10)
#			i.e. with 329 models, 12 views, 50 clusters, 4 labels:
#			Vr (490x329], U (12 x 250x50), Uless (12 x 250x50), V (12 x 50x239), Vless (12 x 50x239), W (490x4)
#			newY=W'*Vr (4x239) --> get labelc (329x1)
#			calculates purity of clustering
#			calculates ModelCla (??)
#			calculates newX (for each view we have arbitrary amount of features per model)
#
# 			(and so in the next iteration U has arbitrary amount of features x 50 per view)
# 	runs the "style_localization"
#		for each view: ...
#		outputs a file style_index.txt in folder style_patch, where it seems like each model has two of its
#		30 patches sampled initially picked as style-patches (probably the ones closer to clusters)
step4:
	cd $(ThisDir) \
		&& matlab -nodesktop -nosplash -r "Complete_run('$(Data)',0);exit"

#	reads the model obj file, and its accompanied seeds (of the 30 patches), and the style_index.txt created
#	in previous step, and colors the style patches and outputs all views..
#	takes ~10 min for 329 models
step5:
	chmod 777 $(BackProjectExe) \
    		&& chmod 777 $(ThisDir)/data/$(Data)/* \
    		&& $(BackProjectExe) "$(ThisDir)/Back_projected/configs/$(Data).yml"
