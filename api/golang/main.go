package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

type Task struct {
	Id   int    `json:"id`
	Name string `json:"string"`
	Desc string `json:"string"`
}

func homeHandler(w http.ResponseWriter, r *http.Request) {
	newTask := Task{Id: 1, Name: "demo task", Desc: "this is related with vault"}

	jsonTask, err := json.Marshal(newTask)
	if err != nil {
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write(jsonTask)
	return
}

func main() {
	mux := http.NewServeMux()

	mux.HandleFunc("/", homeHandler)

	err := http.ListenAndServe(":8000", mux)
	fmt.Println("web server started on port :8000")
	if err != nil {
		panic(err)
	}
}
