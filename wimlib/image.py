# from wimlib import _backend, WIMError, WIMFile

# class WIMImage(object):
# 	def __init__(self, wim, index=0):
# 		self._wim_struct = wim._wim_struct if type(wim) is WIMFile else wim
# 		self.index = index

# 		# If we have a index this is not a new image
# 		if self.index:
# 			pass

# 	def get_property(self, property_name):
# 		value = _backend.lib.wimlib_get_image_property(self._wim_struct, self.index, property_name)
# 		if value == _backend.ffi.NULL:
# 			return None
# 		return value

# 	def set_property(self, property_name, value):
# 		ret = _backend.lib.wimlib_set_propery_name(self._wim_struct, self.index, property_name, value)
# 		if ret:
# 			raise WIMError(ret)

# 	@property
# 	def name(self):
# 		value = _backend.lib.wimlib_get_image_name(self._wim_struct, self.index) 
# 		if value == _backend.ffi.NULL:
# 			return None
# 		return value

# 	@name.setter
# 	def name(self, name):
# 		ret = _backend.lib.wimlib_set_image_name(self._wim_struct, self.index, name)
# 		if ret:
# 			raise WIMError(ret)

# 	@property
# 	def description(self):
# 		value = _backend.lib.wimlib_get_image_description(self._wim_struct, self.index) 
# 		if value == _backend.ffi.NULL:
# 			return None
# 		return value

# 	@description.setter
# 	def description(self, descripion):
# 		ret = _backend.lib.wimlib_set_image_descripion(self._wim_struct, self.index, descripion)
# 		if ret:
# 			raise WIMError(ret)


# 	def rename_path(self, source_path, dest_path):
# 		pass

# 	def delete_path(self, path, flags):
# 		pass

# 	def add_tree(sefl, source, target, flags):
# 		pass

# 	def export(self, dest_wim, desc_name=None, dest_desciption=None, flags=None):
# 		pass

# 	def update(self, commands, flags):
# 		""" Update an image using commands """
# 		pass

# 	def set_flags(self, flags):
# 		pass


	


	
	
