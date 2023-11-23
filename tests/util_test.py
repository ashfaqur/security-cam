from src.capture.util import validate_crop_frame_parameters, validate
import pytest
import tempfile


def test_validate() -> None:
    # Test when img_dir is not a directory
    with pytest.raises(ValueError):
        validate("not_a_directory", "uploader")

    # Test when uploader is not a file
    with pytest.raises(ValueError):
        validate(tempfile.gettempdir(), "not_a_file")

    # Test when both img_dir and uploader are valid
    with tempfile.TemporaryDirectory() as img_dir:
        with tempfile.NamedTemporaryFile() as uploader:
            validate(img_dir, uploader.name)


def test_validate_crop_frame_parameters() -> None:
    # Test case 1: Valid crop frame parameters
    validate_crop_frame_parameters((0, 10, 0, 10), 20, 20)

    # Test case 2: Invalid x parameter (negative)
    with pytest.raises(ValueError):
        validate_crop_frame_parameters((-1, 10, 0, 10), 20, 20)

    # Test case 3: Invalid x parameter (greater than height)
    with pytest.raises(ValueError):
        validate_crop_frame_parameters((21, 10, 0, 10), 20, 20)

    # Test case 4: Invalid x parameter (x1 > x2)
    with pytest.raises(ValueError):
        validate_crop_frame_parameters((10, 0, 0, 10), 20, 20)

    # Test case 5: Invalid y parameter (negative)
    with pytest.raises(ValueError):
        validate_crop_frame_parameters((0, 10, -1, 10), 20, 20)

    # Test case 6: Invalid y parameter (greater than width)
    with pytest.raises(ValueError):
        validate_crop_frame_parameters((0, 10, 21, 10), 20, 20)

    # Test case 7: Invalid y parameter (y1 > y2)
    with pytest.raises(ValueError):
        validate_crop_frame_parameters((0, 10, 10, 0), 20, 20)
