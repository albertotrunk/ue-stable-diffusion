# TODO custom hooks object for segmentation maps?
def augment_segmentation_map(self, segmentation_map, hooks=None):
    """
    Augment a single segmentation map.

    Parameters
    ----------
    segmentation_map : (H,W,C) ndarray or (H,W) ndarray
        The segmentation map to augment.
        Expected dtypes are integer-likes, e.g. int32.

    hooks : None or ia.HooksImages, optional(default=None)
        HooksImages object to dynamically interfere with the augmentation
        process.

    Returns
    -------
    out : ndarray
        The corresponding augmented segmentation maps.

    """
    assert segmentation_map.ndim in [2, 3], "Expected segmentation map to have shape (height, width, [channels]), got shape %s." % (segmentation_map.shape,)
    return self.augment_segmentation_maps([segmentation_map], hooks=hooks)[0]
    
# TODO custom hooks object for segmentation maps?
def augment_segmentation_maps(self, segmentation_map, parents=None, hooks=None):
    """
    Augment multiple segmentation maps.

    Parameters
    ----------
    segmentation_maps : (N,H,W,C) ndarray or (N,H,W) ndarray or list of (H,W,C) ndarray or list of (H,W) ndarray
        Segmentation maps to augment. The input can be a list of numpy arrays or
        a single array. Each segmentation map is expected to have
        shape (H, W, C) or (H, W), where H is the height, W is the width
        and C are the number of classes. Number of classes may differ
        between segmentation maps. If a list is chosen, height and width
        may differ per between images. Expected dtypes are integer-likes,
        e.g. int32.

    parents : None or list of Augmenter, optional(default=None)
        Parent augmenters that have previously been called before the
        call to this function. Usually you can leave this parameter as None.
        It is set automatically for child augmenters.

    hooks : None or ia.HooksImages, optional(default=None)
        HooksImages object to dynamically interfere with the augmentation
        process.

    Returns
    -------
    result : ndarray or list
        Corresponding augmented segmentation maps.

    """
    if self.deterministic:
        state_orig = self.random_state.get_state()

    if parents is None:
        parents = []

    if hooks is None:
        hooks = ia.HooksImages()

    if ia.is_np_array(segmentation_maps):
        input_type = "array"
        input_added_axis = False

        assert segmentation_maps.ndim in [3, 4], "Expected 3d/4d array of form (N, height, width) or (N, height, width, classes), got shape %s." % (images.shape,)

        # copy the input, we don't want to augment it in-place
        smaps_copy = np.copy(segmentation_maps)

        if smaps_copy.ndim == 3 and smaps_copy.shape[-1] <= 5:
            warnings.warn(
                "You provided a numpy array of shape %s as input to augment_segmentation_maps(), "
                "which was interpreted as (N, H, W). The last dimension however has "
                "a value <=5, which indicates that you provided a single map "
                "with shape (H, W, C) instead. If that is the case, you should use "
                "augment_segmentation_map(map) or augment_segmentation_maps([map]), otherwise "
                "you will not get the expected augmentations." % (smaps_copy.shape,)
            )

        # for 2D input images (i.e. shape (N, H, W)), we add a channel axis (i.e. (N, H, W, 1)),
        # so that all augmenters can rely on the input having a channel axis and
        # don't have to add if/else statements for 2D images
        if smaps_copy.ndim == 3:
            smaps_copy = smaps_copy[..., np.newaxis]
            input_added_axis = True
    elif ia.is_iterable(segmentation_maps):
        input_type = "list"
        input_added_axis = []

        if len(segmentation_maps) == 0:
            smaps_copy = []
        else:
            assert all(segmentation_maps.ndim in [2, 3] for smap in segmentation_maps), "Expected list of segmentation maps with each map having shape (height, width) or (height, width, classes), got shapes %s." % ([smap.shape for smap in segmentation_maps],)

            # copy images and add channel axis for 2D images (see above,
            # as for list inputs each image can have different shape, it
            # is done here on a per images basis)
            smaps_copy = []
            input_added_axis = []
            for smap in segmentation_maps:
                smap_copy = np.copy(smap)
                if smap.ndim == 2:
                    smap_copy = smap_copy[:, :, np.newaxis]
                    input_added_axis.append(True)
                else:
                    input_added_axis.append(False)
                smaps_copy.append(smap_copy)
    else:
        raise Exception("Expected segmentation maps as one numpy array or list/tuple of numpy arrays, got %s." % (type(segmentation_maps),))

    smaps_copy = hooks.preprocess(smaps_copy, augmenter=self, parents=parents)

    #if ia.is_np_array(images) != ia.is_np_array(images_copy):
    #    print("[WARNING] images vs images_copy", ia.is_np_array(images), ia.is_np_array(images_copy))
    #if ia.is_np_array(images):
        #assert images.shape[0] > 0, images.shape
    #    print("images.shape", images.shape)
    #if ia.is_np_array(images_copy):
    #    print("images_copy.shape", images_copy.shape)

    # the is_activated() call allows to use hooks that selectively
    # deactivate specific augmenters in previously defined augmentation
    # sequences
    if hooks.is_activated(smaps_copy, augmenter=self, parents=parents, default=self.activated):
        if len(smaps_copy) > 0:
            result = self._augment_segmentation_maps(
                smaps_copy,
                random_state=ia.copy_random_state(self.random_state),
                parents=parents,
                hooks=hooks
            )
            # move "forward" the random state, so that the next call to
            # augment_images() will use different random values
            ia.forward_random_state(self.random_state)
        else:
            result = smaps_copy
    else:
        result = smaps_copy

    result = hooks.postprocess(result, augmenter=self, parents=parents)

    # remove temporarily added channel axis for 2D input images
    if input_type == "array":
        if input_added_axis == True:
            result = np.squeeze(result, axis=3)
    if input_type == "list":
        for i in sm.xrange(len(result)):
            if input_added_axis[i] == True:
                result[i] = np.squeeze(result[i], axis=2)

    if self.deterministic:
        self.random_state.set_state(state_orig)

    return result

def _augment_segmentation_maps(self, segmentation_maps, random_state, parents, hooks):
    """
    Augment multiple segmentation maps.

    This is the internal variation of `augment_segmentation_maps()`.
    It is called from `augment_segmentation_maps()` and should usually not
    be called directly.
    It has to be implemented by every augmenter.
    This method may transform the segmentation maps in-place.
    This method does not have to care about determinism or the
    Augmenter instance's `random_state` variable. The parameter
    `random_state` takes care of both of these.

    Parameters
    ----------
    segmentation_maps : (N,H,W,C) ndarray or list of (H,W,C) ndarray
        Segmentation maps to augment.
        They may be changed in-place.
        Either a list of (H, W, C) arrays or a single (N, H, W, C) array,
        where N = number of images, H = height of images, W = width of
        images, C = number of classes.
        In the case of a list as input, H, W and C may change per image.

    random_state : np.random.RandomState
        The random state to use for all sampling tasks during the
        augmentation.

    parents : list of Augmenter
        See augment_images().

    hooks : ia.HooksImages
        See augment_images().

    Returns
    ----------
    images : (N,H,W,C) ndarray or list of (H,W,C) ndarray
        The augmented segmentation maps.

    """
    # default behaviour is to apply no changes to the maps
    return segmentation_maps
