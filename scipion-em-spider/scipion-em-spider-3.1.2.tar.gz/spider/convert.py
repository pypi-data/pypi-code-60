# **************************************************************************
# *
# * Authors:     J.M. De la Rosa Trevin (delarosatrevin@scilifelab.se)
# *
# * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 3 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

import numpy
from os.path import splitext, split

from pwem.objects import Transform
from pwem.constants import NO_INDEX, ALIGN_2D, ALIGN_3D, ALIGN_PROJ
import pwem.convert.transformations as transformations
from pyworkflow.utils.path import moveFile

from .utils import SpiderDocFile, runTemplate
from .constants import (SHIFTX, SHIFTY, ANGLE_PSI,
                        ANGLE_THE, ANGLE_PHI, FLIP)


def locationToSpider(index, filename):
    """ Convert an index and filename location
    to a string with @ as expected in Spider.
    """
    # TODO: Maybe we need to add more logic dependent of the format
    if index != NO_INDEX:
        return "%s@%d" % (filename, index)
    
    return filename


def spiderToLocation(spiderFilename):
    """ Return a location (index, filename) given
    a Spider filename with the filename@index structure. """
    if '@' in spiderFilename:
        filename, index = spiderFilename.split('@')
        return int(index), str(filename)
    else:
        return NO_INDEX, str(spiderFilename)


def writeSetOfImages(imgSet, stackFn, selFn):
    """ Write a SetOfMicrographs as a Spider stack and selfile.
    Params:
        imgSet: the SetOfMicrograph instance.
        stackFn: the filename where to write the stack.
        selFn: the filename of the Spider selection file.
    """
    doc = SpiderDocFile(selFn, 'w+')

    for i in range(imgSet.getSize()):
        doc.writeValues(i+1)

    imgSet.writeStack(stackFn, applyTransform=True)
    doc.close()

    convertEndian(stackFn, imgSet.getSize())


def convertEndian(stackFn, stackSize):
    """ Convert the stack file generated by Xmipp
    to one that Spider likes more.
    Params:
        stackFn: the filename of the images stack
        stackSize: the number of particles in the stack
    """
    fn, ext = splitext(stackFn)
    fnDir, fnBase = split(fn)
    # Change to BigEndian
    runTemplate('../cp_endian.spi', ext[1:],
                {'[particles]': fnBase + '@******',
                 '[particles_big]': fnBase + '_big@******',
                 '[numberOfParticles]': stackSize
                 }, cwd=fnDir)
    moveFile(fn + '_big' + ext, stackFn)
    
    
# ------------- Geometry conversions ---------------------------------------

def geometryFromMatrix(matrix, inverseTransform):
    if inverseTransform:
        matrix = numpy.linalg.inv(matrix)
        shifts = -transformations.translation_from_matrix(matrix)
    else:
        shifts = transformations.translation_from_matrix(matrix)
    angles = -numpy.rad2deg(transformations.euler_from_matrix(matrix,
                                                              axes='szyz'))
    return shifts, angles


def matrixFromGeometry(shifts, angles, inverseTransform):
    """ Create the transformation matrix from a given
    2D shifts in X and Y...and the 3 euler angles.
    """
    from numpy import deg2rad
    radAngles = -deg2rad(angles)

    M = transformations.euler_matrix(radAngles[0], radAngles[1], radAngles[2],
                                     'szyz')
    if inverseTransform:
        from numpy.linalg import inv
        M[:3, 3] = -shifts[:3]
        M = inv(M)
    else:
        M[:3, 3] = shifts[:3]

    return M


def rowToAlignment(alignmentRow, alignType):
    """
    is2D == True-> matrix is 2D (2D images alignment)
            otherwise matrix is 3D (3D volume alignment or projection)
    invTransform == True  -> for xmipp implies projection
    """
    is2D = alignType == ALIGN_2D
    inverseTransform = True  # alignType == em.ALIGN_PROJ

    alignment = Transform()
    angles = numpy.zeros(3)
    shifts = numpy.zeros(3)
    angles[2] = alignmentRow.get('ANGLE_PSI')
    shifts[0] = alignmentRow.get('SHIFTX')
    shifts[1] = alignmentRow.get('SHIFTY')
    if not is2D:
        angles[0] = alignmentRow.get('ANGLE_PHI')
        angles[1] = alignmentRow.get('ANGLE_THE')

    M = matrixFromGeometry(shifts, angles, inverseTransform)
    alignment.setMatrix(M)

    return alignment


def alignmentToRow(alignment, alignmentRow, alignType):
    """
    is2D == True-> matrix is 2D (2D images alignment)
            otherwise matrix is 3D (3D volume alignment or projection)
    invTransform == True  -> for xmipp implies projection
                          -> for xmipp implies alignment
    """
    is2D = alignType == ALIGN_2D
    inverseTransform = alignType == ALIGN_PROJ
    # only flip is meaningful if 2D case
    # in that case the 2x2 determinant is negative
    flip = False
    matrix = alignment.getMatrix()
    
    if alignType == ALIGN_2D:
        # get 2x2 matrix and check if negative
        flip = bool(numpy.linalg.det(matrix[0:2, 0:2]) < 0)
        if flip:
            matrix[0, :2] *= -1.  # invert only the first two columns keep x
            matrix[2, 2] = 1.  # set 3D rot
        else:
            pass

    elif alignType == ALIGN_3D:
        flip = bool(numpy.linalg.det(matrix[0:3, 0:3]) < 0)
        if flip:
            matrix[0, :4] *= -1.  # now, invert first line including x
            matrix[3, 3] = 1.  # set 3D rot
        else:
            pass

    else:
        flip = bool(numpy.linalg.det(matrix[0:3, 0:3]) < 0)
        if flip:
            matrix[0, :4] *= -1.  # now, invert first line including x
    shifts, angles = geometryFromMatrix(matrix, inverseTransform)
    alignmentRow[SHIFTX] = -shifts[0]
    alignmentRow[SHIFTY] = -shifts[1]
    
    if is2D:
        angle = angles[0] + angles[2]
        alignmentRow[ANGLE_PSI] = angle
    else:
        alignmentRow[ANGLE_PHI] = angles[0]
        alignmentRow[ANGLE_THE] = angles[1]
        alignmentRow[ANGLE_PSI] = -angles[2]
        
    alignmentRow[FLIP] = -1 if flip else 1


def createItemMatrix(item, row, align):
    item.setTransform(rowToAlignment(row, alignType=align))
