# -*- coding: utf-8 -*- # pylint: disable=too-many-lines
#
# Imports ###########################################################
import pkg_resources
import json
import logging
import urllib
import webob

from xblock.core import XBlock
from xblock.exceptions import JsonHandlerError
from xblock.fields import Scope, String, Dict, Float, Boolean, Integer
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader
from xblockutils.settings import XBlockWithSettingsMixin, ThemableXBlockMixin

from .utils import _, DummyTranslationService, FeedbackMessage, FeedbackMessages, ItemStats, StateMigration, Constants
# Globals ###########################################################

loader = ResourceLoader(__name__)

@XBlock.wants('settings')
@XBlock.needs('i18n')
class PaellaXBlock(XBlock,
    XBlockWithSettingsMixin,
    ThemableXBlockMixin):



    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    display_name = String(
        display_name="Display Name",
        help="Display name for this module in case the source video doesn't have any.",
        default="Paella Video",
        scope=Scope.settings
    )

    video_data = String(
        display_name="Video Data",
        help="JSON data that defines the video structure that paella will display",
        default='{"metadata":{"duration":0,"title":"Easy"},"streams":[{"sources":{"mp4":[{"src":"http://paellaplayer.upv.es/demo/repository/belmar-multiresolution/media/240-presenter.mp4","mimetype":"video/mp4"}]}}]}',
        scope=Scope.settings
    )

    mode = String(
        display_name=("Mode"),
        help=(
            "HLS Video: an video from an hls manifest will need "
            "the source url to play it. "
            "Youtube video: a video from youtube will only need "
            "the video Id to play it. "
            "MP4 video: an MP4 video will need the source url "
            "to play it. "
        ),
        scope=Scope.settings,
        values=[
            {"display_name": "MP4 video", "value": "mp4"},
            {"display_name": "Youtube Video", "value": "youtube"},
            {"display_name": "HLS Video", "value": "hls"},
        ],
        default="mp4",
        enforce_type=True,
    )

    video_id = String(
        display_name="VideoID",
        help="Identifier of the first video when using easy mode ",
        default='http://paellaplayer.upv.es/demo/repository/belmar-multiresolution/media/240-presenter.mp4',
        scope=Scope.settings
    )

    mode_b = String(
        display_name=("Mode 2"),
        help=(
            "HLS Video: an video from an hls manifest will need "
            "the source url to play it. "
            "Youtube video: a video from youtube will only need "
            "the video Id to play it. "
            "MP4 video: an MP4 video will need the source url "
            "to play it. "
        ),
        scope=Scope.settings,
        values=[
            {"display_name": "MP4 video", "value": "mp4"},
            {"display_name": "Youtube Video", "value": "youtube"},
            {"display_name": "HLS Video", "value": "hls"},
        ],
        default="mp4",
        enforce_type=True,
    )

    video_id_b = String(
        display_name="Video ID 2",
        help="Identifier of the second video when using easy mode ",
        default='',
        scope=Scope.settings
    )

    def _get_block_id(self):
        """
        Return unique ID of this block. Useful for HTML ID attributes.
        Works both in LMS/Studio and workbench runtimes:
        - In LMS/Studio, use the location.html_id method.
        - In the workbench, use the usage_id.
        """
        if hasattr(self, 'location'):
            return self.location.html_id()  # pylint: disable=no-member
        else:
            return unicode(self.scope_ids.usage_id)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        """
        The primary view of the PaellaXBlock, shown to students
        when viewing courses.
        """
        id_suffix = self._get_block_id()

        context = {
            'id_suffix': id_suffix,
            'self': self,
            'player': self.runtime.local_resource_url(self, 'public/player/index.html' )
        }

        fragment = Fragment()
        fragment.add_content(loader.render_template('static/html/paellaplayer.html', context))

        css_urls = (
            'public/css/paellaplayer.css',
        )
        js_urls = (
            'public/js/src/paellaplayer.js',
        )
        for css_url in css_urls:
            fragment.add_css_url(self.runtime.local_resource_url(self, css_url))
        for js_url in js_urls:
            fragment.add_javascript_url(self.runtime.local_resource_url(self, js_url))

        fragment.initialize_js('PaellaXBlock', {
            'data': self.video_data})

        return fragment



        """
        self.player = self.runtime.local_resource_url(self, 'public/player/index.html' )

        html = self.resource_string("static/html/paellaplayer.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/paellaplayer.css"))
        frag.add_javascript(self.resource_string("static/js/src/paellaplayer.js"))
        frag.initialize_js('PaellaXBlock')
        return frag
        """


        # TO-DO: change this view to display your data your own way.

    def studio_view(self, context=None):
        """
        The primary view of the paellaXBlock, shown to teachers
        when editing courses.
        """
        id_suffix = self._get_block_id()

        parsed = json.loads(self.video_data)
        pretty_json = json.dumps(parsed, indent=4, sort_keys=True)
        context = {
            'id_suffix': id_suffix,
            'fields': self.fields,
            'self': self,
            'pretty': pretty_json,
            'video_title': parsed['metadata']['title'],
            'data': urllib.quote(json.dumps(self.video_data)),
        }

        fragment = Fragment()
        fragment.add_content(loader.render_template('static/html/paellaplayer_edit.html', context))

        css_urls = (
            'public/css/paellaplayer_edit.css',
        )
        js_urls = (
            'public/js/vendor/handlebars-v1.1.2.js',
            'public/js/src/paellaplayer_edit.js',
        )
        for css_url in css_urls:
            fragment.add_css_url(self.runtime.local_resource_url(self, css_url))
        for js_url in js_urls:
            fragment.add_javascript_url(self.runtime.local_resource_url(self, js_url))

        fragment.initialize_js('PaellaXBlock', {
            'data': self.video_data})

        return fragment

    @XBlock.json_handler
    def save_paella(self, data, suffix=''):
        """
        Save state handler.
        data = {
        'title': title.value,
        'modes': modes,
        'video_ids': ids,
        'video_data':videodata[0].value
        };
        """

        self.display_name = data['title']
        self.video_data = data['video_data']
        self.mode = data['modes'][0]
        self.mode_b = data['modes'][1]
        self.video_id = data['video_ids'][0]
        self.video_id_b = data['video_ids'][1]

        return {
            'result': 'success',
        }

    @XBlock.json_handler
    def getData(self,data,suffix=''):
        return json.loads(self.video_data)


    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("PaellaXBlock",
             """<paellaplayer/>
             """)
        ]
