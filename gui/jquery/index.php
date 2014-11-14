<?php
/***************************************
 * http://www.program-o.com
 * PROGRAM O
 * Version: 2.4.3
 * FILE: index.php
 * AUTHOR: Elizabeth Perreau and Dave Morton
 * DATE: 07-23-2013
 * DETAILS: This is the interface for the Program O JSON API
 ***************************************/
$cookie_name = 'Program_O_JSON_GUI';
$botId = filter_input(INPUT_GET, 'bot_id');
$convo_id = (isset($_COOKIE[$cookie_name])) ? $_COOKIE[$cookie_name] : jq_get_convo_id();
$bot_id = (isset($_COOKIE['bot_id'])) ? $_COOKIE['bot_id'] : ($botId !== false && $botId !== null) ? $botId : 1;
setcookie('bot_id', $bot_id);
// Experimental code
/*
  $base_URL  = 'http://' . $_SERVER['HTTP_HOST'];                                   // set domain name for the script
  $this_path = str_replace(DIRECTORY_SEPARATOR, '/', realpath(dirname(__FILE__)));  // The current location of this file, normalized to use forward slashes
  $this_path = str_replace($_SERVER['DOCUMENT_ROOT'], $base_URL, $this_path);       // transform it from a file path to a URL
  $url = str_replace('gui/jquery', 'chatbot/conversation_start.php', $this_path);   // and set it to the correct script location

  Example URL's for use with the chatbot API
  $url = 'http://api.program-o.com/v2.3.1/chatbot/';
  $url = 'http://localhost/Program-O/Program-O/chatbot/conversation_start.php';
  $url = 'chat.php';
*/

$url = 'http://web.stanford.edu/~mulrich/cgi-bin/Program-O/chatbot/conversation_start.php';

/**
 * Function jq_get_convo_id
 *
 *
 * @return string
 */
function jq_get_convo_id()
{
    global $cookie_name;
    session_name($cookie_name);
    session_start();
    $convo_id = session_id();
    session_destroy();
    setcookie($cookie_name, $convo_id);
    return $convo_id;
}

?>
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" type="text/css" href="main.css" media="all"/>
    <link rel="icon" href="./favicon.ico" type="image/x-icon"/>
    <link rel="shortcut icon" href="./favicon.ico" type="image/x-icon"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>ChameleonBot</title>
    <meta name="Description" content="A CS 221 project by Marcus, Mark, and Tristan."/>
    <meta name="keywords" content="Open Source, AIML, PHP, MySQL, Chatbot, Program-O, Version2"/>
    <meta name="keywords" content="Open Source, AIML, PHP, MySQL, Chatbot, Program-O, Version2"/>
    <style type="text/css">
        h3 {
            text-align: center;
        }

        hr {
            width: 80%;
            color: green;
            margin-left: 0;
        }

        body {
            padding: 20px;
        }

        #shameless_plug, #urlwarning {
            margin-top: 20px;
        }

        #urlwarning {
            right: auto;
            left: 10px;
            width: 50%;
            font-size: large;
            font-weight: bold;
            background-color: white;
        }

        .centerthis {
            width: 90%;
        }

        #chatdiv {
            margin-top: 20px;
            text-align: center;
            width: 100%;
        }

    </style>
</head>
<body>
<h3>ChameleonBot</h3>

<p>
    The beginnings of a CS 221 project by Marcus, Mark, and Tristan.
</p>

<div class="centerthis">
    <div id="chatboard">
        <div class="botsay">Hello!</div>
    </div>
    <div id="spinner" class="spinner" style="display:none;">
        <img id="img-spinner" src="spinner.gif" alt="Loading"/>
    </div>
</div>
<div class="clearthis"></div>
<div class="centerthis">
    <form method="post" name="talkform" id="talkform" action="index.php">
        <div id="chatdiv">
            <label for="submit">Me:</label>
            <label for="say"></label><input type="text" name="say" id="say" size="60"/>
            <input type="submit" name="submit" id="submit" class="submit" value="say"/>
            <input type="hidden" name="convo_id" id="convo_id" value="<?php echo $convo_id; ?>"/>
            <input type="hidden" name="bot_id" id="bot_id" value="<?php echo $bot_id; ?>"/>
            <input type="hidden" name="format" id="format" value="json"/>
        </div>
    </form>
</div>
<div id="shameless_plug">
    Chatbot powered by code from <a href="http://www.program-o.com" target="_top">program-o.com</a>
</div>
<script type="text/javascript" src="jquery-1.9.1.min.js"></script>
<script type="text/javascript">
    $(document).ready(function () {
        // put all your jQuery goodness in here.

        var spinner = $('#spinner');
        window.location.hash = '/arnold_schwarzenegger';
        $('#talkform').submit(function (e) {
            e.preventDefault();
            var user = $('#say').val();
            $('#chatboard').append(
                $('<div>', {class: 'usersay', text: user})
            );
            var formdata = $("#talkform").serialize();
            formdata += '&bot_name=' + window.location.hash.substr(1);
            $('#say').val('');
            $('#say').focus();
            spinner.show();
            $.post('<?php echo $url ?>', formdata, function (data) {
                var b = data.botsay;
                if (b == null) {
                    b = 'I have nothing to say.'
                }
                if (b.indexOf('[img]') >= 0) {
                    b = showImg(b);
                }
                if (b.indexOf('[link') >= 0) {
                    b = makeLink(b);
                }
                var usersay = data.usersay;
                if (user != usersay) {
                    $('.usersay').text(usersay);
                }
                $('#chatboard').append(
                    $('<div>', {class: 'botsay'}).html(b)
                );
            }, 'json').fail(function (xhr, textStatus, errorThrown) {
                $('#chatboard').append(
                    $('<div>', {class: 'botsay'}).html('Sorry, it appears that my servers are down. Maybe you would like to refresh this page and try again?')
                );
            }).always(function () {
                spinner.hide();
            });
            return false;
        });
    });
    function showImg(input) {
        var regEx = /\[img\](.*?)\[\/img\]/;
        var repl = '<br><a href="$1" target="_blank"><img src="$1" alt="$1" width="150" /></a>';
        var out = input.replace(regEx, repl);
        console.log('out = ' + out);
        return out
    }
    function makeLink(input) {
        var regEx = /\[link=(.*?)\](.*?)\[\/link\]/;
        var repl = '<a href="$1" target="_blank">$2</a>';
        var out = input.replace(regEx, repl);
        console.log('out = ' + out);
        return out;
    }
</script>
</body>
</html>
