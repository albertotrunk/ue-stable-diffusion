
        """
        input_state = random_state.get_state()
        samples = self._draw_samples(size, random_state)
        after_state = random_state.get_state()

        # make sure that the random state is changed at least once
        if input_state[2] == after_state[2] and input_state[1][0] == after_state[1][0]:
            ia.forward_random_state(random_state)

        #print("input_state", input_state)
        input_first = input_state[1][0]
        input_sum = np.sum(input_state[1])
        input_max, input_min = np.max(input_state[1]), np.min(input_state[1])
        input_pos = input_state[2]


        after_first = after_state[1][0]
        after_sum = np.sum(after_state[1])
        after_max, after_min = np.max(after_state[1]), np.min(after_state[1])
        after_pos = after_state[2]

        #print("after state", random_state.get_state())
        print("samples",  samples.shape)
        print("firsts", input_first, after_first, input_first == after_first)
        print("sums", input_sum, after_sum, input_sum == after_sum)
        print("mins", input_min, after_min, input_min == after_min)
        print("maxs", input_max, after_max, input_max == after_max)
        print("pos", input_pos, after_pos, input_pos == after_pos)
        """
