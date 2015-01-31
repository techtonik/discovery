package main

import (
  "fmt"
  "io/ioutil"
)

var header = 
`rot13 v1.0  String to ROT13 Conversion
Wrap Labs Software, January 2015`

func main() {
  fmt.Println(header + "\n")

  contents, _ := ioutil.ReadFile("caffeine.txt")
  fmt.Println(string(contents))
}
