/*
Replacement for MOL2NAM software used in Andrew's Dalke
article on wrapping programs with Python. Features:

[x] always output header (to stderr)
[x] mol2nam <filename>  - process file to stdout
[x] mol2nam -           - process stdin input to stdout

Replacement just decodes few known rot13 lines.
*/

package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
)

var header = "rot13 v1.0  String to ROT13 Conversion\n" +
	"Wrap Labs Software, January 2015\n"
var usage = "usage: rot13 <filename>\n"

func fakerot13(text string) string {
	m := make(map[string]string)
	m["phenol"] = "curaby"
	m["c1ccccc1O"] = "p1ppppp1B"
	m["caffeine"] = "pnssrvar"
	m["1,3,7-gevzrguly-3,7-qvulqebchevar-2,6-qvbar"] =
		"1,3,7-trimethyl-3,7-dihydropurine-2,6-dione"
	return m[text]
}

func main() {
	fmt.Fprintln(os.Stderr, header)

	if len(os.Args[1:]) == 0 {
		fmt.Println(usage)
		os.Exit(-1)
	}

	var contents []byte
	if os.Args[1] == "-" {
		contents, _ = ioutil.ReadAll(os.Stdin)
	} else {
		contents, _ = ioutil.ReadFile(os.Args[1])
	}
	text := strings.TrimSpace(string(contents))
	fmt.Println(fakerot13(text))
}
