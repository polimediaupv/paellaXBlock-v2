# Edx Xblock for Paella Player #
This Xblocks integrates paella player into OpenEdx.
You can easily integrate the XBlock into the Edx platform and start to use the player.


## Installation instructions ##
In order to install the XBlock into your Edx Server you will need to.

## Download the XBlock from github. Place the files inside your server.

		git clone https://github.com/polimediaupv/paellaXBlock-v2


##.   Install your block::
You must replace `/path/to/your/block` with the path where you have downloaded the xblock

		sudo -u edxapp /edx/bin/pip.edxapp install /path/to/your/block

##.  Enable the block

  In ``edx-platform/lms/envs/common.py``, uncomment:

        # from xmodule.x_module import prefer_xmodules
        # XBLOCK_SELECT_FUNCTION = prefer_xmodules

  In ``edx-platform/cms/envs/common.py``, uncomment:

        # from xmodule.x_module import prefer_xmodules
        # XBLOCK_SELECT_FUNCTION = prefer_xmodules

  In ``edx-platform/cms/envs/common.py``, change:

            'ALLOW_ALL_ADVANCED_COMPONENTS': False,

   to:

            'ALLOW_ALL_ADVANCED_COMPONENTS': True,

##.  Add the block to your courses' advanced settings in Studio

    #. Log in to Studio, and open your course
    #. Settings -> Advanced Settings
    #. Change the value for the key ``"advanced_modules"`` to ``paellaplayer``


##.  Add your block into your course

    #. Edit a unit
    #. Advanced -> paellaplayer

##. Deploying your XBlock

To deploy your block to your own hosted version of edx-platform, you need to install it
into the virtualenv that the platform is running out of, and add to the list of ``ADVANCED_COMPONENT_TYPES``
in ``edx-platform/cms/djangoapps/contentstore/views/component.py``.

#. Using the XBlock in the course

.In the Studio go to:

![Settings->Advanced Settings](https://raw.githubusercontent.com/polimediaupv/paellaXBlock-v2/master/doc/img/1.png)

.Add a paellaplayer policy key on the advanced_modules keys

![Policy key added](https://raw.githubusercontent.com/polimediaupv/paellaXBlock-v2/master/doc/img/2.png)

.After that, a new button called Advanced will appear in your unit edit view

![Advanced](https://raw.githubusercontent.com/polimediaupv/paellaXBlock-v2/master/doc/img/3.png)

.And a new option called Paella Video will appear. Wich will add the component with the paella demo video to the course.

![Adding paella](https://raw.githubusercontent.com/polimediaupv/paellaXBlock-v2/master/doc/img/4.png)

.You can change the parameters of the video pressing the edit button.

![Playing paella](https://raw.githubusercontent.com/polimediaupv/paellaXBlock-v2/master/doc/img/5.png)

.By default we will enter in advanced edition mode where we can edit the data.json that stablises the content that will play paellaplayer.

![Playing paella](https://raw.githubusercontent.com/polimediaupv/paellaXBlock-v2/master/doc/img/6.png)

.You can learn more about the data.json format in the [PaellaPlayer documentation](https://github.com/polimediaupv/paella/blob/master/doc/adopter_doc/integrate_datajson.md)

.In case you just want to view a video/s that is stored in mp4,youtube or hls and don't want to generate the data.json you can switch to the basic view pressing the toggle view button.

![Playing paella](https://raw.githubusercontent.com/polimediaupv/paellaXBlock-v2/master/doc/img/7.png)

.In this mode we can set the video Title (1)

.Set the type and source/id of the first video (2)

.Set the type and source/id of the second video (3)

![Playing paella](https://raw.githubusercontent.com/polimediaupv/paellaXBlock-v2/master/doc/img/8.png)

.Save it to see the result in Paella Player or go to advanced mode to see the data.json generated.