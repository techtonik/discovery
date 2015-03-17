package main

import "fmt"
import "os"

func main() {
  fmt.Fprintln(os.Stderr, "This is a stderr printed line.")
}
