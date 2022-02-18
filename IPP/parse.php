<?php
ini_set('display_errors', 'stderr');

include 'errors.php';
include 'stats.php';
include 'help.php';

class outXML {
    private static $output;

    private final function __construct() {
        $this->order = 1;
        $this->arg = 0;
    
        $this->code_XML = new DomDocument('1.0', 'UTF-8');
        $this->code_XML->formatOutput = true;
        $this->prog_XML = $this->code_XML->createElement('program');
        $this->prog_XML->setAttribute('language', 'IPPcode22');
        $this->code_XML->appendChild($this->prog_XML);
    }

    public static function createXML() {
        if (!isset(self::$output))
            self::$output = new outXML();

        return self::$output;
    }

    private $order;
    private $arg;
    private $code_XML;
    private $prog_XML;
    private $opcode_XML;

    function getOrder()  { return $this->order; }
    function incOrder()  { $this->order++; }
    function incArg()    { $this->arg++;   }
    function setArgTo0() { $this->arg = 0; }

    function createInstr($name_code) {
        $this->opcode_XML = $this->code_XML->createElement('instruction');
        $this->opcode_XML->setAttribute('order', $this->order);
        $this->opcode_XML->setAttribute('opcode', $name_code);
    }

    function createArg($value, $type) {
        $arg_XML = $this->code_XML->createElement("arg".$this->arg, $value);
        $arg_XML->setAttribute('type', $type);
        $this->opcode_XML->appendChild($arg_XML);
    }

    function finishInstr() {    
        $this->prog_XML->appendChild($this->opcode_XML);
    }

    function printXML() {
        fwrite(STDOUT, $this->code_XML->saveXML());
    } 
}

$REGEXP_TYPE   = "/^(int|bool|string)$/";
$REGEXP_VAR    = "/^(GF|LF|TF)@(\w|[_\-$%&*?!])*$/";
$REGEXP_INT    = "/^int@([-\+]?[0-9]+$)/";
$REGEXP_STRING = "/^string@(([^\s\#\\\\]|\\\\[0-9]{3})*$)/";
$REGEXP_NIL    = "/^nil@nil$/";
$REGEXP_BOOL   = "/^bool@(false|true)$/";
$REGEXP_LABEL  = "/^(\w|[_\-$%&*?!])*$/";

$OPCODES = ["DEFVAR"      => ["<var>"],                       "POPS"      => ["<var>"],
            "CREATEFRAME" => [],                              "PUSHFRAME" => [],
            "POPFRAME"    => [],                              "RETURN"    => [],
            "BREAK"       => [],                              "STRLEN"    => ["<var>", "<symb>"],
            "CALL"        => ["<label>"],                     "LABEL"     => ["<label>"],
            "JUMP"        => ["<label>"],                     "TYPE"      => ["<var>", "<symb>"],
            "PUSHS"       => ["<symb>"],                      "WRITE"     => ["<symb>"],
            "EXIT"        => ["<symb>"],                      "DPRINT"    => ["<symb>"],
            "MOVE"        => ["<var>", "<symb>"],             "INT2CHAR"  => ["<var>", "<symb>"],
            "JUMPIFEQ"    => ["<label>", "<symb>", "<symb>"], "JUMPIFNEQ" => ["<label>", "<symb>", "<symb>"],
            "ADD"         => ["<var>", "<symb>", "<symb>"],   "SUB"       => ["<var>", "<symb>", "<symb>"],
            "MUL"         => ["<var>", "<symb>", "<symb>"],   "IDIV"      => ["<var>", "<symb>", "<symb>"],
            "LT"          => ["<var>", "<symb>", "<symb>"],   "GT"        => ["<var>", "<symb>", "<symb>"],
            "EQ"          => ["<var>", "<symb>", "<symb>"],   "AND"       => ["<var>", "<symb>", "<symb>"],
            "OR"          => ["<var>", "<symb>", "<symb>"],   "NOT"       => ["<var>", "<symb>", "<symb>"],
            "CONCAT"      => ["<var>", "<symb>", "<symb>"],   "GETCHAR"   => ["<var>", "<symb>", "<symb>"],
            "SETCHAR"     => ["<var>", "<symb>", "<symb>"],   "READ"      => ["<var>", "<type>"],
            "STRI2INT"    => ["<var>", "<symb>", "<symb>"]
           ];

function parseType($arg) {
    $OUTXML = outXML::createXML();
    global $REGEXP_TYPE;

    if (preg_match($REGEXP_TYPE, $arg) == false)
        reportError(SYNTAX_LEX_ERR, SYNTAX_LEX_ERR_MSG);

    $OUTXML->createArg($arg, "type");
}

