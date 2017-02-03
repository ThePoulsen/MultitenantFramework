## -*- coding: utf-8 -*-

def sijaxSuccess(msg):
    return """ <ul class="flashes">
                      <div id="w1" class="alert alert-success fade in">
                        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                        <h4><i class="fa fa-asterisk"></i>&nbsp;success!</h4>{}
                    </div>
                    </ul>  """.format(str(msg))
