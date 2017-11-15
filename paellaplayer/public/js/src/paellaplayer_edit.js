/* Javascript for PaellaXBlock. */
function PaellaXBlock(runtime, element,params) {
    // Set up gettext in case it isn't available in the client runtime:
    /***************************************************************************************************/

    /*******************************************************************************************/

    function paellaSaved(result) {
        $('.server', element).text();
        $('.video_id', element).text(result.video_id);
        $('.display_name', element).text(result.display_name);
    }

    $(element).find('.cancel-button').bind('click', function() {
        runtime.notify('cancel', {});
    });

    $(element).find('.toggle-button').bind('click', function(){

        tabs = $(element).find("section");
        for (var i=0;i<tabs.length;i++){tabs[i].classList.toggle("m-fadeIn");tabs[i].classList.toggle("m-fadeOut");}
    });

    $(element).find('.video_data').bind('input',function(event){
        $(element).find('.video_id').each(function(intIndex){this.value=""})
        $(element).find('.video_title')[0].value = JSON.parse(this.value)['metadata']['title'];
    });

    $(element).find('.video_title').bind('input',function(event){
        //change title in json
        videodata = $(element).find('.video_data');
        console.log(videodata[0].value);
        var videodataJSON = JSON.parse(videodata[0].value);//
        videodataJSON['metadata']['title']=this.value;
        videodata[0].value = JSON.stringify(videodataJSON, undefined, 2);
    });

    var generate_data = function(){
        var title = $(element).find('.video_title')[0];
        var modes = [];
        $(element).find('.video_mode').each(function(intIndex){modes.push(this.value);});


        newdata = {"metadata": {
                "duration": 0,
                "title": title.value
            },
            "streams": []};
        $(element).find('.video_id').each(function(intIndex){
            if (this.value!="")
            {
                var stream = {}
                if (modes[intIndex]!='youtube'){
                  stream = {
                                "sources": {
                                    [modes[intIndex]]: [
                                        {
                                            "src": this.value,
                                            "mimetype": "video/mp4",
                                        }
                                    ]
                                }
                            };

                }else{
                   stream = {
                                "sources": {
                                    "youtube": [
                                        {
                                            "id":this.value,
                                            "res": {
                                                "w": 1280,
                                                "h": 720
                                            }
                                        }
                                    ]
                                }
                            };

                }
                newdata['streams'].push(stream)
            }
        });
        videodata[0].value = JSON.stringify(newdata, undefined, 2);
    }

    $(element).find('.video_id').bind('input',function(event){
        videodata = $(element).find('.video_data');
        console.log(videodata[0].value);
        //parse new json
        generate_data();
    });

    $(element).find('.save-button').bind('click', function() {

        var title = $(element).find('.video_title')[0];
        var modes = [];
        $(element).find('.video_mode').each(function(intIndex){modes.push(this.value);})
        var ids = [];
        $(element).find('.video_id').each(function(intIndex){ids.push(this.value);})
        videodata = $(element).find('.video_data');

        var data = {
            'title': title.value,
            'modes': modes,
            'video_ids': ids,
            'video_data':videodata[0].value
        };
        console.log('saving');
        $('.xblock-editor-error-message', element).html();
        $('.xblock-editor-error-message', element).css('display', 'none');
        var handlerUrl = runtime.handlerUrl(element, 'save_paella');
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
            if (response.result === 'success') {
                window.location.reload(false);
            } else {
                $('.xblock-editor-error-message', element).html('Error: '+response.message);
                $('.xblock-editor-error-message', element).css('display', 'block');
            }
        });
    });

    $(function ($) {
        /* Here's where you'd do things on page load. */
    });
}