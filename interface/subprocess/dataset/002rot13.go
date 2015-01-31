package main

import (
  "fmt"
  "io/ioutil"
  "os"
)

var header = 
  "rot13 v1.0  String to ROT13 Conversion\n" +
  "Wrap Labs Software, January 2015\n"
var usage =
  "usage: rot13 <filename>\n"

func main() {
  fmt.Println(header)

  if len(os.Args[1:]) == 0 {
    fmt.Println(usage)
    os.Exit(-1)
  }

  contents, _ := ioutil.ReadFile(os.Args[1])
  fmt.Println(string(contents))
}
