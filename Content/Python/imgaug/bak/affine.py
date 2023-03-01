class AbstractAffine(Augmenter):
    def __init__(self):
        super(AbstractAffine, self).__init__(name=name, deterministic=deterministic, random_state=random_state)

        self.scale = self._process_scale_param()

    def _process_scale_param(self, scale):
        # scale
        # float | (float, float) | [float, float] | StochasticParameter
        def scale_handle_param(param, allow_dict):
            if isinstance(param, StochasticParameter):
                return param
            elif ia.is_single_number(param):
                assert param > 0.0, "Expected scale to have range (0, inf), got value %.4f. Note: The value to _not_ change the scale of images is 1.0, not 0.0." % (param,)
                return Deterministic(param)
            elif ia.is_iterable(param) and not isinstance(param, dict):
                assert len(param) == 2, "Expected scale tuple/list with 2 entries, got %d entries." % (len(param),)
                assert param[0] > 0.0 and param[1] > 0.0, "Expected scale tuple/list to have values in range (0, inf), got values %.4f and %.4f. Note: The value to _not_ change the scale of images is 1.0, not 0.0." % (param[0], param[1])
                return Uniform(param[0], param[1])
            elif allow_dict and isinstance(param, dict):
                assert "x" in param or "y" in param
                x = param.get("x")
                y = param.get("y")

                x = x if x is not None else 1.0
                y = y if y is not None else 1.0

                return (scale_handle_param(x, False), scale_handle_param(y, False))
            else:
                raise Exception("Expected float, int, tuple/list with 2 entries or StochasticParameter. Got %s." % (type(param),))
        return scale_handle_param(scale, True)

    def _process_translate_param(self, translate_percent, translate_px):
        # translate
        if translate_percent is None and translate_px is None:
            translate_px = 0

        assert translate_percent is None or translate_px is None

        if translate_percent is not None:
            # translate by percent
            def translate_handle_param(param, allow_dict):
                if ia.is_single_number(param):
                    return Deterministic(float(param))
                elif ia.is_iterable(param) and not isinstance(param, dict):
                    assert len(param) == 2, "Expected translate_percent tuple/list with 2 entries, got %d entries." % (len(param),)
                    all_numbers = all([ia.is_single_number(p) for p in param])
                    assert all_numbers, "Expected translate_percent tuple/list to contain only numbers, got types %s." % (str([type(p) for p in param]),)
                    #assert param[0] > 0.0 and param[1] > 0.0, "Expected translate_percent tuple/list to have values in range (0, inf), got values %.4f and %.4f." % (param[0], param[1])
                    return Uniform(param[0], param[1])
                elif allow_dict and isinstance(param, dict):
                    assert "x" in param or "y" in param
                    x = param.get("x")
                    y = param.get("y")

                    x = x if x is not None else 0
                    y = y if y is not None else 0

                    return (translate_handle_param(x, False), translate_handle_param(y, False))
                elif isinstance(param, StochasticParameter):
                    return param
                else:
                    raise Exception("Expected float, int or tuple/list with 2 entries of both floats or ints or StochasticParameter. Got %s." % (type(param),))
            translate = translate_handle_param(translate_percent, True)
        else:
            # translate by pixels
            def translate_handle_param(param, allow_dict):
                if ia.is_single_integer(param):
                    return Deterministic(param)
                elif ia.is_iterable(param) and not isinstance(param, dict):
                    assert len(param) == 2, "Expected translate_px tuple/list with 2 entries, got %d entries." % (len(param),)
                    all_integer = all([ia.is_single_integer(p) for p in param])
                    assert all_integer, "Expected translate_px tuple/list to contain only integers, got types %s." % (str([type(p) for p in param]),)
                    return DiscreteUniform(param[0], param[1])
                elif allow_dict and isinstance(param, dict):
                    assert "x" in param or "y" in param
                    x = param.get("x")
                    y = param.get("y")

                    x = x if x is not None else 0
                    y = y if y is not None else 0

                    return (translate_handle_param(x, False), translate_handle_param(y, False))
                elif isinstance(param, StochasticParameter):
                    return param
                else:
                    raise Exception("Expected int or tuple/list with 2 ints or StochasticParameter. Got %s." % (type(param),))
            translate = translate_handle_param(translate_px, True)

        return translate

    def _process_rotate_param(self, rotate):
        # StochasticParameter | float | int | (float or int, float or int) | [float or int, float or int]
        if isinstance(rotate, StochasticParameter):
            return rotate
        elif ia.is_single_number(rotate):
            return Deterministic(rotate)
        elif ia.is_iterable(rotate):
            assert len(rotate) == 2, "Expected rotate tuple/list with 2 entries, got %d entries." % (len(rotate),)
            assert all([ia.is_single_number(val) for val in rotate]), "Expected floats/ints in rotate tuple/list"
            return Uniform(rotate[0], rotate[1])
        else:
            raise Exception("Expected float, int, tuple/list with 2 entries or StochasticParameter. Got %s." % (type(rotate),))

    def _process_shear_param(self, shear):
        # StochasticParameter | float | int | (float or int, float or int) | [float or int, float or int]
        if isinstance(shear, StochasticParameter):
            return shear = shear
        elif ia.is_single_number(shear):
            return shear = Deterministic(shear)
        elif ia.is_iterable(shear):
            assert len(shear) == 2, "Expected rotate tuple/list with 2 entries, got %d entries." % (len(shear),)
            assert all([ia.is_single_number(val) for val in shear]), "Expected floats/ints in shear tuple/list."
            return shear = Uniform(shear[0], shear[1])
        else:
            raise Exception("Expected float, int, tuple/list with 2 entries or StochasticParameter. Got %s." % (type(shear),))

    def _augment_keypoints(self, keypoints_on_images, random_state, parents, hooks):
        result = []
        nb_images = len(keypoints_on_images)
        scale_samples, translate_samples, rotate_samples, shear_samples, cval_samples, mode_samples, order_samples = self._draw_samples(nb_images, random_state)

        for i, keypoints_on_image in enumerate(keypoints_on_images):
            height, width = keypoints_on_image.height, keypoints_on_image.width
            shift_x = width / 2.0 - 0.5
            shift_y = height / 2.0 - 0.5
            scale_x, scale_y = scale_samples[0][i], scale_samples[1][i]
            translate_x, translate_y = translate_samples[0][i], translate_samples[1][i]
            #assert isinstance(translate_x, (float, int))
            #assert isinstance(translate_y, (float, int))
            if ia.is_single_float(translate_y):
                translate_y_px = int(round(translate_y * keypoints_on_image.shape[0]))
            else:
                translate_y_px = translate_y
            if ia.is_single_float(translate_x):
                translate_x_px = int(round(translate_x * keypoints_on_image.shape[1]))
            else:
                translate_x_px = translate_x
            rotate = rotate_samples[i]
            shear = shear_samples[i]
            #cval = cval_samples[i]
            #mode = mode_samples[i]
            #order = order_samples[i]
            if scale_x != 1.0 or scale_y != 1.0 or translate_x_px != 0 or translate_y_px != 0 or rotate != 0 or shear != 0:
                matrix_to_topleft = tf.SimilarityTransform(translation=[-shift_x, -shift_y])
                matrix_transforms = tf.AffineTransform(
                    scale=(scale_x, scale_y),
                    translation=(translate_x_px, translate_y_px),
                    rotation=math.radians(rotate),
                    shear=math.radians(shear)
                )
                matrix_to_center = tf.SimilarityTransform(translation=[shift_x, shift_y])
                matrix = (matrix_to_topleft + matrix_transforms + matrix_to_center)

                coords = keypoints_on_image.get_coords_array()
                #print("coords", coords)
                #print("matrix", matrix.params)
                coords_aug = tf.matrix_transform(coords, matrix.params)
                #print("coords before", coords)
                #print("coordsa ftre", coords_aug, np.around(coords_aug).astype(np.int32))
                result.append(ia.KeypointsOnImage.from_coords_array(np.around(coords_aug).astype(np.int32), shape=keypoints_on_image.shape))
            else:
                result.append(keypoints_on_image)
        return result

    def _sample_affine_parameters(self, nb_samples, seed):
        if isinstance(self.scale, tuple):
            scale_samples = (
                self.scale[0].draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 10)),
                self.scale[1].draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 20)),
            )
        else:
            scale_samples = self.scale.draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 30))
            scale_samples = (scale_samples, scale_samples)

        if isinstance(self.translate, tuple):
            translate_samples = (
                self.translate[0].draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 40)),
                self.translate[1].draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 50)),
            )
        else:
            translate_samples = self.translate.draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 60))
            translate_samples = (translate_samples, translate_samples)

        assert translate_samples[0].dtype in [np.int32, np.int64, np.float32, np.float64]
        assert translate_samples[1].dtype in [np.int32, np.int64, np.float32, np.float64]

        rotate_samples = self.rotate.draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 70))
        shear_samples = self.shear.draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 80))

        return scale_samples, translate_samples, rotate_samples, shear_samples

    def _draw_samples(self, nb_samples, random_state, nb_cval_values=None):
        seed = random_state.randint(0, 10**6, 1)[0]

        if isinstance(self.scale, tuple):
            scale_samples = (
                self.scale[0].draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 10)),
                self.scale[1].draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 20)),
            )
        else:
            scale_samples = self.scale.draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 30))
            scale_samples = (scale_samples, scale_samples)

        if isinstance(self.translate, tuple):
            translate_samples = (
                self.translate[0].draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 40)),
                self.translate[1].draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 50)),
            )
        else:
            translate_samples = self.translate.draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 60))
            translate_samples = (translate_samples, translate_samples)

        assert translate_samples[0].dtype in [np.int32, np.int64, np.float32, np.float64]
        assert translate_samples[1].dtype in [np.int32, np.int64, np.float32, np.float64]

        rotate_samples = self.rotate.draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 70))
        shear_samples = self.shear.draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 80))

        cval_samples = self.cval.draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 90))
        mode_samples = self.mode.draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 100))
        order_samples = self.order.draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 110))

        return scale_samples, translate_samples, rotate_samples, shear_samples, cval_samples, mode_samples, order_samples

