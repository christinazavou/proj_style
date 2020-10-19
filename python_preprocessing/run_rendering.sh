#!/bin/bash

DATADIR="/media/christina/Data/ANNFASS_data/buildnet"
RENDERDIR="/media/christina/Data/ANNFASS_data/blender_render"
FILENAME='RESIDENTIALvilla_mesh3265Marios.ply'
blender \
  --background \
  --python MultiCamerasRender.py -- \
  --datadir ${DATADIR} \
  --renderdir ${RENDERDIR} \
  --filename ${FILENAME}
