def is_animated(commands):
    return any(filter(lambda tup: tup[0] in {'frames', 'vary', 'basename'}, commands))

def num_frames(commands):
    for cmd in commands:
        if cmd[0] == 'frames':
            return cmd[1]
    else:
        raise AttributeError('Please specify the number of frames using the following command: frames <number>')

def get_basename(commands):
    for cmd in commands:
        if cmd[0] == 'basename':
            return cmd[1]
    else:
        raise AttributeError('Please specify the filename prefix using the following command: basename <prefix>')

def get_knob_specs(commands, frames):
    # Truncated `vary` commands
    vcmds = [cmd[1:] for cmd in commands if cmd[0] == 'vary']
    # Dict of arrays of knob values
    knobs = {knob: [float(nan)] * frames for knob in [t[0] for t in vcmds]}
    # Set the knob values
    for knob, frame0, frame1, value0, value1 in vcmds:
        if 0 <= frame0 < frame1 <= frames:
            pass
        else:
            raise ValueError('First and last frame numbers out of bounds: %d, %d.  Total number of frames: %d' % (frame0, frame1, frames))
