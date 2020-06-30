(function (global){
    var ajax = {};

    function getAjaxObject(){
        if(window.XMLHttpRequest){
            return new XMLHttpRequest();
        }
        else if(window.ActiveXObject){
            return new ActiveXObject();
        }
        else {
            global.alert("I suggest that you \
                have a physical relation with yourself!!!");
            return null;
        }
    }

    ajax.sendGetRequest = (reqURL,requestHandler,isJsonResponse) => {
        var request = getAjaxObject();
        request.onreadystatechange = () => {
            handleResponse(request,requestHandler,isJsonResponse);
        };

        request.open("GET",reqURL,true);
        request.send(null);
    };

    function handleResponse(request,requestHandler,isJsonResponse) {
        if( (request.readyState == 4 ) && 
            request.status === 200){
            
            if(isJsonResponse === undefined){
                isJsonResponse = true;
            }
            if(isJsonResponse){
                requestHandler(JSON.parse(request.responseText));    
            }
            else {
                requestHandler(request.responseText);
            }    
        }
        
    }

    global.$ajax_util = ajax;

})(window);