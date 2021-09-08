
Data ?= building_yu
ThisDir ?= /media/graphicslab/BigData/zavou/ANNFASS_CODE/proj_style
SampleAndHogExe ?= $(ThisDir)/sample_and_hog/cmake-build-debug/SampleAndHog

# sample
#(creates folders under "patch" and off files under "sample_points"
# in every patch (.txt) file the HOG (900 dimension) of the patch is saved
step1:
	chmod 777 $(SampleAndHogExe) \
		&& chmod 777 $(ThisDir)/data/$(Data)/* \
		&& $(SampleAndHogExe) "sampling" "$(ThisDir)/sample_and_hog/configs/$(Data).yml"

# cluster
# runs the "run_CT":
#	  creates folder "hog" which stores the V matrix for each view
# runs the "run_cluster":
#     creates the folder "cluster" : FIXME: empty V so cant run kmeans
step2:
	cd $(ThisDir) \
		&& matlab -nodesktop -nosplash -r "Complete_run('$(Data)',1);exit"
