#!/usr/bin/env python

# Copyright 2016  Vimal Manohar
# Apache 2.0.

"""This script converts kaldi-style utt2spk and segments to a NIST RTTM
file.
The RTTM format is
<type> <file-id> <channel-id> <begin-time> \
        <duration> <ortho> <stype> <name> <conf>
<type> = SPEAKER for each segment.
<file-id> - the File-ID of the recording
<channel-id> - the Channel-ID, usually 1
<begin-time> - start time of segment
<duration> - duration of segment
<ortho> - <NA> (this is ignored)
<stype> - <NA> (this is ignored)
<name> - speaker name or id
<conf> - <NA> (this is ignored)
"""

from __future__ import print_function
import argparse
import sys

sys.path.insert(0, 'steps')

class NullstrToNoneAction(argparse.Action):
    """ A custom action to convert empty strings passed by shell to None in
    python. This is necessary as shell scripts print null strings when a
    variable is not specified. We could use the more apt None in python. """

    def __call__(self, parser, namespace, values, option_string=None):
        if values.strip() == "":
            setattr(namespace, self.dest, None)
        else:
            setattr(namespace, self.dest, values)


class smart_open(object):
    """
    This class is designed to be used with the "with" construct in python
    to open files. It is similar to the python open() function, but
    treats the input "-" specially to return either sys.stdout or sys.stdin
    depending on whether the mode is "w" or "r".
    e.g.: with smart_open(filename, 'w') as fh:
            print ("foo", file=fh)
    """
    def __init__(self, filename, mode="r"):
        self.filename = filename
        self.mode = mode
        assert self.mode == "w" or self.mode == "r"

    def __enter__(self):
        if self.filename == "-" and self.mode == "w":
            self.file_handle = sys.stdout
        elif self.filename == "-" and self.mode == "r":
            self.file_handle = sys.stdin
        else:
            self.file_handle = open(self.filename, self.mode)
        return self.file_handle

    def __exit__(self, *args):
        if self.filename != "-":
            self.file_handle.close()



def get_args():
    parser = argparse.ArgumentParser(
        description="""This script converts kaldi-style utt2spk and
        segments to a NIST RTTM file""")

    parser.add_argument("--reco2file-and-channel", type=str,
                        action=NullstrToNoneAction,
                        help="""Input reco2file_and_channel.
                        The format is <recording-id> <file-id> <channel-id>.
                        If not provided, then <recording-id> is taken as the
                        <file-id> with <channel-id> = 1.""")
    parser.add_argument("utt2spk", type=str,
                        help="Input utt2spk file")
    parser.add_argument("segments", type=str,
                        help="Input segments file")
    parser.add_argument("rttm_file", type=str,
                        help="Output RTTM file")

    args = parser.parse_args()
    return args


def main():
    args = get_args()

    if args.reco2file_and_channel is not None:
        reco2file_and_channel = {}
        with smart_open(args.reco2file_and_channel) as fh:
            for line in fh:
                parts = line.strip().split()
                reco2file_and_channel[parts[0]] = (parts[1], parts[2])

    utt2spk = {}
    with smart_open(args.utt2spk) as fh:
        for line in fh:
            parts = line.strip().split()
            utt2spk[parts[0]] = parts[1]

    with smart_open(args.segments) as segments_reader, \
            smart_open(args.rttm_file, 'w') as rttm_writer:
        for line in segments_reader:
            parts = line.strip().split()

            utt = parts[0]
            spkr = utt2spk[utt]

            reco = parts[1]
            file_id = reco
            channel = 1

            if args.reco2file_and_channel is not None:
                try:
                    file_id, channel = reco2file_and_channel[reco]
                except KeyError:
                    raise RuntimeError(
                        "Could not find recording {0} in {1}".format(
                            reco, args.reco2file_and_channel))

            start_time = float(parts[2])
            duration = float(parts[3]) - start_time

            print("SPEAKER {0} {1} {2:7.2f} {3:7.2f} "
                  "<NA> <NA> {4} <NA>".format(
                      file_id, channel, start_time,
                      duration, spkr), file=rttm_writer)


if __name__ == '__main__':
    main()