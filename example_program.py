from pathlib import Path

import napari
import typer
from napari.settings import get_settings
from napari.utils.notifications import NotificationSeverity

from tilt_image_excluder import TiltImageExcluderWidget
from tilt_image_excluder.data_models import TiltSeriesSet

cli = typer.Typer(add_completion=False)


def tilt_series_metadata_to_tilt_series_set(metadata_file: Path) -> TiltSeriesSet:
    raise NotImplementedError


@cli.command(name='tilt_image_excluder')
def exclude_tilt_images_cli(
    tilt_series_metadata_file: Path = typer.Option(...),
    output_directory: Path = typer.Option(...),
    cache_size: int = typer.Option(5, help='number of cached tilt-series')
):
    viewer = napari.Viewer()
    settings = get_settings()
    settings.application.gui_notification_level = NotificationSeverity.ERROR
    metadata = tilt_series_metadata_to_tilt_series_set(tilt_series_metadata_file)
    dock_widget = TiltImageExcluderWidget(
        viewer=viewer,
        metadata=metadata,
        cache_size=cache_size,
        save_button_label='save me!',
        output_global_metadata_file=output_directory / 'selected_tilt_series.star'
    )
    viewer.window.add_dock_widget(dock_widget, name='RELION tilt-image excluder')
    viewer.text_overlay.text = """
    keyboard shortcuts
    - '[' and ']' for previous/next tilt-series
    - '↑' and '↓' for previous/next image
    - 'PageUp' and 'PageDown' for first/last image
    - 'Enter' to select/deselect an image
    """
    viewer.text_overlay.visible = True
    napari.run()
