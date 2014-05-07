import abc
import logging
import os

from PIL import Image

from watermarks.core.method import BaseMethod


logger = logging.getLogger()


class BaseReader(BaseMethod):
    __metaclass__ = abc.ABCMeta

    def __init__(self, destination, format):
        '''
        :param str destination:
            Destination where extracted watermarks will be stored.

        :param str format:
            Watermark format.
        '''
        self.destination = destination
        self.format = format

    def _process_file(self, filepath):
        src_img = Image.open(filepath)
        if src_img.format not in self.allowed_formats:
            logger.warning('File "%s" is in not allowed format. (skip)', filepath)
            return []

        if src_img.mode in self.allowed_modes:
            generated_filepaths = []
            base_name, _ = os.path.splitext(os.path.basename(filepath))
            logger.info('Processing file "%s"', filepath)
            dst_imgs = self._create_watermarked(src_img)
            for band_name, dst_img in zip(src_img.getbands(), dst_imgs):
                dst_filepath = os.path.join(self.destination, '%s_%s.%s' % (base_name, band_name, self.format))
                dst_img.save(dst_filepath)
                logger.info('Generated file "%s".', dst_filepath)
                generated_filepaths.append(dst_filepath)
            return generated_filepaths
        else:
            logger.warning('File "%s" is in unsupported mode "%s". (skip)', filepath, src_img.mode)
            return []
