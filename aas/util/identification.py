import abc
import uuid
from typing import Optional

from .. import model


class AbstractIdentifierGenerator(metaclass=abc.ABCMeta):
    """
    Abstract base class for identifier generators that generate identifiers based on an internal schema and an
    (optional) proposal.

    Different Implementations of IdentifierGenerators may generate differently formed ids, e.g. URNs, HTTP-scheme IRIs,
    IRDIs, etc. Some of them may use a given private namespace and create ids within this namespace, others may just
    use long random numbers to ensure uniqueness.
    """
    @abc.abstractmethod
    def generate_id(self, proposal: Optional[str] = None) -> model.Identifier:
        """
        Generate a new Identifier for an Identifiable object.

        :param proposal: An optional string for a proposed suffix of the Identification (e.g. the last path part or
                         fragment of an IRI). It may be ignored by some implementations of or be changed if the
                         resulting id is already existing.
        """
        pass


class UUIDGenerator(AbstractIdentifierGenerator):
    """
    An IdentifierGenerator, that generates URNs of version 1 UUIDs according to RFC 4122.
    """
    def __init__(self):
        super().__init__()
        self._sequence = 0

    def generate_id(self, proposal: Optional[str] = None) -> model.Identifier:
        uuid_ = uuid.uuid1(clock_seq=self._sequence)
        self._sequence += 1
        return model.Identifier("urn:uuid:{}".format(uuid_), model.IdentifierType.IRI)
