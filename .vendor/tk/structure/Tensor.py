# automatically generated by the FlatBuffers compiler, do not modify

# namespace: structure

import flatbuffers


class Tensor(object):
  __slots__ = ['_tab']

  @classmethod
  def GetRootAsTensor(cls, buf, offset):
    n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
    x = Tensor()
    x.Init(buf, n + offset)
    return x

  # Tensor
  def Init(self, buf, pos):
    self._tab = flatbuffers.table.Table(buf, pos)

  # Tensor
  def Name(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
    if o != 0:
      return self._tab.String(o + self._tab.Pos)
    return None

  # Tensor
  def Info(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
    if o != 0:
      return self._tab.String(o + self._tab.Pos)
    return None

  # Tensor
  def Shape(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
    if o != 0:
      return self._tab.Get(flatbuffers.number_types.Uint32Flags, o + self._tab.Pos)
    return 0

  # Tensor
  def Size(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
    if o != 0:
      return self._tab.Get(flatbuffers.number_types.Uint32Flags, o + self._tab.Pos)
    return 0

  # Tensor
  def Data(self, j):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
    if o != 0:
      a = self._tab.Vector(o)
      return self._tab.Get(flatbuffers.number_types.Float32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
    return 0

  # Tensor
  def DataAsNumpy(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
    if o != 0:
      return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Float32Flags, o)
    return 0

  # Tensor
  def DataLength(self):
    o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
    if o != 0:
      return self._tab.VectorLen(o)
    return 0


def TensorStart(builder): builder.StartObject(5)


def TensorAddName(builder, name): builder.PrependUOffsetTRelativeSlot(
    0, flatbuffers.number_types.UOffsetTFlags.py_type(name), 0)


def TensorAddInfo(builder, info): builder.PrependUOffsetTRelativeSlot(
    1, flatbuffers.number_types.UOffsetTFlags.py_type(info), 0)


def TensorAddShape(builder, shape): builder.PrependUint32Slot(2, shape, 0)


def TensorAddSize(builder, size): builder.PrependUint32Slot(3, size, 0)


def TensorAddData(builder, data): builder.PrependUOffsetTRelativeSlot(
    4, flatbuffers.number_types.UOffsetTFlags.py_type(data), 0)


def TensorStartDataVector(
    builder, numElems): return builder.StartVector(4, numElems, 4)


def TensorEnd(builder): return builder.EndObject()