function parseVar($arg) {
    $OUTXML = outXML::createXML();
    global $REGEXP_VAR;

    if (preg_match($REGEXP_VAR, $arg) == false)
        reportError(SYNTAX_LEX_ERR, SYNTAX_LEX_ERR_MSG);

    $OUTXML->createArg($arg, "var");
}

function parseSymb($arg) {
    $arr = array();
    $OUTXML = outXML::createXML();
    global $REGEXP_BOOL;
    global $REGEXP_STRING;
    global $REGEXP_NIL;
    global $REGEXP_INT;
    global $REGEXP_VAR;

    if (preg_match($REGEXP_STRING, $arg, $arr)) {
        $arr[1] = replaceSpecSymbols($arr[1]);
        $OUTXML->createArg($arr[1], "string");
    }
    else if (preg_match($REGEXP_INT, $arg, $arr))
        $OUTXML->createArg($arr[1], "int");
    else if (preg_match($REGEXP_BOOL, $arg, $arr))
        $OUTXML->createArg($arr[1], "bool");
    else if (preg_match($REGEXP_NIL, $arg, $arr))
        $OUTXML->createArg("nil", "nil");
    else if (preg_match($REGEXP_VAR, $arg))
        $OUTXML->createArg($arg, "var");
    else
        reportError(SYNTAX_LEX_ERR, SYNTAX_LEX_ERR_MSG);
}

function parseLabel($arg) {
    $OUTXML = outXML::createXML();
    global $REGEXP_LABEL;

    if (preg_match($REGEXP_LABEL, $arg) == false)
        reportError(SYNTAX_LEX_ERR, SYNTAX_LEX_ERR_MSG);

    $OUTXML->createArg($arg, "label");
}

function parseArgs($arg_line, $arg_exp) {
    switch ($arg_exp) {
        case "<var>":
            parseVar($arg_line);
            break;
        case "<type>":
            parseType($arg_line);
            break;
        case "<label>":
            parseLabel($arg_line);
            break;
        case "<symb>":
            parseSymb($arg_line);
            break;
    }
}

function checkCountArgs($args, $line_arr) {
    $OUTXML = outXML::createXML();
    $real_args = count($line_arr) - 1;
    $exp_args = count($args);

    if ($exp_args !== $real_args)
        reportError(SYNTAX_LEX_ERR, SYNTAX_LEX_ERR_MSG);
    
    $OUTXML->createInstr($line_arr[0]);
    
    for ($i = 1; $i <= $exp_args; $i++) {
        $OUTXML->incArg();
        parseArgs($line_arr[$i], $args[$i-1]);
    }

    $OUTXML->finishInstr();
    $OUTXML->incOrder();
    
    $OUTXML->setArgTo0();
    return true;
}

function scanner() {
    $OUTXML = outXML::createXML();
    $STATS = Stats::createStats();
    $line_arr;
    global $OPCODES;

    while (false !== ($line = fgets(STDIN))) {
        if (preg_match("~#[^\r\n]*~", $line)) {
            $line = substr($line, 0, strpos($line, "#"));
            $STATS->incComments();
        }

        # delete new line in the end of line + delete myltiple whitespaces
        $line = rtrim($line);
        $line = preg_replace('/\s+/', ' ', $line);

        if ($line == "")
            continue;
        
        # the line ".IPPcode22" must be the first unique line 
        # in the program excepting empty lines
        if (strcmp($line, ".IPPcode22") == 0) {
            if ($STATS->getHeader() == false && $OUTXML->getOrder() == 1) {
                $STATS->setHeader();
                continue;
            }
            else {
                reportError(WRONG_HEADER, WRONG_HEADER_MSG);
            }
        }

        $line_arr = explode(" ", $line);
        $line_arr[0] = strtoupper($line_arr[0]);

        checkLabels($line_arr);
        
        foreach ($OPCODES as $opcode => $args) {
            if (strcmp($opcode, $line_arr[0]) == 0) {
                checkCountArgs($args, $line_arr);
                break;
            }
        }

        # if opcode of the instruction is not correct, 
        # $ORDER will not be increased
        $STATS->incInstructions();
        if ($STATS->getInstructions() !== $OUTXML->getOrder() - 1)
            reportError(WRONG_OPCODE, WRONG_OPCODE_MSG);
    }
    
    if ($STATS->getHeader() == false)
        reportError(WRONG_HEADER, WRONG_HEADER_MSG);
}

helper($argv);
$ret = parseCmdLine($argc, $argv);
scanner();

if ($ret == true) {
    sortJumps();
    writeStats($argv, $argc);
}

printXML();
exit(0);

?>