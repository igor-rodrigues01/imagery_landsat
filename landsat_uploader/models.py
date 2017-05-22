from django.utils.encoding import python_2_unicode_compatible
from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.conf import settings


class Satellite(object):
    pass

@python_2_unicode_compatible
class Scene(models.Model):
    """Class to register the Scenes of Landsat imagery"""

    sat_options = (
        ('L8', 'Landsat 8'),
        ('L7', 'Landsat 7'),
        ('L5', 'Landsat 5'),
        )

    status_options = (
        ('created', _('Created')),
        ('downloading', _('Downloading')),
        ('dl_failed', _('Download Failed')),
        ('downloaded', _('Downloaded')),
        ('processing', _('Processing')),
        ('p_failed', _('Processing Failed')),
        ('processed', _('Processed'))
        )

    path = models.CharField(max_length=3)
    row = models.CharField(max_length=3)
    sat = models.CharField(_('Satellite'), choices=sat_options, max_length=50)
    date = models.DateField(_('Date'))
    name = models.CharField(_('Name'), max_length=255, unique=True)
    cloud_rate = models.FloatField(_('Cloud Rate'), null=True, blank=True)
    geom = models.PolygonField(srid=4326, null=True, blank=True)
    status = models.CharField(choices=status_options, max_length=50)

    class Meta:
        ordering = ['-date', 'path', 'row']
        verbose_name = _('Scene')


    def __str__(self):
        return '%s %s-%s %s' % (self.sat, self.path, self.row, self.date.strftime('%x'))

    def dir(self):
        """Return the folder where the files of the scenes are saved."""
        return join(settings.MEDIA_ROOT, self.sat, self.name)


@python_2_unicode_compatible
class Image(models.Model):
    """
    Class to register the image files. 
    All Images are associated with one Scene object.False
    """
    name = models.CharField(_('Name'), max_length=100, unique=True)
    type = models.CharField(_('Type'), max_length=30)
    creation_date = models.DateField(_('Creation date'), auto_now_add=True)
    scene = models.ForeignKey(Scene, related_name='images')

    def __str__(self):
        return '%s' % self.name

    def url(self):
        """URL string to be used concatenated with MEDIA_URL"""
        return join(settings.MEDIA_URL, self.scene.sat, self.scene.name, self.name)

    def file_path(self):
        """File path of the Image in the filesystem."""
        return '%s' % join(self.scene.dir(), self.name)

    def file_exists(self):
        """Test if the file exists on filesystem."""
        return isfile(self.file_path())

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Image, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')