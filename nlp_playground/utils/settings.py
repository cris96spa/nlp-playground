import torch


def get_device():
    """
    Returns the device type (CPU or GPU) based on the availability of accellerators.
    """
    return (
        torch.accelerator.current_accelerator().type
        if torch.accelerator.is_available()
        else "cpu"
    )
