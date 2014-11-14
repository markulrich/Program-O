<?php

// Outputs all the result of shellcommand "ls", and returns
// the last output line into $last_line. Stores the return value
// of the shell command in $retval.
$result = array();
exec( 'python scrape_quotes.py arnold_schwarzenegger', $result);
foreach ( $result as $v )
{
    echo $v;
}


// Printing additional info
?>