class AffineSkimage(Augmenter):
    """
    Augmenter to apply affine transformations to images.

    This is mostly a wrapper around skimage's AffineTransform class and
    warp function.

    Affine transformations
    involve:
        - Translation ("move" image on the x-/y-axis)
        - Rotation
        - Scaling ("zoom" in/out)
        - Shear (move one side of the image, turning a square into a trapezoid)

    All such transformations can create "new" pixels in the image without a
    defined content, e.g. if the image is translated to the left, pixels
    are created on the right.
    A method has to be defined to deal with these pixel values. The
    parameters `cval` and `mode` of this class deal with this.

    Some transformations involve interpolations between several pixels
    of the input image to generate output pixel values. The parameter `order`
    deals with the method of interpolation used for this.

    Parameters
    ----------
    scale : float or tuple of two floats or StochasticParameter or dict {"x": float/tuple/StochasticParameter, "y": float/tuple/StochasticParameter}, optional(default=1.0)
        Scaling factor to use, where 1.0 represents no change and 0.5 is
        zoomed out to 50 percent of the original size.
            * If a single float, then that value will be used for all images.
            * If a tuple (a, b), then a value will be sampled from the range
              a <= x <= b per image. That value will be used identically for
              both x- and y-axis.
            * If a StochasticParameter, then from that parameter a value will
              be sampled per image (again, used for both x- and y-axis).
            * If a dictionary, then it is expected to have the keys "x" and/or "y".
              Each of these keys can have the same values as described before
              for this whole parameter (`scale`). Using a dictionary allows to
              set different values for the axis. If they are set to the same
              ranges, different values may still be sampled per axis.

    translate_percent : float or tuple of two floats or StochasticParameter or dict {"x": float/tuple/StochasticParameter, "y": float/tuple/StochasticParameter}, optional(default=1.0)
        Translation in percent relative to the image
        height/width (x-translation, y-translation) to use,
        where 0 represents no change and 0.5 is half of the image
        height/width.
            * If a single float, then that value will be used for all images.
            * If a tuple (a, b), then a value will be sampled from the range
              a <= x <= b per image. That percent value will be used identically
              for both x- and y-axis.
            * If a StochasticParameter, then from that parameter a value will
              be sampled per image (again, used for both x- and y-axis).
            * If a dictionary, then it is expected to have the keys "x" and/or "y".
              Each of these keys can have the same values as described before
              for this whole parameter (`translate_percent`).
              Using a dictionary allows to set different values for the axis.
              If they are set to the same ranges, different values may still
              be sampled per axis.

    translate_px : int or tuple of two ints or StochasticParameter or dict {"x": int/tuple/StochasticParameter, "y": int/tuple/StochasticParameter}, optional(default=1.0)
        Translation in
        pixels.
            * If a single int, then that value will be used for all images.
            * If a tuple (a, b), then a value will be sampled from the discrete
              range [a .. b] per image. That number will be used identically
              for both x- and y-axis.
            * If a StochasticParameter, then from that parameter a value will
              be sampled per image (again, used for both x- and y-axis).
            * If a dictionary, then it is expected to have the keys "x" and/or "y".
              Each of these keys can have the same values as described before
              for this whole parameter (`translate_px`).
              Using a dictionary allows to set different values for the axis.
              If they are set to the same ranges, different values may still
              be sampled per axis.

    rotate : float or int or tuple of two floats/ints or StochasticParameter, optional(default=0)
        Rotation in degrees (NOT radians), i.e. expected value range is
        0 to 360 for positive rotations (may also be negative).
            * If a float/int, then that value will be used for all images.
            * If a tuple (a, b), then a value will be sampled per image from the
              range a <= x <= b and be used as the rotation value.
            * If a StochasticParameter, then this parameter will be used to
              sample the rotation value per image.

    shear : float or int or tuple of two floats/ints or StochasticParameter, optional(default=0)
        Shear in degrees (NOT radians), i.e. expected value range is
        0 to 360 for positive shear (may also be negative).
            * If a float/int, then that value will be used for all images.
            * If a tuple (a, b), then a value will be sampled per image from the
              range a <= x <= b and be used as the rotation value.
            * If a StochasticParameter, then this parameter will be used to
              sample the shear value per image.

    order : int or iterable of int or ia.ALL or StochasticParameter, optional(default=1)
        Interpolation order to use. Same meaning as in
        skimage:
            * 0: Nearest-neighbor
            * 1: Bi-linear (default)
            * 2: Bi-quadratic (not recommended by skimage)
            * 3: Bi-cubic
            * 4: Bi-quartic
            * 5: Bi-quintic
        Method 0 and 1 are fast, 3 is a bit slower, 4 and 5 are very
        slow.
            * If a single int, then that order will be used for all images.
            * If an iterable, then for each image a random value will be sampled
              from that iterable (i.e. list of allowed order values).
            * If ia.ALL, then equivalant to list [0, 1, 3, 4, 5].
            * If StochasticParameter, then that parameter is queried per image
              to sample the order value to use.

    cval : number or tuple of two number or ia.ALL or StochasticParameter, optional(default=0)
        The constant value used for skimage's transform function.
        This is the value used to fill up pixels in the result image that
        didn't exist in the input image (e.g. when translating to the left,
        some new pixels are created at the right). Such a fill-up with a
        constant value only happens, when `mode` is "constant".
        For standard uint8 images (value range 0-255), this value may also
        come from the range 0-255. It may be a float value, even for
        integer image dtypes.
            * If this is a single int or float, then that value will be used
              (e.g. 0 results in black pixels).
            * If a tuple (a, b), then a random value from the range a <= x <= b
              is picked per image.
            * If ia.ALL, a value from the discrete range [0 .. 255] will be
              sampled per image.
            * If a StochasticParameter, a new value will be sampled from the
              parameter per image.

    mode : string or list of string or ia.ALL or StochasticParameter, optional(default="constant")
        Parameter that defines the handling of newly created pixels.
        Same meaning as in skimage (and numpy.pad):
            * "constant": Pads with a constant value
            * "edge": Pads with the edge values of array
            * "symmetric": Pads with the reflection of the vector mirrored
              along the edge of the array.
            * "reflect": Pads with the reflection of the vector mirrored on
              the first and last values of the vector along each axis.
            * "wrap": Pads with the wrap of the vector along the axis.
              The first values are used to pad the end and the end values
              are used to pad the beginning.
        The datatype of the parameter may
        be:
            * If a single string, then that mode will be used for all images.
            * If a list of strings, then per image a random mode will be picked
              from that list.
            * If ia.ALL, then a random mode from all possible modes will be
              picked.
            * If StochasticParameter, then the mode will be sampled from that
              parameter per image, i.e. it must return only the above mentioned
              strings.

    name : string, optional(default=None)
        See `Augmenter.__init__()`

    deterministic : bool, optional(default=False)
        See `Augmenter.__init__()`

    random_state : int or np.random.RandomState or None, optional(default=None)
        See `Augmenter.__init__()`

    Examples
    --------
    >>> aug = iaa.Affine(scale=2.0)

    zooms all images by a factor of 2.

    >>> aug = iaa.Affine(translate_px=16)

    translates all images on the x- and y-axis by 16 pixels (to the
    right/top), fills up any new pixels with zero (black values).

    >>> aug = iaa.Affine(translate_percent=0.1)

    translates all images on the x- and y-axis by 10 percent of their
    width/height (to the right/top), fills up any new pixels with zero
    (black values).

    >>> aug = iaa.Affine(rotate=35)

    rotates all images by 35 degrees, fills up any new pixels with zero
    (black values).

    >>> aug = iaa.Affine(shear=15)

    rotates all images by 15 degrees, fills up any new pixels with zero
    (black values).

    >>> aug = iaa.Affine(translate_px=(-16, 16))

    translates all images on the x- and y-axis by a random value
    between -16 and 16 pixels (to the right/top) (same for both axis, i.e.
    sampled once per image), fills up any new pixels with zero (black values).

    >>> aug = iaa.Affine(translate_px={"x": (-16, 16), "y": (-4, 4)})

    translates all images on the x-axis by a random value
    between -16 and 16 pixels (to the right) and on the y-axis by a
    random value between -4 and 4 pixels to the top. Even if both ranges
    were the same, both axis could use different samples.
    Fills up any new pixels with zero (black values).

    >>> aug = iaa.Affine(scale=2.0, order=[0, 1])

    same as previously, but uses (randomly) either nearest neighbour
    interpolation or linear interpolation.

    >>> aug = iaa.Affine(translate_px=16, cval=(0, 255))

    same as previously, but fills up any new pixels with a random
    brightness (same for the whole image).

    >>> aug = iaa.Affine(translate_px=16, mode=["constant", "edge"])

    same as previously, but fills up the new pixels in only 50 percent
    of all images with black values. In the other 50 percent of all cases,
    the value of the nearest edge is used.

    """

    def __init__(self, scale=1.0, translate_percent=None, translate_px=None,
                 rotate=0.0, shear=0.0, order=1, cval=0, mode="constant",
                 name=None, deterministic=False, random_state=None):
        super(Affine, self).__init__(name=name, deterministic=deterministic, random_state=random_state)

        # Peformance:
        #  1.0x order 0
        #  1.5x order 1
        #  3.0x order 3
        # 30.0x order 4
        # 60.0x order 5
        # measurement based on 256x256x3 batches, difference is smaller
        # on smaller images (seems to grow more like exponentially with image
        # size)
        if order == ia.ALL:
            # self.order = DiscreteUniform(0, 5)
            self.order = Choice([0, 1, 3, 4, 5]) # dont use order=2 (bi-quadratic) because that is apparently currently not recommended (and throws a warning)
        elif ia.is_single_integer(order):
            assert 0 <= order <= 5, "Expected order's integer value to be in range 0 <= x <= 5, got %d." % (order,)
            self.order = Deterministic(order)
        elif isinstance(order, list):
            assert all([ia.is_single_integer(val) for val in order]), "Expected order list to only contain integers, got types %s." % (str([type(val) for val in order]),)
            assert all([0 <= val <= 5 for val in order]), "Expected all of order's integer values to be in range 0 <= x <= 5, got %s." % (str(order),)
            self.order = Choice(order)
        elif isinstance(order, StochasticParameter):
            self.order = order
        else:
            raise Exception("Expected order to be imgaug.ALL, int, list of int or StochasticParameter, got %s." % (type(order),))

        if cval == ia.ALL:
            self.cval = DiscreteUniform(0, 255)
        elif ia.is_single_number(cval):
            self.cval = Deterministic(cval)
        elif ia.is_iterable(cval):
            assert len(cval) == 2
            assert 0 <= cval[0] <= 255
            assert 0 <= cval[1] <= 255
            self.cval = Uniform(cval[0], cval[1])
        elif isinstance(cval, StochasticParameter):
            self.cval = cval
        else:
            raise Exception("Expected cval to be imgaug.ALL, int, float or StochasticParameter, got %s." % (type(cval),))

        # constant, edge, symmetric, reflect, wrap
        if mode == ia.ALL:
            self.mode = Choice(["constant", "edge", "symmetric", "reflect", "wrap"])
        elif ia.is_string(mode):
            self.mode = Deterministic(mode)
        elif isinstance(mode, list):
            assert all([ia.is_string(val) for val in mode])
            self.mode = Choice(mode)
        elif isinstance(mode, StochasticParameter):
            self.mode = mode
        else:
            raise Exception("Expected mode to be imgaug.ALL, a string, a list of strings or StochasticParameter, got %s." % (type(mode),))

        # scale
        # float | (float, float) | [float, float] | StochasticParameter
        def scale_handle_param(param, allow_dict):
            if isinstance(param, StochasticParameter):
                return param
            elif ia.is_single_number(param):
                assert param > 0.0, "Expected scale to have range (0, inf), got value %.4f. Note: The value to _not_ change the scale of images is 1.0, not 0.0." % (param,)
                return Deterministic(param)
            elif ia.is_iterable(param) and not isinstance(param, dict):
                assert len(param) == 2, "Expected scale tuple/list with 2 entries, got %d entries." % (len(param),)
                assert param[0] > 0.0 and param[1] > 0.0, "Expected scale tuple/list to have values in range (0, inf), got values %.4f and %.4f. Note: The value to _not_ change the scale of images is 1.0, not 0.0." % (param[0], param[1])
                return Uniform(param[0], param[1])
            elif allow_dict and isinstance(param, dict):
                assert "x" in param or "y" in param
                x = param.get("x")
                y = param.get("y")

                x = x if x is not None else 1.0
                y = y if y is not None else 1.0

                return (scale_handle_param(x, False), scale_handle_param(y, False))
            else:
                raise Exception("Expected float, int, tuple/list with 2 entries or StochasticParameter. Got %s." % (type(param),))
        self.scale = scale_handle_param(scale, True)

        # translate
        if translate_percent is None and translate_px is None:
            translate_px = 0

        assert translate_percent is None or translate_px is None

        if translate_percent is not None:
            # translate by percent
            def translate_handle_param(param, allow_dict):
                if ia.is_single_number(param):
                    return Deterministic(float(param))
                elif ia.is_iterable(param) and not isinstance(param, dict):
                    assert len(param) == 2, "Expected translate_percent tuple/list with 2 entries, got %d entries." % (len(param),)
                    all_numbers = all([ia.is_single_number(p) for p in param])
                    assert all_numbers, "Expected translate_percent tuple/list to contain only numbers, got types %s." % (str([type(p) for p in param]),)
                    #assert param[0] > 0.0 and param[1] > 0.0, "Expected translate_percent tuple/list to have values in range (0, inf), got values %.4f and %.4f." % (param[0], param[1])
                    return Uniform(param[0], param[1])
                elif allow_dict and isinstance(param, dict):
                    assert "x" in param or "y" in param
                    x = param.get("x")
                    y = param.get("y")

                    x = x if x is not None else 0
                    y = y if y is not None else 0

                    return (translate_handle_param(x, False), translate_handle_param(y, False))
                elif isinstance(param, StochasticParameter):
                    return param
                else:
                    raise Exception("Expected float, int or tuple/list with 2 entries of both floats or ints or StochasticParameter. Got %s." % (type(param),))
            self.translate = translate_handle_param(translate_percent, True)
        else:
            # translate by pixels
            def translate_handle_param(param, allow_dict):
                if ia.is_single_integer(param):
                    return Deterministic(param)
                elif ia.is_iterable(param) and not isinstance(param, dict):
                    assert len(param) == 2, "Expected translate_px tuple/list with 2 entries, got %d entries." % (len(param),)
                    all_integer = all([ia.is_single_integer(p) for p in param])
                    assert all_integer, "Expected translate_px tuple/list to contain only integers, got types %s." % (str([type(p) for p in param]),)
                    return DiscreteUniform(param[0], param[1])
                elif allow_dict and isinstance(param, dict):
                    assert "x" in param or "y" in param
                    x = param.get("x")
                    y = param.get("y")

                    x = x if x is not None else 0
                    y = y if y is not None else 0

                    return (translate_handle_param(x, False), translate_handle_param(y, False))
                elif isinstance(param, StochasticParameter):
                    return param
                else:
                    raise Exception("Expected int or tuple/list with 2 ints or StochasticParameter. Got %s." % (type(param),))
            self.translate = translate_handle_param(translate_px, True)

        # rotate
        # StochasticParameter | float | int | (float or int, float or int) | [float or int, float or int]
        if isinstance(rotate, StochasticParameter):
            self.rotate = rotate
        elif ia.is_single_number(rotate):
            self.rotate = Deterministic(rotate)
        elif ia.is_iterable(rotate):
            assert len(rotate) == 2, "Expected rotate tuple/list with 2 entries, got %d entries." % (len(rotate),)
            assert all([ia.is_single_number(val) for val in rotate]), "Expected floats/ints in rotate tuple/list"
            self.rotate = Uniform(rotate[0], rotate[1])
        else:
            raise Exception("Expected float, int, tuple/list with 2 entries or StochasticParameter. Got %s." % (type(rotate),))

        # shear
        # StochasticParameter | float | int | (float or int, float or int) | [float or int, float or int]
        if isinstance(shear, StochasticParameter):
            self.shear = shear
        elif ia.is_single_number(shear):
            self.shear = Deterministic(shear)
        elif ia.is_iterable(shear):
            assert len(shear) == 2, "Expected rotate tuple/list with 2 entries, got %d entries." % (len(shear),)
            assert all([ia.is_single_number(val) for val in shear]), "Expected floats/ints in shear tuple/list."
            self.shear = Uniform(shear[0], shear[1])
        else:
            raise Exception("Expected float, int, tuple/list with 2 entries or StochasticParameter. Got %s." % (type(shear),))

    def _augment_images(self, images, random_state, parents, hooks):
        #images = images if isinstance(images, list) else [images]
        nb_images = len(images)
        #result = [None] * nb_images
        result = images

        scale_samples, translate_samples, rotate_samples, shear_samples, cval_samples, mode_samples, order_samples = self._draw_samples(nb_images, random_state)

        for i in sm.xrange(nb_images):
            height, width = images[i].shape[0], images[i].shape[1]
            shift_x = width / 2.0 - 0.5
            shift_y = height / 2.0 - 0.5
            scale_x, scale_y = scale_samples[0][i], scale_samples[1][i]
            translate_x, translate_y = translate_samples[0][i], translate_samples[1][i]
            #assert isinstance(translate_x, (float, int))
            #assert isinstance(translate_y, (float, int))
            if ia.is_single_float(translate_y):
                translate_y_px = int(round(translate_y * images[i].shape[0]))
            else:
                translate_y_px = translate_y
            if ia.is_single_float(translate_x):
                translate_x_px = int(round(translate_x * images[i].shape[1]))
            else:
                translate_x_px = translate_x
            rotate = rotate_samples[i]
            shear = shear_samples[i]
            cval = cval_samples[i]
            mode = mode_samples[i]
            order = order_samples[i]
            if scale_x != 1.0 or scale_y != 1.0 or translate_x_px != 0 or translate_y_px != 0 or rotate != 0 or shear != 0:
                matrix_to_topleft = tf.SimilarityTransform(translation=[-shift_x, -shift_y])
                matrix_transforms = tf.AffineTransform(
                    scale=(scale_x, scale_y),
                    translation=(translate_x_px, translate_y_px),
                    rotation=math.radians(rotate),
                    shear=math.radians(shear)
                )
                matrix_to_center = tf.SimilarityTransform(translation=[shift_x, shift_y])
                matrix = (matrix_to_topleft + matrix_transforms + matrix_to_center)
                image_warped = tf.warp(
                    images[i],
                    matrix.inverse,
                    order=order,
                    mode=mode,
                    cval=cval,
                    preserve_range=True
                )
                # warp changes uint8 to float64, making this necessary
                if image_warped.dtype != images[i].dtype:
                    image_warped = image_warped.astype(images[i].dtype, copy=False)
                result[i] = image_warped
            else:
                result[i] = images[i]

        return result

    def _augment_keypoints(self, keypoints_on_images, random_state, parents, hooks):
        result = []
        nb_images = len(keypoints_on_images)
        scale_samples, translate_samples, rotate_samples, shear_samples, cval_samples, mode_samples, order_samples = self._draw_samples(nb_images, random_state)

        for i, keypoints_on_image in enumerate(keypoints_on_images):
            height, width = keypoints_on_image.height, keypoints_on_image.width
            shift_x = width / 2.0 - 0.5
            shift_y = height / 2.0 - 0.5
            scale_x, scale_y = scale_samples[0][i], scale_samples[1][i]
            translate_x, translate_y = translate_samples[0][i], translate_samples[1][i]
            #assert isinstance(translate_x, (float, int))
            #assert isinstance(translate_y, (float, int))
            if ia.is_single_float(translate_y):
                translate_y_px = int(round(translate_y * keypoints_on_image.shape[0]))
            else:
                translate_y_px = translate_y
            if ia.is_single_float(translate_x):
                translate_x_px = int(round(translate_x * keypoints_on_image.shape[1]))
            else:
                translate_x_px = translate_x
            rotate = rotate_samples[i]
            shear = shear_samples[i]
            #cval = cval_samples[i]
            #mode = mode_samples[i]
            #order = order_samples[i]
            if scale_x != 1.0 or scale_y != 1.0 or translate_x_px != 0 or translate_y_px != 0 or rotate != 0 or shear != 0:
                matrix_to_topleft = tf.SimilarityTransform(translation=[-shift_x, -shift_y])
                matrix_transforms = tf.AffineTransform(
                    scale=(scale_x, scale_y),
                    translation=(translate_x_px, translate_y_px),
                    rotation=math.radians(rotate),
                    shear=math.radians(shear)
                )
                matrix_to_center = tf.SimilarityTransform(translation=[shift_x, shift_y])
                matrix = (matrix_to_topleft + matrix_transforms + matrix_to_center)

                coords = keypoints_on_image.get_coords_array()
                #print("coords", coords)
                #print("matrix", matrix.params)
                coords_aug = tf.matrix_transform(coords, matrix.params)
                #print("coords before", coords)
                #print("coordsa ftre", coords_aug, np.around(coords_aug).astype(np.int32))
                result.append(ia.KeypointsOnImage.from_coords_array(np.around(coords_aug).astype(np.int32), shape=keypoints_on_image.shape))
            else:
                result.append(keypoints_on_image)
        return result

    def get_parameters(self):
        return [self.scale, self.translate, self.rotate, self.shear]

    def _draw_samples(self, nb_samples, random_state):
        seed = random_state.randint(0, 10**6, 1)[0]

        if isinstance(self.scale, tuple):
            scale_samples = (
                self.scale[0].draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 10)),
                self.scale[1].draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 20)),
            )
        else:
            scale_samples = self.scale.draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 30))
            scale_samples = (scale_samples, scale_samples)

        if isinstance(self.translate, tuple):
            translate_samples = (
                self.translate[0].draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 40)),
                self.translate[1].draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 50)),
            )
        else:
            translate_samples = self.translate.draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 60))
            translate_samples = (translate_samples, translate_samples)

        assert translate_samples[0].dtype in [np.int32, np.int64, np.float32, np.float64]
        assert translate_samples[1].dtype in [np.int32, np.int64, np.float32, np.float64]

        rotate_samples = self.rotate.draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 70))
        shear_samples = self.shear.draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 80))

        cval_samples = self.cval.draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 90))
        mode_samples = self.mode.draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 100))
        order_samples = self.order.draw_samples((nb_samples,), random_state=ia.new_random_state(seed + 110))

        return scale_samples, translate_samples, rotate_samples, shear_samples, cval_samples, mode_samples, order_samples
