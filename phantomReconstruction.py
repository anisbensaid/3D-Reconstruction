import numpy as np
from scipy import misc
 
import astra
 
# Create phantom.
phantom = np.zeros((128, 128))
phantom[32 : 64, 32 : 64] = np.ones((32, 32))
phantom[64 : 96, 64 : 96] = np.ones((32, 32))
misc.imsave('phantom.png', phantom)
 
# Create geometries and projector.
vol_geom = astra.create_vol_geom(128, 128)
angles = np.linspace(0, np.pi, 180, endpoint=False)
proj_geom = astra.create_proj_geom('parallel', 1., 128, angles)
projector_id = astra.create_projector('linear', proj_geom, vol_geom)
 
# Create sinogram.
sinogram_id, sinogram = astra.create_sino(phantom, projector_id)
misc.imsave('sinogram.png', sinogram)
 
# Create reconstruction.
reconstruction_id = astra.data2d.create('-vol', vol_geom)
cfg = astra.astra_dict('SIRT')
cfg['ReconstructionDataId'] = reconstruction_id
cfg['ProjectionDataId'] = sinogram_id
cfg['ProjectorId'] = projector_id
cfg['option'] = {}
cfg['option']['MinConstraint'] = 0.  # Force solution to be nonnegative.
algorithm_id = astra.algorithm.create(cfg)
astra.algorithm.run(algorithm_id, 100)  # 100 iterations.
reconstruction = astra.data2d.get(reconstruction_id)
misc.imsave('reconstruction.png', reconstruction)
 
# Cleanup.
astra.algorithm.delete(algorithm_id)
astra.data2d.delete(reconstruction_id)
astra.data2d.delete(sinogram_id)
astra.projector.delete(projector_id)
