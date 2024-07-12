#!/usr/bin/env python
#
# This code has been adapted from: https://git.fmrib.ox.ac.uk/paulmc/fslpy
#
# This project is available under the Apache License, Version 2.0
#
# path.py - Utility functions for working with file/directory paths.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains a few utility functions for working with file system
paths.


.. autosummary::
   :nosignatures:

   deepest
   shallowest
   addExt
   removeExt
   getExt
"""


import os.path as op


class PathError(Exception):
    """``Exception`` class raised by :func:`addExt` and :func:`getExt`."""

    pass


def deepest(path, suffixes):
    """Finds the deepest directory which ends with one of the given
    sequence of suffixes, or returns ``None`` if no directories end
    with any of the suffixes.
    """

    path = path.strip()

    if path == op.sep or path == "":
        return None

    path = path.rstrip(op.sep)

    if any([path.endswith(s) for s in suffixes]):
        return path

    return deepest(op.dirname(path), suffixes)


def shallowest(path, suffixes):
    """Finds the shallowest directory which ends with one of the given
    sequence of suffixes, or returns ``None`` if no directories end
    with any of the suffixes.
    """

    path = path.strip()

    # We've reached the root of the file system
    if path == op.sep or path == "":
        return None

    path = path.rstrip(op.sep)
    parent = shallowest(op.dirname(path), suffixes)

    if parent is not None:
        return parent

    if any([path.endswith(s) for s in suffixes]):
        return path

    return None


def addExt(prefix, allowedExts, mustExist=True, defaultExt=None, replace=None):
    """Adds a file extension to the given file ``prefix``.

    If ``mustExist`` is False, and the file does not already have a
    supported extension, the default extension is appended and the new
    file name returned. If the prefix already has a supported extension,
    it is returned unchanged.

    If ``mustExist`` is ``True`` (the default), the function checks to see
    if any files exist that have the given prefix, and a supported file
    extension.  A :exc:`ValueError` is raised if:

       - No files exist with the given prefix and a supported extension.

       - ``replace`` is ``None``, and more than one file exists with the
         given prefix, and a supported extension.

    Otherwise the full file name is returned.

    :arg prefix:      The file name prefix to modify.

    :arg allowedExts: List of allowed file extensions.

    :arg mustExist:   Whether the file must exist or not.

    :arg defaultExt:  Default file extension to use.

    :arg replace:     If multiple files exist with the same ``prefix`` and
                      supported extensions (e.g. ``file.hdr`` and
                      ``file.img``), this dictionary can be used to resolve
                      ambiguities. It must have the structure::

                          {
                              suffix : [replacement, ...],
                              ...
                          }

                      If files with ``suffix`` and one of the ``replacement``
                      suffixes exists, the ``suffix`` file will
                      be ignored, and replaced with the ``replacement`` file.
                      If multiple ``replacement`` files exist alongside the
                      ``suffix`` file, a ``PathError`` is raised.

    .. note:: The primary use-case of the ``replace`` parameter is to resolve
              ambiguity with respect to NIFTI and ANALYSE75 image pairs. By
              specifying ``replace={'.hdr' : ['.img'. '.img.gz'}``, the
              ``addExt`` function is able to figure out what you mean when you
              wish to add an extension to ``file``, and ``file.hdr`` and
              either ``file.img`` or ``file.img.gz`` (but not both) exist.
    """

    if replace is None:
        replace = {}

    if not mustExist:
        # the provided file name already
        # ends with a supported extension
        if any([prefix.endswith(ext) for ext in allowedExts]):
            return prefix

        if defaultExt is not None:
            return prefix + defaultExt
        else:
            return None

    # If the provided prefix already ends with a
    # supported extension , check to see that it exists
    if any([prefix.endswith(ext) for ext in allowedExts]):
        allPaths = [prefix]

    # Otherwise, make a bunch of file names, one per
    # supported extension, and test to see if exactly
    # one of them exists.
    else:
        allPaths = [prefix + ext for ext in allowedExts]

    exists = [op.isfile(e) for e in allPaths]
    nexists = sum(exists)

    # Could not find any supported file
    # with the specified prefix
    if nexists == 0:
        raise PathError(
            "Could not find a supported file " "with prefix {}".format(prefix)
        )

    # Ambiguity! More than one supported
    # file with the specified prefix.
    elif nexists > 1:
        # Remove non-existent paths from the
        # extended list, get all their
        # suffixes, and potential replacements
        allPaths = [allPaths[i] for i in range(len(allPaths)) if exists[i]]
        suffixes = [getExt(e, allowedExts) for e in allPaths]
        replacements = [replace.get(s) for s in suffixes]
        hasReplace = [r is not None for r in replacements]

        # If any replacement has been specified
        # for any of the existing suffixes,
        # see if we have a unique match for
        # exactly one existing suffix, the
        # one to be ignored/replaced.
        if sum(hasReplace) == 1:
            # Make sure there is exactly one potential
            # replacement for this suffix. If there's
            # more than one (e.g. file.hdr plus both
            # file.img and file.img.gz) we can't resolve
            # the ambiguity. In this case the code will
            # fall through to the raise statement below.
            toReplace = allPaths[hasReplace.index(True)]
            replacements = replacements[hasReplace.index(True)]
            replacements = [prefix + ext for ext in replacements]
            replExists = [r in allPaths for r in replacements]

            if sum(replExists) == 1:
                replacedBy = replacements[replExists.index(True)]
                allPaths[allPaths.index(toReplace)] = replacedBy
                allPaths = list(set(allPaths))

        exists = [True] * len(allPaths)

        # There's more than one path match -
        # we can't resolve the ambiguity
        if len(allPaths) > 1:
            raise PathError("More than one file with " "prefix {}".format(prefix))

    # Return the full file name of the
    # supported file that was found
    extIdx = exists.index(True)
    return allPaths[extIdx]


def isImage(fileName, allowedExts=None):
    """Check if the file is an image, i.e. ends with .nii or .nii.gz

    :arg fileName:    The file name to check.

    """
    if allowedExts == None:
        allowedExts = (".NII", ".NII.GZ")

    upperFileName = fileName.upper()
    extension = getImageExt(upperFileName)
    extMatches = [upperFileName.endswith(ext) for ext in allowedExts]

    return any(extMatches)


def removeImageExt(fileName):
    return removeExt(fileName, allowedExts=[".nii", ".nii.gz", ".NII", ".NII.GZ"])


def getImageExt(fileName):
    return getExt(fileName, allowedExts=[".nii", ".nii.gz", ".NII", ".NII.GZ"])


def removeExt(fileName, allowedExts=None):
    """Removes the extension from the given file name. Raises some kind
    of error if allowedExts is not None, and the file does not match
    any of the specified extensions.

    :arg fileName:    The file name to strip.

    :arg allowedExts: A list of strings containing the allowed file
                      extensions.
    """

    if allowedExts is None:
        return op.splitext(fileName)[0]

    # figure out the extension of the given file
    extMatches = [fileName.endswith(ext) for ext in allowedExts]

    # the file does not have a supported extension
    if not any(extMatches):
        raise ValueError(
            "{} does not match any extensions: " "{}".format(fileName, allowedExts)
        )

    # figure out the length of the matched extension
    extIdx = extMatches.index(True)
    extLen = len(allowedExts[extIdx])

    # and trim it from the file name
    return fileName[:-extLen]


def getExt(fileName, allowedExts=None):
    """Returns the extension from the given file name.

    If ``allowedExts`` is ``None``, this function is equivalent to using::

        os.path.splitext(fileName)[1]

    If ``allowedExts`` is provided, but the file does not end with an allowed
    extension, a :exc:`PathError` is raised.

    :arg allowedExts: Allowed/recognised file extensions.
    """

    # If allowedExts is not specified,
    # we just use op.splitext
    if allowedExts is None:
        return op.splitext(fileName)[1]

    # Otherwise, try and find a suffix match
    extMatches = [fileName.endswith(ext) for ext in allowedExts]

    if not any(extMatches):
        return ""

    extIdx = extMatches.index(True)
    return allowedExts[extIdx]
