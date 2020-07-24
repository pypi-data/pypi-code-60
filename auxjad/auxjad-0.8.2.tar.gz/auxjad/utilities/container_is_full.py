import abjad

from .underfull_duration import underfull_duration


def container_is_full(container: abjad.Container) -> bool:
    r"""Returns a ``bool`` representing whether the last bar of an input
    container (of type ``abjad.Container`` or child class) is fully filled in
    or not.

    Example:
        Returns ``True`` if the last bar of any container (or child class) is
        full, otherwise returns ``False``. If no time signature is encountered,
        it uses LilyPond's convention and considers the container as in 4/4.

        >>> container1 = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Container(r"c'4 d'4 e'4")
        >>> container3 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4")
        >>> container4 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4 d'4 e'4 f'4")
        >>> auxjad.container_is_full(container1)
        True
        >>> auxjad.container_is_full(container2)
        False
        >>> auxjad.container_is_full(container3)
        False
        >>> auxjad.container_is_full(container4)
        True

    Example:
        Handles any time signatures as well as changes of time signature.

        >>> container1 = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Container(r"\time 3/4 a2. \time 2/4 r2")
        >>> container3 = abjad.Container(r"\time 5/4 g1 ~ g4 \time 4/4 af'2")
        >>> container4 = abjad.Container(r"\time 6/8 c'2 ~ c'8")
        >>> auxjad.container_is_full(container1)
        True
        >>> auxjad.container_is_full(container2)
        True
        >>> auxjad.container_is_full(container3)
        False
        >>> auxjad.container_is_full(container4)
        False

    Example:
        Correctly handles partial time signatures.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> time_signature = abjad.TimeSignature((3, 4), partial=(1, 4))
        >>> abjad.attach(time_signature, container[0])
        >>> auxjad.container_is_full(container)
        True

    Example:
        It also handles multi-measure rests.

        >>> container1 = abjad.Container(r"R1")
        >>> container2 = abjad.Container(r"\time 3/4 R1*3/4 \time 2/4 r2")
        >>> container3 = abjad.Container(r"\time 5/4 R1*5/4 \time 4/4 g''4")
        >>> container4 = abjad.Container(r"\time 6/8 R1*1/2")
        >>> auxjad.container_is_full(container1)
        True
        >>> auxjad.container_is_full(container2)
        True
        >>> auxjad.container_is_full(container3)
        False
        >>> auxjad.container_is_full(container4)
        False

    ..  error::

        If a container is malformed, i.e. it has an underfilled bar before a
        time signature change, the function raises a ``ValueError`` exception.

        >>> container = abjad.Container(r"\time 5/4 g''1 \time 4/4 f'1")
        >>> auxjad.container_is_full(container)
        ValueError: 'container' is malformed, with an underfull bar preceeding
        a time signature change

    ..  warning::

        The input container must be a contiguous logical voice. When dealing
        with a container with multiple subcontainers (e.g. a score containings
        multiple staves), the best approach is to cycle through these
        subcontainers, applying this function to them individually.
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("argument must be 'abjad.Container' or child class")
    if not abjad.select(container).leaves().are_contiguous_logical_voice():
        raise ValueError("argument must be contiguous logical voice")
    return underfull_duration(container) == abjad.Duration(0)
